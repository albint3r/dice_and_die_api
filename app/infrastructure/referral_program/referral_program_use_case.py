from app.domain.referral_program.errors.errors import ReferredUserAlreadyExistError
from app.domain.referral_program.use_cases.i_referral_program_repository import IReferralProgramRepository
from app.domain.referral_program.use_cases.i_referral_program_use_case import IReferralProgramUseCase


class ReferralProgramUseCase(IReferralProgramUseCase):
    """This class handles the referral system"""
    repo: IReferralProgramRepository

    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str):
        if self.repo.can_user_be_referred(referred_user_id):
            self.repo.create_referral_program_from_promoter(promoter_user_id, referred_user_id)
            return
        raise ReferredUserAlreadyExistError(
            f'Can add reference because referred user id:{referred_user_id} already exist.')

    def create_referral_transactions(self, referred_user_id: str, amount: float):
        pass

    def get_promoter_user_history(self, promoter_user_id: str):
        pass