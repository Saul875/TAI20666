from typing import Optional
from fastapi import FastAPI,status,HTTPException
import asyncio
from pydantic import BaseModel, Field

app = FastAPI(
    title='API de Biblioteca Digital',
    description='Control de libros y préstamos',
    version='1.0'
)

# BD ficticia
libros = [
    {"id": 1, "titulo": "La chica del Tren", "autor": "Paula Hawkins", "fecha_de_publicacion": 2015, "estado": "disponible"},
    {"id": 2, "titulo": "Escrito en el agua", "autor": "Paula Hawkings", "fecha_de_publicacion": 2011, "estado": "prestado"},
]

prestamos = []

#Pydantics
#Libro
class LibroBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único del libro", example=1)
    titulo: str = Field(..., min_length=2, max_length=100, description="Título del libro", example="Escrito en el Agua")
    autor: str = Field(..., min_length=2, max_length=100, description="Autor del libro", example="Paula Hawkins")
    anio_publicacion: int = Field(..., gt=1450, le=2026, description="Año de publicación del libro", example=2015)
    estado: str = Field(..., pattern="^(disponible|prestado)$", description="Estado del libro", example="disponible")

#Usuario
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único del usuario", example=1)
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre completo del usuario", example="Juan Pérez")
    correo: str = Field(..., pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Correo electrónico del usuario", example="juan.perez@mail.com")

#Prestamos
class PrestamoBase(BaseModel):
    libro_id: int = Field(..., gt=0, description="ID del libro", example=1)
    usuario_id: int = Field(..., gt=0, description="ID del usuario", example=1)

#Devolucion
class DevolverLibro(BaseModel):
    libro_id: int = Field(..., gt=0, description="ID del libro", example=1)

#Gets
@app.get("/", tags=['Inicio'])
async def Inicio():
    return {"mensaje": "Bienvenido a la API de Biblioteca Digital"}

@app.get("/v1/libros", tags=['Libros'])
async def lista_libros():
    return {"status": "200", "data": libros}

@app.get("/v1/libros/{id}", tags=['Libros'])
async def buscar_libro(id: int):
    for libro in libros:
        if libro["id"] == id:
            return {"status": "200", "data": libro}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

#Posts
@app.post("/v1/libros", tags=['Libros'])
async def registrar_libro(libro: LibroBase):
    for existing_libro in libros:
        if existing_libro["id"] == libro.id:
            raise HTTPException(status_code=409, detail="El libro ya existe")
    libros.append(libro.dict())
    return {"status": "201", "message": "Libro registrado correctamente", "data": libro}

@app.post("/v1/prestamos", tags=['Préstamos'])
async def registrar_prestamo(prestamo: PrestamoBase):
    for libro in libros:
        if libro["id"] == prestamo.libro_id:
            if libro["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="El libro ya está prestado")
            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())  # Registrar el préstamo
            return {"status": "200", "message": "Préstamo registrado correctamente", "data": prestamo}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/v1/devolver", tags=['Préstamos'])
async def devolver_libro(devolucion: DevolverLibro):
    for libro in libros:
        if libro["id"] == devolucion.libro_id:
            if libro["estado"] == "disponible":
                raise HTTPException(status_code=409, detail="El libro no está prestado")
            libro["estado"] = "disponible"

            prestamos[:] = [prestamo for prestamo in prestamos if prestamo["libro_id"] != devolucion.libro_id]
            return {"status": "200", "message": "Libro devuelto correctamente"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

