from httpx import AsyncClient


async def test_register_login_and_current_user(client: AsyncClient) -> None:
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "founder@example.com",
            "password": "SecurePass123!",
            "full_name": "Control Center Founder",
        },
    )
    assert register_response.status_code == 201
    token = register_response.json()["access_token"]

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "founder@example.com", "password": "SecurePass123!"},
    )
    assert login_response.status_code == 200

    me_response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "founder@example.com"


async def test_duplicate_registration_is_rejected(client: AsyncClient) -> None:
    payload = {
        "email": "founder@example.com",
        "password": "SecurePass123!",
        "full_name": "Founder",
    }
    assert (await client.post("/api/v1/auth/register", json=payload)).status_code == 201
    assert (await client.post("/api/v1/auth/register", json=payload)).status_code == 409
