from typing import List

import aiohttp
from core.config import main_config
from schemas.aggregated_posts import QuestionRequest
from schemas.smart_parser_api import ChannelAddRequest, ChannelAddResponse
from services.base_api_service import BaseService


class SmartParserService(BaseService):
    async def add_channels(self, channel_request: ChannelAddRequest) -> List[ChannelAddResponse]:
        url = f"{self.base_url}/channel/add"
        data = channel_request.model_dump()
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

    async def ask_question(self, question_request: QuestionRequest) -> str:
        url = f"{self.base_url}/question/ask"
        data = question_request.model_dump()
        try:
            response = await self.post(url, data=data)
            return response
        except aiohttp.ClientResponseError as e:
            # Handle HTTP errors
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")
            raise


smart_parser_service = SmartParserService(
    host=main_config.smart_parser_api_host,
    port=main_config.smart_parser_api_port,
    api_key=main_config.smart_parser_api_key,
)
