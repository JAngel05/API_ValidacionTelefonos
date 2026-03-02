from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from db import SessionDep, get_Session
from models import Telefonos
import httpx

router = APIRouter(prefix = "/telefonos", tags = ["Validacion"])

API_KEY = "884D6E4C095347CD8804D6825C2A868F"
VERIPHONE_URL = "https://api.veriphone.io/v2/verify"


@router.post("/Verificar/{numero}", response_model=Telefonos)
async def VerificarGuardar(numero:str, session = Depends(get_Session)):
    db_tel = session.exec(select(Telefonos).where(Telefonos.numero == numero)).first()
    if db_tel:
        return db_tel

    url = VERIPHONE_URL
    params = {"phone": numero, "key": API_KEY}

    async with httpx.AsyncClient() as Client:
        resp = await Client.get(url, params = params)
    data = resp.json()
    if not data.get("phone_valid"):
       raise HTTPException(status_code = 400, detail = "Número no válido por el proveedor")

    nuevo_tel = Telefonos(
        numero = data.get("phone"),
        pais = data.get("country"),
        tipo = "Celular" if data.get("phone_type" )== "mobile"
                     else "Fijo",
        compañia = data.get("carrier", ""))
    session.add(nuevo_tel)
    session.commit()
    session.refresh(nuevo_tel)
    return nuevo_tel
