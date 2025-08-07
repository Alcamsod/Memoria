import os
import io
from datetime import date, timedelta, datetime, timezone
import pandas as pd
import requests
from flask import Flask, request
from google.cloud import storage, bigquery
from google.api_core.exceptions import NotFound
from dotenv import load_dotenv

# Cargamos las variables de entorno del .venv
load_dotenv()

app = Flask(__name__)

# Parámetros globales
BUCKET_NAME = "casusopropellersdev-datos-luz"
PROJECT_ID = "casusopropellersdev"
DATASET_ID = "precios_luz_energia"
TABLE_ID = "precios_mercado_diario_horario"
INDICATORS = {
    "precio_eur_mwh": 600,
    "generacion_solar_mwh": 10206,
    "generacion_eolica_mwh": 2038,
    "demanda_mwh": 10004,
}

ESIOS_API_TOKEN = os.environ.get("ESIOS_API_TOKEN")
# Esquema de la tabla de BigQuery
TABLE_SCHEMA = [
    bigquery.SchemaField("fecha_hora", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("precio_eur_mwh", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("generacion_solar_mwh", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("generacion_eolica_mwh", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("demanda_mwh", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("fecha_carga", "TIMESTAMP", mode="NULLABLE"),
]

# Inicializamos los clientes de BigQuery y GCS
try:
    bq_client = bigquery.Client(project=PROJECT_ID)
    gcs_client = storage.Client(project=PROJECT_ID)
    print("Clientes de Google Cloud inicializados correctamente.")
except Exception as e:
    print(f"Error al inicializar los clientes de Google Cloud: {e}")
    bq_client = None
    gcs_client = None


def obtener_ultima_fecha_bq(client, project_id, dataset_id, table_id):
    """
    Consulta BigQuery para obtener la fecha de la última carga
    """
    if not client:
        print("El cliente de BigQuery no está inicializado.")
        return None

    table_ref_str = f"{project_id}.{dataset_id}.{table_id}"
    query = f"SELECT MAX(fecha_hora) AS ultima_fecha FROM `{table_ref_str}`"

    try:
        query_job = client.query(query)
        results = query_job.result()
        row = next(iter(results), None)
        if row and row.ultima_fecha:
            # Obtenemos el datetime
            return row.ultima_fecha.astimezone(timezone.utc)
        else:
            # Si la tabla está vacía
            return None
    except NotFound:
        print(f"La tabla {table_ref_str} no existe. Es la primera carga.")
        return None
    except Exception as e:
        print(f"Error al consultar la última fecha en BigQuery: {e}")
        return None


def obtener_datos_esios(indicator_id, start_date_str, end_date_str):
    """
    Hace la llamada a ESIOS para un indicador y devuelve los datos.
    """
    if not ESIOS_API_TOKEN:
        raise ValueError("La variable de entorno ESIOS_API_TOKEN no está configurada.")

    url = (
        f"https://api.esios.ree.es/indicators/{indicator_id}"
        f"?start_date={start_date_str}&end_date={end_date_str}&time_trunc=hour"
    )
    headers = {
        "Accept": "application/json; application/vnd.esios-api-v1+json",
        "Content-Type": "application/json",
        "x-api-key": ESIOS_API_TOKEN,
        "User-Agent": "Evenbytes - extracción precios luz",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    valores = response.json().get("indicator", {}).get("values", [])

    if not valores:
        return pd.DataFrame()

    df = pd.DataFrame(valores)
    df = df[["datetime", "value"]]
    df.rename(columns={"datetime": "fecha_hora", "value": indicator_id}, inplace=True)
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], utc=True)
    return df


def subir_a_bigquery(df, client, project_id, dataset_id, table_id, schema):
    """
    Sube un DataFrame a BigQuery, añadiendo los nuevos datos a la tabla existente
    """
    if not client:
        raise ConnectionError(
            "El cliente de BigQuery no está disponible para la carga."
        )

    table_ref_str = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(schema=schema, write_disposition="WRITE_APPEND")

    try:
        load_job = client.load_table_from_dataframe(
            df, table_ref_str, job_config=job_config
        )
        load_job.result()
        print(f"Cargados {load_job.output_rows} registros en BigQuery: {table_ref_str}")
    except Exception as e:
        print(f"Error al subir datos a BigQuery: {e}")
        raise


@app.route("/", methods=["GET", "POST"])
def obtener_precios_y_subir():
    """
    Extrae, transforma y carga los datos de precios, generación y demanda en BigQuery y GCS.
    """
    if not bq_client or not gcs_client:
        msg = "Los clientes de Google Cloud no se pudieron inicializar. Abortando ejecución."
        print(msg)
        return msg, 500
    try:
        # Definimos la fecha de inicio de consulta
        ultima_fecha_bq = obtener_ultima_fecha_bq(
            bq_client, PROJECT_ID, DATASET_ID, TABLE_ID
        )

        # La fecha fin es siempre ayer
        fecha_fin_proceso = date.today() - timedelta(days=1)

        if ultima_fecha_bq:
            # La fecha de inicio es el día de la última consulta
            fecha_inicio_proceso = ultima_fecha_bq.date()
        else:
            # Si no hay datos, empezamos un día antes
            print(
                "No se encontraron datos en BigQuery, se iniciará la carga desde un día antes."
            )
            fecha_inicio_proceso = date.today() - timedelta(days=1)

        if fecha_inicio_proceso > fecha_fin_proceso:
            msg = "Los datos ya están actualizados hasta el día de ayer. No se requiere ninguna acción."
            print(msg)
            return msg, 200

        print(
            f"Extrayendo datos desde {fecha_inicio_proceso.strftime('%Y-%m-%d')} hasta {fecha_fin_proceso.strftime('%Y-%m-%d')}"
        )

        lista_df_dias = []
        current_date = fecha_inicio_proceso
        while current_date <= fecha_fin_proceso:
            start_date_str = current_date.strftime("%Y-%m-%dT00:00")
            end_date_str = current_date.strftime("%Y-%m-%dT23:59")

            print(f"Procesando día: {current_date.strftime('%Y-%m-%d')}")

            df_dia_final = None
            for col_name, indicator_id in INDICATORS.items():
                df = obtener_datos_esios(indicator_id, start_date_str, end_date_str)
                if not df.empty:
                    df.rename(columns={indicator_id: col_name}, inplace=True)
                    if df_dia_final is None:
                        df_dia_final = df
                    else:
                        df_dia_final = pd.merge(
                            df_dia_final, df, on="fecha_hora", how="outer"
                        )

            if df_dia_final is not None and not df_dia_final.empty:
                lista_df_dias.append(df_dia_final)

            current_date += timedelta(days=1)

        if not lista_df_dias:
            msg = "No se obtuvieron nuevos datos de la API de ESIOS en el rango de fechas consultado."
            print(msg)
            return msg, 200

        # Preparamos los datos para subirlo
        df_final = pd.concat(lista_df_dias, ignore_index=True)
        df_final.sort_values(by="fecha_hora", inplace=True)
        df_final.reset_index(drop=True, inplace=True)
        df_final["fecha_carga"] = datetime.now(timezone.utc)

        # Reordenamos las columnas
        column_order = [field.name for field in TABLE_SCHEMA]
        df_final = df_final[column_order]

        print(f"Se procesaron un total de {len(df_final)} registros.")

        # Lo subimos a GCS
        fecha_ejecucion_str = date.today().strftime("%Y-%m-%d")
        carpeta = f"{fecha_ejecucion_str}"
        csv_filename = f"{carpeta}/precios_{fecha_inicio_proceso.strftime('%Y%m%d')}_a_{fecha_fin_proceso.strftime('%Y%m%d')}.csv"

        bucket = gcs_client.bucket(BUCKET_NAME)
        blob = bucket.blob(csv_filename)

        with io.StringIO() as csv_buffer:
            df_final.to_csv(csv_buffer, index=False, encoding="utf-8")
            blob.upload_from_string(csv_buffer.getvalue(), content_type="text/csv")

        print(f"Archivo '{csv_filename}' subido correctamente a GCS.")

        # Lo subimos a BigQuery
        subir_a_bigquery(
            df_final, bq_client, PROJECT_ID, DATASET_ID, TABLE_ID, TABLE_SCHEMA
        )

        msg = f"Proceso completado. Datos desde {fecha_inicio_proceso} hasta {fecha_fin_proceso} cargados en GCS y BigQuery."
        print(msg)
        return msg, 200

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error HTTP en la llamada a la API ESIOS: {e.response.status_code} - {e.response.text}"
        print(error_msg)
        return error_msg, 502
    except Exception as error:
        error_msg = f"Error inesperado durante la ejecución: {error}"
        print(error_msg)
        return error_msg, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
