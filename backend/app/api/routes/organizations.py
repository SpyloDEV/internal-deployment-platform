from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
)
from app.services.organization_service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate, current_user: CurrentUser, session: DbSession
) -> OrganizationRead:
    organization = await OrganizationService(session).create(
        user_id=current_user.id, name=payload.name, slug=payload.slug
    )
    await session.commit()
    await session.refresh(organization)
    return organization


@router.get("", response_model=list[OrganizationRead])
async def list_organizations(
    current_user: CurrentUser, session: DbSession
) -> list[OrganizationRead]:
    return await OrganizationService(session).list(user_id=current_user.id)


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    organization_id: str, current_user: CurrentUser, session: DbSession
) -> OrganizationRead:
    return await OrganizationService(session).get(
        organization_id=organization_id, user_id=current_user.id
    )


@router.patch("/{organization_id}", response_model=OrganizationRead)
async def update_organization(
    organization_id: str,
    payload: OrganizationUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> OrganizationRead:
    organization = await OrganizationService(session).update(
        organization_id=organization_id,
        user_id=current_user.id,
        data=payload.model_dump(exclude_unset=True),
    )
    await session.commit()
    await session.refresh(organization)
    return organization
