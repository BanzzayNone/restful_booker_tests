import pytest
from config.settings import settings


@pytest.fixture(scope="function")
def auth_token(api_client) -> str:
    """
    Получает токен авторизации через эндпоинт /auth.
    
    :param api_client: Фикстура умного HTTP-клиента
    :return: Строка с токеном для подстановки в заголовки
    """
    
    payload = {
        "username": settings.AUTH_USERNAME,
        "password": settings.AUTH_PASSWORD
    }
    
    response = api_client.post("/auth", json=payload)
    
    assert response.status_code == 200, f"Auth failed: {response.text}"
    
    token = response.json()["token"]
    return token