from fastapi import FastAPI

from .routers import buses_router

app = FastAPI()
app.include_router(buses_router)
