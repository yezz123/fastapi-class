# Fastapi-Class 🦜

![Class](https://user-images.githubusercontent.com/52716203/137606695-f110f129-08b1-45f3-a445-962c1f28378c.png)

<p align="center">
    <em>Classes and Decorators to use FastAPI with Class based routing</em>
</p>

[![codecov](https://codecov.io/gh/yezz123/fastapi-class/branch/main/graph/badge.svg?token=1W73kO30IL)](https://codecov.io/gh/yezz123/fastapi-class)
[![Testing](https://github.com/yezz123/fastapi-class/actions/workflows/test.yml/badge.svg)](https://github.com/yezz123/fastapi-class/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/fastapi-class.svg)](https://badge.fury.io/py/fastapi-class)
[![Downloads](https://pepy.tech/badge/fastapi-class/month)](https://pepy.tech/project/fastapi-class)
[![Downloads](https://pepy.tech/badge/fastapi-class/week)](https://pepy.tech/project/fastapi-class)
[![Language](https://img.shields.io/badge/Language-Python-green?style)](https://github.com/yezz123)
[![framework](https://img.shields.io/badge/Framework-FastAPI-blue?style)](https://fastapi.tiangolo.com/)
[![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flatcolor=BC4E99)](https://github.com/yezz123/fastapi-class)
[![Pypi](https://img.shields.io/pypi/pyversions/fastapi-class.svg?color=%2334D058)](https://pypi.org/project/fastapi-class)

---

**Source Code**: <https://github.com/yezz123/fastapi-class>

**Install the project**: `pip install fastapi-class`

---

Classes and Decorators to use FastAPI with `class based routing`. In particular this allows you to
construct an **instance** of a class and have methods of that instance be route handlers for FastAPI & Python 3.8.

- Older Versions of Python:
  - Unfortunately this does not work with `async` routes with Python versions less than 3.8 [due to bugs in `inspect.iscoroutinefunction`](https://stackoverflow.com/a/52422903/1431244). Specifically with older versions of Python `iscoroutinefunction` incorrectly returns false so `async` routes aren't `await`'d. We therefore only support Python versions >= 3.8.

## Example 🐢

```py
from ping import pong
# Some fictional ping pong class
from fastapi_class import Routable, get, delete

def parse_arg() -> argparse.Namespace:
   """parse command line arguments."""
   ...


class UserRoutes(Routable):
   """Inherits from Routable."""

   # Note injection here by simply passing values to the constructor.
   # Other injection frameworks also work.
   # supported as there's nothing special about this __init__ method.
   def __init__(self, pong: pong) -> None:
      """Constructor. The pong is injected here."""
      self.__pong = pong

   @get('/user/{name}')
   def get_user_by_name(name: str) -> User:
      # Use our injected pong instance.
      return self.__pong.get_user_by_name(name)

   @delete('/user/{name}')
   def delete_user(name: str) -> None:
      self.__pong.delete(name)


def main():
    args = parse_args()
    # Configure the pong per command line arguments
    pong = pong(args.url, args.user, args.password)
    # Simple intuitive injection
    user_routes = UserRoutes(pong)

    app = FastAPI()
    # router member inherited from Routable and configured per the annotations.
    app.include_router(user_routes.router)
```

## Why 🐣

FastAPI generally has one define routes like:

```py
app = FastAPI()

@app.get('/echo/{x}')
def echo(x: int) -> int:
   return x
```

__Note:__ that `app` is a global. Furthermore, [FastAPI's suggested way of doing dependency injection](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/) is handy for things like pulling values out of header in the HTTP request. However, they don't work well for more standard dependency injection scenarios where we'd like to do something like inject a Data Access Object or database connection. For that, FastAPI suggests [their parameterized dependencies](https://fastapi.tiangolo.com/advanced/advanced-dependencies/) which might look something like:

```py
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

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
pip install -r requirements.dev.txt
```

### Format the code 💅

Execute the following command to apply `pre-commit` formatting:

```bash
make lint
```

## License 🍻

This project is licensed under the terms of the MIT license.
