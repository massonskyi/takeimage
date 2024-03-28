from typing import Optional

from pydantic import BaseModel


class ImageRequest(BaseModel):
    text: str
    negative: str | None = None
    style: str | None = None
    count_request: int | None = 1
    width: int | None = 1024
    height: int | None = 1024
