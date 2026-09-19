import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# Base de datos separada, solo para tests, en memoria (no se guarda en disco)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_inicio():
    response = client.get("/")
    assert response.status_code == 200


def test_crear_producto():
    nuevo_producto = {
        "nombre": "Producto de prueba",
        "descripcion": "Creado desde un test automatizado",
        "precio": 15000.0,
        "cantidad_disponible": 5
    }
    response = client.post("/productos", json=nuevo_producto)
    assert response.status_code == 200
    data = response.json()
    assert data["producto"]["nombre"] == "Producto de prueba"


def test_listar_productos():
    response = client.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_producto_inexistente():
    response = client.get("/productos/99999")
    assert response.status_code == 404