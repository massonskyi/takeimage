import base64
import datetime
import io
import json
import os
import random
import time
from typing import List

from PIL import Image
import requests

KANDINSKY_TOKEN, KANDINSKY_SECRET_KEY = ('4162FAF83B851FC4B579A20700880E9C', 'F292C805F82E2A081644F5F850EF6F2E')

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


def text2image(text, negative=None, style="DEFAULT", count_request=1, images=1, width=1024, height=1024) \
        -> list[bytes]:
    """
    Converts a text string to an image of the given width and height
    :param text: Text to convert into an image
    :param negative: Positive or negative values for negative values (negative values are)
    :param style: The style of the image (default "DEFAULT")[UHD, KANDINSKY, ANIME]
    :param count_request: The number of times the image should be generated (default 1)
    :param images: 1
    :param width: The width of the image (default 1024)
    :param height: The height of the image (default 1024)
    :return:
    """
    print("initialized model")
    r = random.randint(0, 100000)
    result = []
    for iteration in range(count_request):
        print(
            f"settings generation: iteration {iteration}\nr {r}\nprompt {text}\nnegative {negative}\nstyle {style}\n width {width}\nheight {height}")
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', KANDINSKY_TOKEN, KANDINSKY_SECRET_KEY)
        model_id = api.get_model()
        uuid = api.generate(prompt=text, model=model_id, negative_prompt=negative, style=style, images=images,
                            width=width, height=height)
        print("start generation model")
        images = api.check_generation(uuid)

        image_base64 = images[0]
        image_data = base64.b64decode(image_base64)
        print("end generation\nstart saving and sender")
        if not os.path.exists(save_file_path):
            os.makedirs(save_file_path, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"{text.split('.')[0].replace(' ', '_')}_{timestamp}_{iteration}_{r}.jpg"
        filepath = os.path.join(os.path.join(os.path.join(save_file_path, str(timestamp)), str(r)), filename)

        if not os.path.exists(os.path.join(os.path.join(save_file_path, str(timestamp)), str(r))):
            os.makedirs(os.path.join(os.path.join(save_file_path, str(timestamp)), str(r)), exist_ok=True)

        i = Image.open(io.BytesIO(image_data))
        i.save(fp=filepath)
        print(f"end saving to{filepath}")
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
        # "negativePromptUnclip": "яркие цвета, кислотность, высокая контрастность",
        # "style": "ANIME",
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