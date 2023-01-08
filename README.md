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

This package provides classes and decorators to use FastAPI with class based routing in Python 3.8. This allows you to construct an instance of a class and have methods of that instance be route handlers for FastAPI.

**Note**: This package does not support async routes with Python versions less than 3.8 due to bugs in [`inspect.iscoroutinefunction`](https://stackoverflow.com/a/52422903/1431244). Specifically, with older versions of Python `iscoroutinefunction` incorrectly returns false so async routes are not awaited. As a result, this package only supports Python versions >= 3.8.

To get started, install the package using pip:

```sh
pip install fastapi-class
```

### Example

let's imagine that this code is part of a system that manages a list of users. The `Dao` class represents a Data Access Object, which is responsible for storing and retrieving user data from a database.

The `UserRoutes` class is responsible for defining the routes (i.e., the URL paths) that users can access to perform various actions on the user data.

Here's how the code could be used in a real world scenario:

```py
import argparse

from dao import Dao
from fastapi import FastAPI

from fastapi_class.decorators import delete, get
from fastapi_class.routable import Routable


def parse_arg() -> argparse.Namespace:
    """parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Example of FastAPI class based routing."
    )
    parser.add_argument("--url", type=str, help="URL to connect to.")
    parser.add_argument("--user", type=str, help="User to connect with.")
    parser.add_argument("--password", type=str, help="Password to connect with.")
    return parser.parse_args()


class UserRoutes(Routable):
    """Inherits from Routable."""

    # Note injection here by simply passing values to the constructor. Other injection frameworks also
    # supported as there's nothing special about this __init__ method.
    def __init__(self, dao: Dao) -> None:
        """Constructor. The Dao is injected here."""
        super().__init__()
        self.__dao = Dao

    @get("/user/{name}")
    def get_user_by_name(self, name: str) -> str:
        # Use our injected DAO instance.
        return self.__dao.get_user_by_name(name)

    @delete("/user/{name}")
    def delete_user(self, name: str) -> None:
        self.__dao.delete(name)


def main():
    args = parse_arg()
    # Configure the DAO per command line arguments
    dao = Dao(args.url, args.user, args.password)
    # Simple intuitive injection
    user_routes = UserRoutes(dao)
    app = FastAPI()
    # router member inherited from cr.Routable and configured per the annotations.
    app.include_router(user_routes.router)
```

## Explanation

FastAPI generally has one define routes like:

```py
from fastapi import FastAPI

app = FastAPI()

@app.get('/echo/{x}')
def echo(x: int) -> int:
   return x
```

**Note**: that `app` is a global. Furthermore, [FastAPI's suggested way of doing dependency injection](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/) is handy for things like pulling values out of header in the HTTP request. However, they don't work well for more standard dependency injection scenarios where we'd like to do something like inject a Data Access Object or database connection. For that, FastAPI suggests [their parameterized dependencies](https://fastapi.tiangolo.com/advanced/advanced-dependencies/) which might look something like:

```py
from fastapi import FastAPI

app = FastAPI()

class ValueToInject:
   # Value to inject into the function.
   def __init__(self, y: int) -> None:
      self.y = y

   def __call__(self) -> int:
      return self.y

to_add = ValueToInject(2)

@app.get('/add/{x}')
def add(x: int, y: Depends(to_add)) -> int:
   return x + y
```

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

> Note: You can also generate a coverage report with:

```bash
bash scripts/test_html.sh
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
