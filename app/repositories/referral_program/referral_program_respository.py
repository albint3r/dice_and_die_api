from app.db.db import _DataBase
from app.domain.referral_program.use_cases.i_referral_program_repository import IReferralProgramRepository


class ReferralProgramRepository(IReferralProgramRepository):
    db: _DataBase

    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str):
        pass

    def create_referral_transactions(self, referred_user_id: str, amount: float):
        pass

    def get_promoter_user_history(self, promoter_user_id: str):
        pass
