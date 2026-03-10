#importaciones
from typing import Optional
from fastapi import FastAPI,status,HTTPException, Depends
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Iniciaclización o instancia de la API
app= FastAPI(
    title='Mi primer API',
    description='Silva Ongay Saúl',
    version='1.0'
)

#BD ficticia
citas=[
    {"id":1,"cita":"hora", 18:10 ,"nombre":"Juanes","edad":50},
    {"id":2,"cita":"hora", 19:10 ,"nombre":"Emiliano","edad":21},
    {"id":3,"cita":"hora", 20:10 ,"nombre":"Mauchín","edad":48},
]

#Modelo de validacion Pydantic
class CitasBase(BaseModel):
    id:int = Field(...,gt=0,description="Identificador de usuario", example="1")
    nombre:str = Field(...,min_length=5, max_length= 50, description="Nombre del usuario")
    edad:int = Field(...,ge=0, le=121, description= "Edad válida entre 0 y 121")
    fecha:int = Field(..., max_length= 100, description="Motivo no máximo de 100 caracteres")

security = HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usaurioAuth = secrets.compare_digest(credentials.username,"SaulSilvaOngay")
    contraAuth = secrets.compare_digest(credentials.password,"1234")

    if not (usaurioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas xdxd",
        )
    
    return credentials.username


#Endpoints
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Consultorio Médico"}




@app.get("/v1/citas/", tags=['CRUD citas'])
async def consultaCitas():
    
    return{
        "status":"200",
        "total": len(citas),
        "data":citas
    }

#
@app.get("/v1/buscarcita/{id}", tags=['Parametro obligatorio'])
async def consultaCitas(id:int):
    await asyncio.sleep(3)
    return {"Cita encontrada":id}


@app.post("/v1/citas/", tags=['CRUD citas'])
async def agregar_citas(citas:CitasBase):
    for usr in citas:
        if usr["id"] == citas.id:
            raise HTTPException(
            status_code= 400,
            detail= "El ID ya existe xd"
        )
    citas.append(citas)
    return{
        "mensaje": "Cita agregada exitosamente",
        "datos":citas,
        "status":"200"
    }


@app.delete("/v1/cita/{id}", tags=['CRUD Citas'])
async def eliminar_cita(id: int, citasAuth: str = Depends(verificar_Peticion)):

    for idx, usr in enumerate(citas):
        if usr["id"] == id:
            del citas[idx]
            return {
                "mensaje": f"Usuario eliminado exitosamente por {citasAuth}",
                "status": "200"
            }
        raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )
    
#Swagger es lo que se utiliza para la documentación automática