# API de aprendices SENA

Proyecto académico de **Carlos Narváez, aprendiz del SENA**. Esta aplicación
implementa una API REST para registrar y administrar aprendices con FastAPI y
MongoDB, además de un cliente interactivo de consola que consume sus endpoints
mediante la librería `requests`.

## Tabla de contenido

- [Funciones](#funciones)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y configuración](#instalación-y-configuración)
- [Ejecución](#ejecución)
- [Uso de la consola](#uso-de-la-consola)
- [Endpoints de la API](#endpoints-de-la-api)
- [Modelo de datos](#modelo-de-datos)
- [Respuestas y errores](#respuestas-y-errores)
- [Pruebas](#pruebas)
- [Solución de problemas](#solución-de-problemas)
- [Seguridad](#seguridad)

## Funciones

- Crear aprendices con validación de datos y correo electrónico.
- Consultar todos los registros o uno específico por su identificador.
- Actualizar los campos enviados de un aprendiz.
- Eliminar un registro con confirmación desde la consola.
- Comprobar el estado de la conexión con MongoDB.
- Consultar la API desde un menú de consola con `requests`.
- Explorar y probar endpoints con la documentación OpenAPI de FastAPI.

## Tecnologías

- **Python 3.10 o superior**: el código usa tipos como `str | None`.
- **FastAPI**: API REST y documentación OpenAPI.
- **Pydantic y EmailStr**: validación de datos y correos.
- **PyMongo**: conexión y operaciones con MongoDB.
- **Requests**: peticiones HTTP desde la aplicación de consola.
- **Uvicorn**: servidor ASGI para ejecutar la API.
- **Certifi**: certificados CA para la conexión TLS a MongoDB.
- **Unittest y FastAPI TestClient**: pruebas automatizadas.

Las dependencias están declaradas en [`requirements.txt`](./requirements.txt).

## Estructura del proyecto

```text
FastApi_BD/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py       # Configuración y conexión a MongoDB
│   │   └── model.py          # Modelos y validaciones Pydantic
│   ├── templates/
│   │   └── controllers.py    # Operaciones CRUD y errores HTTP
│   └── views/
│       ├── __init__.py
│       ├── health.py         # Endpoint de diagnóstico de MongoDB
│       ├── main.py           # Aplicación FastAPI y endpoints REST
│       └── views.py          # Menú CLI; cliente HTTP con requests
├── test/
│   └── test_main.py          # Pruebas automatizadas sin MongoDB real
└── data/                     # Directorio de datos del proyecto
```

## Requisitos

- Python 3.10 o superior.
- Una instancia de MongoDB, local o alojada (por ejemplo, MongoDB Atlas).
- Acceso a la red para instalar dependencias y consumir la API.

## Instalación y configuración

Clona el repositorio y entra al directorio del proyecto:

```bash
git clone https://github.com/22CarlosNarvaez/Fast_API.git
cd Fast_API
```

Se recomienda crear un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

Configura la URI de MongoDB en la variable de entorno `MONGO_URL`. No agregues
credenciales al código ni al repositorio.

Linux o macOS:

```bash
export MONGO_URL='mongodb+srv://usuario:contraseña@cluster.mongodb.net/'
```

Windows PowerShell:

```powershell
$env:MONGO_URL = 'mongodb+srv://usuario:contraseña@cluster.mongodb.net/'
```

La configuración admite estas variables opcionales:

| Variable | Valor predeterminado | Descripción |
|---|---|---|
| `MONGO_URL` | Sin valor | URI de conexión. Es necesaria para operaciones de base de datos. |
| `MONGO_DB_NAME` | `amb703` | Nombre de la base de datos. |
| `MONGO_COLLECTION_NAME` | `trainee` | Nombre de la colección de aprendices. |
| `API_BASE_URL` | `https://fast-api-97xd.onrender.com` | Dirección base a la que se conecta el cliente de consola. |

Para ejecutar la consola contra una API iniciada localmente, configura también:

Linux o macOS:

```bash
export API_BASE_URL='http://127.0.0.1:8000'
```

Windows PowerShell:

```powershell
$env:API_BASE_URL = 'http://127.0.0.1:8000'
```

En MongoDB Atlas, verifica que el usuario tenga permisos sobre la base de datos
y que la dirección IP del equipo esté autorizada en **Network Access**. Si la
contraseña contiene caracteres especiales, codifícala para usarla en la URI.

## Ejecución

Inicia la API desde la raíz del repositorio:

```bash
uvicorn src.views.main:app --reload
```

La API local queda disponible en `http://127.0.0.1:8000`. Deja ese proceso en
ejecución y abre otra terminal para iniciar el cliente de consola:

```bash
python -m src.views.views
```

La consola usa Render por defecto. Para que utilice el servidor local, define
`API_BASE_URL=http://127.0.0.1:8000` en el entorno antes de abrirla.

Documentación interactiva:

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

Si `MONGO_URL` no está configurada, el servidor puede iniciar, pero los
endpoints que necesitan MongoDB responden con HTTP 503.

## Uso de la consola

Al ejecutar `python -m src.views.views`, aparece un menú:

```text
1. Inicio de la API
2. Estado de MongoDB
3. Crear aprendiz
4. Listar aprendices
5. Buscar por ID
6. Actualizar aprendiz
7. Eliminar aprendiz
0. Salir
```

Para crear un registro, ingresa los siete campos solicitados. La edad debe ser
un número entero y el correo debe tener un formato válido. Para modificar un
registro, deja en blanco los campos que no quieras cambiar; la consola solicita
confirmación antes de eliminar. Los errores HTTP y de conexión se muestran en
la terminal.

## Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Mensaje de bienvenida. |
| `GET` | `/health/db` | Comprueba la disponibilidad de MongoDB. |
| `POST` | `/trainees` | Crea un aprendiz. |
| `GET` | `/trainees` | Lista todos los aprendices. |
| `GET` | `/trainees/{trainee_id}` | Busca un aprendiz por su ID de MongoDB. |
| `PUT` | `/trainees/{trainee_id}` | Actualiza uno o más campos del aprendiz. |
| `DELETE` | `/trainees/{trainee_id}` | Elimina el aprendiz indicado. |

Ejemplo de cuerpo para crear un aprendiz:

```json
{
  "document": "123456789",
  "firstname": "Ana",
  "lastname": "Pérez",
  "email": "ana.perez@example.com",
  "age": 20,
  "program": "Análisis y Desarrollo de Software",
  "record_number": "1234567"
}
```

Ejemplo de actualización parcial mediante `PUT`:

```json
{
  "program": "Desarrollo de Software",
  "age": 21
}
```

El ID usado en las rutas individuales es el valor `id` devuelto por la API
(representación hexadecimal de un `ObjectId` de MongoDB).

## Modelo de datos

| Campo | Tipo | Requerido al crear | Validación |
|---|---|---:|---|
| `document` | Cadena | Sí | Documento del aprendiz. |
| `firstname` | Cadena | Sí | Nombre. |
| `lastname` | Cadena | Sí | Apellido. |
| `email` | Cadena | Sí | Debe ser un correo válido. |
| `age` | Entero | Sí | Edad del aprendiz. |
| `program` | Cadena | Sí | Programa de formación. |
| `record_number` | Cadena | Sí | Número de ficha. |

Las respuestas de consulta incluyen además `id`, generado a partir del
identificador `_id` almacenado por MongoDB.

## Respuestas y errores

- **200 OK**: consulta, actualización o eliminación completada.
- **200 OK**: comprobación de base de datos exitosa, con
  `{"status": "ok", "database": "connected"}`.
- **422 Unprocessable Entity**: datos de entrada inválidos; por ejemplo, correo
  no válido o campos requeridos ausentes al crear.
- **400 Bad Request**: solicitud de actualización sin campos para modificar.
- **404 Not Found**: ID de aprendiz inválido o aprendiz inexistente.
- **503 Service Unavailable**: MongoDB no está configurado o no puede completar
  la operación.

Los detalles del error se devuelven en la respuesta JSON de FastAPI bajo la
propiedad `detail`.

## Pruebas

Desde la raíz del proyecto, ejecuta:

```bash
python -m unittest discover -s test -v
```

Las pruebas verifican las llamadas HTTP que genera la consola, el menú CRUD y
algunos estados de la API. No requieren una conexión real a MongoDB.

## Solución de problemas

### La consola no puede conectarse a la API

Comprueba que la dirección impresa al iniciar el cliente sea la esperada. Para
usar el servidor local, verifica que Uvicorn esté ejecutándose y define
`API_BASE_URL=http://127.0.0.1:8000`.

### La API responde HTTP 503

Configura `MONGO_URL`, revisa que sea válida y confirma el acceso de red y los
permisos del usuario de MongoDB. Los nombres de base y colección se pueden
ajustar con `MONGO_DB_NAME` y `MONGO_COLLECTION_NAME`.

### La instalación de paquetes no está permitida por el sistema

Algunas distribuciones de Linux protegen el Python global. Crea y activa el
entorno virtual descrito en [Instalación y configuración](#instalación-y-configuración)
y vuelve a ejecutar `python -m pip install -r requirements.txt` dentro de él.

### FastAPI muestra un error de validación

Consulta el contenido de `detail` en la respuesta o usa `/docs` para revisar el
esquema esperado. Para crear registros, todos los campos del modelo son
obligatorios y `email` debe tener formato de correo.

## Seguridad

- Mantén `MONGO_URL` fuera del código, de capturas de pantalla y del control de
  versiones.
- No subas archivos con credenciales ni compartas URIs de conexión.
- Si una contraseña o URI fue expuesta, cámbiala en MongoDB y actualiza la
  variable de entorno.
- En un entorno público o productivo, restringe el acceso de red y configura
  autenticación, HTTPS y controles de acceso según las necesidades del servicio.
