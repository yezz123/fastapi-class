![Class](https://user-images.githubusercontent.com/52716203/137606695-f110f129-08b1-45f3-a445-962c1f28378c.png)

<p align="center">
    <em>Classes and Decorators to use FastAPI with Class based routing</em>
</p>

<p align="center">
<a href="https://github.com/yezz123/fastapi-class/actions/workflows/ci.yml" target="_blank">
    <img src="https://github.com/yezz123/fastapi-class/actions/workflows/ci.yml/badge.svg" alt="Continuous Integration">
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
<a href="https://pepy.tech/project/fastapi_class" target="_blank">
    <img src="https://static.pepy.tech/badge/fastapi_class" alt="Test">
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
from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi_class import View

app = FastAPI()

class ItemModel(BaseModel):
    id: int
    name: str
    description: str = None

@View(app)
class ItemView:
    async def post(self, item: ItemModel):
        return item

    async def get(self, item_id: int = Query(..., gt=0)):
        return {"item_id": item_id}

```

### Response model 📦

`Exception` in list need to be either function that return `fastapi.HTTPException` itself. In case of a function it is required to have all of it's arguments to be `optional`.

```py
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from fastapi_class import View

app = FastAPI()

NOT_AUTHORIZED = HTTPException(401, "Not authorized.")
NOT_ALLOWED = HTTPException(405, "Method not allowed.")
NOT_FOUND = lambda item_id="item_id": HTTPException(404, f"Item with {item_id} not found.")

class ItemResponse(BaseModel):
    field: str | None = None

@View(app)
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

    async def get(self):
        ...

    async def put(self):
        ...

    async def delete(self):
        ...
```

### Customized Endpoints

```py
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from fastapi_class import View, endpoint

app = FastAPI()

NOT_AUTHORIZED = HTTPException(401, "Not authorized.")
NOT_ALLOWED = HTTPException(405, "Method not allowed.")
NOT_FOUND = lambda item_id="item_id": HTTPException(404, f"Item with {item_id} not found.")
EXCEPTION = HTTPException(400, "Example.")

class UserResponse(BaseModel):
    field: str | None = None

@View(app)
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

    async def get(self):
        ...

    async def put(self):
        ...

    async def delete(self):
        ...

    @endpoint(("PUT"), path="edit")
    async def edit(self):
        ...
```

**Note:** The `edit()` endpoint is decorated with the `@endpoint(("PUT",), path="edit")` decorator, which specifies that this endpoint should handle `PUT` requests to the `/edit` path,
using `@endpoint("PUT", path="edit")` has the same effect

## Development 🚧

### Setup environment 📦

__Note:__ You should have `uv` installed, if not you can install it with:

```bash
pip install uv
```

Then you can install the dependencies with:

```bash
# Install dependencies
uv sync --all-extras
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
