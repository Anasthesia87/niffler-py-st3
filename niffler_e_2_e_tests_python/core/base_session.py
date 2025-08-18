import allure
import curlify
from jinja2 import Environment, FileSystemLoader
from requests import Session
from pathlib import Path
from allure_commons.types import AttachmentType


class BaseSession(Session):
    def __init__(self, base_url: str, use_colored_templates: bool = True):
        super().__init__()
        self.base_url = base_url.rstrip('/')
        self._init_jinja_env(use_colored_templates)

    def _init_jinja_env(self, use_colored: bool):
        """Инициализация Jinja2 окружения для шаблонов"""
        templates_path = Path(__file__).parent.parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(templates_path)),
            autoescape=True
        )
        self.template_name = "http-colored-request.ftl" if use_colored else "http-request.ftl"

    def _log_request(self, request):
        """Логирование запроса с цветным оформлением"""
        try:
            template = self.env.get_template(self.template_name)
            curl = curlify.to_curl(request)
            rendered = template.render(request=request, curl=curl)

            allure.attach(
                body=rendered,
                name="HTTP Request",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )
        except Exception as e:
            allure.attach(
                f"Template rendering failed: {str(e)}",
                name="Template Error",
                attachment_type=AttachmentType.TEXT
            )

    def _log_response(self, response):
        """Логирование ответа с цветным оформлением"""
        try:
            template = self.env.get_template("http-colored-response.ftl")
            rendered = template.render(response=response)

            allure.attach(
                body=rendered,
                name=f"Response {response.status_code}",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )
        except Exception as e:
            allure.attach(
                f"Response template error: {str(e)}",
                name="Template Error",
                attachment_type=AttachmentType.TEXT
            )

    def request(self, method, url, **kwargs):
        """Переопределенный метод request с логированием запроса и ответа"""
        full_url = f"{self.base_url}/{url.lstrip('/')}"

        # Выполняем запрос
        response = super().request(method, full_url, **kwargs)

        # Логируем запрос и ответ
        self._log_request(response.request)
        self._log_response(response)

        return response


def create_session(base_url: str, use_colored_templates: bool = True) -> BaseSession:
    """Фабрика для создания сессии с настройкой логирования"""
    return BaseSession(
        base_url=base_url,
        use_colored_templates=use_colored_templates
    )