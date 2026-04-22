from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.analytics import router as analytics_router
from app.routes.predict import router as predict_router

app = FastAPI(title="E-WASP Early Warning System")

app.include_router(upload_router)
app.include_router(analytics_router)
app.include_router(predict_router)