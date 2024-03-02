from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException, WebSocketException

from app.infrastructure.lobby.lobby_websocket_manager import lobby_websocket_manager
from app.infrastructure.logs.logger import logger_conf
from app.infrastructure.logs.middleware import log_request_middleware
from app.routes.auth import auth
from app.routes.game import game
from app.routes.lobby import lobby

app = FastAPI()
# Logs
# app.add_event_handler("startup", lobby_websocket_manager.check_inactive_connections)
app.middleware("http")(log_request_middleware)
# This show General Error in the app
app.add_exception_handler(HTTPException, logger_conf.handle_http_exception)
app.add_exception_handler(WebSocketException, logger_conf.handle_websocket_exception)
app.add_exception_handler(RequestValidationError, logger_conf.handle_request_validation_exception)
app.add_exception_handler(Exception, logger_conf.handle_unhandled_exception)
# Routes
app.include_router(auth.router)
app.include_router(game.router)
app.include_router(lobby.router)
