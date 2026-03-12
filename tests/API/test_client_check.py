import pytest

# ТОЛЬКО проверка работы фикстуры fixtures/api_client.py и параметров, можно заменить командами проверок каждого файла

def test_api_client_works(api_client):
    """
    Проверка, что фикстура api_client работает корректно.
    Запустите: pytest tests/api/test_client_check.py -v
    """
    assert api_client is not None
    
    assert api_client.base_url == "https://restful-booker.herokuapp.com"
    
    assert api_client.headers["Content-Type"] == "application/json"
    
    response = api_client.get("/booking")
    assert response.status_code == 200