from datetime import datetime, timezone

from sqlalchemy import ARRAY, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Post(Base):
    __tablename__ = "posts"

    post_link = Column(String, primary_key=True, unique=True)
    channel_link = Column(String, ForeignKey("channels.channel_link"), nullable=False)
    text: str = Column(Text, nullable=False)  # TODO: rename this parameter
    title = Column(Text, nullable=True)
    embedding = Column(ARRAY(Float), nullable=True)
    amount_reactions = Column(Integer, default=0)
    amount_comments = Column(Integer, default=0)
    published_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    channel = relationship("Channel", back_populates="posts")

    aggregated_posts = relationship(
        "AggregatedPost",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
