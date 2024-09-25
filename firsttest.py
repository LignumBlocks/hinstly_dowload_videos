from apify_client import ApifyClient
import requests
import json

# Tu token de Apify
API_TOKEN = "apify_api_V0XudUMeuHkEpXn7e4KWP6MCjVoeOC0oXMBf"

# Inicializa el cliente de Apify con tu token
client = ApifyClient(API_TOKEN)

# Prepara el input del Actor para buscar por perfil y almacenar en un Key Value Store específico
run_input = {
    "profiles": ["nobudgetbabe"],  # Cambia "nombre_del_perfil" por el nombre del perfil de TikTok que quieres buscar
    "resultsPerPage": 2,                # Número de resultados por perfil
    "excludePinnedPosts": True,         # Excluye los posts fijados si es necesario
    "shouldDownloadVideos": True,       # Configura si deseas descargar los videos
    "shouldDownloadCovers": False,      # Configura si deseas descargar las imágenes de portada
    "shouldDownloadSubtitles": False,   # Configura si deseas descargar los subtítulos
    "shouldDownloadSlideshowImages": False,  # Configura si deseas descargar imágenes de presentaciones
    "videoKvStoreIdOrName": "roiky-store"  # Nombre o ID del Key Value Store
}

# Ejecuta el Actor y espera a que termine
run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

# Obtenemos el nombre del Key Value Store del input del Actor
kv_store_name = run_input["videoKvStoreIdOrName"]

# Obtenemos la lista de Key Value Stores
kv_store_list_url = f"https://api.apify.com/v2/key-value-stores?token={API_TOKEN}"
kv_store_list_response = requests.get(kv_store_list_url)

# Verifica si la respuesta es correcta y accede a 'data' y luego a 'items'
if kv_store_list_response.status_code == 200:
    response_json = kv_store_list_response.json()
    
    if "data" in response_json and "items" in response_json["data"]:
        kv_stores = response_json["data"]["items"]
        
        # Filtramos el Key Value Store por nombre (usamos el valor de run_input["videoKvStoreIdOrName"])
        kv_store_id = None
        
        for store in kv_stores:
            if store["name"] == kv_store_name:
                kv_store_id = store["id"]
                break

        if kv_store_id:
            # Si encontramos el Key Value Store, obtenemos las claves de los videos almacenados
            kv_store_keys_url = f"https://api.apify.com/v2/key-value-stores/{kv_store_id}/keys?token={API_TOKEN}"
            kv_store_keys_response = requests.get(kv_store_keys_url)
            
            if kv_store_keys_response.status_code == 200:
                keys_data = kv_store_keys_response.json()
                videos = keys_data["data"]["items"]
                
                # Variable para almacenar los resultados
                profile_data = {
                    "profile_id": None,
                    "profile_name": None,
                    "videos": []
                }

                # Itera sobre los resultados del dataset y construye el JSON
                for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                    # Extrae los detalles del perfil una sola vez
                    if not profile_data["profile_id"] and not profile_data["profile_name"]:
                        profile_data["profile_id"] = item.get("authorMeta", {}).get("id")
                        profile_data["profile_name"] = item.get("authorMeta", {}).get("name")

                    # Agrega las URLs de los videos y los links donde se almacenaron
                    for video in videos:
                        profile_data["videos"].append({
                            "video_url": item.get("webVideoUrl"),
                            "storage_link": f"https://api.apify.com/v2/key-value-stores/{kv_store_id}/records/{video['key']}"
                        })

                # Guarda el resultado en un archivo JSON
                with open("tiktok_profile_data.json", "w") as outfile:
                    json.dump(profile_data, outfile, indent=4)

                print("Datos guardados en tiktok_profile_data.json")
            else:
                print(f"Error al obtener las claves de los videos del Key Value Store: {kv_store_keys_response.status_code}")
        else:
            print(f"Error: No se encontró el Key Value Store con el nombre {kv_store_name}")
    else:
        print(f"La respuesta no contiene 'data' o 'items'. Respuesta: {response_json}")
else:
    print(f"Error al obtener la lista de Key Value Stores: {kv_store_list_response.status_code}")
