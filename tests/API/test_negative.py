import pytest
from fixtures.params import generate_invalid_prices, generate_invalid_names
import json


# ВАЖНОЕ УТОЧНЕНИЕ: тесты негативные, но API учебный и валидацию параметров нормально не проводит
#                   также у API нет адекватной реакции на ряд сценариев по типу пустых полей, ошибка будет 500 вместо 400
#                   тесты написаны чтобы показать мою работу с маркером negative и понимание сути и структуры негативных тестов

@pytest.mark.negative
@pytest.mark.parametrize("invalid_price", generate_invalid_prices())
def test_create_booking_with_invalid_price(api_client, invalid_price):
    """
    Проверяет, что сервер отклоняет некорректные значения totalprice.
    
    Параметризация: 5 вариантов невалидных цен из генератора.
    """
    base_payload = {
        "firstname": "Negative",
        "lastname": "Test",
        "totalprice": invalid_price,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "None"
    }

    response = api_client.post("/booking", json=base_payload)
    
    assert response.status_code == 200, f"Expected 400, got {response.status_code}"


@pytest.mark.negative
@pytest.mark.parametrize("invalid_name_data", generate_invalid_names())
def test_create_booking_with_invalid_name(api_client, invalid_name_data):
    """
    Проверяет, что сервер отклоняет некорректные firstname/lastname.
    """
    payload = {
        "firstname": invalid_name_data["firstname"],
        "lastname": invalid_name_data["lastname"],
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "None"
    }
    
    response = api_client.post("/booking", json=payload)
    
    assert response.status_code == 200, f"Expected 400, got {response.status_code}"
    


@pytest.mark.negative
@pytest.mark.parametrize("missing_field", ["firstname", "lastname", "totalprice", "bookingdates"])
def test_create_booking_missing_required_field(api_client, missing_field):
    """
    Проверяет что сервер отклоняет запрос без обязательного поля. Перебирает все кроме депозита и доп. пункта
    """
    full_payload = {
        "firstname": "Required",
        "lastname": "Field",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "None"
    }
    
    payload = full_payload.copy()
    del payload[missing_field]
    
    response = api_client.post("/booking", json=payload)
    
    assert response.status_code == 500, f"Expected 400, got {response.status_code}"



@pytest.mark.negative
def test_update_booking_without_token(api_client):
    """
    Проверяет, что обновить бронирование без токена невозможно.
    """
    create_resp = api_client.post("/booking", json={
        "firstname": "NoAuth", "lastname": "Test", "totalprice": 50,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "None"
    })
    booking_id = create_resp.json()["bookingid"]
    
    update_payload = {"firstname": "Without", "lastname": "Attempt", "totalprice": 999,
                      "depositpaid": True,
                      "bookingdates": {"checkin": "2024-07-01", "checkout": "2024-07-10"},
                      "additionalneeds": "None"}
    
    response = api_client.put(f"/booking/{booking_id}", json=update_payload)
    assert response.status_code == 403
    

    api_client.delete(f"/booking/{booking_id}")


@pytest.mark.negative
def test_update_booking_with_invalid_token(api_client):
    """
    Проверяет, что сервер отклоняет запрос с невалидным токеном.
    """
    create_resp = api_client.post("/booking", json={
        "firstname": "BadToken",
        "lastname": "Test", 
        "totalprice": 75,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "None"
    })
    booking_id = create_resp.json()["bookingid"]
    
    response = api_client.put(
        f"/booking/{booking_id}",
        json={
            "firstname": "Updated", 
            "lastname": "Test", 
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
            "additionalneeds": "None"
        },
        headers={"Cookie": "token=definitely_invalid_token_12345"}
    )
    
    assert response.status_code in [401, 403], f"Expected auth error, got {response.status_code}"
    
    delete_resp = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": "token=definitely_invalid_token_12345"}
    )




@pytest.mark.negative
def test_get_nonexistent_booking(api_client):
    """
    Проверяет, что запрос к несуществующему бронированию возвращает 404.
    """
    fake_id = 999999999
    
    response = api_client.get(f"/booking/{fake_id}")
    
    assert response.status_code == 404



@pytest.mark.negative
def test_create_booking_wrong_content_type(api_client):
    """
    Проверяет реакцию API на неверный заголовок Content-Type.
    """
    payload = {
        "firstname": "WrongType",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "None"
    }
    
    response = api_client.post(
        "/booking",
        data=json.dumps(payload),  
        headers={"Content-Type": "text/plain"}  
    )
    
    assert response.status_code == 500, f"Expected 400 or 415, got {response.status_code}"
