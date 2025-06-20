from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api import router as api_router

app = FastAPI(title="Recipe Card Builder")

app.mount("/api", api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
