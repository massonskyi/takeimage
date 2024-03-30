import base64
from typing import List, Dict, Tuple, Any

from modules.t2i.Text2Image import Text2ImageAPI


def get_all_style() \
        -> List[Dict[str, str]]:
    return [
        {"name": "DEFAULT", "title": "Свой стиль", "titleEn": "No style",
         "image": "https://cdn.fusionbrain.ai/static/download/img-style-personal.png"},
        {"name": "KANDINSKY", "title": "Кандинский", "titleEn": "Kandinsky",
         "image": "https://cdn.fusionbrain.ai/static/download/img-style-kandinsky.png"},
        {"name": "UHD", "title": "Детальное фото", "titleEn": "Detailed photo",
         "image": "https://cdn.fusionbrain.ai/static/download/img-style-detail-photo.png"},
        {"name": "ANIME", "title": "Аниме", "titleEn": "Anime",
         "image": "https://cdn.fusionbrain.ai/static/download/img-style-anime.png"},
    ]


def text2image(
        text,
        negative=None,
        style="DEFAULT",
        count_request=1,
        width=1024,
        height=1024
) -> Tuple[List[bytes], Dict[str, Any]]:
    result = []
    api = Text2ImageAPI()
    load_response = api.load()
    if load_response['code_app'] != 1000:
        return result, load_response

    for iteration in range(count_request):
        model_id = api.get_model()
        if model_id['code_app'] != 2000:
            return result, model_id

        uuid = api.generate(
            prompt=text,
            negative_prompt=negative,
            style=style,
            width=width,
            height=height
        )

        if uuid['code_app'] != 3000:
            return result, uuid

        images = api.check_generation(uuid['data'])
        if images['code_app'] != 4000:
            return result, images

        image_base64 = images['data'][0]
        image_data = base64.b64decode(image_base64)

        result.append(image_data)

    return result, {
        "code_app": 0,
        "message": "Images generated successfully",
        "data": result
    }
