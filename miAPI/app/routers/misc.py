from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags= ["Varios"])

#Endpoints
@router.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI "}

@router.get("/")
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST "}

@router.get("/")
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"calificacion en TAI es 7 "}

@router.get("/")
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado":id}

@router.get("/")
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios: #Se busca usuario en el diccionario de usuarios
            if usuario["id"]== id:
                return { "Usuario encontrado":id,
                        "Datos": usuario 
                        }
            
        return {"Mensaje":"Usuario no encontrado"}
    
    else: 
        return {"AVISO":"No se proporcionó ID"}