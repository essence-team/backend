from typing import List

from pydantic import BaseModel


# Define the data models
class ChannelAddRequest(BaseModel):
    channel_links: List[str]


class ChannelAddResponse(BaseModel):
    channel_link: str
    exists: bool
