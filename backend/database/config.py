from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from database.models import Maintenance, Motorcycle, Owner, Admin # Importando os modelos
import os
from dotenv import load_dotenv

load_dotenv()  # Carregar variáveis do .env

MONGO_URI = os.getenv("MONGO_URI")

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["sistema_manutencao"]
    await init_beanie(database, document_models=[Admin, Owner, Motorcycle, Maintenance])
