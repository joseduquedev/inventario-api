from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from modelos import Producto, ProductoDB
from database import engine, Base, get_db

from typing import Optional

from modelos import Producto, ProductoDB, UsuarioDB, UsuarioRegistro
from auth import (
    hashear_password,
    verificar_password,
    crear_token,
    obtener_usuario_actual,
)

from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI()

# simulación de la base de datos
inventario = []
# variable id
contador_id = 1


# endpoint de prueba


@app.get("/")
def inicio():
    return {"mensaje": "Api de inventario en proceso de desarrollo"}


@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    item = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item


@app.get("/productos")
def listar_productos(nombre: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(ProductoDB)
    if nombre:
        query = query.filter(ProductoDB.nombre.ilike(f"%{nombre}%"))
    return query.all()


@app.post("/productos")
def crear_producto(
    producto: Producto,
    db: Session = Depends(get_db),
    usuario: str = Depends(obtener_usuario_actual),
):
    nuevo_producto = ProductoDB(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        cantidad_disponible=producto.cantidad_disponible,
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return {"mensaje": "Producto creado", "producto": nuevo_producto}


@app.put("/productos/{producto_id}")
def actualizar_producto(
    producto_id: int,
    producto: Producto,
    db: Session = Depends(get_db),
    usuario: str = Depends(obtener_usuario_actual),
):
    item = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    item.nombre = producto.nombre
    item.descripcion = producto.descripcion
    item.precio = producto.precio
    item.cantidad_disponible = producto.cantidad_disponible
    db.commit()
    db.refresh(item)
    return {"mensaje": "Producto actualizado", "producto": item}


@app.delete("/productos/{producto_id}")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(obtener_usuario_actual),
):
    item = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(item)
    db.commit()
    return {"mensaje": "Producto eliminado", "producto": item}


@app.post("/usuarios")
def registrar_usuario(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    usuario_existente = (
        db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first()
    )
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ese email ya está registrado")

    nuevo_usuario = UsuarioDB(
        email=usuario.email, password_hash=hashear_password(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado con éxito", "email": nuevo_usuario.email}


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    usuario_db = (
        db.query(UsuarioDB).filter(UsuarioDB.email == form_data.username).first()
    )

    if usuario_db is None or not verificar_password(
        form_data.password, usuario_db.password_hash
    ):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    token = crear_token(usuario_db.email)
    return {"access_token": token, "token_type": "bearer"}
