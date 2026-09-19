from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from modelos import Producto, ProductoDB
from database import engine, Base, get_db

from typing import Optional

from modelos import Producto, ProductoDB, UsuarioDB, UsuarioRegistro
from auth import hashear_password

Base.metadata.create_all(bind=engine)

app = FastAPI()

#simulación de la base de datos
inventario = []
#variable id
contador_id= 1


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
def listar_productos(nombre: Optional[str] = None , db: Session = Depends(get_db)):
    query = db.query(ProductoDB)
    if nombre:
        query = query.filter(ProductoDB.nombre.ilike(f"%{nombre}%"))
    return query.all()

@app.post("/productos")
def crear_producto(producto: Producto, db: Session = Depends(get_db)):
    nuevo_producto = ProductoDB(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        cantidad_disponible=producto.cantidad_disponible
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return {"mensaje": "Producto creado", "producto": nuevo_producto}

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto, db: Session = Depends(get_db)):
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
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    item = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(item)
    db.commit()
    return {"mensaje": "Producto eliminado", "producto": item}


@app.post("/usuarios")
def registrar_usuario(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ese email ya está registrado")

    nuevo_usuario = UsuarioDB(
        email=usuario.email,
        password_hash=hashear_password(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado con éxito", "email": nuevo_usuario.email}

