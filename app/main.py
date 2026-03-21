from app.core.logger import logger
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.config import settings

from app.api.v1.users import router as user_router
from app.api.v1.airlines import router as airline_router
from app.api.v1.airports import router as airport_router
from app.api.v1.flights import router as flight_router
from app.api.v1.aircrafts import router as aircraft_router
from app.helpers.exception_handler import add_exception_handler
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)
add_exception_handler(app=app)

app.include_router(user_router)
app.include_router(airline_router)
app.include_router(airport_router)
app.include_router(flight_router)
app.include_router(aircraft_router)
@app.get('/', include_in_schema=False)
async def root():
    """
    Автоматическое перенаправление на страницу документации Swagger.
    """
    return RedirectResponse(url='/docs')