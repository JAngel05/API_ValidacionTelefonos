from fastapi import FastAPI
from db import engine
from sqlmodel import SQLModel
from routers import telefono

app = FastAPI(title = "Validación de teléfonos")

@app.on_event("startup")
def Inicio():
    SQLModel.metadata.create_all(engine)

app.include_router(telefono.router)

@app.get("/")
def root(): 
    return{"status":"online"}
