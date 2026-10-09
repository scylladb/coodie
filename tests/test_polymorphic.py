from typing import Annotated
from uuid import UUID, uuid4

import pytest
from pydantic import Field

from coodie.fields import PrimaryKey
from tests.conftest import _maybe_await
from tests.models import make_pet_hierarchy, make_vehicle_hierarchy

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture(params=["sync", "async"])
def variant(request):
    return request.param


@pytest.fixture
def document_cls(variant):
    if variant == "sync":
        from coodie.sync.document import Document

        return Document
    from coodie.aio.document import Document

    return Document


@pytest.fixture
def pet_hierarchy(document_cls):
    return make_pet_hierarchy(document_cls)


@pytest.fixture
def Pet(pet_hierarchy):
    return pet_hierarchy[0]


@pytest.fixture
def Cat(pet_hierarchy):
    return pet_hierarchy[1]


@pytest.fixture
def Dog(pet_hierarchy):
    return pet_hierarchy[2]


@pytest.fixture
def vehicle_hierarchy(document_cls):
    return make_vehicle_hierarchy(document_cls)


@pytest.fixture
def Vehicle(vehicle_hierarchy):
    return vehicle_hierarchy[0]


@pytest.fixture
def Truck(vehicle_hierarchy):
    return vehicle_hierarchy[1]


# ------------------------------------------------------------------
# 9.1 – Discriminator value in Settings
# ------------------------------------------------------------------


def test_discriminator_value_on_subclass(Cat, Dog):
    assert Cat.Settings.__discriminator_value__ == "cat"
    assert Dog.Settings.__discriminator_value__ == "dog"


def test_no_discriminator_value_on_base(Pet):
    assert not hasattr(Pet.Settings, "__discriminator_value__")


# ------------------------------------------------------------------
# 9.2 – Discriminator column detected by schema helpers
# ------------------------------------------------------------------


def test_find_discriminator_column(Pet, Cat, Dog):
    from coodie.schema import _find_discriminator_column

    assert _find_discriminator_column(Pet) == "pet_type"
    assert _find_discriminator_column(Cat) == "pet_type"
    assert _find_discriminator_column(Dog) == "pet_type"


def test_find_discriminator_column_not_polymorphic(document_cls):
    from coodie.schema import _find_discriminator_column

    class Plain(document_cls):
        id: Annotated[UUID, PrimaryKey()] = Field(default_factory=uuid4)

        class Settings:
            name = "plain"
            keyspace = "test_ks"

    assert _find_discriminator_column(Plain) is None


def test_resolve_polymorphic_base(Pet, Cat, Dog):
    from coodie.schema import _resolve_polymorphic_base

    assert _resolve_polymorphic_base(Pet) is Pet
    assert _resolve_polymorphic_base(Cat) is Pet
    assert _resolve_polymorphic_base(Dog) is Pet


def test_build_subclass_map(Pet, Cat, Dog):
    from coodie.schema import _build_subclass_map

    mapping = _build_subclass_map(Pet)
    assert mapping["cat"] is Cat
    assert mapping["dog"] is Dog
    # Pet has no __discriminator_value__ so it's not in the map
    assert "pet" not in mapping


def test_discriminator_column_in_schema(Pet):
    """The discriminator column appears in build_schema output."""
    from coodie.schema import build_schema

    # Clear cache to rebuild
    if hasattr(Pet, "__schema__") and "__schema__" in Pet.__dict__:
        delattr(Pet, "__schema__")
    schema = build_schema(Pet)
    col_names = [c.name for c in schema]
    assert "pet_type" in col_names


# ------------------------------------------------------------------
# 9.3 – find()/get() auto-filter by discriminator
# ------------------------------------------------------------------


def test_subclass_find_adds_discriminator_filter(registered_mock_driver, Cat):
    qs = Cat.find(name="Whiskers")
    # Verify discriminator filter was added
    disc_filters = [(col, op, val) for col, op, val in qs._where if col == "pet_type"]
    assert len(disc_filters) == 1
    assert disc_filters[0] == ("pet_type", "=", "cat")


def test_base_find_no_discriminator_filter(registered_mock_driver, Pet):
    qs = Pet.find(name="Any")
    disc_filters = [(col, op, val) for col, op, val in qs._where if col == "pet_type"]
    assert len(disc_filters) == 0


async def test_subclass_find_one_filters(registered_mock_driver, Cat):
    pid = uuid4()
    registered_mock_driver.set_return_rows([{"id": pid, "name": "Whiskers", "pet_type": "cat", "cuteness": 9.5}])
    doc = await _maybe_await(Cat.find_one, name="Whiskers")
    assert doc is not None
    assert isinstance(doc, Cat)
    stmt, params = registered_mock_driver.executed[0]
    assert '"pet_type" = ?' in stmt
    assert "cat" in params


async def test_subclass_get_filters(registered_mock_driver, Dog):
    pid = uuid4()
    registered_mock_driver.set_return_rows([{"id": pid, "name": "Buddy", "pet_type": "dog", "loudness": 8}])
    doc = await _maybe_await(Dog.get, name="Buddy")
    assert isinstance(doc, Dog)
    stmt, params = registered_mock_driver.executed[0]
    assert '"pet_type" = ?' in stmt
    assert "dog" in params


# ------------------------------------------------------------------
# 9.4 – save()/insert() auto-set discriminator
# ------------------------------------------------------------------


async def test_save_sets_discriminator(registered_mock_driver, Cat):
    cat = Cat(name="Whiskers", cuteness=9.5)
    await _maybe_await(cat.save)
    stmt, params = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.pets" in stmt
    assert "cat" in params


async def test_insert_sets_discriminator(registered_mock_driver, Dog):
    dog = Dog(name="Buddy", loudness=8)
    await _maybe_await(dog.insert)
    stmt, params = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.pets" in stmt
    assert "IF NOT EXISTS" in stmt
    assert "dog" in params


async def test_base_save_without_discriminator_value(registered_mock_driver, Pet):
    """Base class without __discriminator_value__ saves normally."""
    pet = Pet(name="Generic")
    await _maybe_await(pet.save)
    stmt, params = registered_mock_driver.executed[0]
    assert "INSERT INTO test_ks.pets" in stmt
    # pet_type should be the default empty string, not overwritten
    assert "cat" not in params
    assert "dog" not in params


# ------------------------------------------------------------------
# 9.5 – Polymorphic deserialization (correct subclass from base query)
# ------------------------------------------------------------------


async def test_base_query_returns_correct_subclasses(registered_mock_driver, Pet, Cat, Dog):
    registered_mock_driver.set_return_rows(
        [
            {
                "id": uuid4(),
                "name": "Whiskers",
                "pet_type": "cat",
                "cuteness": 9.5,
                "loudness": None,
            },
            {
                "id": uuid4(),
                "name": "Buddy",
                "pet_type": "dog",
                "cuteness": None,
                "loudness": 8,
            },
        ]
    )
    results = await _maybe_await(Pet.find().all)
    assert len(results) == 2
    assert isinstance(results[0], Cat)
    assert results[0].name == "Whiskers"
    assert results[0].cuteness == 9.5
    assert isinstance(results[1], Dog)
    assert results[1].name == "Buddy"
    assert results[1].loudness == 8


async def test_unknown_discriminator_falls_back_to_queried_class(registered_mock_driver, Pet):
    registered_mock_driver.set_return_rows([{"id": uuid4(), "name": "Parrot", "pet_type": "bird"}])
    results = await _maybe_await(Pet.find().all)
    assert len(results) == 1
    assert isinstance(results[0], Pet)
    assert results[0].name == "Parrot"


async def test_subclass_query_returns_only_subclass(registered_mock_driver, Cat):
    pid = uuid4()
    registered_mock_driver.set_return_rows([{"id": pid, "name": "Whiskers", "pet_type": "cat", "cuteness": 9.5}])
    results = await _maybe_await(Cat.find().all)
    assert len(results) == 1
    assert isinstance(results[0], Cat)
    assert results[0].cuteness == 9.5


# ------------------------------------------------------------------
# Table/keyspace delegation
# ------------------------------------------------------------------


def test_subclass_uses_base_table(Pet, Cat, Dog):
    assert Cat._get_table() == "pets"
    assert Dog._get_table() == "pets"
    assert Pet._get_table() == "pets"


def test_subclass_uses_base_keyspace(Cat, Dog):
    assert Cat._get_keyspace() == "test_ks"
    assert Dog._get_keyspace() == "test_ks"


# ------------------------------------------------------------------
# Base class with discriminator_value
# ------------------------------------------------------------------


def test_base_with_discriminator_value_filters(registered_mock_driver, Vehicle):
    """Base with __discriminator_value__ also auto-filters."""
    qs = Vehicle.find(make="Ford")
    disc_filters = [(col, op, val) for col, op, val in qs._where if col == "vehicle_type"]
    assert len(disc_filters) == 1
    assert disc_filters[0] == ("vehicle_type", "=", "vehicle")


async def test_base_with_discriminator_value_saves(registered_mock_driver, Vehicle):
    v = Vehicle(make="Ford")
    await _maybe_await(v.save)
    _stmt, params = registered_mock_driver.executed[0]
    assert "vehicle" in params


# ------------------------------------------------------------------
# Edge cases
# ------------------------------------------------------------------


def test_queryset_iter_polymorphic(registered_mock_driver, variant, Pet, Cat):
    if variant == "async":
        pytest.skip("sync __iter__ not available on async QuerySet")
    registered_mock_driver.set_return_rows(
        [
            {"id": uuid4(), "name": "Whiskers", "pet_type": "cat", "cuteness": 9.5},
        ]
    )
    items = list(Pet.find())
    assert len(items) == 1
    assert isinstance(items[0], Cat)


async def test_queryset_first_polymorphic(registered_mock_driver, Pet, Dog):
    registered_mock_driver.set_return_rows([{"id": uuid4(), "name": "Buddy", "pet_type": "dog", "loudness": 8}])
    doc = await _maybe_await(Pet.find().first)
    assert isinstance(doc, Dog)
