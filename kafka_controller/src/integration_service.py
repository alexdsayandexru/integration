import requests


class IntegrationService:
    @staticmethod
    def call_remote_method(url_args):
        response = requests.post(url_args)
        return response.text
