"""
As you create more complex FastAPI applications, you may find yourself frequently repeating the same dependencies in multiple related endpoints.

A common question people have as they become more comfortable with FastAPI is how they can reduce the number of times they have to copy/paste the same dependency into related routes.

fastapi_class provides a `class-based view` decorator `@View` to help reduce the amount of boilerplate necessary when developing related routes.

Inspired by the `class-based view` in [Fastapi-utils](https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/).

- Example to kick things off:

```python
from fastapi import FastAPI, APIRouter, Query
from pydantic import BaseModel

from fastapi_class import View

app = FastAPI()
router = APIRouter()

class ItemModel(BaseModel):
    id: int
    name: str
    description: str = None


@View(router)
class ItemView:

    async def get(self, query: str = Query(), limit: int = 50, offset: int = 0):
        pass

    def post(self, user: ItemModel):
        pass
```

"""


__version__ = "3.1.0"

from fastapi_class.exceptions import (
    UNKNOWN_SERVER_ERROR_DETAIL,
    ExceptionAbstract,
    FormattedMessageException,
)
from fastapi_class.openapi import ExceptionModel, _exceptions_to_responses
from fastapi_class.routers import Metadata, Method, endpoint
from fastapi_class.views import View

__all__ = [
    "View",
    "endpoint",
    "Method",
    "Metadata",
    "FormattedMessageException",
    "UNKNOWN_SERVER_ERROR_DETAIL",
    "ExceptionAbstract",
    "ExceptionModel",
    "_exceptions_to_responses",
]
