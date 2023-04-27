"""
As you create more complex FastAPI applications, you may find yourself frequently repeating the same dependencies in multiple related endpoints.

A common question people have as they become more comfortable with FastAPI is how they can reduce the number of times they have to copy/paste the same dependency into related routes.

Inspired by the `class-based view` in [Fastapi-utils](https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/).

"""


__version__ = "3.3.0"

from .config import configure_app
from .errors import (
    APIError,
    ConflictAPIError,
    ErrorDetails,
    NotFoundAPIError,
    ServiceUnavailableAPIError,
    errors,
)
from .healthcheck import HealthCheck
from .response import JsonResponse
from .routers import ViewRouter, register_view
from .serializer import PydanticSerializer

__all__ = [
    "__version__",
    "configure_app",
    "APIError",
    "ConflictAPIError",
    "ErrorDetails",
    "NotFoundAPIError",
    "ServiceUnavailableAPIError",
    "errors",
    "JsonResponse",
    "ViewRouter",
    "register_view",
    "PydanticSerializer",
    "HealthCheck",
]
