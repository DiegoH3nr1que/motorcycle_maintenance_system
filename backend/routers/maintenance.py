from fastapi import APIRouter, HTTPException
from database.models import Maintenance, Motorcycle
from database.schemas import MaintenanceSchema
from typing import List
from datetime import datetime
from bson import ObjectId
import pytz

router = APIRouter(prefix="/maintenances", tags=["Maintenances"] )

@router.post("/maintenance/create", response_model=MaintenanceSchema)
async def create_maintenance(maintenance: MaintenanceSchema):
    brazil_tz = pytz.timezone("America/Sao_Paulo")
    new_maintenance = Maintenance(**maintenance.model_dump())
    
    # Buscar a moto associada
    motorcycle = await Motorcycle.get(maintenance.motorcycle_id)
    if not motorcycle:
        raise HTTPException(status_code=404, detail="Moto não encontrada")
    
    await new_maintenance.insert()
    # Criar um registro de manutenção para o histórico
    maintenance_record = {
        "date": new_maintenance.maintenance_date,
        "description": new_maintenance.description
    }

    # Adicionar a nova manutenção ao histórico da moto
    motorcycle.maintenance_history.append(maintenance_record)

    # 📌 Converter last_maintenance para offset-aware antes da comparação
    if motorcycle.last_maintenance:
        motorcycle.last_maintenance = motorcycle.last_maintenance.replace(tzinfo=brazil_tz)

    # 📌 Atualizar `last_maintenance` apenas se for mais recente
    if not motorcycle.last_maintenance or new_maintenance.maintenance_date > motorcycle.last_maintenance:
        motorcycle.last_maintenance = new_maintenance.maintenance_date

    # Salvar alterações na moto
    await motorcycle.save()

    return new_maintenance

@router.get("/maintenance/list", response_model=List[MaintenanceSchema])
async def list_maintenance():
    return await Maintenance.find_all().to_list()

@router.get("/maintenance/{id}", response_model=MaintenanceSchema)
async def get_maintenance(id: str):
    maintenance = await Maintenance.get(id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="manutenção não encontrada")
    return maintenance

@router.delete("/maintenance/{id}")
async def delete_maintenance(id: str):
    maintenance = await Maintenance.get(id)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    
    await remove_maintenance_from_motorcycle(maintenance)
    await maintenance.delete()
    return {"message": "Manutenção removida com sucesso"}

async def remove_maintenance_from_motorcycle(maintenance):
    motorcycle = await Motorcycle.get(maintenance.motorcycle_id)
    if motorcycle:
        # Convertendo a data da manutenção para ISO 8601 para garantir a comparação correta
        maintenance_date_iso = maintenance.maintenance_date
        print(maintenance_date_iso)

        # Filtra a lista removendo a manutenção com a data correspondente
        motorcycle.maintenance_history = [
            item for item in motorcycle.maintenance_history if item["date"] != maintenance.maintenance_date
        ]

        await motorcycle.save()

            
