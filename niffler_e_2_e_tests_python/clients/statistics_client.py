import allure
import requests
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response


class NifflerStatisticsClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json"
        }

    @staticmethod
    def attach_response(response: Response, *args, **kwargs):
        attachment_name = response.request.method + " " + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    def get_total_statistics(self):
        """Получить общую статистику расходов"""
        response = requests.get(
            f"{self.base_url}/v2/stat/total",
            headers=self.headers
        )
        return response