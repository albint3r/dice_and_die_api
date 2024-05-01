from app.db.db import _DataBase
from app.domain.referral_program.entities.referral_program import ReferralProgram
from app.domain.referral_program.errors.errors import ReferralProgramCreationError, AddingTransactionBonusError
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
        except Exception as _:
            return False

    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str) -> None:
        try:
            query = 'INSERT INTO referral_program (promoter_user_id, referred_user_id) VALUES (%s, %s);'
            values = (promoter_user_id, referred_user_id)
            self.db.execute(query, values)
        except Exception as e:
            raise ReferralProgramCreationError(f'Error linking the promoter and the referred. This is your error: {e}')

    def get_promoter_user_history(self, promoter_user_id: str) -> PromoterUserHistoryResponse:
        query = "SELECT * FROM referral_program WHERE promoter_user_id=%s;"
        values = (promoter_user_id,)
        response = self.db.query(query, values, fetch_all=True)
        if response:
            referrals = [ReferralProgram(**referral) for referral in response]
            return PromoterUserHistoryResponse(referrals=referrals)
        return PromoterUserHistoryResponse(referrals=[])

    def create_referral_transactions(self, referral_code: str, amount: float) -> None:
        try:
            query = 'INSERT INTO referral_transactions (referral_code, amount) VALUES (%s, %s);'
            values = (referral_code, amount)
            self.db.execute(query, values)
        except Exception:
            raise AddingTransactionBonusError(f'Adding Amount to referral_code fail: {referral_code}')

    def get_referred_record(self, referred_user_id: str) -> ReferralProgram | None:
        query = "SELECT * FROM referral_program WHERE referred_user_id=%s;"
        values = (referred_user_id,)
        response = self.db.query(query, values, fetch_all=False)
        if response:
            return ReferralProgram(**response)

    def update_referred_record(self, referral_code: str, total_rewards: float, total_deposits: int) -> None:
        query = ("UPDATE referral_program "
                 "SET total_rewards=%s, total_deposits=%s "
                 "WHERE referral_code=%s;")
        values = (total_rewards, total_deposits, referral_code)
        self.db.execute(query, values)
