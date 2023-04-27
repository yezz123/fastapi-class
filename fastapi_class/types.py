from __future__ import annotations

from typing import Protocol, TypeVar

Entity = TypeVar("Entity")


class Repository(Protocol[Entity]):
    """Repository interface for CRUD operations."""

    async def retrieve(self, *args, **kwargs) -> Entity | None:
        """Retrieve a single entity."""
        ...

    async def create(self, *args, **kwargs) -> Entity | None:
        """Create a single entity."""
        ...

    async def update(self, *args, **kwargs) -> Entity | None:
        """Update a single entity."""
        ...

    async def partial_update(self, *args, **kwargs) -> Entity | None:
        """Update a single entity with partial data."""
        ...

    async def delete(self, *args, **kwargs) -> None:
        """Delete a single entity."""
        ...

    async def list(self, *args, **kwargs) -> list[Entity]:
        """List entities."""
        ...


class SideService(Protocol):
    """Side service interface."""

    async def start(self, *args, **kwargs) -> None:
        """Start the side service."""
        ...

    async def stop(self, *args, **kwargs) -> None:
        """Stop the side service."""
        ...
