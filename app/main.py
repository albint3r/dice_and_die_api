from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from app.logs.exception_handlers import (request_validation_exception_handler, http_exception_handler,
                                         unhandled_exception_handler)
from app.logs.middleware import log_request_middleware
from app.routes.auth import auth
from app.routes.game import game
from app.routes.lobby import lobby

app = FastAPI()
# Logs
app.middleware("http")(log_request_middleware)
# This show General Error in the app
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
# Routes
app.include_router(auth.router)
app.include_router(game.router)
app.include_router(lobby.router)
