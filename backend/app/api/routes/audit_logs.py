from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.audit_log import AuditLogRead
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("", response_model=list[AuditLogRead])
async def list_audit_logs(
    current_user: CurrentUser,
    session: DbSession,
    organization_id: str | None = Query(default=None),
) -> list[AuditLogRead]:
    return await AuditLogService(session).list_logs(
        user_id=current_user.id, organization_id=organization_id
    )
