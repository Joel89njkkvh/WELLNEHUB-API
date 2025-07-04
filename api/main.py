from fastapi import FastAPI
from routes import user
from database.connection import Base, engine
from models import user as user_model

# Crear las tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WellnesHub API")

# Registrar rutas
app.include_router(user.router, prefix="/api/user", tags=["Usuarios"])
