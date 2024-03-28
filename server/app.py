import base64
from typing import List, Optional

from fastapi import FastAPI, HTTPException

from server.models import ImageRequest
from t2image.Text2Image import text2image, get_all_style

app = FastAPI()


@app.get("/api/v1/styles", response_model=List[dict])
def get_styles():
    return get_all_style()


@app.post("/api/v1/generate", response_model=List[dict])
def generate_images(request: ImageRequest):
    if request.count_request <= 0:
        raise HTTPException(status_code=400, detail="count_request must be greater than 0")

    images = text2image(request.text, request.negative, request.style, request.count_request,  request.width,
                        request.height)

    if not images:
        raise HTTPException(status_code=500, detail="Failed to generate images")

    return [{"image": base64.b64encode(image_data).decode()} for image_data in images]
