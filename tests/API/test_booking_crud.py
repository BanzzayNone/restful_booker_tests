import pytest


def test_create_and_delete_booking(api_client, auth_token):

    payload = {
        "firstname": "Portfolio",
        "lastname": "Test",
        "totalprice": 500,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "Wi-Fi"
    }
    
    create_resp = api_client.post("/booking", json=payload)
    assert create_resp.status_code == 200
    booking_id = create_resp.json()["bookingid"]
    
    get_resp = api_client.get(f"/booking/{booking_id}")
    assert get_resp.json()["firstname"] == "Portfolio"
    
    update_payload = payload | {"totalprice": 999}  
    update_resp = api_client.put(
        f"/booking/{booking_id}",
        json=update_payload,
        headers={"Cookie": f"token={auth_token}"}  
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["totalprice"] == 999
    
    delete_resp = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )
    assert delete_resp.status_code == 201  
    
    assert api_client.get(f"/booking/{booking_id}").status_code == 404

def test_update_with_invalid_token(api_client):
    create_resp = api_client.post("/booking", json={
        "firstname": "Temp", "lastname": "User", "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-15"},
        "additionalneeds": "None"
    })
    booking_id = create_resp.json()["bookingid"]
    
    response = api_client.put(
        f"/booking/{booking_id}",
        json={"firstname": "Hacker"},
        headers={"Cookie": "token=invalid_token_12345"}
    )
    
    assert response.status_code in [403, 401]

    import pytest


# 2 теста ТОЛЬКО для проверки работы *fixtures/auth.py

def test_auth_token_is_string(auth_token):
    assert isinstance(auth_token, str)
    assert len(auth_token) > 0


def test_token_works_in_request(api_client, auth_token):
    """Проверяем, что токен даёт доступ к защищённому эндпоинту."""
    
    original_payload = {
        "firstname": "A", "lastname": "B", "totalprice": 10,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
        "additionalneeds": "None"
    }
    create = api_client.post("/booking", json=original_payload)
    booking_id = create.json()["bookingid"]
    
    update_payload = original_payload | {"firstname": "Updated"}
    
    response = api_client.put(
        f"/booking/{booking_id}",
        json=update_payload,
        headers={"Cookie": f"token={auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["firstname"] == "Updated"
    
    api_client.delete(f"/booking/{booking_id}", headers={"Cookie": f"token={auth_token}"})