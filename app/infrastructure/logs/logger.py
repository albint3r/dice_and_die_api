import logging
import sys
from typing import Union, Final

from fastapi import Request, status
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response

from app.domain.logs.i_logger_configurator import ILoggerConfigurator
from app.infrastructure.logs.slack_bot import slack_bot


# For more information about the implementation check this blog post link
# https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983
# This is other article to set the below configs:
# https://www.codeschat.com/article/145.html

class LoggerConfigurator(ILoggerConfigurator):

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def set_up(self) -> None:
        """Initialize all the configuration of the logger."""
        # Disable uvicorn access logger
        uvicorn_access = logging.getLogger("uvicorn.access")
        uvicorn_access.disabled = True
        # Create Logger
        self._logger = logging.getLogger("uvicorn")
        self._logger.setLevel(logging.getLevelName(logging.INFO))
        # Set Server Configuration Format
        fh = logging.FileHandler(filename=self._storage_file_path)
        formatter = logging.Formatter(self._log_format)
        fh.setFormatter(formatter)
        self._logger.addHandler(fh)  # Exporting logs to a file

    async def handle_request_validation_exception(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        This is a wrapper to the default RequestValidationException handler of FastAPI.
        This function will be called when client input is not valid.
        """
        self._logger.debug("Our custom [request_validation_exception_handler] was called")
        body = await request.body()
        query_params = request.query_params._dict  # noqa
        detail = {"errors": exc.errors(), "body": body.decode(), "query_params": query_params}
        self._logger.info(detail)
        return await _request_validation_exception_handler(request, exc)

    async def handle_http_exception(self, request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
        """
        This middleware will log all unhandled exceptions.
        Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
        """
        self._logger.debug("Our custom [http_exception_handler] was called")
        host = getattr(getattr(request, "client", None), "host", None)
        port = getattr(getattr(request, "client", None), "port", None)
        url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
        exception_type, exception_value, _ = sys.exc_info()
        exception_name = getattr(exception_type, "__name__", None)
        log_msg = f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error => [{exception_name}: {exception_value.detail}]'
        self._logger.error(log_msg)
        self.storage_logger.store_log_msg(log_msg)
        return await _http_exception_handler(request, exc)

    async def handle_unhandled_exception(self, request: Request, exc: Exception) -> PlainTextResponse:
        """
        Handle unhandled exception.
        """
        self._logger.debug("Our custom [unhandled_exception_handler] was called")
        host = getattr(getattr(request, "client", None), "host", None)
        port = getattr(getattr(request, "client", None), "port", None)
        url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
        exception_type, exception_value, _ = sys.exc_info()
        exception_name = getattr(exception_type, "__name__", None)
        log_msg = f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error => [{exception_name}: {exception_value}]'
        self._logger.error(log_msg)
        self.storage_logger.store_log_msg(log_msg)
        return PlainTextResponse(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


logger_conf: Final[LoggerConfigurator] = LoggerConfigurator(storage_logger=slack_bot)
logger_conf.set_up()
