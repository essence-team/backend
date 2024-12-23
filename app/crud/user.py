from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_user(session: AsyncSession, user_id: str, username: str, digest_freq: str) -> User:
    user = User(user_id=user_id, username=username, digest_freq=digest_freq)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_all_users(session: AsyncSession) -> list[User]:
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def update_digest_params(session: AsyncSession, user_id: int, new_freq: str, new_time: int) -> User | None:
    user = await get_user(session, user_id)
    if user:
        user.digest_freq = new_freq
        user.digest_time = new_time
        await session.commit()
        await session.refresh(user)
    return user
