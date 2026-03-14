from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class BookingDates(BaseModel):
    """Модель валидации полей bookingdates в ответе API."""
    checkin: str = Field(..., description="Дата заезда в формате YYYY-MM-DD")
    checkout: str = Field(..., description="Дата выезда в формате YYYY-MM-DD")

    @field_validator("checkin", "checkout")
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        """Проверка соответствия даты формату YYYY-MM-DD."""
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            raise ValueError(f"Invalid date format: {value}. Expected YYYY-MM-DD")


class BookingData(BaseModel):
    """Модель валидации тела бронирования (внутренний объект booking)."""
    firstname: str = Field(..., min_length=1, max_length=50, description="Имя гостя")
    lastname: str = Field(..., min_length=1, max_length=50, description="Фамилия гостя")
    totalprice: int = Field(..., ge=0, description="Общая стоимость бронирования")
    depositpaid: bool = Field(..., description="Оплачен ли депозит")
    bookingdates: BookingDates = Field(..., description="Даты заезда и выезда")
    additionalneeds: Optional[str] = Field(None, description="Дополнительные пожелания")

    @field_validator("bookingdates")
    @classmethod
    def validate_dates_order(cls, value: BookingDates) -> BookingDates:
        """Проверка, что дата выезда не раньше даты заезда."""
        checkin = date.fromisoformat(value.checkin)
        checkout = date.fromisoformat(value.checkout)

        if checkout < checkin:
            raise ValueError(f"checkout ({checkout}) cannot be before checkin ({checkin})")

        return value


class BookingResponse(BaseModel):
    """Модель валидации полного ответа API при создании бронирования."""
    bookingid: int = Field(..., gt=0, description="Уникальный идентификатор бронирования")
    booking: BookingData = Field(..., description="Данные бронирования")


class BookingUpdateResponse(BookingData):
    """Модель валидации ответа API при обновлении бронирования (PUT/PATCH)."""
    pass
