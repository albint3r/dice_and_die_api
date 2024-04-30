from pydantic import BaseModel


class PromoterUserRequest(BaseModel):
    """This is the PromoterUserRequest"""
    promoter_user_id: str
    referred_user_id: str


class PromoterUserHistoryRequest(BaseModel):
    """This is the PromoterUserRequest"""
    promoter_user_id: str


class ReferredUserRequest(BaseModel):
    """This is the ReferredUserRequest"""
    referred_user_id: str
    amount: float | None = None
