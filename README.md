# Pokedex del Profesor Oak

Dashboard web para analizar datos de Pokemon, desarrollado como prueba tecnica.

## Tabla de Contenidos

- [Pokedex del Profesor Oak](#pokedex-del-profesor-oak)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Contexto](#contexto)
  - [Que hace el proyecto](#que-hace-el-proyecto)
  - [Checklist de requisitos](#checklist-de-requisitos)
    - [Vista principal con columnas requeridas](#vista-principal-con-columnas-requeridas)
    - [Filtros del profesor Oak](#filtros-del-profesor-oak)
    - [Transformacion de datos](#transformacion-de-datos)
    - [Especificaciones tecnicas](#especificaciones-tecnicas)
  - [Extras implementados](#extras-implementados)
  - [Tecnologias utilizadas](#tecnologias-utilizadas)
  - [Como ejecutar el proyecto](#como-ejecutar-el-proyecto)
    - [Requisitos previos](#requisitos-previos)
    - [Pasos](#pasos)
    - [Que sucede al iniciar](#que-sucede-al-iniciar)
  - [Ejecutar tests](#ejecutar-tests)
    - [Resultado esperado](#resultado-esperado)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Notas adicionales](#notas-adicionales)
  - [Autor](#autor)

---

## Contexto

Este proyecto fue desarrollado como respuesta a una prueba tecnica con el siguiente enunciado:

> *"Estas empezando a trabajar en el laboratorio del profesor Oak y te ha asignado una tarea crucial: disenar la infraestructura tecnica para analizar los datos de la Pokedex."*

El desafio consistia en consumir la [PokeAPI](https://pokeapi.co/) para listar los primeros 50 Pokemon, implementar filtros especificos y demostrar conocimientos en arquitectura de software, DevOps y buenas practicas de desarrollo.

---

## Que hace el proyecto

1. **Descarga automatica** de los primeros 50 Pokemon desde la PokeAPI al iniciar el contenedor
2. **Persiste los datos** en una base de datos PostgreSQL (no depende de la API para funcionar)
3. **Muestra un dashboard** con tabla interactiva que incluye: ID, imagen, nombre, nombre invertido, tipos, altura y peso
4. **Permite filtrar** los datos segun los criterios del profesor Oak mediante botones en la interfaz

---

## Checklist de requisitos

Cada punto del enunciado original y como fue resuelto:

### Vista principal con columnas requeridas

| Columna | Implementacion |
|---------|----------------|
| ID | Campo `id` como clave primaria en el modelo `Pokemon` |
| Nombre | Campo `name` con capitalizacion aplicada en el ETL |
| Tipo(s) | Campo `types` como `JSONField` para soportar multiples tipos |
| Altura | Campo `height` almacenado en decimetros (formato de la API) |
| Peso | Campo `weight` almacenado en hectogramos (formato de la API) |

### Filtros del profesor Oak

| Filtro | Requisito | Implementacion |
|--------|-----------|----------------|
| Peso | Pokemon con peso > 30 y < 80 | `Pokemon.objects.filter(weight__gt=30, weight__lt=80)` |
| Tipo | Pokemon tipo "grass" | `Pokemon.objects.filter(types__icontains='grass')` |
| Combinado | Pokemon tipo "flying" con altura > 10 | `Pokemon.objects.filter(types__icontains='flying', height__gt=10)` |

### Transformacion de datos

| Requisito | Implementacion |
|-----------|----------------|
| Nombre invertido | Se calcula en el ETL con `name[::-1]` y se almacena en el campo `name_inverted` |

### Especificaciones tecnicas

| Requisito | Implementacion |
|-----------|----------------|
| Backend Python + Django | Django 6.0.1 con patron MTV (Model-Template-View) |
| Persistencia de datos | PostgreSQL 15 con volumen Docker para persistencia |
| Contenedorizacion | Dockerfile multi-stage + docker-compose con health checks |
| Variables de entorno | Archivo `.env` con `python-dotenv` y `dj-database-url` |
| Estructura profesional | Codigo fuente en `src/`, separacion de config y apps |

---

## Extras implementados

Funcionalidades adicionales que aportan valor al proyecto:

| Extra | Descripcion |
|-------|-------------|
| **Multi-stage build** | Dockerfile optimizado que reduce el tamano de la imagen (~30% mas pequena) |
| **Health checks** | Verificacion automatica de que PostgreSQL y Django estan listos antes de aceptar trafico |
| **Pipeline CI/CD** | GitHub Actions con 3 jobs: linting, tests con PostgreSQL real, y build de Docker |
| **Cache de dependencias** | El CI cachea las dependencias de pip para acelerar ejecuciones |
| **Tests automatizados** | Suite de tests unitarios y de integracion que validan los filtros |
| **Panel de administracion** | Django Admin configurado para gestionar Pokemon manualmente |
| **Imagenes de sprites** | La tabla muestra la imagen oficial de cada Pokemon |
| **ETL idempotente** | El comando `load_pokemons` usa upsert, puede ejecutarse multiples veces sin duplicar datos |

---

## Tecnologias utilizadas

| Categoria | Tecnologia |
|-----------|------------|
| Backend | Python 3.12, Django 6.0.1 |
| Base de datos | PostgreSQL 15 |
| Servidor WSGI | Gunicorn |
| Archivos estaticos | WhiteNoise |
| Contenedores | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Linting | flake8 |
| Frontend | Bootstrap 5, HTML5 |

---

## Como ejecutar el proyecto

### Requisitos previos

- Docker y Docker Compose instalados
- Git

### Pasos
1. **Iniciar Docker Desktop**

2. **Clonar el repositorio**

```bash
git clone https://github.com/dvoliva/pokedex-project.git
cd pokedex-project
```

2. **Configurar variables de entorno**

```bash
cp .env.example .env
```

Editar el archivo `.env` con tus valores (o dejar los de ejemplo para desarrollo).

3. **Levantar los contenedores**

```bash
docker-compose up --build
```

4. **Acceder a la aplicacion**

Abrir en el navegador: [http://localhost:8000](http://localhost:8000)

### Que sucede al iniciar

1. Docker Compose levanta PostgreSQL y espera a que este listo (health check)
2. Django ejecuta las migraciones de base de datos
3. El comando `load_pokemons` descarga los 50 Pokemon desde la PokeAPI
4. Gunicorn inicia el servidor en el puerto 8000

---

## Ejecutar tests
En una terminal nueva:

```bash
docker-compose exec web python src/manage.py test pokemons
```

### Resultado esperado

```
Creating test database for alias 'default'...
.....
----------------------------------------------------------------------
Ran 5 tests in 0.XXXs

OK
```

---

## Estructura del proyecto

```
pokedex-project/
├── .github/workflows/
│   └── ci.yml              # pipeline de integracion continua
├── src/
│   ├── config/             # configuracion del proyecto django
│   │   ├── settings.py     # configuracion principal con variables de entorno
│   │   ├── urls.py         # rutas principales
│   │   └── wsgi.py         # punto de entrada para gunicorn
│   └── pokemons/           # aplicacion principal
│       ├── management/commands/
│       │   └── load_pokemons.py  # etl: descarga pokemon de la api
│       ├── templates/pokemons/
│       │   └── list.html   # template del dashboard
│       ├── models.py       # modelo de datos pokemon
│       ├── views.py        # logica de filtros
│       ├── urls.py         # rutas de la app
│       ├── admin.py        # configuracion del admin
│       └── tests.py        # suite de pruebas
├── Dockerfile              # imagen multi-stage optimizada
├── docker-compose.yml      # orquestacion de servicios
├── requirements.txt        # dependencias python
├── .env.example            # plantilla de variables de entorno
└── .gitignore              # archivos ignorados por git
```

---

## Notas adicionales

- Los datos de peso y altura estan en las unidades originales de la PokeAPI (hectogramos y decimetros)
- El proyecto esta desplegado en: https://pokedex-project-nzff.onrender.com/

---

## Autor

Diego Venegas Oliva

---

Desarrollado como prueba tecnica - 2026
