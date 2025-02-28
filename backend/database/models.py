from beanie import Document
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from passlib.context import CryptContext
import pytz

brazil_tz = pytz.timezone("America/Sao_Paulo")

class Owner(Document):
    name_owner : str
    phone: str
    email: str
    birth_date: date
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    status: str = "Ativo"
    created_at: datetime = datetime.now(brazil_tz)

    class Settings:
        collection = "owners"

class Motorcycle(Document):
    brand: str  
    model: str  
    odometer_km: int  
    registration_year: int
    plate: str  
    chassis: str  
    owner_name: Optional[str] = None  # Nome do proprietário (pode ser nulo)
    owner_phone: Optional[str] = None  # Telefone do proprietário (pode ser nulo)
    last_maintenance: Optional[datetime] = None  # Última manutenção (pode ser nulo)
    maintenance_history: List[dict] = []  
    upcoming_maintenance: List[dict] = []
    status: str  # Status: "Active", "Inactive", "Under Maintenance"

    class Settings:
        collection = "motorcycles"

class Maintenance(Document):
    motorcycle_id: str  # Referência ao veículo (Motorcycle)
    owner_id: Optional[str]  # Referência ao proprietário (Owner)
    maintenance_date: datetime = datetime.now(brazil_tz).isoformat()
    odometer_km: int 
    description: str
    maintenance_photos: List[str] = []  # URLs das fotos da manutenção (array)

    class Settings:
        collection = "maintenance"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Admin(Document):
    username: str
    email: EmailStr  # Validação automática de e-mail
    password_hash: str  # Senha será armazenada como hash
    created_at: datetime = datetime.now(brazil_tz)
    last_login: datetime = None  # Pode começar como None

    class Settings:
        collection = "admins"

    # Método para criar hash da senha
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    # Método para verificar senha
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)