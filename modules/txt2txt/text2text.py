import logging
import json
from typing import Any, Dict

import requests

from config import read_env


class ChatAi:
    access_token: str = None
    rq_uid: str = None
    authorization_data: str = None
    payload_data: str = None
    logger: logging.Logger = None

    def load_env(self):
        self.logger = logging.getLogger(__name__)

        self.rq_uid = read_env("gchcfg.env").get('RqUID')
        self.authorization_data = read_env("gchcfg.env").get('authorization_data')
        self.payload_data = read_env("gchcfg.env").get('payload_data')

        if not self.rq_uid or not self.authorization_data or not self.payload_data:
            raise Exception('Не удалось загрузить данные. Проверьте правильность переменных окружения.')

    def get_token(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload = f'scope={self.payload_data}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': f'{self.rq_uid}',
            'Authorization': f'Basic {self.authorization_data}'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
            self.access_token = response['access_token']
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error during token request: {e}")
            raise

    def query(self, query: str, temperature: float = 0.7, top_p: float = 0.1, n: int = 1, stream: bool = False,
              max_tokens: int = 512, repetition_penalty: float = 1) -> Dict[str, Any]:
        self.get_token()
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
            "model": "GigaChat:latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"{query}"
                }
            ],
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": stream,
            "max_tokens": max_tokens,
            "repetition_penalty": repetition_penalty
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
            return response['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error during query request: {e}")
            raise
