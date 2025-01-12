from typing import List

from pydantic import BaseModel


class PostModel(BaseModel):
    channel_link: str
    post_link: str
    importance_score: float


class AggregatedPostModel(BaseModel):
    cluster: int
    title: str
    posts: List[PostModel]


class QuestionRequest(BaseModel):
    user_id: str
    clusters: List[int]
    digest_text: str
    query_history: List[str]
