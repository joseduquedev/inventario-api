# 📦 Inventario API

API REST para la gestión de inventario de productos, desarrollada con 
FastAPI y SQLAlchemy, con persistencia en base de datos SQLite.

Proyecto construido como parte de mi proceso
de ampliación de stack backend, sumando Python y FastAPI
a mi experiencia previa en PHP/MySQL, aplicando buenas prácticas de 
arquitectura de APIs REST.

## ¿Qué hace?

Permite gestionar el inventario de productos de un negocio: crear, 
consultar, actualizar y eliminar productos, además de filtrar por nombre.

## Tecnologías

- Python 3
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Pydantic (validación de datos)
- Uvicorn (servidor ASGI)

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Mensaje de estado de la API |
| GET | `/productos` | Lista todos los productos (admite filtro opcional `?nombre=`) |
| GET | `/productos/{id}` | Obtiene un producto específico por su id |
| POST | `/productos` | Crea un nuevo producto |
| PUT | `/productos/{id}` | Actualiza un producto existente |
| DELETE | `/productos/{id}` | Elimina un producto |

## Modelo de datos

```json
{
  "nombre": "string",
  "descripcion": "string",
  "precio": 0.0,
  "cantidad_disponible": 0
}
```

## Cómo ejecutarlo localmente

```bash
git clone https://github.com/joseduquedev/inventario-api.git
cd inventario-api
python -m venv venv
```

Activar el entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

Instalar dependencias:
```bash
pip install fastapi uvicorn sqlalchemy
```

Ejecutar el servidor:
```bash
uvicorn main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`, y la documentación 
interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

## Características técnicas

- Validación automática de datos con Pydantic
- Manejo de errores HTTP correcto (404 para recursos no encontrados, 
  422 para datos inválidos)
- Separación de responsabilidades: modelos Pydantic (API) vs modelos 
  SQLAlchemy (base de datos)
- Persistencia real en base de datos, no en memoria

## Autor

**José Humberto Duque Castiblanco**  
Ingeniero de Sistemas | Backend Developer en formación (Python/FastAPI)  
Envigado, Colombia
