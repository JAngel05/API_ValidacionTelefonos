from sqlmodel import Session, create_engine, Session as SessionType
from typing import Annotated, Generator
from fastapi import Depends

DATABASE_URL = "mysql+pymysql://jjesus:jjesus005@localhost/ProyectoT"

engine = create_engine (DATABASE_URL, echo = True)

def get_Session() -> Generator[SessionType, None, None]: 
    with Session (engine) as session:
          yield session

SessionDep = Annotated[SessionType, Depends(get_Session)]

