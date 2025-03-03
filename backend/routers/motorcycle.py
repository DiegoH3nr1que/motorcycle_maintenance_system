from fastapi import APIRouter, HTTPException
from database.models import Motorcycle
from database.schemas import MotorcycleSchema
from typing import List

router = APIRouter(prefix="/motorcycles", tags=["Motorcycles"])

@router.post("/motorcycles/create", response_model=MotorcycleSchema)
async def create_motorcycle(moto: MotorcycleSchema):
    new_moto = Motorcycle(**moto.model_dump())
    await new_moto.insert()
    return new_moto

@router.get("/motorcycles/list", response_model=List[MotorcycleSchema])
async def list_motorcycle():
    return await Motorcycle.find_all().to_list()

@router.get("/motorcycles/{id}", response_model=MotorcycleSchema)
async def get_motorcycle(id: str):
    moto = await Motorcycle.get(id)
    if not moto:
        raise HTTPException(status_code=404, detail="Moto não encontrada")
    return moto

@router.patch("/motorcycles/{id}/reserve", response_model=MotorcycleSchema)
async def reserve_motorcycle(id:str, renter_data: dict):
    moto = await Motorcycle.get(id)
    if not moto:
        raise HTTPException(status_code=404, detail="Moto não encontrada")
    
    print(renter_data)

    moto.owner_name = renter_data.get("owner_name")
    moto.owner_cpf = renter_data.get("owner_cpf")
    moto.owner_phone = renter_data.get("owner_phone")

    await moto.save()
    return moto
