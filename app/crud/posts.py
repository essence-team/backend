from typing import List

from models.channel import Channel
from models.post import Post
from models.user_channel import UserChannel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_all_posts_for_user(session: AsyncSession, user_id: int) -> List[Post]:
    query = (
        select(Post)
        .join(Channel, Post.channel_link == Channel.channel_link)
        .join(UserChannel, Channel.channel_link == UserChannel.channel_link)
        .filter(UserChannel.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalars().all()
