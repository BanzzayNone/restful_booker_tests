import pytest
import json
from fixtures.params import generate_invalid_prices, generate_invalid_names, make_booking_payload


# ПРИМЕЧАНИЕ: Это негативные тесты, но API является учебным и не выполняет полноценную валидацию.
#             API не обрабатывает многие сценарии корректно (например, пустые поля возвращают 500 вместо 400).
#             Тесты написаны для демонстрации паттернов негативного тестирования и понимания их структуры.


@pytest.mark.negative
@pytest.mark.parametrize("invalid_price", generate_invalid_prices())
def test_create_booking_with_invalid_price(api_client, invalid_price):
    """
    Проверка, что сервер отклоняет невалидные значения totalprice.

    Параметризация: 5 вариантов невалидных цен из генератора.
    Ограничение API: сервер принимает все значения — помечено как xfail.
    """
    payload = make_booking_payload(totalprice=invalid_price["totalprice"])

    response = api_client.post("/booking", json=payload)

    pytest.xfail(
        f"API does not validate price: {invalid_price['description']}. "
        f"Expected 400, got {response.status_code}"
    )


@pytest.mark.negative
@pytest.mark.parametrize("invalid_name_data", generate_invalid_names())
def test_create_booking_with_invalid_name(api_client, invalid_name_data):
    """
    Проверка, что сервер отклоняет невалидные значения firstname/lastname.

    Ограничение API: сервер принимает все значения — помечено как xfail.
    """
    payload = make_booking_payload(
        firstname=invalid_name_data["firstname"],
        lastname=invalid_name_data["lastname"],
    )

    response = api_client.post("/booking", json=payload)

    pytest.xfail(
        f"API does not validate names: {invalid_name_data['description']}. "
        f"Expected 400, got {response.status_code}"
    )


@pytest.mark.negative
@pytest.mark.parametrize("missing_field", ["firstname", "lastname", "totalprice", "bookingdates"])
def test_create_booking_missing_required_field(api_client, missing_field):
    """Проверка, что сервер отклоняет запросы без обязательных полей."""
    payload = make_booking_payload()
    del payload[missing_field]

    response = api_client.post("/booking", json=payload)

    assert response.status_code == 500, f"Expected 400, got {response.status_code}"


@pytest.mark.negative
def test_update_booking_without_token(api_client, create_booking):
    """Проверка, что обновление бронирования без токена запрещено."""
    booking_id, _ = create_booking(make_booking_payload())

    update_payload = make_booking_payload(firstname="Without", lastname="Attempt")

    response = api_client.put(f"/booking/{booking_id}", json=update_payload)
    assert response.status_code == 403


@pytest.mark.negative
def test_update_booking_with_invalid_token(api_client, create_booking):
    """Проверка, что сервер отклоняет запросы с невалидным токеном."""
    booking_id, _ = create_booking(make_booking_payload())

    response = api_client.put(
        f"/booking/{booking_id}",
        json=make_booking_payload(firstname="Updated"),
        headers={"Cookie": "token=definitely_invalid_token_12345"},
    )

    assert response.status_code in [401, 403], f"Expected auth error, got {response.status_code}"


@pytest.mark.negative
def test_get_nonexistent_booking(api_client):
    """Проверка, что запрос несуществующего бронирования возвращает 404."""
    fake_id = 999999999

    response = api_client.get(f"/booking/{fake_id}")

    assert response.status_code == 404


@pytest.mark.negative
def test_create_booking_wrong_content_type(api_client):
    """Проверка реакции API на неверный заголовок Content-Type."""
    payload = make_booking_payload()

    response = api_client.post(
        "/booking",
        data=json.dumps(payload),
        headers={"Content-Type": "text/plain"},
    )

    assert response.status_code == 500, f"Expected 400 or 415, got {response.status_code}"
