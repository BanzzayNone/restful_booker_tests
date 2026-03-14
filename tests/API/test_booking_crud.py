import pytest
from fixtures.params import make_booking_payload
from schemas.validators import validate_booking_response


@pytest.mark.regression
def test_create_and_delete_booking(api_client, auth_headers, create_booking):
    """Полный CRUD-цикл: создание, чтение, обновление, удаление бронирования."""
    payload = make_booking_payload(firstname="Portfolio", additionalneeds="Wi-Fi")
    booking_id, data = create_booking(payload)

    validated = validate_booking_response(data)
    assert validated.bookingid > 0

    get_resp = api_client.get(f"/booking/{booking_id}")
    assert get_resp.json()["firstname"] == "Portfolio"

    update_payload = payload | {"totalprice": 999}
    update_resp = api_client.put(
        f"/booking/{booking_id}",
        json=update_payload,
        headers=auth_headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["totalprice"] == 999

    delete_resp = api_client.delete(
        f"/booking/{booking_id}",
        headers=auth_headers,
    )
    assert delete_resp.status_code == 201

    assert api_client.get(f"/booking/{booking_id}").status_code == 404


@pytest.mark.regression
def test_update_with_invalid_token(api_client, create_booking):
    """Проверка, что обновление с невалидным токеном отклоняется."""
    booking_id, _ = create_booking(make_booking_payload())

    response = api_client.put(
        f"/booking/{booking_id}",
        json={"firstname": "Hacker"},
        headers={"Cookie": "token=invalid_token_12345"},
    )

    assert response.status_code in [403, 401]


@pytest.mark.smoke
def test_auth_token_is_string(auth_token):
    """Проверка, что фикстура auth_token возвращает непустую строку."""
    assert isinstance(auth_token, str)
    assert len(auth_token) > 0


@pytest.mark.regression
def test_token_works_in_request(api_client, auth_headers, create_booking):
    """Проверка, что токен предоставляет доступ к защищённым эндпоинтам."""
    payload = make_booking_payload()
    booking_id, _ = create_booking(payload)

    update_payload = payload | {"firstname": "Updated"}

    response = api_client.put(
        f"/booking/{booking_id}",
        json=update_payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["firstname"] == "Updated"
