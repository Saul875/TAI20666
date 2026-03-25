from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

#1. deninir la URL de conexión
DATABASE_URL= os.getenv(
    "DATABASE_URL", "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2. Creamos el motor de conexión
engine= create_engine(DATABASE_URL)

#3. Agregamos el gestor de sesiones
SesionLocal= sessionmaker(autocommit= False, autoflush= False, bind= engine)

#4. Base declarativa para modelos
Base= declarative_base()

#5. funcion para el manejo en session en los request
def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
        