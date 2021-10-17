# Deep Dive into Async Python

## What Do "Sync" and "Async" Mean?

Web applications often have to deal with many requests, all arriving from different clients and within a short period of time. To avoid processing delays it is considered a must that they should be able to handle several requests at the same time, something commonly known as concurrency. I will continue to use web applications as an example throughout this article, but keep in mind that there are other types of applications that also benefit from having multiple tasks done concurrently, so this discussion isn't specific to the web.

The terms "sync" and "async" refer to two ways in which to write applications that use concurrency. The so called "sync" servers use the underlying operating system support of threads and processes to implement this concurrency. Here is a diagram of how a sync deployment might look:

![image](https://blog.miguelgrinberg.com/static/images/web-perf-sync.png)

## Partial Object

The "partial object" is a way to send a subset of an object to the client, the full concept is to provide a way to send a subset of an object to the client, and the client can then request the rest of the object. This is useful for sending a subset of an object to the client, and the client can then request the rest of the object.

That why FastAPI Class allows you to construct an **instance** of a class and have methods of that instance be route handlers for FastAPI & Python 3.8.

- Older Versions of Python:
  - Unfortunately this does not work with `async` routes with Python versions less than 3.8 [due to bugs in `inspect.iscoroutinefunction`](https://stackoverflow.com/a/52422903/1431244). Specifically with older versions of Python `iscoroutinefunction` incorrectly returns false so `async` routes aren't `await`'d. We therefore only support Python versions >= 3.8.

## Why This?

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
