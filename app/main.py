from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "E-WASP Phase 1 Running"}