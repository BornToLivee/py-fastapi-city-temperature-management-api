from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from city_temperature_app import crud, schemas
from database import get_db

router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return db_city


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.update_city(db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return db_city


@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return db_city
