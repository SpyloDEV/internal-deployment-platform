import asyncio

from app.db.session import AsyncSessionLocal
from app.services.deployment_service import DeploymentService
from app.workers.celery_app import celery_app


async def _run_mock_deployment(
    environment_id: str, user_id: str, commit_sha: str
) -> None:
    async with AsyncSessionLocal() as session:
        await DeploymentService(session).trigger(
            environment_id=environment_id,
            user_id=user_id,
            data={"commit_sha": commit_sha, "force_failure": False},
        )
        await session.commit()


@celery_app.task(name="app.workers.tasks.run_deployment")
def run_deployment(environment_id: str, user_id: str, commit_sha: str) -> None:
    asyncio.run(_run_mock_deployment(environment_id, user_id, commit_sha))
