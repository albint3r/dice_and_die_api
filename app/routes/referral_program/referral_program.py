from fastapi import APIRouter

from app.domain.referral_program.schemas.request import PromoterUserRequest, ReferredUserRequest, \
    PromoterUserHistoryRequest
from app.domain.referral_program.schemas.response import PromoterUserHistoryResponse
from app.inyectables import referral_program_use_case_dependency

router = APIRouter(tags=['referral_program'], prefix='/v2/referral_program')


@router.post('/promoter_user')
async def create_referral_program_from_promoter(request: PromoterUserRequest,
                                                use_case: referral_program_use_case_dependency):
    return 'Hello '


@router.post('/referred_user/deposit')
async def update_referral_program(request: ReferredUserRequest,
                                  use_case: referral_program_use_case_dependency):
    return ' world'


@router.get('/promoter_user/history')
async def get_promoter_user_history(request: PromoterUserHistoryRequest,
                                    use_case: referral_program_use_case_dependency) -> PromoterUserHistoryResponse:
    return 'Hello world'
