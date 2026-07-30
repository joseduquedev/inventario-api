from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from modelos import Producto, ProductoDB
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

#simulación de la base de datos
inventario = []
#variable id
contador_id= 1


@app.get("/")
def inicio():
    return {"mensaje": "Api de inventario en proceso de desarrollo"}

@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    #return inventario
    return db.query(ProductoDB).all()

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
        return {"error": "Producto no encontrado"}
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
        return {"error": "Producto no encontrado"}
    db.delete(item)
    db.commit()
    return {"mensaje": "Producto eliminado", "producto": item}

'''
@app.post("/productos")
def crear_producto(producto: Producto):
    global contador_id
    nuevo_producto = producto.model_dump()
    nuevo_producto["id"] = contador_id
    contador_id += 1
    inventario.append(nuevo_producto)
    return {"mensaje": "Producto creado", "producto": producto}


@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto):
    for item in inventario:
        if item["id"]== producto_id:
            item["nombre"] = producto.nombre
            item["descripcion"] = producto.descripcion
            item["precio"] = producto.precio
            item["cantidad_disponible"] = producto.cantidad_disponible
            return {"mensaje": "Producto actualizado" , "producto": item}
    return {"error": "Producto no encontrado"}

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    for item in inventario:
        if item["id"] == producto_id:
            inventario.remove(item)
            return {"mensaje": "Producto eliminado" , "producto": item}
    return {"error": "Producto no encontrado"}
'''

