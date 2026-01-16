# =============================================================================
# STAGE 1: Builder - Instala dependencias en un entorno aislado
# =============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Evita archivos .pyc y asegura logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias en el directorio del usuario (no requiere root en runtime)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: Runtime - Imagen final optimizada para producción
# =============================================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala curl para health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copia SOLO las dependencias instaladas desde el builder
COPY --from=builder /root/.local /root/.local

# Asegura que los binarios instalados estén en el PATH
ENV PATH=/root/.local/bin:$PATH

# Copia el código fuente
COPY . .

EXPOSE 8000

# Comando de inicio: migraciones, assets estáticos, carga de datos y servidor
CMD python src/manage.py collectstatic --noinput && \
    python src/manage.py migrate && \
    python src/manage.py load_pokemons && \
    gunicorn --chdir src --bind 0.0.0.0:8000 config.wsgi:application