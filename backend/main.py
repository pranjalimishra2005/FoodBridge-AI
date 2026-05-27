from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.database import init_db
from backend.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting FoodBridge AI Backend...")

    await init_db()

    print("Database connected successfully")

    yield

    # Shutdown
    print("Shutting down FoodBridge AI Backend...")


app = FastAPI(
    title="FoodBridge AI API",
    description="AI-powered food donation and distribution platform",
    version="1.0.0",
    lifespan=lifespan,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root Route
@app.get("/")
async def root():
    return {
        "message": "FoodBridge AI API running successfully"
    }


# Public Health Route
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Server is healthy"
    }


# Routers
app.include_router(
    auth_router,
    tags=["Authentication"],
)

from backend.routers import donations

app.include_router(donations.router)
