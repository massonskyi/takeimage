import json
import logging
import time
from json import JSONDecodeError
from typing import Dict, Any

import requests

from config import (
    read_env
)
from modules.t2i.ErrorCodes import ErrorCodes


class Text2ImageAPI:
    kandinsky_token: str = None
    kandinsky_secret_key: str = None
    URL: str = None
    AUTH_HEADERS: dict = None
    uuid_model: str = None
    logger: logging.Logger = None
    error_codes: ErrorCodes = ErrorCodes()

    def load(self):
        self.logger = logging.getLogger(__name__)

        self.kandinsky_token = read_env().get('KANDINSKY_TOKEN')
        self.kandinsky_secret_key = read_env().get('KANDINSKY_SECRET_KEY')

        if self.kandinsky_token and self.kandinsky_secret_key:
            self.URL = 'https://api-key.fusionbrain.ai/'
            self.AUTH_HEADERS = {
                'X-Key': f'Key {self.kandinsky_token}',
                'X-Secret': f'Secret {self.kandinsky_secret_key}',
            }
            self.get_model()
            return {
                "code_app": self.error_codes.API_LOAD_SUCCESS,
                "message": "Text2ImageAPI successfully loaded",
                "data": self
            }
        else:
            return {
                "code_app": self.error_codes.API_LOAD_FAILED,
                "message": "KANDINSKY_TOKEN or KANDINSKY_SECRET_KEY not setup",
                "data": None
            }

    def get_model(self) -> Dict[str, str | int | Any] | None:
        try:
            response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
            response.raise_for_status()
            data = response.json()
            self.uuid_model = data[0]['id']
            return {
                "code_app": self.error_codes.MODELS_LOAD_SUCCESS,
                "message": "Models successfully loaded",
                "data": self.uuid_model
            }
        except requests.exceptions.RequestException as e:
            return {
                "code_app": self.error_codes.MODELS_LOAD_REQUEST_FAILED,
                "message": f"{e}",
                "data": None
            }
        except KeyError as e:
            return {
                "code_app": self.error_codes.MODELS_LOAD_KEY_ERROR,
                "message": f"{e}",
                "data": None
            }
        except JSONDecodeError as e:
            return {
                "code_app": self.error_codes.MODELS_LOAD_JSON_DECODE_ERROR,
                "message": f"{e}",
                "data": None
            }
        except Exception as e:
            return {
                "code_app": self.error_codes.MODELS_LOAD_UNKNOWN_ERROR,
                "message": f"{e}",
                "data": None
            }

    def generate(
            self,
            prompt,
            negative_prompt=None,
            style="DEFAULT",
            width=1024,
            height=1024
    ) -> dict[str, str | int | Any] | None:
        try:
            params = {
                "type": "GENERATE",
                "numImages": 1,
                "width": width,
                "height": height,
                "negativePromptUnclip": negative_prompt,
                "style": style,
                "generateParams": {
                    "query": f"{prompt}"
                }
            }
            data = {
                'model_id': (None, self.uuid_model),
                'params': (None, json.dumps(params), 'application/json')
            }
            response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
            response.raise_for_status()
            data = response.json()
            return {
                "code_app": self.error_codes.IMAGE_GENERATION_STARTED,
                "message": "Starting image generation",
                "data": data['uuid']
            }
        except requests.exceptions.RequestException as e:
            return {
                "code_app": self.error_codes.IMAGE_GENERATION_REQUEST_FAILED,
                "message": f"{e}",
                "data": None
            }
        except json.JSONDecodeError as e:
            return {
                "code_app": self.error_codes.IMAGE_GENERATION_JSON_DECODE_ERROR,
                "message": f"{e}",
                "data": None
            }
        except KeyError as e:
            return {
                "code_app": self.error_codes.IMAGE_GENERATION_KEY_ERROR,
                "message": f"{e}",
                "data": None
            }
        except Exception as e:
            return {
                "code_app": self.error_codes.IMAGE_GENERATION_UNKNOWN_ERROR,
                "message": f"{e}",
                "data": None
            }

    def check_generation(
            self,
            request_id,
            attempts=10,
            delay=10
    ):
        self.logger.info(f"Checking generation status for request_id: {request_id}")

        while attempts > 0:
            try:
                response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id,
                                        headers=self.AUTH_HEADERS)
                response.raise_for_status()
                data = response.json()

                status = data.get('status')
                if status is None:
                    self.logger.warning(f"Status not found in response data for request_id: {request_id}")
                    return {
                        "code_app": self.error_codes.GENERATION_STATUS_NOT_FOUND,
                        "message": f"Status not found in response data for request_id: {request_id}",
                        "data": None
                    }

                if status == 'DONE':
                    self.logger.info(f"Generation completed for request_id: {request_id}")
                    return {
                        "code_app": self.error_codes.GENERATION_COMPLETED,
                        "message": f"Generation completed for request_id: {request_id}",
                        "data": data['images']
                    }

                attempts -= 1
                time.sleep(delay)
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error making the request for request_id: {request_id}: {e}")
                return {
                    "code_app": self.error_codes.GENERATION_REQUEST_FAILED,
                    "message": f"Error making the request for request_id: {request_id}: {e}",
                    "data": None
                }
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON for request_id: {request_id}: {e}")
                return {
                    "code_app": self.error_codes.GENERATION_JSON_DECODE_ERROR,
                    "message": f"Error decoding JSON for request_id: {request_id}: {e}",
                    "data": None
                }
            except Exception as e:
                self.logger.error(f"Unexpected error for request_id: {request_id}: {e}")
                return {
                    "code_app": self.error_codes.GENERATION_UNKNOWN_ERROR,
                    "message": f"Unexpected error for request_id: {request_id}: {e}",
                    "data": None
                }

        self.logger.warning(f"Generation request timed out for request_id: {request_id}")
        return {
            "code_app": self.error_codes.GENERATION_TIMEOUT,
            "message": f"Generation request timed out for request_id: {request_id}",
            "data": None
        }
