# app/decorators.py
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from functools import wraps

# -----------------------------
# Logging Configuration
# -----------------------------
# Configure the basic logging system. This will print INFO level logs to console.
# You can later configure it to log to a file if needed.
logging.basicConfig(level=logging.INFO)

API_KEY = "my_secret_key"         # change this to secure value in production
# API_KEY_NAME: The name of the HTTP header that will carry the API key.
API_KEY_NAME = "x-api-key"        # header name used for authentication

# -----------------------------
# APIKeyHeader Dependency
# -----------------------------
# FastAPI provides built-in support for security dependencies.
# APIKeyHeader automatically extracts the API key from the specified header.
# auto_error=True means that if the header is missing, FastAPI automatically raises an error.

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# -----------------------------
# API Key Authentication Dependency
# -----------------------------
def api_key_auth(x_api_key: str = Depends(api_key_header)):
    """
    FastAPI dependency to enforce an API key header.
    Now integrated with Swagger UI "Authorize" button.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return True

# Logging decorator
# A decorator is a function that wraps another function to add extra behavior without changing the original function.
def log_action(func):
    @wraps(func)  # ✅ Important: keeps original signature for FastAPI & Swagger
    def wrapper(*args, **kwargs):
        print(f"Action: {func.__name__} called with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper


# def log_action(func):
#     """Decorator to log function calls (for internal debugging/logging)."""
#     def wrapper(*args, **kwargs):
#         logging.info(f"Executing {func.__name__}")
#         return func(*args, **kwargs)
#     return wrapper
