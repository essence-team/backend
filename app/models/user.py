from enum import Enum

from models.base import Base
from sqlalchemy import CheckConstraint, Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship


class DigestFreq(Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# Модель пользователя
class User(Base):
    __tablename__ = "users"

    user_id = Column(String(30), primary_key=True, index=True)
    username = Column(String(30), unique=True, nullable=False)
    digest_freq = Column(SQLEnum(DigestFreq), nullable=False)
    digest_time = Column(Integer, nullable=False, default=12)  # Время отправки дайджеста

    __table_args__ = (CheckConstraint("digest_time >= 6 AND digest_time <= 24", name="check_digest_time"),)

    # Связь с таблицей Subscriptions и UserChannels
    subscriptions = relationship("Subscription", back_populates="user")
    user_channels = relationship("UserChannel", back_populates="user")
