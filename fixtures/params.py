from faker import Faker
from typing import List, Dict, Any
from datetime import timedelta


fake = Faker()
Faker.seed(40)


def _generate_date_range() -> Dict[str, str]:
    """Генерация валидного диапазона дат, где checkin < checkout."""
    checkin = fake.date_between(start_date="-1y", end_date="+1y")
    checkout = checkin + timedelta(days=fake.random_int(min=1, max=30))
    return {
        "checkin": checkin.isoformat(),
        "checkout": checkout.isoformat(),
    }


def make_booking_payload(**overrides: Any) -> Dict[str, Any]:
    """
    Фабрика для создания одного payload бронирования с возможностью переопределения полей.

    :param overrides: Поля для переопределения в сгенерированном payload
    :return: Полный словарь payload бронирования
    """
    payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=1, max=5000),
        "depositpaid": fake.boolean(),
        "bookingdates": _generate_date_range(),
        "additionalneeds": fake.sentence(nb_words=3),
    }
    payload.update(overrides)
    return payload


def generate_valid_bookings(count: int = 10) -> List[Dict]:
    """
    Генерация списка валидных payload бронирований.

    :param count: Количество payload для генерации
    :return: Список словарей для POST /booking
    """
    return [make_booking_payload() for _ in range(count)]


def generate_invalid_prices() -> List[Dict]:
    """
    Генерация данных с невалидными значениями totalprice.

    :return: Список словарей для тестов валидации цены
    """
    return [
        {"totalprice": -1, "description": "Отрицательная цена"},
        {"totalprice": -100, "description": "Большая отрицательная цена"},
        {"totalprice": 0, "description": "Нулевая цена"},
        {"totalprice": 9999999999999999999999999999999, "description": "Экстремально большая цена"},
        {"totalprice": "not_a_number", "description": "Строка вместо числа"},
    ]


def generate_invalid_names() -> List[Dict]:
    """
    Генерация данных с невалидными значениями firstname/lastname.

    :return: Список словарей для тестов валидации имён
    """
    return [
        {"firstname": "", "lastname": "Valid", "description": "Пустое имя"},
        {"firstname": "   ", "lastname": "Valid", "description": "Только пробелы"},
        {"firstname": "A" * 510, "lastname": "Valid", "description": "Экстремально длинное имя"},
        {"firstname": "123", "lastname": "Valid", "description": "Цифры вместо имени"},
        {"firstname": "@#$%__", "lastname": "Valid", "description": "Спецсимволы вместо имени"},
    ]


def generate_boundary_prices() -> List[Dict]:
    """
    Генерация данных с граничными значениями totalprice.

    :return: Список словарей для тестов граничных значений
    """
    return [
        {"totalprice": 1, "description": "Минимальная положительная цена"},
        {"totalprice": 100, "description": "Средняя цена"},
        {"totalprice": 5000, "description": "Высокая цена"},
        {"totalprice": 10000, "description": "Максимальная граничная цена"},
    ]


def generate_invalid_bookings(invalid_type: str = "price") -> List[Dict]:
    """
    Генерация полных объектов бронирования с одним невалидным полем.

    :param invalid_type: Тип невалидности ("price", "name", "dates")
    :return: Список полных словарей для POST /booking
    """
    bookings = []

    if invalid_type == "price":
        for invalid in generate_invalid_prices():
            bookings.append(make_booking_payload(totalprice=invalid["totalprice"]))

    elif invalid_type == "name":
        for invalid in generate_invalid_names():
            bookings.append(make_booking_payload(
                firstname=invalid["firstname"],
                lastname=invalid["lastname"],
            ))

    return bookings
