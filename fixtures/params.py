from faker import Faker
from typing import List, Dict
from random import random


fake = Faker()
Faker.seed(40)


def generate_valid_bookings(count: int = 10) -> List[Dict]:
    """
    Генерирует список валидных данных для создания бронирований.
    
    :param count: Количество наборов данных для генерации
    :return: Список словарей с полными данными для POST /booking
    """
    bookings = []
    
    for varholder in range(count):
        booking = {
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "totalprice": fake.random_int(min=1, max=5000),
            "depositpaid": fake.boolean(),
            "bookingdates": {
                "checkin": fake.past_date().isoformat(),
                "checkout": fake.future_date().isoformat()
            },
            "additionalneeds": fake.sentence(nb_words=3)
        }
        bookings.append(booking)
    
    return bookings


def generate_invalid_prices() -> List[Dict]:
    """
    Генерирует данные с некорректными значениями totalprice.
    
    :return: Список словарей для тестов валидации цены
    """
    return [
        {"totalprice": -1, "description": "Отрицательная цена"},
        {"totalprice": -100, "description": "Сильно отрицательная цена"},
        {"totalprice": 0, "description": "Нулевая цена"},
        {"totalprice": 9999999999999999999999999999999, "description": "Слишком большая цена"},
        {"totalprice": "not_a_number", "description": "Строка вместо числа"},
    ]


def generate_invalid_names() -> List[Dict]:
    """
    Генерирует данные с некорректными значениями firstname/lastname.
    
    :return: Список словарей для тестов валидации имён
    """
    return [
        {"firstname": "", "lastname": "Valid", "description": "Пустое имя"},
        {"firstname": "   ", "lastname": "Valid", "description": "Только пробелы"},
        {"firstname": "A" * 510, "lastname": "Valid", "description": "Слишком длинное имя"},
        {"firstname": "123", "lastname": "Valid", "description": "Цифры в имени"},
        {"firstname": "@#$%__", "lastname": "Valid", "description": "Спецсимволы в имени"},
    ]


def generate_boundary_prices() -> List[Dict]:
    """
    Генерирует данные с граничными значениями totalprice.
    
    :return: Список словарей для тестов граничных значений
    """
    return [
        {"totalprice": 1, "description": "Минимальная положительная цена"},
        {"totalprice": 100, "description": "Средняя цена"},
        {"totalprice": 5000, "description": "Высокая цена"},
        {"totalprice": 10000, "description": "Максимальная граница"},
    ]


def generate_invalid_bookings(invalid_type: str = "price") -> List[Dict]:
    """
    Генерирует полные объекты бронирования с одним невалидным полем.
    
    :param invalid_type: Тип невалидности ("price", "name", "dates")
    :return: Список полных словарей для POST /booking
    """
    base_booking = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": fake.future_date().isoformat(),
            "checkout": fake.future_date().isoformat()
        },
        "additionalneeds": "None"
    }
    
    bookings = []
    
    if invalid_type == "price":
        for invalid in generate_invalid_prices():
            booking = base_booking | {"totalprice": invalid["totalprice"]}
            bookings.append(booking)
    
    elif invalid_type == "name":
        for invalid in generate_invalid_names():
            booking = base_booking | {
                "firstname": invalid["firstname"],
                "lastname": invalid["lastname"]
            }
            bookings.append(booking)
    
    return bookings