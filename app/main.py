from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from app.infrastructure.logs.logger import logger_conf
from app.infrastructure.logs.middleware import log_request_middleware
from app.routes.auth import auth
from app.routes.game import game
from app.routes.lobby import lobby

app = FastAPI()
# Logs
app.middleware("http")(log_request_middleware)
# This show General Error in the app
app.add_exception_handler(RequestValidationError, logger_conf.handle_request_validation_exception)
app.add_exception_handler(HTTPException, logger_conf.handle_http_exception)
app.add_exception_handler(Exception, logger_conf.handle_unhandled_exception)
# Routes
app.include_router(auth.router)
app.include_router(game.router)
app.include_router(lobby.router)
