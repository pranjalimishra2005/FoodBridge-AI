from fastapi import FastAPI

app = FastAPI(
    title="FoodBridge AI API",
    version="1.0.0"
)

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "FoodBridge API"
    }