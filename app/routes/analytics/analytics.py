from fastapi import APIRouter

from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.inyectables import analytics_use_case_dependency

router = APIRouter(tags=['analytics'], prefix='/v2/analytics')


@router.get('/play/history')
async def get_single_play_history(use_case: analytics_use_case_dependency) -> list[SinglePlayHistory]:
    return use_case.get_plays_history()
