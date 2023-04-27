from abc import ABC

from .api import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from .generics import (
    GenericCreateView,
    GenericDestroyView,
    GenericListView,
    GenericRetrieveView,
    GenericUpdateView,
)


class ReadOnlyAPIViewSet(ListAPIView, RetrieveAPIView, ABC):
    ...


class ListCreateAPIViewSet(ListAPIView, CreateAPIView, ABC):
    ...


class RetrieveUpdateAPIViewSet(RetrieveAPIView, UpdateAPIView, ABC):
    ...


class RetrieveUpdateDestroyAPIViewSet(
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, ABC
):
    ...


class ListRetrieveUpdateDestroyAPIViewSet(
    ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ABC
):
    ...


class ListCreateDestroyAPIViewSet(ListAPIView, CreateAPIView, DestroyAPIView, ABC):
    ...


class APIViewSet(
    ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ABC
):
    ...


class GenericReadOnlyViewSet(GenericListView, GenericRetrieveView, ABC):
    ...


class GenericListCreateViewSet(GenericListView, GenericCreateView, ABC):
    ...


class GenericRetrieveUpdateViewSet(GenericRetrieveView, GenericUpdateView, ABC):
    ...


class GenericRetrieveUpdateDestroyAPIViewSet(
    GenericRetrieveView, GenericUpdateView, GenericDestroyView, ABC
):
    ...


class GenericListRetrieveUpdateDeleteViewSet(
    GenericListView, GenericRetrieveView, GenericUpdateView, GenericDestroyView, ABC
):
    ...


class GenericViewSet(
    GenericListView,
    GenericCreateView,
    GenericRetrieveView,
    GenericUpdateView,
    GenericDestroyView,
    ABC,
):
    ...
