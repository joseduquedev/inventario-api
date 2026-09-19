# 📦 Inventario API

API REST para la gestión de inventario de productos, con autenticación 
JWT, desarrollada con FastAPI y SQLAlchemy, con persistencia en base 
de datos SQLite.

Proyecto construido ampliando mi stack backend (PHP/MySQL) con Python 
y FastAPI, aplicando buenas prácticas de arquitectura de APIs REST: 
autenticación, validaciones de negocio, manejo de errores HTTP y 
testing automatizado.

## ¿Qué hace?

Permite gestionar el inventario de productos de un negocio: registro 
y login de usuarios con autenticación JWT, creación, consulta, 
actualización y eliminación de productos (protegidas por login), y 
filtrado por nombre.

## Tecnologías

- Python 3
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Pydantic (validación de datos)
- Passlib + bcrypt (hash de contraseñas)
- python-jose (tokens JWT)
- pytest (testing automatizado)
- Uvicorn (servidor ASGI)

## Endpoints

### Autenticación

| Método | Ruta | Descripción | Requiere token |
|--------|------|-------------|----------------|
| POST | `/usuarios` | Registra un nuevo usuario | No |
| POST | `/login` | Inicia sesión y devuelve un token JWT | No |

### Productos

| Método | Ruta | Descripción | Requiere token |
|--------|------|-------------|----------------|
| GET | `/` | Mensaje de estado de la API | No |
| GET | `/productos` | Lista todos los productos (admite filtro opcional `?nombre=`) | No |
| GET | `/productos/{id}` | Obtiene un producto específico por su id | No |
| POST | `/productos` | Crea un nuevo producto | **Sí** |
| PUT | `/productos/{id}` | Actualiza un producto existente | **Sí** |
| DELETE | `/productos/{id}` | Elimina un producto | **Sí** |

## Autenticación

La API usa JWT (JSON Web Tokens). Tras un login exitoso, se devuelve 
un `access_token` que debe enviarse en el header `Authorization` de 
las rutas protegidas:

Authorization: Bearer <tu_token>


### Reglas de contraseña (registro)

- Mínimo 8 caracteres
- Al menos 1 número
- Al menos 1 letra mayúscula
- Al menos 1 carácter especial

## Modelo de datos

**Producto**
```json
{
  "nombre": "string",
  "descripcion": "string",
  "precio": 0.0,
  "cantidad_disponible": 0
}
```

**Usuario (registro)**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "Ejemplo123!"
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
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto con una clave secreta 
propia:

SECRET_KEY=tu_clave_secreta_generada


Puedes generar una clave segura con:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Ejecutar el servidor:
```bash
uvicorn main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`, y la documentación 
interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

## Ejecutar los tests

```bash
pytest
```

Los tests usan una base de datos SQLite en memoria, aislada de la base 
de datos real.

## Características técnicas

- Autenticación JWT con expiración de token
- Contraseñas hasheadas con bcrypt (nunca almacenadas en texto plano)
- Validación de datos con Pydantic (email válido, reglas de contraseña)
- Manejo de errores HTTP correcto (401, 404, 422)
- Separación de responsabilidades: modelos Pydantic (API) vs modelos 
  SQLAlchemy (base de datos)
- Persistencia real en base de datos, no en memoria
- Suite de tests automatizados con pytest
- Clave secreta gestionada por variables de entorno (no expuesta en 
  el código)

## Autor

**José Humberto Duque Castiblanco**  
Ingeniero de Sistemas | Backend Developer (PHP/MySQL, Python/FastAPI)  
Envigado, Colombia