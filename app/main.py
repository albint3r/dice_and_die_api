import firebase_admin
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException, WebSocketException
from firebase_admin import credentials

from app.infrastructure.logs.logger import logger_conf
from app.infrastructure.logs.middleware import log_request_middleware
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import auth
from app.routes.game import game
from app.routes.lobby import lobby
from app.routes.analytics import analytics

app = FastAPI()
cred = credentials.Certificate('dice-n-die-5a5d411f3e82.json')
firebase_admin.initialize_app(cred)

# Logs
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
app.include_router(analytics.router)
