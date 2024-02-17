from fastapi import FastAPI

from app.routes.game import game

app = FastAPI()

app.include_router(game.router)
