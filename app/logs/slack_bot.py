from pydantic import BaseModel, validate_call
from slack import WebClient
from slack.errors import SlackApiError

from credentials_provider import credentials_provider


class _SlackBot(BaseModel):
    slack_token: str
    slack_chanel: str

    def post_msg(self, message: str) -> None:
        """Post Error Message in Slack Tobe Total"""
        client = WebClient(token=self.slack_token)

        try:
            client.chat_postMessage(channel=self.slack_chanel, text=message)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'


slack_bot = _SlackBot(slack_token=credentials_provider.slack_token, slack_chanel=credentials_provider.slack_chanel)
