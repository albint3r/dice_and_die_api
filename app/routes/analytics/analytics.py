from fastapi import APIRouter, Depends

from app.db.db import db
from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.analytics.use_cases.i_analytics_use_case import IAnalyticsUseCase
from app.infrastructure.analytics.analytics_use_case import AnalyticsUseCase
from app.repositories.analytics.analytics_repository import AnalyticsRepository

router = APIRouter(tags=['analytics'], prefix='/v2/analytics')


async def _get_use_case() -> IAnalyticsUseCase:
    return AnalyticsUseCase(repo=AnalyticsRepository(db=db))


@router.get('/play/history')
async def get_single_play_history(use_case: IAnalyticsUseCase = Depends(_get_use_case)) -> list[SinglePlayHistory]:
    return use_case.get_plays_history()
