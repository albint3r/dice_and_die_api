from fastapi import FastAPI

from app.routes.game import game
from app.routes.auth import auth

app = FastAPI()

app.include_router(game.router)
app.include_router(auth.router)
