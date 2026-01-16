# 1. IMAGEN BASE: Usamos Python oficial versión "slim" (ligera, basada en Debian)
# Es el estándar para producción. Alpine es más ligera pero da problemas con librerías C.
FROM python:3.12-slim

# 2. DIRECTORIO DE TRABAJO: Creamos una carpeta /app dentro del contenedor
WORKDIR /app

# 3. VARIABLES DE ENTORNO (Best Practices para Python en Docker)
# Evita que Python genere archivos .pyc (basura en contenedores)
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que los logs de Python se vean en la terminal inmediatamente (sin buffer)
ENV PYTHONUNBUFFERED=1

# 4. DEPENDENCIAS
# Primero copiamos SOLO el requirements.txt. 
# Esto es un truco de caché: si cambias tu código pero no tus dependencias, 
# Docker no reinstalará todo de nuevo (ahorra minutos de build).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. CÓDIGO FUENTE
# Ahora sí, copiamos todo el resto del código a /app
COPY . .

# 6. PUERTO
# Documentamos que el contenedor usará el puerto 8000
EXPOSE 8000

# 7. COMANDO DE ARRANQUE
# Ejecutamos el servidor escuchando en 0.0.0.0 (todas las interfaces).
# Si usas 127.0.0.1 dentro de Docker, nadie desde afuera podrá conectarse.
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]