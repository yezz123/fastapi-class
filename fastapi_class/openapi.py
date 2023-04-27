from fastapi import FastAPI
from fastapi.routing import APIRoute


def simplify_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated clients have simpler api function names

    Operation IDs are generated from the endpoint name and the HTTP method.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
