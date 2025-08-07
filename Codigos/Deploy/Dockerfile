# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo.
COPY . .

# Puerto expuesto por Flask
EXPOSE 8080

# Define el comando para ejecutar la aplicación.
CMD ["gunicorn", "-w", "4", "-b", ":8080", "data-extraction-api-esios:app"]