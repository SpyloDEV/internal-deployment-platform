from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.common import Message
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate
from app.services.service_registry_service import ServiceRegistryService

router = APIRouter(prefix="/services", tags=["Service Registry"])


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
async def create_service(
    payload: ServiceCreate, current_user: CurrentUser, session: DbSession
) -> ServiceRead:
    service = await ServiceRegistryService(session).create(
        user_id=current_user.id, data=payload.model_dump()
    )
    await session.commit()
    await session.refresh(service)
    return service


@router.get("", response_model=list[ServiceRead])
async def list_services(
    current_user: CurrentUser,
    session: DbSession,
    organization_id: str | None = Query(default=None),
) -> list[ServiceRead]:
    return await ServiceRegistryService(session).list(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/{service_id}", response_model=ServiceRead)
async def get_service(
    service_id: str, current_user: CurrentUser, session: DbSession
) -> ServiceRead:
    return await ServiceRegistryService(session).get(
        service_id=service_id, user_id=current_user.id
    )


@router.patch("/{service_id}", response_model=ServiceRead)
async def update_service(
    service_id: str,
    payload: ServiceUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> ServiceRead:
    service = await ServiceRegistryService(session).update(
        service_id=service_id,
        user_id=current_user.id,
        data=payload.model_dump(exclude_unset=True),
    )
    await session.commit()
    await session.refresh(service)
    return service


@router.delete("/{service_id}", response_model=Message)
async def delete_service(
    service_id: str, current_user: CurrentUser, session: DbSession
) -> Message:
    service = await ServiceRegistryService(session).delete(
        service_id=service_id, user_id=current_user.id
    )
    await session.delete(service)
    await session.commit()
    return Message(message="Service removed from deployment catalog.")
