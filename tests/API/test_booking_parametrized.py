import pytest
from schemas.validators import validate_booking_response, validate_booking_update
from fixtures.params import generate_valid_bookings, generate_boundary_prices
from pydantic import BaseModel, ValidationError, field_validator



@pytest.mark.contract
@pytest.mark.parametrize("booking_data", generate_valid_bookings(count=10))
def test_create_booking_parametrized(api_client, booking_data):
    """
    Параметризованный тест создания бронирования.
    
    По 10 прогонов с данными из Faker.
    Проверяет: статус-код, структуру ответа, наличие bookingid.
    """
    response = api_client.post("/booking", json=booking_data)
    
    assert response.status_code == 200, f"Create failed: {response.text}"
    
    validated = validate_booking_response(response.json())
    
    assert validated.bookingid > 0
    
    assert validated.booking.firstname == booking_data["firstname"]
    assert validated.booking.totalprice == booking_data["totalprice"]



@pytest.mark.contract
@pytest.mark.parametrize("booking_data", generate_valid_bookings(count=5))
def test_full_crud_cycle(api_client, auth_token, booking_data):
    """
    Параметризованный тест полного CRUD цикла.
    По 5 прогонов с разными данными.
    """
    create_resp = api_client.post("/booking", json=booking_data)
    assert create_resp.status_code == 200
    booking_id = create_resp.json()["bookingid"]
    
    read_resp = api_client.get(f"/booking/{booking_id}")
    assert read_resp.status_code == 200
    assert read_resp.json()["firstname"] == booking_data["firstname"]
    
    update_data = booking_data | {
        "firstname": "Updated",
        "totalprice": booking_data["totalprice"] + 100
    }
    
    update_resp = api_client.put(
        f"/booking/{booking_id}",
        json=update_data,
        headers={"Cookie": f"token={auth_token}"}
    )
    assert update_resp.status_code == 200
    
    validated_update = validate_booking_update(update_resp.json())
    assert validated_update.firstname == "Updated"
    assert validated_update.totalprice == booking_data["totalprice"] + 100
    
    delete_resp = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )
    assert delete_resp.status_code == 201
    
    verify_resp = api_client.get(f"/booking/{booking_id}")
    assert verify_resp.status_code == 404


@pytest.mark.smoke
def test_get_all_bookings(api_client):
    """
    Smoke-тест получения списка всех бронирований.
    """
    response = api_client.get("/booking")
    
    assert response.status_code == 200
    
    bookings_list = response.json()
    assert isinstance(bookings_list, list)
    
    if len(bookings_list) > 0:
        assert "bookingid" in bookings_list[0]


@pytest.mark.parametrize("booking_data", generate_valid_bookings(count=3))
def test_get_booking_by_id(api_client, booking_data):
    """
    Параметризованный тест чтения конкретного бронирования.
    По 3 прогона с разными данными.
    """
    create_resp = api_client.post("/booking", json=booking_data)
    booking_id = create_resp.json()["bookingid"]
    
    create_resp = api_client.post("/booking", json=booking_data)
    assert create_resp.status_code == 200, f"Create failed: {create_resp.json()}"  
    booking_id = create_resp.json()["bookingid"]
    
    api_client.delete(f"/booking/{booking_id}")



@pytest.mark.parametrize("price_data", generate_boundary_prices())
def test_update_with_boundary_prices(api_client, auth_token, price_data):
    """
    Параметризованный тест обновления с граничными значениями цены.
    """
    base_data = {
        "firstname": "Boundary",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-10"},
        "additionalneeds": "None"
    }
    
    create_resp = api_client.post("/booking", json=base_data)
    booking_id = create_resp.json()["bookingid"]
    
    update_data = base_data | {"totalprice": price_data["totalprice"]}
    
    update_resp = api_client.put(
        f"/booking/{booking_id}",
        json=update_data,
        headers={"Cookie": f"token={auth_token}"}
    )
    
    assert update_resp.status_code == 200
    assert update_resp.json()["totalprice"] == price_data["totalprice"]
    
    api_client.delete(f"/booking/{booking_id}", headers={"Cookie": f"token={auth_token}"})