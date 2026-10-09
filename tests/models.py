"""Shared model factory functions for sync/async merged tests.

⚠ Do NOT add ``from __future__ import annotations`` to this file.
PEP 563 stores annotations as strings, and ``get_type_hints()``
cannot resolve them for classes defined in local scope, which would
cause ``build_schema()`` to return empty columns.
"""

from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from coodie.fields import (
    ClusteringKey,
    Counter,
    Discriminator,
    Indexed,
    PrimaryKey,
    Static,
)


def make_product(base_cls):
    class Product(base_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str
        brand: Annotated[str, Indexed()] = "Unknown"
        price: float = 0.0
        description: str | None = None

        class Settings:
            name = "products"
            keyspace = "test_ks"

    return Product


def make_tagged_product(base_cls):
    class TaggedProduct(base_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""
        price: float = 0.0
        tags: set[str] = Field(default_factory=set)
        items: list[str] = Field(default_factory=list)
        meta: dict[str, str] = Field(default_factory=dict)

        class Settings:
            name = "tagged_products"
            keyspace = "test_ks"

    return TaggedProduct


def make_page_view(counter_cls):
    class PageView(counter_cls):
        url: Annotated[str, PrimaryKey()]
        view_count: Annotated[int, Counter()] = 0
        unique_visitors: Annotated[int, Counter()] = 0

        class Settings:
            name = "page_views"
            keyspace = "test_ks"

    return PageView


def make_products_by_brand(mv_cls):
    class ProductsByBrand(mv_cls):
        brand: Annotated[str, PrimaryKey()]
        id: Annotated[UUID, ClusteringKey()] = Field(default_factory=uuid4)
        name: str = ""
        price: float = 0.0

        class Settings:
            name = "products_by_brand"
            keyspace = "test_ks"
            __base_table__ = "products"

    return ProductsByBrand


def make_item(base_cls):
    class Item(base_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""
        rating: int = 0

        class Settings:
            name = "items"
            keyspace = "test_ks"

    return Item


def make_pet_hierarchy(base_cls):
    class Pet(base_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        name: str = ""
        pet_type: Annotated[str, Discriminator()] = ""

        class Settings:
            name = "pets"
            keyspace = "test_ks"

    class Cat(Pet):
        cuteness: float = 0.0

        class Settings:
            __discriminator_value__ = "cat"

    class Dog(Pet):
        loudness: int = 0

        class Settings:
            __discriminator_value__ = "dog"

    return Pet, Cat, Dog


def make_vehicle_hierarchy(base_cls):
    class Vehicle(base_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)
        make: str = ""
        vehicle_type: Annotated[str, Discriminator()] = ""

        class Settings:
            name = "vehicles"
            keyspace = "test_ks"
            __discriminator_value__ = "vehicle"

    class Truck(Vehicle):
        payload_tons: float = 0.0

        class Settings:
            __discriminator_value__ = "truck"

    return Vehicle, Truck


def make_sensor_reading(base_cls):
    class SensorReading(base_cls):
        sensor_id: Annotated[str, PrimaryKey()]
        reading_time: Annotated[str, ClusteringKey()]
        sensor_name: Annotated[str, Static()] = ""
        value: float = 0.0

        class Settings:
            name = "sensor_readings"
            keyspace = "test_ks"

    return SensorReading
