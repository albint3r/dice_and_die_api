from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.analytics.use_cases.i_analytics_use_case import IAnalyticsUseCase
from app.repositories.analytics.analytics_repository import AnalyticsRepository


class AnalyticsUseCase(IAnalyticsUseCase):
    repo: AnalyticsRepository

    def get_plays_history(self) -> list[SinglePlayHistory]:
        return self.repo.get_plays_history()
