from app.db.db import _DataBase
from app.domain.referral_program.entities.referral_program import ReferralProgram
from app.domain.referral_program.errors.errors import ReferralProgramCreationError
from app.domain.referral_program.schemas.response import PromoterUserHistoryResponse
from app.domain.referral_program.use_cases.i_referral_program_repository import IReferralProgramRepository


class ReferralProgramRepository(IReferralProgramRepository):
    db: _DataBase

    def can_user_be_referred(self, referred_user_id: str) -> bool:
        try:
            query = "SELECT * FROM referral_program WHERE referred_user_id=%s;"
            values = (referred_user_id,)
            response = self.db.query(query, values, fetch_all=False)
            return response is None
        except Exception:
            return False

    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str):
        try:
            query = 'INSERT INTO referral_program (promoter_user_id, referred_user_id) VALUES (%s, %s);'
            values = (promoter_user_id, referred_user_id)
            self.db.execute(query, values)
        except Exception as e:
            raise ReferralProgramCreationError(f'Error linking the promoter and the referred. This is your error: {e}')

    def create_referral_transactions(self, referred_user_id: str, amount: float):
        pass

    def get_promoter_user_history(self, promoter_user_id: str) -> PromoterUserHistoryResponse:
        query = "SELECT * FROM referral_program WHERE promoter_user_id=%s;"
        values = (promoter_user_id,)
        response = self.db.query(query, values, fetch_all=True)
        if response:
            referrals = [ReferralProgram(**referral) for referral in response]
            return PromoterUserHistoryResponse(referrals=referrals)
        return PromoterUserHistoryResponse(referrals=[])
