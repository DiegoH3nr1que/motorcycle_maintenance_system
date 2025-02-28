from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import pytz

brazil_tz = pytz.timezone("America/Sao_Paulo")
# 📌 Schema para Motorcycle (Moto)
class MotorcycleSchema(BaseModel):
    brand: str
    model: str
    odometer_km: int
    registration_year: int
    plate: str
    chassis: str
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    last_maintenance: Optional[datetime] = None
    maintenance_history: List[dict] = []
    upcoming_maintenance: List[dict] = []
    status: str

# 📌 Schema para Maintenance (Manutenção)
class MaintenanceSchema(BaseModel):
    motorcycle_id: str
    owner_id: Optional[str] = None
    maintenance_date: datetime = datetime.now(brazil_tz).isoformat()
    odometer_km: int
    description: str
    maintenance_photos: List[str] = []

# 📌 Schema para Admin
class AdminSchema(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime = datetime.now(brazil_tz)
    last_login: Optional[datetime] = None
