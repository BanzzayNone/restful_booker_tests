import pytest
import logging
from fixtures.api_client import api_client
from fixtures.auth import auth_token, auth_headers

logger = logging.getLogger(__name__)


@pytest.fixture
def create_booking(api_client, auth_headers):
    """
    Фикстура-фабрика для создания бронирований с гарантированной очисткой после теста.

    Использование:
        booking_id, data = create_booking(payload)

    Все созданные бронирования удаляются после теста (best-effort).
    """
    created_ids = []

    def _create(payload: dict):
        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200, f"Failed to create booking: {response.text}"
        data = response.json()
        booking_id = data["bookingid"]
        created_ids.append(booking_id)
        return booking_id, data

    yield _create

    for booking_id in created_ids:
        try:
            api_client.delete(f"/booking/{booking_id}", headers=auth_headers)
        except Exception:
            logger.warning("Failed to cleanup booking %s", booking_id)
