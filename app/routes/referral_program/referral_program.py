from fastapi import APIRouter, Response, status, HTTPException

from app.domain.referral_program.schemas.request import ReferredUserRequest, \
    PromoterUserHistoryRequest
from app.domain.referral_program.schemas.response import PromoterUserHistoryResponse
from app.infrastructure.auth.auth_handler_impl import token_http_dependency
from app.inyectables import referral_program_use_case_dependency

router = APIRouter(tags=['referral_program'], prefix='/v2/referral_program')


@router.post('/promoter/history')
async def get_promoter_user_history(use_case: referral_program_use_case_dependency,
                                    user_id: token_http_dependency) -> PromoterUserHistoryResponse:
    return use_case.get_promoter_user_history(promoter_user_id=user_id)


# I left this old code only for next testings of the logic in the deposito from the user.
# At the moment We don't know how we are going to monetize. So the first part of the referral program is to track
# the referred people from the users. Is possible that the solution only is give a percentage of the money
# from each user deposit. This deposit would be retained until the player made 10 bets.

# @router.post('/referred_user/deposit')
# async def update_referral_transaction(request: ReferredUserRequest,
#                                       use_case: referral_program_use_case_dependency,
#                                       user_id: token_http_dependency):
#     use_case.create_referral_transactions(referred_user_id=user_id, amount=request.amount)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

