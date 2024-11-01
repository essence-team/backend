from pydantic import BaseModel


class SubscriptionActivate(BaseModel):
    payment_id: str
    user_id: str
    duration_days: int


class SubscriptionDeactivate(BaseModel):
    user_id: str
