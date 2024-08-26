import asyncio
from typing import Sequence

import httpx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from city_temperature_app import (
    crud,
    models,
    schemas,
)
from city_temperature_app.get_temperature_from_api import (
    fetch_temperatures_from_api
)
from database import SessionLocal, get_db

router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: AsyncSession = Depends(get_db),
) -> Sequence[models.DBTemperature]:
    temperatures = await crud.get_temperatures(db)
    if not temperatures:
        raise HTTPException(
            status_code=404, detail="There are no temperatures yet"
        )
    return temperatures


@router.get(
    "/temperatures/{city_id}", response_model=list[schemas.Temperature]
)
async def read_temperature_by_city_id(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> Sequence[models.DBTemperature]:
    temperatures = await crud.get_temperatures(db, city_id)
    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail=f"There are no temperatures yet for city with id {city_id}",
        )
    return temperatures


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)) -> dict:
    cities = await crud.get_cities(db)

    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_temperatures_from_api(client, city, SessionLocal)
            for city in cities
        ]
        await asyncio.gather(*tasks)

    return {"status": "Temperatures updated"}
