from fastapi import FastAPI
from src.routes.game import game
from src.routes.waiting_room import waiting_room

app = FastAPI()

app.include_router(waiting_room.router)
app.include_router(game.router)
