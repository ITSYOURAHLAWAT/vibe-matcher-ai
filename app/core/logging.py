import logging
import sys
from pythonjsonlogger import jsonlogger
from app.core.config import settings

def setup_logging():
    """
    Configures structured JSON logging for the application.
    """
    logger = logging.getLogger()
    
    # Clear existing handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)
        
    handler = logging.StreamHandler(sys.stdout)
    
    if settings.DEBUG_MODE:
        logger.setLevel(logging.DEBUG)
        # Use simple formatting for debug mode for readability, or keep JSON
        # For this requirement, "Structured Logging" implies JSON even in debug usually, 
        # but let's stick to JSON for consistency.
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
    else:
        logger.setLevel(logging.INFO)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Set log levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    
    return logger
