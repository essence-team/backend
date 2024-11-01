from typing import List

import aiohttp
from schemas.smart_parser_api import ChannelAddRequest, ChannelAddResponse
from services.base_api_service import BaseService


class SmartParserService(BaseService):
    async def add_channels(self, channel_request: ChannelAddRequest) -> List[ChannelAddResponse]:
        url = f"{self.base_url}/channel/add"
        data = channel_request.dict()
        try:
            response_json = await self.post(url, data=data)
            responses = [ChannelAddResponse(**item) for item in response_json]
            return responses
        except aiohttp.ClientResponseError as e:
            # Handle HTTP errors
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")
            raise
