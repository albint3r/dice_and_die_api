from pydantic import BaseModel

from app.db.db import _DataBase
from app.domain.analytics.entities.single_play_history import SinglePlayHistory
from app.domain.analytics.errors.errors import NotExistedSinglePlayHistoryRecords


class AnalyticsRepository(BaseModel):
    db: _DataBase

    def get_plays_history(self) -> list[SinglePlayHistory]:
        """This return a list from single play history"""
        query = 'SELECT * FROM single_play_history;'
        response = self.db.query(query, (), fetch_all=True)
        if response:
            return [SinglePlayHistory(**res) for res in response]
        raise NotExistedSinglePlayHistoryRecords("You don't have any record to return.")
