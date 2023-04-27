from __future__ import annotations

import asyncio
from typing import Sequence

from fastapi import FastAPI

from .errors import ServiceUnavailableAPIError, add_error_handlers
from .healthcheck import HealthCheck
from .openapi import simplify_ids
from .settings import APISettings
from .types import SideService


def add_services_app(app: FastAPI, services: Sequence[SideService]) -> None:
    """
    Add side services to the app.

    Side services are started on app startup and stopped on app shutdown.
    """

    @app.on_event("startup")
    async def start_side_services():
        """Start side services."""
        await asyncio.gather(*[s.start() for s in services])

    @app.on_event("shutdown")
    async def stop_side_services():
        """Stop side services."""
        await asyncio.gather(*[s.stop() for s in services])


def configure_app(
    app: FastAPI,
    enable_error_handlers: bool = True,
    healthcheck: HealthCheck | None = None,
    side_services: Sequence[SideService] | None = None,
    openapi_ids: bool = True,
):
    """
    Configure the app.

    :param app: FastAPI app
    :param enable_error_handlers: enable error handlers
    :param healthcheck: healthcheck instance
    :param side_services: side services
    :param openapi_ids: simplify OpenAPI operation IDs
    """
    if enable_error_handlers:
        add_error_handlers(app)
    if healthcheck:
        app.add_api_route(
            methods=["GET"],
            path=healthcheck.endpoint,
            endpoint=healthcheck.get_endpoint,
            responses={503: {"model": ServiceUnavailableAPIError}},
        )
    if side_services:
        add_services_app(app, side_services)
    if openapi_ids:
        simplify_ids(app)


def create_fastapi_app(settings: APISettings, **kwargs) -> FastAPI:
    """
    Create a FastAPI app.

    :param settings: API settings
    :param kwargs: additional FastAPI kwargs
    :return: FastAPI app
    """
    app = FastAPI(**settings.fastapi_kwargs, **kwargs)
    configure_app(app, **settings.config_kwargs)
    return app


def create_fastapi_from_env(**kwargs):
    """
    Create a FastAPI app from environment variables.

    :param kwargs: additional FastAPI kwargs
    :return: FastAPI app
    """
    settings = APISettings(**kwargs)
    return create_fastapi_app(settings)
