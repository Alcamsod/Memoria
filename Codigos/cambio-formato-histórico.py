import pandas as pd
from datetime import datetime, timezone
# IMPORTANTE: Preguntar si queremos hora en el Update time
# Ruta a tu CSV original
ruta_original = "./archivos/archivos_sinformatear/precio-luz-sinformato.csv"
ruta_nuevo = "./archivos/archivos_formateados/precio-luz-conformato.csv"

# Leer CSV original
df = pd.read_csv(ruta_original, sep=";")
# Crear nuevo DataFrame con columnas requeridas
df_nuevo = pd.DataFrame()
df_nuevo['datetime'] = df['datetime']
df_nuevo['precio'] = df['value']
df_nuevo['update_date'] = datetime.now(timezone.utc).date().isoformat()

# Guardar en nuevo CSV
df_nuevo.to_csv(ruta_nuevo, index=False, encoding='utf-8')
print(f"Archivo transformado guardado como: {ruta_nuevo}")

