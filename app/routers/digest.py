from typing import List

from crud.aggregated_posts import get_top_aggregated_posts_for_user
from crud.user import get_user  # Assuming you have a function to get user by ID
from database import get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from routers import check_api_key_access
from schemas.aggregated_posts import AggregatedPostModel
from sqlalchemy.ext.asyncio import AsyncSession

digest_router = APIRouter(prefix="/digest", tags=["digest"])


@digest_router.get("/", response_model=List[AggregatedPostModel])
async def get_digest_for_user(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    top_n = 10
    top_k = 3

    digest = await get_top_aggregated_posts_for_user(db, user_id, top_n, top_k)
    return digest


@digest_router.post("/ask", response_model=str)
async def ask_question(
    user_id: str,
    question: str,
    clusters: List[int],
    db: AsyncSession = Depends(get_db_session),
    api_key=Depends(check_api_key_access),
):
    # Placeholder logic for answering the question
    answer = f"User {user_id} asked: {question}"
    return answer
