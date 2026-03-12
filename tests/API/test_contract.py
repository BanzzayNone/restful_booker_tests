import pytest
from schemas.validators import validate_booking_response, validate_booking_update


@pytest.mark.contract 
def test_create_booking_contract(api_client):
    """
    Contract-тест: проверяем структуру ответа при создании бронирования.
    """
    payload = {
        "firstname": "Contract",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "Wi-Fi"
    }
    
    response = api_client.post("/booking", json=payload)
    assert response.status_code == 200
    
    validated_data = validate_booking_response(response.json())
    
    assert validated_data.booking.firstname == "Contract"
    assert validated_data.booking.totalprice == 100
    assert validated_data.bookingid > 0


@pytest.mark.contract
def test_update_booking_contract(api_client, auth_token):
    """
    Contract-тест: проверяем структуру ответа при обновлении бронирования.
    """
    create = api_client.post("/booking", json={
        "firstname": "Old", "lastname": "Name", "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-15"},
        "additionalneeds": "None"
    })
    booking_id = create.json()["bookingid"]
    
    update_payload = {
        "firstname": "New", "lastname": "Name", "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {"checkin": "2024-02-01", "checkout": "2024-02-15"},
        "additionalneeds": "Breakfast"
    }
    response = api_client.put(
        f"/booking/{booking_id}",
        json=update_payload,
        headers={"Cookie": f"token={auth_token}"}
    )
    assert response.status_code == 200
    
    validated_data = validate_booking_update(response.json())
    assert validated_data.firstname == "New"
    assert validated_data.totalprice == 200
    
    api_client.delete(f"/booking/{booking_id}", headers={"Cookie": f"token={auth_token}"})