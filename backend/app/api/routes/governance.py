from fastapi import APIRouter

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.policy import DeploymentPolicyRequest, PolicyEvaluationRead
from app.services.environment_service import EnvironmentService
from app.services.policy_service import PolicyService
from app.services.service_registry_service import ServiceRegistryService

router = APIRouter(prefix="/governance", tags=["Governance"])


@router.get("/policies")
async def list_policies(session: DbSession) -> list[dict[str, str]]:
    return PolicyService(session).policy_catalog()


@router.post("/evaluate-deployment", response_model=PolicyEvaluationRead)
async def evaluate_deployment(
    payload: DeploymentPolicyRequest,
    current_user: CurrentUser,
    session: DbSession,
) -> PolicyEvaluationRead:
    environment = await EnvironmentService(session).get(
        environment_id=payload.environment_id, user_id=current_user.id
    )
    service = await ServiceRegistryService(session).get(
        service_id=environment.service_id, user_id=current_user.id
    )
    return await PolicyService(session).evaluate_deployment(
        service=service, environment=environment, user_id=current_user.id
    )
