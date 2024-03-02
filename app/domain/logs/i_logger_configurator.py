import logging
from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException, WebSocketRequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
from pydantic import BaseModel
from starlette.websockets import WebSocket

from app.domain.logs.i_log_storage_gateway import ILogStorageGateWay


# For more information about the implementation check this blog post link
# https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983
# This is other article to set the below configs:
# https://www.codeschat.com/article/145.html

class ILoggerConfigurator(BaseModel, ABC):
    storage_logger: ILogStorageGateWay
    _logger: logging.Logger
    _storage_file_path: str = './server.log'
    _log_format: str = "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)s - %(levelname)s - %(message)s"  # noqa

    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        """Logger"""

    def set_up(self, *args, **kwargs) -> None:
        """Initialize all the configuration of the logger."""

    @abstractmethod
    async def handle_request_validation_exception(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle Request Validators Errors Exceptions logger."""

    @abstractmethod
    async def handle_websocket_exception(self, websocket: WebSocket, exc: WebSocketRequestValidationError):
        """Handle WebSocket Exceptions logger."""

    @abstractmethod
    async def handle_http_exception(self, request: Request, exc: HTTPException) -> JSONResponse | Response:
        """Handle HTTP Exceptions logger."""

    @abstractmethod
    async def handle_unhandled_exception(self, request: Request, exc: Exception) -> PlainTextResponse:
        """Handle General Exception."""

    @abstractmethod
    async def log_inactive_connections(self, user_id: str) -> None:
        """Get the log of the cleaned inactive connections."""

    @abstractmethod
    def log_send_websocket_json(self, *args, **kwargs) -> None:
        """Log the error in when can send json."""
