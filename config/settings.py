import os
from pathlib import Path
from typing import Optional


class Settings:
    """
    Класс конфигурации проекта.
    Все настройки лежат здесь.
    """
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    

    BASE_URL: str = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")
    

    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    AUTH_TIMEOUT: int = int(os.getenv("AUTH_TIMEOUT", "5"))
        

    AUTH_USERNAME: str = os.getenv("AUTH_USERNAME", "admin")
    AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD", "password123")
    

    AUTH_TYPE: str = "token"
        

    DEFAULT_FIRSTNAME: str = os.getenv("TEST_FIRSTNAME", "AutoTest")
    DEFAULT_LASTNAME: str = os.getenv("TEST_LASTNAME", "QAEngineer")
    DEFAULT_TOTAL_PRICE: int = int(os.getenv("TEST_PRICE", "100"))
    

    PRICE_MIN: int = 0
    PRICE_MAX: int = 1000000
    NAME_MIN_LENGTH: int = 1
    NAME_MAX_LENGTH: int = 30



    @property
    def ENDPOINT_AUTH(self) -> str:
        """Эндпоинт получения токена"""
        return "/auth"
    

    @property
    def ENDPOINT_BOOKING(self) -> str:
        """Базовый эндпоинт бронирований"""
        return "/booking"
    
    
    def booking_by_id(self, booking_id: int) -> str:
        """Динамический эндпоинт для работы с конкретным бронированием"""
        return f"{self.ENDPOINT_BOOKING}/{booking_id}"
    



    @property
    def auth_payload(self) -> dict:
        """Готовый payload для авторизации"""
        return {
            "username": self.AUTH_USERNAME,
            "password": self.AUTH_PASSWORD
        }
    


    @property
    def default_booking_payload(self) -> dict:
        """Шаблон создания бронирования с дефолтными значениями"""
        return {
            "firstname": self.DEFAULT_FIRSTNAME,
            "lastname": self.DEFAULT_LASTNAME,
            "totalprice": self.DEFAULT_TOTAL_PRICE,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-15"
            },
            "additionalneeds": "Breakfast"
        }
    


    @staticmethod
    def get_headers(token: Optional[str] = None) -> dict:
        """
        Формирует заголовки для запросов.
        Если передан токен — добавляет Cookie для авторизации.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if token:
            headers["Cookie"] = f"token={token}"
        return headers



settings = Settings()