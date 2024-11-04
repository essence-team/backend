from typing import List

from core.config import main_config
from crud.channel import (
    add_channel_to_user,
    create_channel,
    get_all_channels_for_user,
    get_channel,
    remove_channel_from_user,
)
from database import get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from routers import check_api_key_access
from routers.utils import extract_channel_username
from schemas.channel import ChannelLinkRequest, ChannelResponse
from services.smart_parser_api import ChannelAddRequest, ChannelAddResponse, SmartParserService
from sqlalchemy.ext.asyncio import AsyncSession

channel_router = APIRouter(prefix="/channels", tags=["channels"])


# POST /channels/add — adds a list of channels for a specific user
@channel_router.post(
    "/add",
    status_code=status.HTTP_200_OK,
    response_model=List[ChannelAddResponse],
)
async def add_channels_for_user(
    data: ChannelLinkRequest,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    # Instantiate the SmartParserService
    smart_parser_service = SmartParserService(
        host=main_config.smart_parser_api_host,
        port=main_config.smart_parser_api_port,
        api_key=main_config.smart_parser_api_key,
    )
    try:
        # Create a request object for SmartParserService
        channel_request = ChannelAddRequest(channel_links=data.channel_links)
        # Send the channel links to SmartParserService
        responses = await smart_parser_service.add_channels(channel_request)
    except Exception:
        # Handle exceptions from SmartParserService
        raise HTTPException(status_code=500, detail="Error communicating with SmartParserService")
    finally:
        await smart_parser_service.close()

    # For each channel in the response
    for response in responses:
        channel_username = extract_channel_username(response.channel_link)
        if response.exists:
            # Check if the channel exists in our database
            channel = await get_channel(db, channel_link=channel_username)
            if not channel:
                # Create the channel in our database
                await create_channel(db, channel_link=channel_username)
            # Associate the channel with the user
            try:
                await add_channel_to_user(db, user_id=data.user_id, channel_link=channel_username)
            except Exception:
                # Handle exception if associating the channel with the user fails
                raise HTTPException(status_code=500, detail="Error associating channel with user")
        else:
            # Channel does not exist; optionally log or handle accordingly
            pass

    return responses


# 2. POST /channels/remove — удаляет список каналов для конкретного пользователя
@channel_router.post("/remove", status_code=status.HTTP_200_OK)
async def remove_channels_for_user(
    data: ChannelLinkRequest,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    for channel_link in data.channel_links:
        channel_username = extract_channel_username(channel_link)
        await remove_channel_from_user(db, user_id=data.user_id, channel_link=channel_username)
    return {"detail": "Channels removed successfully"}


# 3. GET /channels/{user_id} — возвращает все каналы для конкретного пользователя
@channel_router.get("/", response_model=List[ChannelResponse])
async def get_channels_for_user(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    channels = await get_all_channels_for_user(db, user_id=user_id)
    return [{"channel_link": channel.channel_link} for channel in channels]
