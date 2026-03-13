import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Конфигурация проекта. Все настройки централизованы здесь."""

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    BASE_URL: str = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")

    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    AUTH_TIMEOUT: int = int(os.getenv("AUTH_TIMEOUT", "5"))

    AUTH_USERNAME: str = os.getenv("AUTH_USERNAME", "")
    AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD", "")

    PRICE_MIN: int = 0
    PRICE_MAX: int = 1000000
    NAME_MIN_LENGTH: int = 1
    NAME_MAX_LENGTH: int = 30

    ENDPOINT_AUTH: str = "/auth"
    ENDPOINT_BOOKING: str = "/booking"

    def __init__(self):
        self._validate()

    def _validate(self):
        """Проверка наличия обязательных учётных данных."""
        if not self.AUTH_USERNAME or not self.AUTH_PASSWORD:
            raise EnvironmentError(
                "AUTH_USERNAME and AUTH_PASSWORD must be set. "
                "Create a .env file from .env.example or set environment variables."
            )

    def booking_by_id(self, booking_id: int) -> str:
        """Эндпоинт для конкретного бронирования по ID."""
        return f"{self.ENDPOINT_BOOKING}/{booking_id}"


settings = Settings()
