import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from services.data_provider import ApifyDataProvider
from services.storage_provider import PostgresStorageProvider
from apify_client import ApifyClient
from models.tiktok_request import TikTokRequest

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener el API_TOKEN desde las variables de entorno
API_TOKEN = os.getenv("API_TOKEN")

# Inicializar ApifyClient con el token
client = ApifyClient(API_TOKEN)

# Inicializar proveedores
data_provider = ApifyDataProvider(client, API_TOKEN)  # Pasamos también el API_TOKEN para usarlo en la clase
storage_provider = PostgresStorageProvider()  # Cambia el proveedor si quieres cambiar el método de almacenamiento

# Inicializar la aplicación FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "TikTok Scraper API is running"}

@app.post("/download_videos/")
def download_videos(request: TikTokRequest):
    try:
        # Obtener datos desde el proveedor
        profile_data = data_provider.fetch_data(request.profile, request.videos_count, request.videoKvStoreIdOrName)
        
        # Almacenar los datos usando el proveedor de almacenamiento
        storage_provider.store(profile_data)

        return profile_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
