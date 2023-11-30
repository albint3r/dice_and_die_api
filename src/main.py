from fastapi import FastAPI
from src.routes.game import game

app = FastAPI()

app.include_router(game.router)
