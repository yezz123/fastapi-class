![Class](https://user-images.githubusercontent.com/52716203/137606695-f110f129-08b1-45f3-a445-962c1f28378c.png)

<p align="center">
    <em>Classes and Decorators to use FastAPI with Class based routing</em>
</p>

<p align="center">
<a href="https://github.com/yezz123/fastapi-class/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/yezz123/fastapi-class/actions/workflows/test.yml/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/yezz123/fastapi-class">
    <img src="https://codecov.io/gh/yezz123/fastapi-class/branch/main/graph/badge.svg"/>
</a>
<a href="https://pypi.org/project/fastapi-class" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi-class?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi-class" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi-class.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Source Code**: <https://github.com/yezz123/fastapi-class>

**Install the project**: `pip install fastapi-class`

---

As you create more complex FastAPI applications, you may find yourself frequently repeating the same dependencies in multiple related endpoints.

A common question people have as they become more comfortable with FastAPI is how they can reduce the number of times they have to copy/paste the same dependency into related routes.

`fastapi_class` provides a `class-based view` decorator `@View` to help reduce the amount of boilerplate necessary when developing related routes.

> Highly inspired by [Fastapi-utils](https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/), Thanks to [@dmontagu](https://github.com/dmontagu) for the great work.

- Example:

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
    def post(self, item: ItemModel):
        return item

    def get(self, item_id: int = Query(..., gt=0)):
        return {"item_id": item_id}

app.include_router(router)
```

### Response model 📦

`Exception` in list need to be either function that return `fastapi.HTTPException` itself. In case of a function it is required to have all of it's arguments to be `optional`.

```py
from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from fastapi_class import View

app = FastAPI()
router = APIRouter()

NOT_AUTHORIZED = HTTPException(401, "Not authorized.")
NOT_ALLOWED = HTTPException(405, "Method not allowed.")
NOT_FOUND  = lambda item_id="item_id": HTTPException(404, f"Item with {item_id} not found.")

class ItemResponse(BaseModel):
    field: str | None = None

@view(router)
class MyView:
    exceptions = {
        "__all__": [NOT_AUTHORIZED],
        "put": [NOT_ALLOWED, NOT_FOUND]
    }

    RESPONSE_MODEL = {
        "put": ItemResponse
    }

    RESPONSE_CLASS = {
        "delete": PlainTextResponse
    }

    def get(self):
        ...
    def put(self):
        ...
    def delete(self):
        ...

app.include_router(router)
```

### Customized Endpoints

```py
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from fastapi_class import View, endpoint

app = FastAPI()
router = APIRouter()

NOT_AUTHORIZED = HTTPException(401, "Not authorized.")
NOT_ALLOWED = HTTPException(405, "Method not allowed.")
NOT_FOUND  = lambda item_id="item_id": HTTPException(404, f"Item with {item_id} not found.")
EXCEPTION = HTTPException(400, "Example.")

class UserResponse(BaseModel):
    field: str | None = None

@View(router)
class MyView:
    exceptions = {
        "__all__": [NOT_AUTHORIZED],
        "put": [NOT_ALLOWED, NOT_FOUND],
        "edit": [EXCEPTION]
    }

    RESPONSE_MODEL = {
        "put": UserResponse,
        "edit": UserResponse
    }

    RESPONSE_CLASS = {
        "delete": PlainTextResponse
    }

    def get(self):
        ...
    def put(self):
        ...
    def delete(self):
        ...
    @endpoint(("PUT",), path="edit")
    def edit(self):
        ...
```

**Note:** The `edit()` endpoint is decorated with the `@endpoint(("PUT",), path="edit")` decorator, which specifies that this endpoint should handle `PUT` requests to the `/edit` path.

## Development 🚧

### Setup environment 📦

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
# Install dependencies
pip install -e .[test,lint]
```

### Run tests 🌝

You can run all the tests with:

```bash
bash scripts/test.sh
```

### Format the code 🍂

Execute the following command to apply `pre-commit` formatting:

```bash
bash scripts/format.sh
```

Execute the following command to apply `mypy` type checking:

```bash
bash scripts/lint.sh
```

## License

This project is licensed under the terms of the MIT license.
