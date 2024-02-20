from fastapi import FastAPI

from app.routes.auth import auth
from app.routes.game import game
from app.routes.lobby import lobby

app = FastAPI()

app.include_router(auth.router)
app.include_router(game.router)
app.include_router(lobby.router)
