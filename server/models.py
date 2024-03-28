from pydantic import BaseModel


class ImageRequest(BaseModel):
    text: str
    negative: str | None = None
    style: str | None = None
    count_request: int | None = 1
    width: int | None = 1024
    height: int | None = 1024


class QuestRequest(BaseModel):
    query: str
    temperature: float | None = None
    top_p: float | None = None
    n: int | None = None
    stream: bool | None = None
    max_tokens: int | None = None
    repetition_penalty: float | None = None
