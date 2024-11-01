from typing import List

from crud.channel import (
    add_channel_to_user,
    create_channel,
    get_all_channels_for_user,
    get_channel,
    remove_channel_from_user,
)
from database import get_db_session
from fastapi import APIRouter, Depends, status
from routers import check_api_key_access
from routers.utils import extract_channel_username
from schemas.channel import ChannelLinkRequest, ChannelResponse
from sqlalchemy.ext.asyncio import AsyncSession

channel_router = APIRouter(prefix="/channels", tags=["channels"])


# 1. POST /channels/add — добавляет список каналов для конкретного пользователя
@channel_router.post("/add", status_code=status.HTTP_200_OK)
async def add_channels_for_user(
    data: ChannelLinkRequest,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    for channel_link in data.channel_links:
        # TODO: добавить проверку на существование канала
        channel_username = extract_channel_username(channel_link)
        channel = await get_channel(db, channel_link=channel_username)
        if not channel:
            channel = await create_channel(db, channel_link=channel_username)

        await add_channel_to_user(db, user_id=data.user_id, channel_link=channel_username)


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
@channel_router.get("/{user_id}", response_model=List[ChannelResponse])
async def get_channels_for_user(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    channels = await get_all_channels_for_user(db, user_id=user_id)
    return [{"channel_link": channel.channel_link} for channel in channels]
