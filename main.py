#!/usr/bin/env python3
"""
Main entry point for the Travel Planner API.
Run this file to start the FastAPI server.
"""

import uvicorn
from travel_planner.config import logger

if __name__ == "__main__":
    logger.info("Starting Travel Planning API server")
    uvicorn.run("travel_planner.api:app", host="0.0.0.0", port=8000, reload=True)
