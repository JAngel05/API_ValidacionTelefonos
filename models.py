from sqlmodel import SQLModel, Field

class Telefonos(SQLModel, table  = True):
      id: int | None = Field(default = None, index= True, primary_key = True)
      numero: str = Field(max_length = 12)
      tipo: str
      compañia: str
      codigo_pais: str
      pais: str
      api_Utilizada: str

class Usuarios (SQLModel, table = True):
      id: int | None = Field(default = None, primary_key = True)
      username: str = Field(unique = True, index = True)
      password: str #Después de la prueba hashear la contraseña.
      rol: str = Field(default = "usuario")

class Tokens (SQLModel, table = True):
      id : int | None = Field(default = None, primary_key = True)
      token : str = Field (unique = True, index = True)
      activo: bool = Field(default = True)
      usuario_id: int | None = Field (default = None, foreign_key = "usuarios.id")
      creado_por_id: int | None = Field(default = None, foreign_key="usuarios.id")

class ProveedoresAPI(SQLModel, table = True):
      id: int | None = Field(default = None, primary_key = True)
      nombre: str = Field(unique = True, index = True)
      url_base: str
      api_key: str
      activa : bool = Field(default = True)
#peticiones
      parametro_num : str
      parametro_key : str
#mapeo
      llave_validacion : str
      llave_numero: str
      llave_pais: str
      llave_tipo: str
      valor_celular: str
      llave_codigo: str
      llave_company :str
