
# TikTok Video Scraper API

Este proyecto es una API construida con FastAPI para descargar y almacenar videos de TikTok en una base de datos PostgreSQL utilizando Apify como proveedor de datos.

## Requisitos

- **Python 3.9+**
- **PostgreSQL**
- **Apify Account** (con token de API)

## Instalación

### 1. Clonar el repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu-usuario/tiktok-video-scraper-api.git
cd tiktok-video-scraper-api
```

### 2. Crear un entorno virtual

Crea y activa un entorno virtual:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual (en MacOS/Linux)
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 4. Configuración de la base de datos

Asegúrate de que tienes PostgreSQL instalado y funcionando. Crea una base de datos para la API:

```sql
CREATE DATABASE tiktok_videos;
```

En PostgreSQL, crea una tabla llamada `videos_queue`:

```sql
CREATE TABLE videos_queue (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(255) NOT NULL,
    download VARCHAR(255),
    processed BOOLEAN DEFAULT FALSE,
    source VARCHAR(255)
);
```

### 5. Variables de entorno

Crea un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:

```bash
API_TOKEN=tu_apify_token
DB_URL=postgresql://user:password@localhost:5432/tiktok_videos
```

Reemplaza `user` y `password` con las credenciales de tu base de datos PostgreSQL.

### 6. Ejecutar la API

Para ejecutar la API, utiliza Uvicorn:

```bash
uvicorn app:app --reload
```

Esto iniciará la API en `http://127.0.0.1:8000`.

### 7. Endpoints

#### `POST /download_videos/`

Este endpoint se utiliza para descargar videos de un perfil de TikTok y almacenarlos en la base de datos.

- **URL**: `http://127.0.0.1:8000/download_videos/`
- **Método**: `POST`
- **Body**: Debe enviar un JSON con los siguientes campos:

```json
{
  "profile": "nombre_del_perfil",
  "videos_count": 3,
  "videoKvStoreIdOrName": "nombre_del_key_value_store"
}
```

- **Respuesta**: Devuelve los detalles del perfil y los enlaces de los videos descargados y almacenados.

### Ejemplo de solicitud `curl`

```bash
curl -X POST "http://127.0.0.1:8000/download_videos/" \
-H "Content-Type: application/json" \
-d '{
  "profile": "nobudgetbabe",
  "videos_count": 3,
  "videoKvStoreIdOrName": "roiky-store"
}'
```

## Despliegue

### Usar con Render.com

1. **Sube tu proyecto a un repositorio de GitHub o GitLab**.
2. **Crea un nuevo Web Service en [render.com](https://render.com/)**.
3. **Conecta el repositorio**.
4. **Configura las variables de entorno**:
   - `API_TOKEN`: Tu token de Apify.
   - `DB_URL`: La URL de tu base de datos PostgreSQL.
5. **Define el comando de arranque** en la configuración de Render:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

## Contribuir

Si deseas contribuir a este proyecto, por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Crea un nuevo Pull Request.

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Puedes consultar más detalles en el archivo `LICENSE`.
