</p><h1>Validador de Teléfonos Internacionales API</h1>
<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
</p>

<p>API RESTful construida con FASTApi y SQLModel</p>

<hr>
<h2>Características principales</h2>
<ul>
  <li><strong>Validación en cascada:</strong> Si un proveedor no encuentra el número, el sistema intenta automáticamente con el siguiente (Numverify ➔ Veriphone ➔ Numlook).</li>
  <li><strong>Caché inteligente:</strong> Antes de consumir créditos de las APIs externas, el sistema verifica si el número ya fue validado y guardado en la base de datos local.</li>
  <li><strong>Persistencia de Datos:</strong> Almacena el número, país, tipo de línea (móvil/fija), compañía telefónica y la API que logró validarlo.</li>
  <li><strong>Paginación integrada:</strong> Endpoint optimizado para listar los teléfonos validados con soporte para <code>limit</code> y <code>offset</code>.</li>
</ul> 

<h2>Tecnología</h2>
<ul>
  <li><strong>Framework Web:</strong> <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a></li>
  <li><strong>ORM & Base de Datos:</strong> <a href="https://sqlmodel.tiangolo.com/" target="_blank">SQLModel</a> / MySQL (PyMySQL)</li>
  <li><strong>Peticiones HTTP:</strong> <a href="https://www.python-httpx.org/" target="_blank">HTTPX</a> (Asíncronas)</li>
</ul>

<h2>Requisitos previos</h2
<ul>
  <li>Python 3.10 o superior.</li>
  <li>Servidor MySQL/MariaDB en ejecución.</li>
</ul>

<h2>Instalación y configuración</h2>
<p><strong>1. Clonar el repositorio y crear un entorno virtual:</strong></p>
<pre><code>git clone &lt;tu-repositorio&gt;
cd &lt;tu-carpeta-del-proyecto&gt;
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
</code></pre>

<p><strong>2. Instalar las dependencias:</strong></p>
<pre><code>pip install fastapi sqlmodel uvicorn pymysql httpx
</code></pre>

<p><strong>3. Configuración de la Base de Datos:</strong></p>
<p>Asegúrate de tener una base de datos llamada <code>ProyectoT</code> en tu servidor local MySQL.<br>

<p><strong>4. Ejecutar la aplicación:</strong></p>
<pre><code>uvicorn main:app --host 0.0.0.0 --port 8000 
</code></pre>
<p>La API estará disponible en <code>http://localhost:8000</code>. Puedes acceder a la documentación interactiva en <code>http://localhost:8000/docs</code>.</p>

<hr>

<h2>Endpoints Principales</h2>

<h3>1. Estado del Servidor</h3>
<ul>
  <li><strong>GET</strong> <code>/</code></li>
  <li><strong>Descripción:</strong> Verifica que la API esté en línea.</li>
</ul>

<h3>2. Verificar Número</h3>
<ul>
  <li><strong>POST</strong> <code>/telefonos/Verificar/{numero}</code></li>
  <li><strong>Descripción:</strong> Toma el número proporcionado, revisa la base de datos local y, si no existe, consulta las APIs externas.</li>
  <li><strong>Ejemplo de Respuesta:</strong></li>
</ul>
<pre><code>{
  "id": 1,
  "numero": "+525512345678",
  "pais": "Mexico",
  "tipo": "Celular",
  "compañia": "Telcel",
  "api_Utilizada": "NumVerify"
}
</code></pre>

<h3>3. Listar Teléfonos Guardados</h3>
<ul>
  <li><strong>GET</strong> <code>/telefonos/</code></li>
  <li><strong>Descripción:</strong> Devuelve una lista de los teléfonos ya validados y guardados en la base de datos.</li>
  <li><strong>Parámetros Query:</strong> <code>offset</code> (int, default=0), <code>limit</code> (int, default=100, max=100).</li>
</ul>

<hr>
<h2>Version:</h2>
<p>Version 1.0</p>

<hr>
<h3>Creado por:</h3> 
<p>Jesus Angel Alvaro Castillo.</p>
