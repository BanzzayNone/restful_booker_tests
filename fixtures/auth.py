import pytest
from config.settings import settings


@pytest.fixture(scope="session")
def auth_token(api_client) -> str:
    """
    Получение токена авторизации через эндпоинт /auth.

    :param api_client: HTTP-клиент с областью видимости session
    :return: Строка токена для использования в заголовках авторизации
    """
    response = api_client.post(
        settings.ENDPOINT_AUTH,
        json={
            "username": settings.AUTH_USERNAME,
            "password": settings.AUTH_PASSWORD,
        },
    )

    assert response.status_code == 200, f"Auth failed: {response.text}"

    token = response.json()["token"]
    return token


@pytest.fixture(scope="session")
def auth_headers(auth_token) -> dict:
    """Возвращает словарь заголовков с cookie токена авторизации."""
    return {"Cookie": f"token={auth_token}"}
