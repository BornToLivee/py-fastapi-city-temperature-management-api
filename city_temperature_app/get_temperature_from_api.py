import os
from datetime import datetime
from typing import Callable

import httpx
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from city_temperature_app import (
    crud,
    models,
    schemas,
)

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")

if WEATHER_API_KEY is None:
    raise ValueError("WEATHER_API_KEY not found(check your .env file)")
if WEATHER_API_URL is None:
    raise ValueError("WEATHER_API_URL not found(check your .env file)")


async def fetch_temperatures_from_api(
        client: httpx.AsyncClient,
        city: models.DBCity,
        db_session_factory: Callable[[], AsyncSession],
) -> None:
    try:
        response = await client.get(
            WEATHER_API_URL, params={"key": WEATHER_API_KEY, "q": city.name}
        )
        data = response.json()
        temperature = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            temperature=data["current"]["temp_c"],
        )
        async with db_session_factory() as new_db_session:
            await crud.create_temperature(new_db_session, temperature)

    except Exception as e:
        print(f"Error: {str(e)}")
