import base64
from typing import List
import logging
from cachetools import TTLCache, cached
from fastapi import FastAPI, HTTPException

from modules.text2text import ChatAi
from server.models import ImageRequest, QuestRequest
from modules.Text2Image import text2image, get_all_style

app = FastAPI()


@app.get("/api/v1/styles", response_model=List[dict])
def get_styles():
    logger = logging.getLogger(__name__)

    styles = get_all_style()
    if not styles:
        raise HTTPException(status_code=500, detail="Failed to fetch styles")

    logger.info("Retrieved available styles")
    return styles


@app.post("/api/v1/generate", response_model=List[dict])
def generate_images(request: ImageRequest):
    logger = logging.getLogger(__name__)

    if request.count_request <= 0:
        raise HTTPException(status_code=400, detail="count_request must be greater than 0")

    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if not request.style or not request.style.strip():
        raise HTTPException(status_code=400, detail="Style cannot be empty")

    if request.width <= 0 or request.height <= 0:
        raise HTTPException(status_code=400, detail="Width and height must be greater than 0")

    images = text2image(request.text, request.negative, request.style, request.count_request, request.width,
                        request.height)

    if not images:
        raise HTTPException(status_code=500, detail="Failed to generate images")

    logger.info(f"Generated {len(images)} images for request: {request.dict()}")
    return [{"image": base64.b64encode(image_data).decode()} for image_data in images]


@app.post("/api/v1/quest", response_model=List[dict])
def generate_answer(request: QuestRequest):
    logger = logging.getLogger(__name__)

    # 1. Error handling and validation
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # 2. Caching
    cache = TTLCache(maxsize=100, ttl=60)

    @cached(cache)
    def get_answer_from_cache(query):
        chat_ai = ChatAi()
        return chat_ai.query(query, temperature=request.temperature, top_p=request.top_p, n=request.n,
                             stream=request.stream, max_tokens=request.max_tokens,
                             repetition_penalty=request.repetition_penalty)

    # 3. Asynchronous processing
    answer = get_answer_from_cache(request.query)

    logger.info(f"Generated answer for query: {request.query}")
    return [{"answer": answer}]
