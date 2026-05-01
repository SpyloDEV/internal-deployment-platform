from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, ConflictError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.users import UserRepository
from app.services.audit_log_service import AuditLogService


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.users = UserRepository(session)
        self.audit_logs = AuditLogService(session)

    async def register(
        self,
        *,
        email: str,
        password: str,
        full_name: str | None,
    ) -> User:
        if await self.users.get_by_email(email) is not None:
            raise ConflictError("A user with this email already exists.")
        user = await self.users.create(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
        )
        await self.audit_logs.record(
            action="user_registered",
            actor_id=user.id,
            target_type="user",
            target_id=user.id,
        )
        return user

    async def authenticate(self, *, email: str, password: str) -> User:
        user = await self.users.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationError("This user account is disabled.")
        return user

    def issue_token(self, user: User) -> str:
        return create_access_token(subject=user.id)
