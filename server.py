import base64
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from t2image.Text2Image import text2image, get_all_style

app = FastAPI()


@app.get("/api/v1/styles", response_model=List[dict])
def get_styles():
    return get_all_style()


@app.post("/api/v1/generate")
def generate_images(
        text: Optional[str],
        negative: Optional[str] = None,
        style: Optional[str] = "DEFAULT",
        count_request: Optional[int] = 1,
        width: Optional[int] = 1024,
        height: Optional[int] = 1024,
):
    if negative == 'nullptr':
        negative = None
    if int(count_request) <= 0:
        raise HTTPException(status_code=400, detail="count_request must be greater than 0")
    print(text, negative, style, int(count_request), 1, width, height)
    images = text2image(text, negative, style, int(count_request), 1, int(width),int(height))

    if not images:
        raise HTTPException(status_code=500, detail="Failed to generate images")

    return [{"image": base64.b64encode(image_data).decode()} for image_data in images]
