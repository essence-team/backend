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
