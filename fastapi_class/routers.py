from fastapi import APIRouter

from .views.api import View


def register_view(router: APIRouter, view: View, prefix: str = ""):
    """Register a view."""
    for route_params in view.get_api_actions(prefix):
        router.add_api_route(**route_params)


class ViewRouter(APIRouter):
    """View router."""

    register_view = register_view
