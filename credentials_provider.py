from typing import Optional, Dict

from dotenv import dotenv_values
from pydantic import BaseModel


class _CredentialsProvider(BaseModel):
    env: Dict[str, Optional[str]] = dotenv_values(".env")

    @property
    def user(self) -> str:
        return self.env.get('MY_SQL_USER')

    @property
    def password(self) -> str:
        return self.env.get('MY_SQL_PASSWORD')

    @property
    def secret(self) -> str:
        return self.env.get('SECRET')

    @property
    def slack_token(self) -> str:
        return self.env.get('slack_token')

    @property
    def slack_log_chanel(self) -> str:
        return self.env.get('slack_log_chanel')


credentials_provider = _CredentialsProvider()
