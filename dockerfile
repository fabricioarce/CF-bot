# Imagen base con Python 3.12.6
FROM python:3.12.6-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Establece la variable de entorno para evitar buffering en logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Comando por defecto para ejecutar el bot
CMD ["python", "src/main.py"]
