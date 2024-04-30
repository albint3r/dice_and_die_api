from fastapi import APIRouter, Response, status, HTTPException

from app.domain.referral_program.schemas.request import PromoterUserRequest, ReferredUserRequest, \
    PromoterUserHistoryRequest
from app.domain.referral_program.schemas.response import PromoterUserHistoryResponse
from app.infrastructure.auth.auth_handler_impl import token_http_dependency
from app.inyectables import referral_program_use_case_dependency

router = APIRouter(tags=['referral_program'], prefix='/v2/referral_program')


@router.post('/promoter')
async def create_referral_program_from_promoter(request: PromoterUserRequest,
                                                use_case: referral_program_use_case_dependency):
    use_case.create_referral_program_from_promoter(promoter_user_id=request.promoter_user_id,
                                                   referred_user_id=request.referred_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/promoter/history')
async def get_promoter_user_history(request: PromoterUserHistoryRequest,
                                    use_case: referral_program_use_case_dependency,
                                    user_id: token_http_dependency) -> PromoterUserHistoryResponse:
    if user_id == request.promoter_user_id:
        return use_case.get_promoter_user_history(promoter_user_id=request.promoter_user_id)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No Authorized.')


@router.post('/referred_user/deposit')
async def update_referral_program(request: ReferredUserRequest,
                                  use_case: referral_program_use_case_dependency,
                                  user_id: token_http_dependency):
    if user_id == request.referred_user_id:
        use_case.create_referral_transactions(referred_user_id=request.referred_user_id, amount=request.amount)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No Authorized.')
