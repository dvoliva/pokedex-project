FROM python:3.12-slim

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python src/manage.py collectstatic --noinput && \
    python src/manage.py migrate && \
    python src/manage.py load_pokemons && \
    gunicorn --chdir src --bind 0.0.0.0:8000 config.wsgi:application