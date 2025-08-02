from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account

app = Flask(__name__)

@app.post("/")
def web_scraping():
    """
    Funcion que accede a la pagina de la wikipedia que contiene el listado por paises de promedios de iq
    extrae de ellas el pais e iq y crea un bucket con un csv con estos datos
    """
    driver = None

    try:
        print("Cargamos las configuraciones del webdriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage") 

        driver = webdriver.Chrome(options=chrome_options)
        print("WebDriver inicializado con exito.")

        # Cargo la pagina en la que quiero scrappear
        driver.get('https://es.wikipedia.org/wiki/CI_y_la_riqueza_de_las_naciones')
        print("Pagina cargada con exito.")
        
        # Busco en cada fila
        filas = driver.find_elements(By.XPATH, './/table[@class = "wikitable sortable jquery-tablesorter"]//tbody//tr')
        print(f"Numero de filas encontradas: {len(filas)}")
        data = []
        
        print("Comenzamos a buscar la informacion de las filas...")
        # Las recorro
        for i, fila in enumerate(filas):
            try:
                # Tomo el elemento de la imagen
                elemento_imagen = fila.find_element(By.XPATH, './/img')
                # Voy a coger ahora el nombre del pais
                texto_completo = elemento_imagen.get_attribute('alt')
                nombre = texto_completo.replace("Bandera de ", "")
                # Quiero extraer los iq ahora
                td_completos = fila.find_elements(By.TAG_NAME, 'td')
                # IQ en tercera columna por lo que lo printeo directamente ahi
                if len(td_completos) > 2:
                    iq = td_completos[2].text
                    posicion = td_completos[0].text
                    data.append({
                        'Posicion': posicion,
                        'NombrePais': nombre,
                        'IQ': iq,
                    })
                else:
                    print(f"La fila {i+1} no tiene suficientes columnas")
            except Exception as error:
                print(f"Error al procesar la fila {i+1}: {error}")

        if driver:
            driver.quit()
            driver = None
        print("WebDriver cerrado tras el scraping.")
        
        # Creo el dataframe en pandas
        df = pd.DataFrame(data)
        
        if df.empty:
            print("No se encontraron datos para exportar.")
            # Asegurado: Retorno explicito para este caso
            return "No se encontraron datos para exportar. El scraping pudo fallar.", 200
        
        # Lo exporto a csv
        csv_filename = 'iq_paises.csv'
        csv_path = os.path.join('/tmp', csv_filename)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"DataFrame guardado localmente en: {csv_path}")
        
        # Compruebo el tipo de dato
        print(df.dtypes)
    
        # Cloud storage
        # Nombre del JSON
        archivo_key = 'sandbox_estudiantes_key.json'
        # Nombre del bucket
        nombre_bucket = 'test_tablas_alberto'
        # Nombre del archivo CSV en GCS (usamos el mismo nombre que el local)
        iq_paises_cgs = csv_filename 
        # Creo las credenciales
        credenciales = service_account.Credentials.from_service_account_file(archivo_key)
        # Inicializo con las credenciales
        storage_cliente = storage.Client(credentials=credenciales)
        # Tomamos la referencia del bucket
        bucket = storage_cliente.bucket(nombre_bucket)
        # Sube el archivo al bucket de GCS
        blob = bucket.blob(iq_paises_cgs)
        blob.upload_from_filename(csv_path)
        print(f"Archivo '{iq_paises_cgs}' subido exitosamente a 'gs://{nombre_bucket}/{iq_paises_cgs}'")
        # Elimino la ruta al csv
        os.remove(csv_path)
        print(f"Archivo local '{csv_path}' eliminado.")
        return "Web scraping y subida a GCS completados exitosamente.", 200

    except FileNotFoundError:
        error_msg = f"Error: No se encontro el archivo de clave JSON '{archivo_key}'. Asegurate de que esta en la raiz del proyecto Docker."
        print(error_msg)
        return error_msg, 500
    except Exception as error:
        error_msg = f"Error inesperado durante la ejecucion: {error}"
        print(error_msg)
        return error_msg, 500
    finally:
        # Si driver != None lo cerramos, por si ha habido algun fallo y no se cierra
        if driver:
            driver.quit()
            print("WebDriver cerrado en el bloque finally final.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)