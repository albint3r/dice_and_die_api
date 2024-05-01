from app.domain.referral_program.errors.errors import ReferredUserAlreadyExistError
from app.domain.referral_program.schemas.response import PromoterUserHistoryResponse
from app.domain.referral_program.use_cases.i_referral_program_repository import IReferralProgramRepository
from app.domain.referral_program.use_cases.i_referral_program_use_case import IReferralProgramUseCase


class ReferralProgramUseCase(IReferralProgramUseCase):
    """This class handles the referral system"""
    repo: IReferralProgramRepository
    _bonus_percentage: float = 0.30

    def create_referral_program_from_promoter(self, promoter_user_id: str, referred_user_id: str) -> None:
        if self.repo.can_user_be_referred(referred_user_id):
            self.repo.create_referral_program_from_promoter(promoter_user_id, referred_user_id)
            return
        raise ReferredUserAlreadyExistError(
            f'Can add reference because referred user id:{referred_user_id} already exist.')

    def get_promoter_user_history(self, promoter_user_id: str) -> PromoterUserHistoryResponse:
        return self.repo.get_promoter_user_history(promoter_user_id)

    def create_referral_transactions(self, referred_user_id: str, amount: float) -> None:
        referral_record = self.repo.get_referred_record(referred_user_id)
        # First We need to create a transaction history to track each movement of the user.
        # After this is importan to update the values of the total to have quick access in the front.
        if referral_record:
            bonus_amount = amount * self._bonus_percentage  # noqa
            self.repo.create_referral_transactions(str(referral_record.referral_code), bonus_amount)
            # Update the curren date in the record of the amount and count operations.
            referral_record.total_rewards = bonus_amount + referral_record.total_rewards
            referral_record.total_deposits += 1
            self.repo.update_referred_record(str(referral_record.referral_code),
                                             referral_record.total_rewards,
                                             referral_record.total_deposits)
