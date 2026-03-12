from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class BookingDates(BaseModel):
    """
    Модель для валидации полей bookingdates в ответе API.
    """
    checkin: str = Field(..., description="Дата заезда в формате YYYY-MM-DD")
    checkout: str = Field(..., description="Дата выезда в формате YYYY-MM-DD")
    

    @field_validator("checkin", "checkout")
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        """
        Проверяет, что дата соответствует формату YYYY-MM-DD.
        
        :param value: Строка даты из ответа API
        :return: Та же строка, если валидна
        :raises ValueError: Если формат не соответствует
        """
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            raise ValueError(f"Invalid date format: {value}. Expected YYYY-MM-DD")

class BookingData(BaseModel):
    """
    Модель для валидации тела бронирования (то, что внутри booking).
    """
    firstname: str = Field(..., min_length=1, max_length=50, description="Имя гостя")
    lastname: str = Field(..., min_length=1, max_length=50, description="Фамилия гостя")
    totalprice: int = Field(..., ge=0, description="Общая стоимость бронирования")
    depositpaid: bool = Field(..., description="Оплачен ли депозит")
    bookingdates: BookingDates = Field(..., description="Даты заезда и выезда")
    additionalneeds: Optional[str] = Field(None, description="Дополнительные потребности")
    
    @field_validator("bookingdates")
    @classmethod
    def validate_dates_order(cls, value: BookingDates) -> BookingDates:
        """
        Проверяет, что дата выезда не раньше даты заезда.
        
        :param value: Объект BookingDates
        :return: Тот же объект, если валиден
        :raises ValueError: Если checkout < checkin
        """
        checkin = date.fromisoformat(value.checkin)
        checkout = date.fromisoformat(value.checkout)
        
        if checkout < checkin:
            raise ValueError(f"checkout ({checkout}) cannot be before checkin ({checkin})")
        
        return value


class BookingResponse(BaseModel):
    """
    Модель для валидации полного ответа API при создании бронирования.
    """
    bookingid: int = Field(..., gt=0, description="Уникальный идентификатор бронирования")
    booking: BookingData = Field(..., description="Данные бронирования")

class BookingUpdateResponse(BaseModel):
    """
    Модель для валидации ответа при обновлении бронирования (PUT/PATCH).
    """
    firstname: str = Field(..., min_length=1)
    lastname: str = Field(..., min_length=1)
    totalprice: int = Field(..., ge=0)
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str]