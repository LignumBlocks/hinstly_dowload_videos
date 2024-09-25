from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Configurar SQLAlchemy
DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` para ver las consultas SQL generadas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir el modelo de la tabla videos_queue
class VideoQueue(Base):
    __tablename__ = "videos_queue"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(255), nullable=False)
    download = Column(String(255), nullable=True)
    processed = Column(Boolean, default=False)
    source = Column(String(255), nullable=False)

# Definir la interfaz abstracta para los proveedores de almacenamiento
class StorageProvider(ABC):
    @abstractmethod
    def store(self, data: dict):
        pass

# Implementación que almacena los datos en PostgreSQL
class PostgresStorageProvider(StorageProvider):
    def __init__(self):
        self.db = SessionLocal()

    def store(self, data: dict):
        try:
            for video in data["videos"]:
                video_entry = VideoQueue(
                    origin=video["video_url"],
                    download=video["download_link"],
                    source="Tiktok"  # Siempre será "Tiktok" según lo especificado
                )
                self.db.add(video_entry)

            self.db.commit()  # Confirmamos los cambios en la base de datos
            print("Datos almacenados en la base de datos.")
        except Exception as e:
            self.db.rollback()  # En caso de error, deshacemos los cambios
            print(f"Error al almacenar los datos: {str(e)}")
        finally:
            self.db.close()  # Cerramos la sesión
