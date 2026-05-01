from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import install_exception_handlers
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        summary="Internal deployment platform API for service delivery, release governance, rollbacks, logs, health checks, and incidents.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        openapi_tags=[
            {"name": "Authentication", "description": "JWT login and identity."},
            {"name": "Organizations", "description": "Organizations and access."},
            {"name": "Teams", "description": "Team ownership and service grouping."},
            {
                "name": "Service Registry",
                "description": "Internal catalog of deployable services.",
            },
            {
                "name": "Environments",
                "description": "Runtime environments per service.",
            },
            {
                "name": "Deployments",
                "description": "Mock release flow, rollbacks, and logs.",
            },
            {
                "name": "Environment Variables",
                "description": "Masked configuration and secret management.",
            },
            {
                "name": "Analytics",
                "description": "Deployment velocity and reliability.",
            },
            {"name": "Governance", "description": "Policy checks before deployments."},
            {"name": "Incidents", "description": "Incident lifecycle and timelines."},
            {"name": "Audit Logs", "description": "Platform activity trail."},
            {"name": "Health", "description": "Service readiness checks."},
        ],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    install_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["Health"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    return app


app = create_app()
