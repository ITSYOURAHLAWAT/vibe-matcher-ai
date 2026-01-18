from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.endpoints import router as api_router
from app.services.ingestion import IngestionPipeline
import logging
from contextlib import asynccontextmanager

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Application startup...")
    
    # Run ingestion if needed
    try:
        pipeline = IngestionPipeline()
        pipeline.run()
    except Exception as e:
        logger.error(f"Startup ingestion failed: {e}")
        
    yield
    
    # Shutdown logic
    logger.info("Application shutdown...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS
# For local development with Vite (usually port 5173)
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Vibe Matcher AI API is running"}
