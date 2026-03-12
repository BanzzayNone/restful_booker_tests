import requests
from requests.sessions import Session
from config.settings import settings
import pytest

class APIClient(Session):
    def __init__(self, base_url: str, timeout: int, default_headers: dict):
        """
        Создаёт экземпляр клиента с настройками.
        
        :param base_url: Базовый адрес API
        :param timeout: Время ожидания ответа в секундах
        :param default_headers: Заголовки по умолчанию для всех запросов
        """
        super().__init__()
        self.base_url = base_url.rstrip('/')
        self.default_timeout = timeout
        self.headers.update(default_headers)


    def request(self, method: str, url: str, **kwargs):
        """
        Переопределяем базовый метод отправки запроса.
        
        Этот метод вызывается внутри .get(), .post(), .put() и др        
        :param method: HTTP-метод
        :param url: Путь к эндпоинту 
        :param kwargs: Дополнительные аргументы 
        """
        
        if url.startswith(('http://', 'https://')):
            full_url = url
        else:
            full_url = f"{self.base_url}{url}"

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.default_timeout

        return super().request(method, full_url, **kwargs)


@pytest.fixture(scope="function")
def api_client():
    """
    Фикстура создаёт APIClient для каждого теста.
    """
    
    client = APIClient(
        base_url=settings.BASE_URL,           
        timeout=settings.REQUEST_TIMEOUT,     
        default_headers={                     
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )
    
    yield client
    
    client.close()