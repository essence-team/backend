from typing import List

from models.channel import Channel
from models.user_channel import UserChannel
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_channel(session: AsyncSession, channel_link: str) -> Channel | None:
    query = select(Channel).filter(Channel.channel_link == channel_link)
    result = await session.execute(query)
    return result.scalars().first()  # Получаем первый результат или None


async def create_channel(session: AsyncSession, channel_link: str) -> Channel:
    # Проверяем, существует ли уже канал с данным channel_link
    channel = await get_channel(session, channel_link)
    if not channel:
        channel = Channel(channel_link=channel_link)
        session.add(channel)
        await session.commit()
        await session.refresh(channel)  # Обновляем объект после добавления
    return channel


async def add_channel_to_user(session: AsyncSession, user_id: int, channel_link: str) -> UserChannel:
    user_channel = UserChannel(user_id=user_id, channel_link=channel_link)
    print(user_channel)

    try:
        session.add(user_channel)
        await session.commit()
        await session.refresh(user_channel)  # Обновляем объект после добавления
    except IntegrityError:  # проверка на уникальность связки юзер-канал
        await session.rollback()

    return user_channel


async def remove_channel_from_user(session: AsyncSession, user_id: int, channel_link: str) -> None:
    # Выполняем запрос для получения конкретной записи UserChannel
    query = delete(UserChannel).where(UserChannel.user_id == user_id, UserChannel.channel_link == channel_link)
    await session.execute(query)
    await session.commit()


async def get_all_channels_for_user(session: AsyncSession, user_id: int) -> List[Channel]:
    # Получаем все каналы, на которые подписан конкретный пользователь
    query = select(Channel).join(UserChannel).filter(UserChannel.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()  # Возвращаем все найденные каналы


# async def get_all_channels_with_subscribers(session: AsyncSession) -> List[Channel]:
#     # Получаем все каналы, на которые подписан хотя бы один пользователь
#     query = select(Channel).join(UserChannel).filter(UserChannel.channel_link.isnot(None)).distinct()
#     result = await session.execute(query)
#     return result.scalars().all()  # Возвращаем все уникальные каналы
