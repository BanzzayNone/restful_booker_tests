from pydantic import ValidationError
from schemas.booking import BookingResponse, BookingData, BookingUpdateResponse
from schemas.auth import AuthResponse
from typing import Dict, Any, Tuple


def validate_booking_response(response_data: Dict[str, Any]) -> BookingResponse:
    """
    Валидация ответа API при создании бронирования.

    :param response_data: Словарь из response.json()
    :return: Валидированный объект BookingResponse
    :raises ValidationError: Если структура не соответствует модели
    """
    return BookingResponse.model_validate(response_data)


def validate_booking_update(response_data: Dict[str, Any]) -> BookingUpdateResponse:
    """
    Валидация ответа API при обновлении бронирования.

    :param response_data: Словарь из response.json()
    :return: Валидированный объект BookingUpdateResponse
    """
    return BookingUpdateResponse.model_validate(response_data)


def validate_auth_response(response_data: Dict[str, Any]) -> AuthResponse:
    """
    Валидация ответа API при аутентификации.

    :param response_data: Словарь из response.json()
    :return: Валидированный объект AuthResponse
    """
    return AuthResponse.model_validate(response_data)


def validate_response(model_class: type, response_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Универсальная валидация, возвращающая (is_valid, error_message) вместо исключения.

    :param model_class: Класс модели Pydantic (например, BookingResponse)
    :param response_data: Словарь из response.json()
    :return: (True, "") если валидно, (False, детали_ошибки) если нет
    """
    try:
        model_class.model_validate(response_data)
        return True, ""
    except ValidationError as e:
        return False, str(e)
