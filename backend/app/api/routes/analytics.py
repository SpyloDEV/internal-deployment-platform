from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.analytics import (
    AnalyticsOverview,
    DeploymentAnalytics,
    ReliabilityAnalytics,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
async def analytics_overview(
    current_user: CurrentUser,
    session: DbSession,
    organization_id: str = Query(...),
) -> AnalyticsOverview:
    return await AnalyticsService(session).overview(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/deployments", response_model=DeploymentAnalytics)
async def deployment_analytics(
    current_user: CurrentUser,
    session: DbSession,
    organization_id: str = Query(...),
) -> DeploymentAnalytics:
    return await AnalyticsService(session).deployments(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/reliability", response_model=ReliabilityAnalytics)
async def reliability_analytics(
    current_user: CurrentUser,
    session: DbSession,
    organization_id: str = Query(...),
) -> ReliabilityAnalytics:
    return await AnalyticsService(session).reliability(
        user_id=current_user.id, organization_id=organization_id
    )
