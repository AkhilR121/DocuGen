#!/usr/bin/env python
"""
Entry point script for running the FastAPI server.
Usage: python run.py --env local|dev|prod
"""
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
