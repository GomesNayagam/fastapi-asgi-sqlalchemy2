import json
import logging
from typing import Any, Callable, Coroutine
import time

import jwt
import requests
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import settings


EXPECTED_AUDIENCE = settings.expected_audience
EXPECTED_ISSUER = settings.expected_issuer
JWKS_URI = settings.jwks_uri

logger = logging.getLogger("Middleware")


class LogTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> Response:
        """
        Add API process time in response headers and log calls
        """
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = str(round(time.time() - start_time, 3))
        response.headers["X-Process-Time"] = process_time

        logger.info(
            "Method=%s Path=%s StatusCode=%s ProcessTime=%s",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware for handling content-type of JavaScript files and serving
    index.html as a fallback for other requests.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> Response:
        """
        Process the request and set the content-type header for JavaScript files or
        serve the index.html file as a fallback for other requests.

        Args:
            request (Request): The incoming request.
            call_next (Callable): The next middleware or handler in the stack.

        Returns:
            Response: The generated response.
        """
        logger.debug(f"Request URL path: {request.url.path}")
        if request.url.path.startswith("/api"):
            try:
                if "Authorization" not in request.headers:
                    return error_response("Unauthorized", 401)
                token_header = request.headers["Authorization"]
                if token_header.startswith("Bearer "):
                    token = token_header.split("Bearer ")[-1]
                    if not validate_token(token):
                        return error_response("Unauthorized", 401)
                else:
                    return error_response("Token should begin with Bearer", 400)
            except Exception as e:
                return error_response(f"{e}", 400)
            response = await call_next(request)
            return response

        response = await call_next(request)
        return response


def error_response(error_msg: str, status_code: int) -> JSONResponse:
    """
    Logs the error message and returns a JSONResponse with the error message.

    Args:
        error_msg (str): the error message to be logged and returned in the JSONResponse
        status_code (int): the HTTP status code

    Returns:
        JSONResponse: JSONResponse containing the error message
    """
    logger.error(error_msg)
    return JSONResponse(
        content={"error": {"message": error_msg}},
        status_code=status_code,
    )


def validate_token(token: str) -> bool:
    """
    Validate a JWT token using the Azure AD JWKS endpoint.

    Args:
        token (str): The JWT token to be validated.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    jwks_uri = JWKS_URI

    jwks = json.loads(requests.get(jwks_uri).text)
    header = jwt.get_unverified_header(token)

    signing_key = None
    for key in jwks["keys"]:
        if key["kid"] == header["kid"]:
            signing_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            break

    if not signing_key:
        return False

    try:
        jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
        )
        return True
    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        return False
