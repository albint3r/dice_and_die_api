from pydantic import BaseModel


class PromoterUserRequest(BaseModel):
    """This is the PromoterUserRequest"""
    promoter_user_id: str


class ReferredUserRequest(BaseModel):
    """This is the ReferredUserRequest"""
    referred_user_id: str
