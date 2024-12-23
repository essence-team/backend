from typing import List

from crud.subscription import (
    create_subscription,
    deactivate_subscription,
    get_all_subscribers,
    get_subscribers_expiring_in_days,
)
from database import get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from routers import check_api_key_access
from schemas.subscription import SubscriptionActivate, SubscriptionDeactivate
from schemas.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession

subscription_router = APIRouter(prefix="/subscription", tags=["subscriptions"])


# 1. POST /subscription/activate — оформить подписку на пользователя на заданное количество дней
@subscription_router.post("/activate", status_code=status.HTTP_201_CREATED)
async def activate_subscription(
    data: SubscriptionActivate,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    new_subscription = await create_subscription(
        db,
        payment_id=data.payment_id,
        user_id=data.user_id,
        duration_days=data.duration_days,
    )
    if new_subscription is None:
        raise HTTPException(status_code=404, detail="User not found or subscription could not be created")


# 2. POST /subscription/deactivate — деактивировать подписку
@subscription_router.post("/deactivate")
async def deactivate_subscription_route(
    data: SubscriptionDeactivate,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    await deactivate_subscription(db, user_id=data.user_id)
    return {"detail": "Subscription deactivated successfully"}


# 3. GET /subscription/subs — возвращает всех текущих подписчиков
@subscription_router.get("/subs", response_model=List[UserResponse])
async def get_all_current_subscribers(
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    subscribers = await get_all_subscribers(db)
    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "digest_freq": user.digest_freq,
            "digest_time": user.digest_time,
            "remaining_days": next((sub.days_remaining() for sub in user.subscriptions if sub.is_active), None),
        }
        for user in subscribers
    ]


# 4. GET /subscription/expiring_subs/{shift_days} — возвращает подписчиков,
# у которых подписка истекает через shift_days дней
@subscription_router.get("/expiring_subs/{shift_days}", response_model=List[UserResponse])
async def get_subscribers_expiring_soon(
    shift_days: int,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    expiring_subscribers = await get_subscribers_expiring_in_days(db, shift=shift_days)
    print(expiring_subscribers)
    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "digest_freq": user.digest_freq,
            "digest_time": user.digest_time,
            "remaining_days": shift_days,
        }
        for user in expiring_subscribers
    ]
