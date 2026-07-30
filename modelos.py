from pydantic import BaseModel
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

