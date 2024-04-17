from contextlib import asynccontextmanager
from typing import Any, Callable, TypeVar

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.core.middleware import AuthMiddleware, LogTimeMiddleware
from app.api.routers.routes import api_router
from app.config import settings
from app.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

app = FastAPI(
    lifespan=lifespan,
    title="FastAPI ASGI Setup",
    description="template playbook with asgi.",
    version="1.0.0",
    docs_url="/",
    root_path=settings.root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
    ],
)


if settings.auth_check is True:
    app.add_middleware(AuthMiddleware)

app.add_middleware(LogTimeMiddleware)

F = TypeVar("F", bound=Callable[..., Any])


# @app.middleware("http")
# async def time_log_middleware(request: Request, call_next: F) -> Response:
#     """
#     Add API process time in response headers and log calls
#     """
#     start_time = time.time()
#     response: Response = await call_next(request)
#     process_time = str(round(time.time() - start_time, 3))
#     response.headers["X-Process-Time"] = process_time

#     logger.info(
#         "Method=%s Path=%s StatusCode=%s ProcessTime=%s",
#         request.method,
#         request.url.path,
#         response.status_code,
#         process_time,
#     )

#     return response


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
