"""
Общие фикстуры для тестов (pytest подхватывает conftest.py автоматически).

Идея: гоняем API на тестовой БД SQLite in-memory, чтобы:
  - не трогать реальную dev-базу (Postgres),
  - каждый тест стартовал на чистых таблицах,
  - было быстро (память, без диска и docker).
"""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401 — импорт регистрирует ВСЕ модели в Base.metadata
from app.database import Base, get_session
from app.main import app

# --- тестовый engine: SQLite в памяти ---
# StaticPool + одно соединение: in-memory БД живёт, пока держим это соединение.
# Без StaticPool каждый коннект получал бы свою пустую БД.
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


# SQLite по умолчанию НЕ проверяет внешние ключи — включаем, чтобы FK работали как в проде
@event.listens_for(test_engine.sync_engine, "connect")
def _enable_fk(dbapi_conn, _):
    dbapi_conn.execute("PRAGMA foreign_keys=ON")


@pytest_asyncio.fixture
async def db_setup():
    """Перед тестом создаёт все таблицы, после — удаляет. Полная изоляция."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_setup):
    """
    HTTP-клиент, бьющий по твоему приложению БЕЗ реального сервера (ASGITransport).
    Подменяет get_session на тестовую сессию через dependency_overrides —
    это тот самый механизм подмены зависимостей (DI) для тестов.
    """

    async def override_get_session():
        async with TestSessionLocal() as session:
            async with session.begin():
                yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()  # убираем подмену после теста
