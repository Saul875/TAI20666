from fastapi import FastAPI,status,HTTPException, Depends, APIRouter
from pydantic import BaseModel
from app.models.usuario import UsuarioBase
from app.data.database import usuarios 
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB


router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD usuarios"]
    )


class UsuarioBase(BaseModel):
    nombre: str = None
    edad: int = None


#Get all users
@router.get("/")
async def consulta_Usuarios(db: Session = Depends(get_db)):

    consultausuarios= db.query(usuarioDB).all()

    return{
        "status":"200",
        "total": len(consultausuarios),
        "data":consultausuarios
    }


#Get user by ID
@router.get("/{id}")
async def consulta_Usuario_Id(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id) .first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Ese usuario no existe bro")
    return usuario


@router.post("/")
async def agregar_usuarios(Usuario:UsuarioBase,db: Session = Depends(get_db)):

    nuevo_usuario= usuarioDB(nombre=Usuario.nombre, edad=Usuario.edad)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)


    return{
        "mensaje": "Usuario agregado exitosamente",
        "datos":Usuario,
        "status":"200"
    }


@router.put("/{id}")
async def actualizar_usuario(id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    usuario_db = db.query(usuarioDB).filter(usuarioDB.id == id) .first()
    if not usuario_db:
            raise HTTPException(status_code=404, detail="Ese usuario no existe brother")
            
    usuario_db.nombre = usuario.nombre
    usuario_db.edad = usuario.edad

    db.commit()
    db.refresh(usuario_db)
    return usuario_db


@router.patch("/{id}")
async def patch_usuario(id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    usuario_db = db.query(usuarioDB).filter(usuarioDB.id == id) .first()
    if not usuario_db:
            raise HTTPException(status_code=404, detail="Ese usuario no existe brother, ni modo")
            
    if usuario.nombre is not None:
        usuario_db.nombre = usuario.nombre
    if usuario.edad is not None:
        usuario_db.edad = usuario.edad

    db.commit()
    db.refresh(usuario_db)
    return usuario_db


@router.delete("/{id}")
async def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Ese usuario no existe bro")
    
    db.delete(usuario_db)
    db.commit()
    
    return {"mensaje": "Usuario eliminado correctamente"}
