import base64
import json
import os
import time
import requests

from config import (
    read_env
)
KANDINSKY_TOKEN, KANDINSKY_SECRET_KEY = read_env()['KANDINSKY_TOKEN'], read_env()['KANDINSKY_SECRET_KEY']

BASE_DIR = os.getcwd()

save_file_path = f"{BASE_DIR}/data"


def get_all_style() -> list:
    return [{"name": "DEFAULT", "title": "Свой стиль", "titleEn": "No style",
             "image": "https://cdn.fusionbrain.ai/static/download/img-style-personal.png"},
            {"name": "KANDINSKY", "title": "Кандинский", "titleEn": "Kandinsky",
             "image": "https://cdn.fusionbrain.ai/static/download/img-style-kandinsky.png"},
            {"name": "UHD", "title": "Детальное фото", "titleEn": "Detailed photo",
             "image": "https://cdn.fusionbrain.ai/static/download/img-style-detail-photo.png"},
            {"name": "ANIME", "title": "Аниме", "titleEn": "Anime",
             "image": "https://cdn.fusionbrain.ai/static/download/img-style-anime.png"},
            ]


def text2image(text, negative=None, style="DEFAULT", count_request=1, width=1024, height=1024) -> list[bytes]:
    result = []
    for iteration in range(count_request):
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', KANDINSKY_TOKEN, KANDINSKY_SECRET_KEY)
        model_id = api.get_model()
        uuid = api.generate(prompt=text, model=model_id, negative_prompt=negative, style=style, width=width, height=height)
        images = api.check_generation(uuid)

        image_base64 = images[0]
        image_data = base64.b64decode(image_base64)

        result.append(image_data)

    return result


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, negative_prompt=None, style="DEFAULT", images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "negativePromptUnclip": negative_prompt,
            "style": style,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
