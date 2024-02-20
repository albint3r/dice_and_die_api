import sys
from typing import Union

from fastapi import Request, status
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response

from app.logs.logger import logger
from app.logs.slack_bot import slack_bot


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.
    This function will be called when client input is not valid.
    """
    logger.debug("Our custom [request_validation_exception_handler] was called")
    body = await request.body()
    query_params = request.query_params._dict  # noqa
    detail = {"errors": exc.errors(), "body": body.decode(), "query_params": query_params}
    logger.info(detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    logger.debug("Our custom [http_exception_handler] was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    log_msg = f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error => [{exception_name}: {exception_value.detail}]'
    logger.error(log_msg)
    # Log Fatal Error to [Slack Logs] Channel
    slack_bot.post_msg(log_msg)
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    logger.debug("Our custom [unhandled_exception_handler] was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    log_msg = f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error => [{exception_name}: {exception_value}]'
    logger.error(log_msg)
    # Log Fatal Error to [Slack Logs] Channel
    slack_bot.post_msg(log_msg)
    return PlainTextResponse(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
