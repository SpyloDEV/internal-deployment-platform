from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.common import Message
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(payload: RegisterRequest, session: DbSession) -> AuthResponse:
    service = AuthService(session)
    user = await service.register(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
    await session.commit()
    await session.refresh(user)
    return AuthResponse(access_token=service.issue_token(user), user=user)


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, session: DbSession) -> AuthResponse:
    service = AuthService(session)
    user = await service.authenticate(email=payload.email, password=payload.password)
    return AuthResponse(access_token=service.issue_token(user), user=user)


@router.post("/logout", response_model=Message)
async def logout(_: CurrentUser) -> Message:
    return Message(message="Logged out. Discard the client token.")


@router.get("/me", response_model=UserRead)
async def current_user(user: CurrentUser) -> UserRead:
    return user
