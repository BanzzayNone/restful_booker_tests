import pytest
from schemas.validators import validate_booking_response, validate_booking_update
from fixtures.params import generate_valid_bookings, generate_boundary_prices, make_booking_payload


@pytest.mark.contract
@pytest.mark.parametrize("booking_data", generate_valid_bookings(count=10))
def test_create_booking_parametrized(api_client, booking_data):
    """
    Параметризованный тест создания бронирования.

    10 запусков с данными, сгенерированными Faker.
    Валидация: статус-код, структура ответа, наличие bookingid.
    """
    response = api_client.post("/booking", json=booking_data)

    assert response.status_code == 200, f"Create failed: {response.text}"

    validated = validate_booking_response(response.json())

    assert validated.bookingid > 0
    assert validated.booking.firstname == booking_data["firstname"]
    assert validated.booking.totalprice == booking_data["totalprice"]


@pytest.mark.contract
@pytest.mark.parametrize("booking_data", generate_valid_bookings(count=5))
def test_full_crud_cycle(api_client, auth_headers, booking_data):
    """
    Параметризованный тест полного CRUD-цикла.
    5 запусков с разными наборами данных.
    """
    create_resp = api_client.post("/booking", json=booking_data)
    assert create_resp.status_code == 200
    booking_id = create_resp.json()["bookingid"]

    read_resp = api_client.get(f"/booking/{booking_id}")
    assert read_resp.status_code == 200
    assert read_resp.json()["firstname"] == booking_data["firstname"]

    update_data = booking_data | {
        "firstname": "Updated",
        "totalprice": booking_data["totalprice"] + 100,
    }

    update_resp = api_client.put(
        f"/booking/{booking_id}",
        json=update_data,
        headers=auth_headers,
    )
    assert update_resp.status_code == 200

    validated_update = validate_booking_update(update_resp.json())
    assert validated_update.firstname == "Updated"
    assert validated_update.totalprice == booking_data["totalprice"] + 100

    delete_resp = api_client.delete(
        f"/booking/{booking_id}",
        headers=auth_headers,
    )
    assert delete_resp.status_code == 201

    verify_resp = api_client.get(f"/booking/{booking_id}")
    assert verify_resp.status_code == 404


@pytest.mark.smoke
def test_get_all_bookings(api_client):
    """Smoke-тест: получение списка всех бронирований."""
    response = api_client.get("/booking")

    assert response.status_code == 200

    bookings_list = response.json()
    assert isinstance(bookings_list, list)

    if len(bookings_list) > 0:
        assert "bookingid" in bookings_list[0]


@pytest.mark.parametrize("booking_data", generate_valid_bookings(count=3))
def test_get_booking_by_id(api_client, auth_headers, booking_data):
    """
    Параметризованный тест чтения конкретного бронирования.
    3 запуска с разными наборами данных.
    """
    create_resp = api_client.post("/booking", json=booking_data)
    assert create_resp.status_code == 200, f"Create failed: {create_resp.text}"
    booking_id = create_resp.json()["bookingid"]

    get_resp = api_client.get(f"/booking/{booking_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["firstname"] == booking_data["firstname"]
    assert get_resp.json()["lastname"] == booking_data["lastname"]
    assert get_resp.json()["totalprice"] == booking_data["totalprice"]

    api_client.delete(f"/booking/{booking_id}", headers=auth_headers)


@pytest.mark.parametrize("price_data", generate_boundary_prices())
def test_update_with_boundary_prices(api_client, auth_headers, price_data):
    """Параметризованный тест обновления с граничными значениями цены."""
    base_data = make_booking_payload(
        firstname="Boundary",
        lastname="Test",
        totalprice=100,
    )

    create_resp = api_client.post("/booking", json=base_data)
    booking_id = create_resp.json()["bookingid"]

    update_data = base_data | {"totalprice": price_data["totalprice"]}

    update_resp = api_client.put(
        f"/booking/{booking_id}",
        json=update_data,
        headers=auth_headers,
    )

    assert update_resp.status_code == 200
    assert update_resp.json()["totalprice"] == price_data["totalprice"]

    api_client.delete(f"/booking/{booking_id}", headers=auth_headers)
