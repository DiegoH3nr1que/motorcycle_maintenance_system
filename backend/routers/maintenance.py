from fastapi import APIRouter, HTTPException
from database.models import Maintenance
from database.schemas import MaintenanceSchema
from typing import List

router = APIRouter(prefix="/maintenances", tags=["Maintenances"] )

@router.post("/maintenance/create", response_model=MaintenanceSchema)
async def create_maintenance(maintenance: MaintenanceSchema):
    new_maintenance = Maintenance(**maintenance.model_dump())
    await new_maintenance.insert()
    return new_maintenance

@router.get("/maintenance/list", response_model=List[MaintenanceSchema])
async def list_maintenance():
    return await Maintenance.find_all().to_list()

@router.get("/maintenance/{id}", response_model=MaintenanceSchema)
async def get_motorcycle(id: str):
    maintenance = await Maintenance.get(id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="manutenção não encontrada")
    return maintenance
