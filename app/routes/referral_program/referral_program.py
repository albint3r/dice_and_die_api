from fastapi import APIRouter

from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.referral_program.schemas.response import PromoterUserHistoryResponse
from app.inyectables import analytics_use_case_dependency

router = APIRouter(tags=['referral_program'], prefix='/v2/referral_program')


@router.post('/promoter_user')
async def create_referral_program_from_promoter():
    return 'Hello '


@router.put('/referred_user/{referred_user_id}')
async def update_referral_program():
    return ' world'


@router.get('/promoter_user/{promoter_user_id}')
async def get_promoter_user_history() -> PromoterUserHistoryResponse:
    return 'Hello world'
