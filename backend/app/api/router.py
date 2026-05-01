from fastapi import APIRouter

from app.api.routes import (
    analytics,
    audit_logs,
    auth,
    deployments,
    env_vars,
    environments,
    governance,
    health,
    incidents,
    organizations,
    services,
    teams,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(teams.router)
api_router.include_router(services.router)
api_router.include_router(environments.router)
api_router.include_router(deployments.router)
api_router.include_router(env_vars.router)
api_router.include_router(health.router)
api_router.include_router(analytics.router)
api_router.include_router(governance.router)
api_router.include_router(audit_logs.router)
api_router.include_router(incidents.router)
