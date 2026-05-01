from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "internal_deployment_platform",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
celery_app.conf.task_routes = {"app.workers.tasks.*": {"queue": "deployments"}}
