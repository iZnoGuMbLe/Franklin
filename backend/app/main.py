from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core import settings, NotFoundException
from app.api.v1.routers import categories, transactions
from app.database import Base, async_engine
import app.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(categories.router,prefix=settings.api_v1_prefix)
app.include_router(transactions.router, prefix=settings.api_v1_prefix)

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exception: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exception)})



