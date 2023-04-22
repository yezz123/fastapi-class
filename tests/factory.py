from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Factory(Generic[T]):
    def __call__(self, *args: Any, **kwds: Any) -> T:
        pass  # pragma: no cover
