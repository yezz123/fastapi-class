from __future__ import annotations

import asyncio
from typing import Any, Callable

from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from .errors import ServiceUnavailableAPIError
from .response import JsonResponse


class HealthCheck:
    """
    Group of functions that perform basic health checks of the application

    Health checks are executed on the /health endpoint.
    """

    def __init__(
        self,
        endpoint: str = "/health",
        checks: list[Callable[[], Any]] | None = None,
        response_class=JsonResponse,
    ):
        """
        :param endpoint: healthcheck endpoint
        :param checks: list of functions that perform health checks
        :param response_class: response class
        """
        self.endpoint = endpoint
        self.response_class = response_class
        self.checks = checks or []

    def add_check(self, func):
        """Add a health check function."""
        self.checks.append(func)

    def register(self):
        """Decorator to register a health check function."""

        def wrapper(func):
            """Wrapper function."""
            self.add_check(func)
            return func

        return wrapper

    async def get_endpoint(self):
        """Get healthcheck endpoint."""
        failed = False
        task = asyncio.gather(*[t() for t in self.checks], return_exceptions=True)
        try:
            results = await asyncio.wait_for(task, timeout=10)
            if any(isinstance(r, Exception) for r in results):
                failed = True
        except asyncio.TimeoutError:
            failed = True
        finally:
            if failed:
                return self.response_class(
                    content=ServiceUnavailableAPIError(
                        detail="Service health check failed"
                    ).dict(),
                    status_code=HTTP_503_SERVICE_UNAVAILABLE,
                )
            return self.response_class(
                content={"status": "ok"}, status_code=HTTP_200_OK
            )
