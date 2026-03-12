from pydantic import BaseModel, Field


class AuthResponse(BaseModel):
    """
    Модель для валидации ответа эндпоинта /auth.
    """
    token: str = Field(..., min_length=1, description="Токен авторизации")