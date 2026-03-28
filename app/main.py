from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.analytics import router as analytics_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(analytics_router)