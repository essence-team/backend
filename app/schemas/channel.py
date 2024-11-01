from typing import List

from pydantic import BaseModel


# Pydantic модели для валидации данных
class ChannelLinkRequest(BaseModel):
    user_id: str
    channel_links: List[str]


class ChannelResponse(BaseModel):
    channel_link: str
