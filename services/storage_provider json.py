from abc import ABC, abstractmethod
import json

class StorageProvider(ABC):
    @abstractmethod
    def store(self, data: dict):
        pass

# Implementación que almacena en local
class LocalStorageProvider(StorageProvider):
    def store(self, data: dict):
        with open("tiktok_profile_data.json", "w") as outfile:
            json.dump(data, outfile, indent=4)
        print("Datos guardados en tiktok_profile_data.json")

# Implementación que podría almacenar en la nube o en una base de datos
class CloudStorageProvider(StorageProvider):
    def store(self, data: dict):
        # Aquí podrías integrar con S3, GCP o cualquier servicio de almacenamiento en la nube
        print("Datos almacenados en la nube")
