from datetime import datetime, timedelta, timezone
from typing import List

from crud.user import get_user
from models.subscription import Subscription
from models.user import User
from sqlalchemy import Date, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def create_subscription(
    session: AsyncSession,
    payment_id: str,
    user_id: int,
    duration_days: int,
) -> Subscription | None:
    user = await get_user(session, user_id)

    if user:
        last_sub = await get_last_subscription(session, user_id)

        await deactivate_subscription(session=session, user_id=user_id)

        new_subscription = Subscription(
            id=payment_id,
            user_id=user_id,
            start_sub=last_sub.end_sub if last_sub else None,
            duration_days=duration_days,
        )
        session.add(new_subscription)
        await session.commit()
        await session.refresh(new_subscription)

        return new_subscription

    return None


async def deactivate_subscription(session: AsyncSession, user_id: int) -> None:
    await session.execute(
        update(Subscription)
        .where(
            Subscription.user_id == user_id,
            Subscription.is_active == True,
            Subscription.end_sub < datetime.now(tz=timezone.utc),
        )
        .values(is_active=False)
    )
    await session.commit()


async def get_all_subscribers(session: AsyncSession) -> List[User]:
    query = select(User).join(Subscription).filter(Subscription.is_active == True).distinct()
    result = await session.execute(query.options(selectinload(User.subscriptions)))
    return result.scalars().all()


async def get_subscribers_expiring_in_days(session: AsyncSession, shift: int) -> List[User]:
    target_date = (datetime.now(tz=timezone.utc) + timedelta(days=shift)).date()

    query = (
        select(User)
        .join(Subscription)
        .filter(Subscription.is_active == True, Subscription.end_sub.cast(Date) == target_date)
    )
    result = await session.execute(query)
    users = result.scalars().all()

    return users


# async def get_active_subscriptions(session: AsyncSession, user_id: int) -> List[Subscription] | None:
#     """Получаем активную подписку пользователя"""
#     query = select(Subscription).where(Subscription.user_id == user_id, Subscription.is_active == True)
#     result = await session.execute(query)
#     return result.scalars().all()


async def get_last_subscription(session: AsyncSession, user_id: int) -> Subscription | None:
    """Получаем последнюю подписку пользователя"""
    query = select(Subscription).where(Subscription.user_id == user_id).order_by(Subscription.start_sub.desc()).limit(1)
    result = await session.execute(query)
    return result.scalars().first()
