import logging
import time
import requests
from requests.sessions import Session
from config.settings import settings
import pytest

logger = logging.getLogger(__name__)


class APIClient(Session):
    def __init__(self, base_url: str, timeout: int, default_headers: dict) -> None:
        """
        Создание экземпляра клиента с предварительно настроенными параметрами.

        :param base_url: Базовый URL API
        :param timeout: Таймаут запроса по умолчанию в секундах
        :param default_headers: Заголовки по умолчанию для всех запросов
        """
        super().__init__()
        self.base_url = base_url.rstrip('/')
        self.default_timeout = timeout
        self.headers.update(default_headers)

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Переопределение базового метода request для добавления префикса URL, таймаута и логирования.

        :param method: HTTP-метод
        :param url: Путь эндпоинта или полный URL
        :param kwargs: Дополнительные аргументы для requests
        """
        if url.startswith(('http://', 'https://')):
            full_url = url
        else:
            full_url = f"{self.base_url}{url}"

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.default_timeout

        start = time.perf_counter()
        response = super().request(method, full_url, **kwargs)
        elapsed = time.perf_counter() - start

        if logger.isEnabledFor(logging.INFO):
            path = url if not url.startswith(('http://', 'https://')) else full_url
            logger.info("%-6s %-25s → %s (%.2fs)", method, path, response.status_code, elapsed)

        return response


@pytest.fixture(scope="session")
def api_client():
    """Фикстура с областью видимости session, предоставляющая настроенный экземпляр APIClient."""
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
