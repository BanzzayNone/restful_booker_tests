import pytest
from schemas.validators import validate_booking_response, validate_booking_update
from fixtures.params import make_booking_payload


@pytest.mark.contract
def test_create_booking_contract(api_client, create_booking):
    """Контрактный тест: валидация структуры ответа при создании бронирования."""
    payload = make_booking_payload(firstname="Contract", totalprice=100, additionalneeds="Wi-Fi")

    booking_id, data = create_booking(payload)

    validated_data = validate_booking_response(data)

    assert validated_data.booking.firstname == "Contract"
    assert validated_data.booking.totalprice == 100
    assert validated_data.bookingid > 0


@pytest.mark.contract
def test_update_booking_contract(api_client, auth_headers, create_booking):
    """Контрактный тест: валидация структуры ответа при обновлении бронирования."""
    payload = make_booking_payload(firstname="Old", lastname="Name", totalprice=100)
    booking_id, _ = create_booking(payload)

    update_payload = make_booking_payload(
        firstname="New",
        lastname="Name",
        totalprice=200,
        depositpaid=False,
        additionalneeds="Breakfast",
    )

    response = api_client.put(
        f"/booking/{booking_id}",
        json=update_payload,
        headers=auth_headers,
    )
    assert response.status_code == 200

    validated_data = validate_booking_update(response.json())
    assert validated_data.firstname == "New"
    assert validated_data.totalprice == 200
