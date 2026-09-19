import re
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import Column, Integer, String, Float
from database import Base

# ---- Modelo SQLAlchemy: define la tabla en la base de datos ----
class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=True)
    cantidad_disponible = Column(Integer, nullable=True)

# ---- Modelo Pydantic: define la forma del JSON que entra/sale por la API ----
class Producto(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    cantidad_disponible: int


# ---- Modelo SQLAlchemy: tabla de usuarios ----
class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)


# ---- Modelo Pydantic: datos que recibe el endpoint de registro ----
class UsuarioRegistro(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validar_password(cls, valor: str) -> str:
        if len(valor) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[0-9]", valor):
            raise ValueError("La contraseña debe tener al menos un número")
        if not re.search(r"[A-Z]", valor):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", valor):
            raise ValueError("La contraseña debe tener al menos un carácter especial")
        return valor

