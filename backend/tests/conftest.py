import os
from collections.abc import AsyncGenerator, Awaitable, Callable
from typing import Any
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

os.environ.setdefault(
    "DATABASE_URL", "sqlite+aiosqlite:///./test_deployment_platform.db"
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/15")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-deployment-platform")
os.environ.setdefault("ENABLE_BACKGROUND_JOBS", "false")

import app.models  # noqa: E402, F401
from app.api import dependencies  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.main import app  # noqa: E402


def _engine_options(database_url: str) -> dict[str, Any]:
    if database_url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {"poolclass": NullPool}


test_engine = create_async_engine(
    os.environ["DATABASE_URL"],
    **_engine_options(os.environ["DATABASE_URL"]),
)
TestingSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def reset_database() -> AsyncGenerator[None, None]:
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator:
        async with TestingSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[dependencies.get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def register_user(
    client: AsyncClient,
) -> Callable[..., Awaitable[dict[str, Any]]]:
    async def _register_user(
        email: str | None = None,
        password: str = "SecurePass123!",
        full_name: str = "Platform Owner",
    ) -> dict[str, Any]:
        user_email = email or f"owner-{uuid4().hex[:8]}@example.com"
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": user_email,
                "password": password,
                "full_name": full_name,
            },
        )
        assert response.status_code == 201, response.text
        return response.json()

    return _register_user


@pytest.fixture
async def auth_headers(
    register_user: Callable[..., Awaitable[dict[str, Any]]],
) -> dict[str, str]:
    account = await register_user(email="platform@example.com")
    return {"Authorization": f"Bearer {account['access_token']}"}


async def create_organization(
    client: AsyncClient,
    headers: dict[str, str],
    *,
    name: str = "Platform Engineering",
) -> dict[str, Any]:
    response = await client.post(
        "/api/v1/organizations",
        headers=headers,
        json={"name": name},
    )
    assert response.status_code == 201, response.text
    return response.json()


async def create_team(
    client: AsyncClient,
    headers: dict[str, str],
    organization_id: str,
    *,
    name: str = "Core Platform",
) -> dict[str, Any]:
    response = await client.post(
        "/api/v1/teams",
        headers=headers,
        json={"organization_id": organization_id, "name": name},
    )
    assert response.status_code == 201, response.text
    return response.json()


async def create_service(
    client: AsyncClient,
    headers: dict[str, str],
    organization_id: str,
    *,
    team_id: str | None = None,
    name: str = "Customer API",
    owner_team: str | None = "Core Platform",
    status: str = "healthy",
) -> dict[str, Any]:
    response = await client.post(
        "/api/v1/services",
        headers=headers,
        json={
            "organization_id": organization_id,
            "team_id": team_id,
            "name": name,
            "description": "Production customer API owned by the platform team.",
            "repository_url": "https://github.com/acme/customer-api",
            "owner_team": owner_team,
            "service_type": "backend",
            "framework": "fastapi",
            "status": status,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


async def create_environment(
    client: AsyncClient,
    headers: dict[str, str],
    service_id: str,
    *,
    name: str = "staging",
    branch: str = "main",
) -> dict[str, Any]:
    response = await client.post(
        f"/api/v1/services/{service_id}/environments",
        headers=headers,
        json={
            "name": name,
            "branch": branch,
            "base_url": f"https://{name}.customer-api.internal",
            "auto_deploy_enabled": name != "production",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()
