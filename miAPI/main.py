#importaciones
from typing import Optional
from fastapi import FastAPI
import asyncio

#Iniciaclización o instancia de la API
app= FastAPI(
    title='Mi primer API',
    description='Silva Ongay Saúl',
    version='1.0'
)

#BD ficticia
usuarios=[
    {"id":1,"nombre":"Saúl","edad":24},
    {"id":2,"nombre":"Memi","edad":21},
    {"id":3,"nombre":"Mauchín","edad":48},
]


#Endpoints
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI "}

@app.get("//v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST "}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"calificacion en TAI es 7 "}

@app.get("/v1/usuario/{id}", tags=['Parametro obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado":id}

@app.get("/v1/usuario_op/{id}", tags=['Parametro opcional'])
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
    
#Swagger es lo que se utiliza para la documentación automática

