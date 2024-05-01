from app.domain.referral_program.errors.errors import ReferredUserAlreadyExistError
from app.domain.referral_program.use_cases.i_referral_program_repository import IReferralProgramRepository
from app.domain.referral_program.use_cases.i_referral_program_use_case import IReferralProgramUseCase


class ReferralProgramUseCase(IReferralProgramUseCase):
    """This class handles the referral system"""
    repo: IReferralProgramRepository
    _bonus_percentage: float = 0.30

    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str):
        if self.repo.can_user_be_referred(referred_user_id):
            self.repo.create_referral_program_from_promoter(promoter_user_id, referred_user_id)
            return
        raise ReferredUserAlreadyExistError(
            f'Can add reference because referred user id:{referred_user_id} already exist.')

    def create_referral_transactions(self, referral_code: str, amount: float):
        referral_record = self.repo.get_referred_record(referral_code)
        if referral_record:
            bonus_amount = amount * self._bonus_percentage  # noqa
            self.repo.create_referral_transactions(referral_record.referral_code, bonus_amount)

    def get_promoter_user_history(self, promoter_user_id: str):
        return self.repo.get_promoter_user_history(promoter_user_id)
