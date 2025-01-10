# Utilizar una imagen base de Python
FROM python:3.12-slim
# Instalar los paquetes necesarios, incluyendo gettext
RUN apt-get update && apt-get install -y \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requerimientos y instalarlos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al directorio de trabajo
COPY . /app/

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ejecutar migraciones y recoger archivos estáticos
RUN python manage.py collectstatic --noinput
RUN django-admin compilemessages

# Exponer el puerto que se utilizará para acceder a la aplicación
EXPOSE 8000

# Ejecutar el servidor
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sequencer.wsgi:application"]