
from sqlmodel import SQLModel, Field

class Telefonos(SQLModel, table  = True):
      id: int | None = Field(default = None, index= True, primary_key = True)
      numero: str
      tipo: str
      compañia: str
      pais: str
      api_Utilizada: str
