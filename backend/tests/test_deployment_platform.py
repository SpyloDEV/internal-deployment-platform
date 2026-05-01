from httpx import AsyncClient

from tests.conftest import (
    create_environment,
    create_organization,
    create_service,
    create_team,
)


async def test_service_environment_and_health_flow(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    organization = await create_organization(client, auth_headers)
    team = await create_team(client, auth_headers, organization["id"])
    service = await create_service(
        client, auth_headers, organization["id"], team_id=team["id"]
    )
    environment = await create_environment(client, auth_headers, service["id"])

    list_response = await client.get(
        "/api/v1/services",
        headers=auth_headers,
        params={"organization_id": organization["id"]},
    )
    assert list_response.status_code == 200
    assert list_response.json()[0]["slug"] == "customer-api"

    health_response = await client.post(
        f"/api/v1/environments/{environment['id']}/health-check",
        headers=auth_headers,
        json={
            "status": "healthy",
            "latency_ms": 83,
            "message": "Synthetic check passed.",
        },
    )
    assert health_response.status_code == 200
    assert health_response.json()["latency_ms"] == 83


async def test_deployment_logs_and_rollback(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    organization = await create_organization(client, auth_headers)
    service = await create_service(client, auth_headers, organization["id"])
    staging = await create_environment(client, auth_headers, service["id"])

    deployment_response = await client.post(
        f"/api/v1/environments/{staging['id']}/deployments",
        headers=auth_headers,
        json={"version": "v1.2.0", "commit_sha": "abc123456"},
    )
    assert deployment_response.status_code == 201, deployment_response.text
    deployment = deployment_response.json()
    assert deployment["status"] == "succeeded"
    assert deployment["duration_seconds"] == 42

    logs_response = await client.get(
        f"/api/v1/deployments/{deployment['id']}/logs", headers=auth_headers
    )
    assert logs_response.status_code == 200
    assert {item["step"] for item in logs_response.json()} >= {"clone", "complete"}

    rollback_response = await client.post(
        f"/api/v1/deployments/{deployment['id']}/rollback", headers=auth_headers
    )
    assert rollback_response.status_code == 200
    assert rollback_response.json()["status"] == "rolled_back"


async def test_env_var_masking_and_audit_log(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    organization = await create_organization(client, auth_headers)
    service = await create_service(client, auth_headers, organization["id"])
    environment = await create_environment(client, auth_headers, service["id"])

    create_response = await client.post(
        f"/api/v1/environments/{environment['id']}/env-vars",
        headers=auth_headers,
        json={"key": "DATABASE_URL", "value": "postgres://secret", "is_secret": True},
    )
    assert create_response.status_code == 201
    assert create_response.json()["value_masked"] == "********"

    audit_response = await client.get(
        "/api/v1/audit-logs",
        headers=auth_headers,
        params={"organization_id": organization["id"]},
    )
    assert audit_response.status_code == 200
    assert "env_var_created" in {item["action"] for item in audit_response.json()}


async def test_policy_blocks_production_without_staging_release(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    organization = await create_organization(client, auth_headers)
    service = await create_service(client, auth_headers, organization["id"])
    production = await create_environment(
        client, auth_headers, service["id"], name="production"
    )

    evaluation = await client.post(
        "/api/v1/governance/evaluate-deployment",
        headers=auth_headers,
        json={"environment_id": production["id"]},
    )
    assert evaluation.status_code == 200
    assert evaluation.json()["status"] == "blocked"

    blocked = await client.post(
        f"/api/v1/environments/{production['id']}/deployments",
        headers=auth_headers,
        json={"commit_sha": "prod123456"},
    )
    assert blocked.status_code == 422


async def test_analytics_and_incident_crud(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    organization = await create_organization(client, auth_headers)
    service = await create_service(client, auth_headers, organization["id"])
    staging = await create_environment(client, auth_headers, service["id"])
    await client.post(
        f"/api/v1/environments/{staging['id']}/deployments",
        headers=auth_headers,
        json={"version": "v2.0.0", "commit_sha": "def123456"},
    )

    analytics = await client.get(
        "/api/v1/analytics/overview",
        headers=auth_headers,
        params={"organization_id": organization["id"]},
    )
    assert analytics.status_code == 200
    assert analytics.json()["total_deployments"] == 1
    assert analytics.json()["success_rate"] == 100.0

    incident_response = await client.post(
        "/api/v1/incidents",
        headers=auth_headers,
        json={
            "organization_id": organization["id"],
            "service_id": service["id"],
            "environment_id": staging["id"],
            "title": "Staging release latency spike",
            "severity": "medium",
        },
    )
    assert incident_response.status_code == 201
    incident = incident_response.json()

    timeline = await client.post(
        f"/api/v1/incidents/{incident['id']}/timeline",
        headers=auth_headers,
        json={"message": "Rollback not required; health check recovered."},
    )
    assert timeline.status_code == 201

    update = await client.patch(
        f"/api/v1/incidents/{incident['id']}",
        headers=auth_headers,
        json={"status": "resolved"},
    )
    assert update.status_code == 200
    assert update.json()["resolved_at"] is not None
