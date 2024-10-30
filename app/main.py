from fastapi import FastAPI

from .dependencies import init_db
from .routers import buses_router, realtime_router, schedule_router, stops_router

init_db()

app = FastAPI()
app.include_router(buses_router)
app.include_router(stops_router)
app.include_router(realtime_router)
app.include_router(schedule_router)
