from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_services: int
    total_environments: int
    total_deployments: int
    successful_deployments: int
    failed_deployments: int
    success_rate: float
    average_duration_seconds: float | None
    rollback_count: int


class DeploymentAnalytics(BaseModel):
    deployments_per_day: list[dict[str, int | str]]
    most_deployed_service: str | None


class ReliabilityAnalytics(BaseModel):
    failure_rate_by_service: list[dict[str, float | int | str]]
