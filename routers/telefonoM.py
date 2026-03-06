from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from db import SessionDep, get_Session
from models import Telefonos, Usuarios
from .auth import validarToken
import httpx

router = APIRouter(prefix = "/telefonos", tags = ["Validacion"])

#llamada a la api de Veriphone
async def consultaVeriphone(numero: str) -> dict | None:
    URL = "https://api.veriphone.io/v2/verify"
    params = {"phone": numero, "key": "884D6E4C095347CD8804D6825C2A868F"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(URL,params = params)
        data = resp.json()

        if data.get("phone_valid"):
            return{
                "numero": data.get("phone"),
                "pais": data.get("country"),
                "tipo": "Celular"if data.get("phone_type") == "mobile" or "fixed_line_or_mobile" else "fijo",
                "codigo_pais": data.get("country_code"),
                "compañia": data.get("carrier") or "Desconocido",
                "api_Utilizada":"Veriphone"
            }
    except Exception:
        pass
    return None

#llamada a la api de Numverify
async def consultaNumverify(numero:str) -> dict | None:
    URL = "http://apilayer.net/api/validate"
    params = {"number": numero, "access_key": "bf0dbbb2e606fe41486ad649a0bf72e2"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(URL,params = params)
        data = resp.json()

        print("Error de numverify: ", data)

        if data.get("valid"):
            return{
                "numero": data.get("international_format") or numero,
                "pais": data.get("country_name"),
                "tipo": "Celular" if data.get("line_type") == "mobile" else "Fijo",
                "codigo_pais": data.get("country_code"),
                "compañia": data.get("carrier") or "Desconocida",
                "api_Utilizada":"NumVerify"
            }

    except Exception:
        pass

    return None

#llamada a la api de numlook
async def consultaNumlook(numero:str) -> dict | None:
    URL = f"https://api.numlookupapi.com/v1/validate/{numero}"
    params = {"apikey":"num_live_vx8a2KrD25ZBuqe5GaTQizwqDseahgHH6a3LDtyR"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(URL, params = params)
        data = resp.json()

        print("Error de NumLook: ", data)

        if data.get("valid"):
            return{
                "numero": data.get("international_format"),
                "pais": data.get("country_name"),
                "tipo": "Celular" if data.get("line_type") == "mobile" else "Fijo",
                "codigo_pais": data.get("country_code"),
                "compañia": data.get("carrier"),
                "api_Utilizada": "Numlook"
           }
    except Exception:
        pass

    return None

@router.post("/Verificar/{numero}")
async def verificar_numero(numero:str, api:str = Query("auto"), session: Session = Depends(get_Session), usuarioActual: Usuarios = Depends(validarToken)):

    db_tel = session.exec(select(Telefonos).where(Telefonos.numero == numero)).first()

    if db_tel:
       return {
           "status" : "success",
           "data": {
               "statuscode": "03",
               "telefono": db_tel.numero,
               "pais": db_tel.pais,
               "tipo": db_tel.tipo,
               "compañia": db_tel.compañia,
               "codigo_pais": db_tel.codigo_pais,
               "api_Utilizada": db_tel.api_Utilizada,
               "mensaje": "Recuperado de la base de datos local"
           }
       }

    datos_tel = None

    #eleccion de apis
    if api == "numverify":
       datos_tel = await consultaNumverify(numero)
    elif api == "veriphone":
       datos_tel = await consultaVeriphone(numero)
    elif api == "numlook":
       datos_tel = await consultaNumlook(numero)
    else:

       datos_tel = await consultaNumverify(numero)

       if not datos_tel:
          print("Numverify no lo encontró, intentando con Veriphone")
          datos_tel = await consultaVeriphone(numero)

       if not datos_tel:
          print("veriphone y NumVerify no lo encontraron, intentando con Numlook")
          datos_tel = await consultaNumlook(numero)

    if not datos_tel:
        return{
            "status": "success",
            "data": {
                "statuscode": "02",
                "telefono": numero,
                "mensaje": "número inválido."
            }
        }

    nuevo_tel = Telefonos(
       numero = datos_tel["numero"].replace("+",""),
       pais = datos_tel["pais"],
       tipo = datos_tel["tipo"],
       codigo_pais = datos_tel["codigo_pais"],
       compañia = datos_tel["compañia"],
       api_Utilizada = datos_tel["api_Utilizada"]
    )

    session.add(nuevo_tel)
    session.commit()
    session.refresh(nuevo_tel)

    return {
        "status": "success",
        "data": {
            "statuscode": "01",
            "telefono": nuevo_tel.numero,
            "zona": nuevo_tel.pais,
            "tipo": nuevo_tel.tipo,
            "Proveedor": nuevo_tel.compañia,
            "mensaje": "Número añádido con éxito."
        }
    }

@router.get("/",response_model = list[Telefonos])
def leerTelefono(Session: SessionDep,
                 offset:int = 0,
                 limit: Annotated[int,Query(le = 100)]= 100):
    telefonos = Session.exec(select(Telefonos).offset(offset).limit(limit)).all()
    return telefonos
