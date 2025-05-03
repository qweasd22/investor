import requests
import logging
from requests.exceptions import RequestException
from PyQt6.QtWidgets import QMessageBox
import sys

class ApiClient:
    def __init__(self, base_url, token):
        try:
            self.base_url = base_url
            self.session = requests.Session()
            self.session.headers.update({"Authorization": f"Token {token}"})
            self.logger = logging.getLogger(self.__class__.__name__)
            # Проверка соединения
            test_response = self._handle_request("get", "clients")
            if not test_response:
                raise Exception("Не удалось подключиться к API")
                
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Инициализация API не удалась: {str(e)}")
            sys.exit(1)

        
    def _handle_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/api/{endpoint}/"
        try:
            response = getattr(self.session, method)(url, **kwargs)
            response.raise_for_status()
            return response.json()  # Гарантированно возвращает dict/list
        except RequestException as e:
            self.logger.error(f"API Error: {str(e)}")
            raise

    def get_clients(self):
        response = self.session.get(f"{self.base_url}/api/clients/")
        response.raise_for_status()
        return response.json()
    
    def get_securities(self):
        response = self.session.get(f"{self.base_url}/api/securities/")
        response.raise_for_status()
        return response.json()
    def get_investments(self):
        response = self.session.get(f"{self.base_url}/api/investments/")
        response.raise_for_status()
        return response.json()
    
    def get_deposits(self):
        response = self.session.get(f"{self.base_url}/api/deposits/")
        response.raise_for_status()
        return response.json()