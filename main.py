import os
import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from apify_client import ApifyClient
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener el API_TOKEN desde las variables de entorno
API_TOKEN = os.getenv("API_TOKEN")

# Inicializar ApifyClient con el token
client = ApifyClient(API_TOKEN)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Definir el modelo para la solicitud de API
class TikTokRequest(BaseModel):
    profile: str
    videos_count: int

# Ruta raíz para verificar que el API esté corriendo
@app.get("/")
def read_root():
    return {"message": "TikTok Scraper API is running"}

# Ruta para buscar videos de un perfil de TikTok
@app.post("/download_videos/")
def download_videos(request: TikTokRequest):
    # Configurar los parámetros de entrada para el actor de Apify
    run_input = {
        "profiles": [request.profile],
        "resultsPerPage": request.videos_count,
        "excludePinnedPosts": True,
        "shouldDownloadVideos": True,
        "shouldDownloadCovers": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadSlideshowImages": False,
        "videoKvStoreIdOrName": request.videoKvStoreIdOrName
    }

    try:
        # Ejecutar el actor de Apify para obtener datos de TikTok
        run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

        # Obtenemos el nombre del Key Value Store del input del Actor
        kv_store_name = run_input["videoKvStoreIdOrName"]

        # Obtenemos la lista de Key Value Stores
        kv_store_list_url = f"https://api.apify.com/v2/key-value-stores?token={API_TOKEN}"
        kv_store_list_response = requests.get(kv_store_list_url)

        if kv_store_list_response.status_code == 200:
            response_json = kv_store_list_response.json()

            # Buscar el Key Value Store por nombre
            kv_store_id = None
            for store in response_json.get("data", {}).get("items", []):
                if store["name"] == kv_store_name:
                    kv_store_id = store["id"]
                    break

            if kv_store_id:
                # Obtener las claves de los videos almacenados
                kv_store_keys_url = f"https://api.apify.com/v2/key-value-stores/{kv_store_id}/keys?token={API_TOKEN}"
                kv_store_keys_response = requests.get(kv_store_keys_url)

                if kv_store_keys_response.status_code == 200:
                    keys_data = kv_store_keys_response.json()
                    videos = keys_data.get("data", {}).get("items", [])

                    # Variable para almacenar los resultados
                    profile_data = {
                        "profile_id": None,
                        "profile_name": None,
                        "videos": []
                    }

                    # Iterar sobre los elementos del dataset
                    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                        # Extraer detalles del perfil una sola vez
                        if not profile_data["profile_id"] and not profile_data["profile_name"]:
                            profile_data["profile_id"] = item.get("authorMeta", {}).get("id")
                            profile_data["profile_name"] = item.get("authorMeta", {}).get("name")

                        # Agregar las URLs de los videos y los enlaces de almacenamiento
                        for video in videos:
                            profile_data["videos"].append({
                                "video_url": item.get("webVideoUrl"),
                                "storage_link": f"https://api.apify.com/v2/key-value-stores/{kv_store_id}/records/{video['key']}"
                            })

                    return profile_data
                else:
                    raise HTTPException(status_code=500, detail="Error al obtener las claves de los videos.")
            else:
                raise HTTPException(status_code=404, detail="Key Value Store no encontrado.")
        else:
            raise HTTPException(status_code=500, detail="Error al obtener la lista de Key Value Stores.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
