from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import status,HTTPException, Depends

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

