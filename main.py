from fastapi import FastAPI
from routers.player import player_api

from db.session import engine, metadata

print('Creating tables')
metadata.create_all(bind=engine)

app = FastAPI(redoc_url=None)

app.include_router(player_api.router)
