from crud.subscription import get_active_subscription
from crud.user import create_user, get_user, update_digest_frequency
from database import get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from routers import check_api_key_access
from schemas.user import UserCreate, UserResponse, UserUpdateDigestFreq
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(prefix="/user", tags=["users"])


# 1. POST user/add — добавить пользователя
@user_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
)
async def add_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    db_user = await create_user(db, user_id=user.user_id, username=user.username, digest_freq=user.digest_freq)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User could not be created")


# 2. GET user/{id} — получить пользователя
@user_router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    id: str,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    user = await get_user(db, user_id=id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    subscription = await get_active_subscription(db, user_id=id)

    user_info = UserResponse(
        user_id=user.user_id,
        username=user.username,
        digest_freq=user.digest_freq,
        remaining_days=subscription.days_remaining() if subscription else None,
    )

    return user_info


# 3. POST user/change_digest_freq — поменять частоту рассылки
@user_router.post("/change_digest_freq", status_code=status.HTTP_200_OK)
async def change_digest_frequency(
    data: UserUpdateDigestFreq,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    updated_user = await update_digest_frequency(db, user_id=data.user_id, new_freq=data.digest_freq)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")


# 4. GET user/all — получить всех пользователей
# @user_router.get("/all", response_model=list[UserResponse])
# async def get_all_users_route(db: AsyncSession = Depends(get_db_session), api_key=Depends(verify_access_api_key)):
#     users = await get_all_users(db)
#     return users
