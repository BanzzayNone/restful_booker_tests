import pytest
from config.settings import settings


# Базовая проверка фикстуры api_client и её конфигурации

@pytest.mark.smoke
def test_api_client_works(api_client):
    """Проверка корректной конфигурации фикстуры api_client."""
    assert api_client is not None

    assert api_client.base_url == settings.BASE_URL

    assert api_client.headers["Content-Type"] == "application/json"

    response = api_client.get("/booking")
    assert response.status_code == 200
