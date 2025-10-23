"""Main FastAPI application for the GoldenCity Memo API.

This module configures and creates the FastAPI application instance
with all necessary middleware and route handlers.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings, setup_logging
from .routes import router

# Setup logging before creating the app
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting up GoldenCity Memo API")
    yield
    logger.info("Shutting down GoldenCity Memo API")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint.
    
    Returns:
        API information and version
    """
    logger.info("Health check endpoint accessed")
    return {
        "message": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "healthy"
    }
