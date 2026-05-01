from enum import StrEnum


def enum_values(enum_cls):
    return [item.value for item in enum_cls]


class WorkspaceRole(StrEnum):
    PLATFORM_OWNER = "platform_owner"
    ADMIN = "admin"
    DEVELOPER = "developer"
    VIEWER = "viewer"
    OWNER = "owner"
    MEMBER = "member"


class UserRole(StrEnum):
    PLATFORM_OWNER = "platform_owner"
    ADMIN = "admin"
    DEVELOPER = "developer"
    VIEWER = "viewer"


class ApiKeyStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"


class LogLevel(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ServiceType(StrEnum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    WORKER = "worker"
    API = "api"


class ServiceFramework(StrEnum):
    NEXTJS = "nextjs"
    FASTAPI = "fastapi"
    NODE = "node"
    PYTHON = "python"
    OTHER = "other"


class EnvironmentName(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    PREVIEW = "preview"


class ServiceEnvironment(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    PREVIEW = "preview"


class ServiceStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class DeploymentStatus(StrEnum):
    QUEUED = "queued"
    BUILDING = "building"
    DEPLOYING = "deploying"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"


class PolicySeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    BLOCKER = "blocker"


class PolicyStatus(StrEnum):
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"


class IncidentSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
