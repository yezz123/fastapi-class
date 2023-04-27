from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, Field, PyObject


class APISettings(BaseSettings):
    """
    API settings.

    This class is used to configure the API.
    """

    debug: bool = Field(False, env="DEBUG")
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI"
    version: str = "0.1.0"

    disable_docs: bool = Field(False, env="DISABLE_DOCS")

    enable_error_handlers: bool = Field(True, env="ERROR_HANDLERS_ENABLE")
    healthcheck: Optional[PyObject] = None
    side_services: List[PyObject] = []
    openapi_ids: bool = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        """
        FastAPI kwargs return a dictionary of the most commonly used keyword arguments when initializing a FastAPI instance.

        If `self.disable_docs` is True, the various docs-related arguments are disabled, preventing your spec from being published.
        """
        fastapi_kwargs = {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
        if self.disable_docs:
            fastapi_kwargs.update(
                {"docs_url": None, "openapi_url": None, "redoc_url": None}
            )
        return fastapi_kwargs

    @property
    def config_kwargs(self) -> Dict[str, Any]:
        """
        This Config Kwargs add the following settings to your FastAPI instance:

        - `enable_error_handlers`: Enable error handlers.
        - `healthcheck`: Healthcheck endpoint
        - `side_services`: Side services
        - `openapi_ids`: Simplify operation IDs so that generated clients have simpler api function names
        """
        return {
            "enable_error_handlers": self.enable_error_handlers,
            "healthcheck": self.healthcheck,
            "side_services": self.side_services,
            "simplify_openapi_ids": self.openapi_ids,
        }

    class Config:
        """API settings config."""

        validate_assignment = True
