from pydantic import ValidationError
from schemas.booking import BookingResponse, BookingData, BookingUpdateResponse
from schemas.auth import AuthResponse
from typing import Dict, Any


def validate_booking_response(response_data: Dict[str, Any]) -> BookingResponse:
    """
    Валидирует ответ API на создание бронирования.
    
    :param response_data: Словарь из response.json()
    :return: Валидированный объект BookingResponse
    :raises ValidationError: Если структура не соответствует модели
    """
    return BookingResponse.model_validate(response_data)


def validate_booking_update(response_data: Dict[str, Any]) -> BookingUpdateResponse:
    """
    Валидирует ответ API на обновление бронирования.
    
    :param response_data: Словарь из response.json()
    :return: Валидированный объект BookingUpdateResponse
    """
    return BookingUpdateResponse.model_validate(response_data)



def validate_auth_response(response_data: Dict[str, Any]) -> AuthResponse:
    """
    Валидирует ответ API на авторизацию.
    
    :param response_data: Словарь из response.json()
    :return: Валидированный объект AuthResponse
    """
    return AuthResponse.model_validate(response_data)



def validate_response(model_class, response_data: Dict[str, Any]) -> bool:
    """
    Универсальная валидация с возвратом True/False вместо исключения.
    
    :param model_class: Pydantic-класс для валидации (например, BookingResponse)
    :param response_data: Словарь из response.json()
    :return: True если валидно, False если нет
    """
    try:
        model_class.model_validate(response_data)
        return True
    except ValidationError:
        return False