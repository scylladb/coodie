"""Integration tests for UserType (UDT) support.

Tests DDL creation, dependency ordering, and round-trip save/load
of documents with UDT-typed fields.
Every test runs twice (sync and async) via the ``variant`` fixture.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID, uuid4

import pytest

from coodie.fields import Frozen, PrimaryKey
from coodie.usertype import UserType
from tests.conftest import _maybe_await

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]

# ---------------------------------------------------------------------------
# UDT model definitions (module-level for stable type names)
# ---------------------------------------------------------------------------


class IAddress(UserType):
    """Simple address UDT used in integration tests."""

    street: str = ""
    city: str = ""

    class Settings:
        __type_name__ = "it_address"
        keyspace = "test_ks"


class IPhone(UserType):
    """Phone number UDT — a nested dependency of IContact."""

    country_code: str = ""
    number: str = ""

    class Settings:
        __type_name__ = "it_phone"
        keyspace = "test_ks"


class IContact(UserType):
    """Contact UDT that embeds IPhone — tests nested dependency resolution."""

    name: str = ""
    phone: IPhone | None = None

    class Settings:
        __type_name__ = "it_contact"
        keyspace = "test_ks"


class AutoPhone(UserType):
    """Only ever synced implicitly via ``Document.sync_table()``."""

    number: str = ""

    class Settings:
        __type_name__ = "it_auto_phone"


class AutoContact(UserType):
    name: str = ""
    phone: AutoPhone | None = None

    class Settings:
        __type_name__ = "it_auto_contact"


# ---------------------------------------------------------------------------
# Helpers for variant-aware Document subclass creation
# ---------------------------------------------------------------------------


async def _type_names(driver, variant) -> set[str]:
    """UDT names that exist in ``test_ks``.

    ``sync_type()`` returns only the DDL it ran, which is nothing once the
    type exists, so tests check the schema instead of the returned list.
    """
    rows = await _maybe_await(
        driver.execute if variant == "sync" else driver.execute_async,
        "SELECT type_name FROM system_schema.types WHERE keyspace_name = ?",
        ["test_ks"],
    )
    return {r["type_name"] for r in rows}


def _make_address_doc(base_cls):
    class AddressDoc(base_cls):
        id: Annotated[UUID, PrimaryKey()] = __import__("pydantic").Field(default_factory=uuid4)
        address: Annotated[IAddress, Frozen()] = __import__("pydantic").Field(default_factory=IAddress)

        class Settings:
            name = "it_address_docs"
            keyspace = "test_ks"

    return AddressDoc


def _make_address_list_doc(base_cls):
    class AddressListDoc(base_cls):
        id: Annotated[UUID, PrimaryKey()] = __import__("pydantic").Field(default_factory=uuid4)
        addresses: Annotated[list[Annotated[IAddress, Frozen()]], Frozen()] = __import__("pydantic").Field(
            default_factory=list
        )

        class Settings:
            name = "it_address_list_docs"
            keyspace = "test_ks"

    return AddressListDoc


def _make_contact_doc(base_cls):
    class ContactDoc(base_cls):
        id: Annotated[UUID, PrimaryKey()] = __import__("pydantic").Field(default_factory=uuid4)
        contact: Annotated[IContact, Frozen()] = __import__("pydantic").Field(default_factory=IContact)

        class Settings:
            name = "it_contact_docs"
            keyspace = "test_ks"

    return ContactDoc


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------


class TestUDTIntegration:
    """Integration tests for UserType DDL and round-trip behaviour."""

    async def test_sync_type_creates_udt(self, coodie_driver, variant) -> None:
        """sync_type() creates the type."""
        if variant == "sync":
            IAddress.sync_type(keyspace="test_ks")
        else:
            await IAddress.sync_type_async(keyspace="test_ks")
        assert "it_address" in await _type_names(coodie_driver, variant)

    async def test_sync_type_nested_dependency_order(self, coodie_driver, variant) -> None:
        """sync_type() on a nested UDT creates dependencies first (IPhone before IContact).

        The server rejects ``CREATE TYPE it_contact`` while ``it_phone`` is
        missing, so a wrong order fails here on a fresh cluster.
        """
        if variant == "sync":
            IContact.sync_type(keyspace="test_ks")
        else:
            await IContact.sync_type_async(keyspace="test_ks")
        assert {"it_phone", "it_contact"} <= await _type_names(coodie_driver, variant)

    async def test_udt_field_roundtrip(self, coodie_driver, variant, driver_type) -> None:
        """A Document with a UDT field can be saved and loaded with equal values."""
        if driver_type == "acsylla":
            pytest.skip("acsylla does not support UDT round-trips")

        if variant == "sync":
            from coodie.sync.document import Document as BaseDoc
        else:
            from coodie.aio.document import Document as BaseDoc

        # Ensure UDT is created first
        if variant == "sync":
            IAddress.sync_type(keyspace="test_ks")
        else:
            await IAddress.sync_type_async(keyspace="test_ks")

        AddressDoc = _make_address_doc(BaseDoc)
        await _maybe_await(AddressDoc.sync_table)

        rid = uuid4()
        addr = IAddress(street="123 Main St", city="Springfield")
        doc = AddressDoc(id=rid, address=addr)
        await _maybe_await(doc.save)

        fetched = await _maybe_await(AddressDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.address is not None
        assert fetched.address.street == "123 Main St"
        assert fetched.address.city == "Springfield"

        await _maybe_await(AddressDoc(id=rid).delete)

    async def test_nested_udt_roundtrip(self, coodie_driver, variant, driver_type) -> None:
        """A UDT containing another UDT survives a save/load round-trip."""
        if driver_type == "acsylla":
            pytest.skip("acsylla does not support UDT round-trips")

        if variant == "sync":
            from coodie.sync.document import Document as BaseDoc

            IContact.sync_type(keyspace="test_ks")
        else:
            from coodie.aio.document import Document as BaseDoc

            await IContact.sync_type_async(keyspace="test_ks")

        ContactDoc = _make_contact_doc(BaseDoc)
        await _maybe_await(ContactDoc.sync_table)

        rid = uuid4()
        phone = IPhone(country_code="+1", number="555-1234")
        contact = IContact(name="Alice", phone=phone)
        doc = ContactDoc(id=rid, contact=contact)
        await _maybe_await(doc.save)

        fetched = await _maybe_await(ContactDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.contact is not None
        assert fetched.contact.name == "Alice"

        await _maybe_await(ContactDoc(id=rid).delete)

    async def test_sync_type_adds_new_field(self, coodie_driver, variant) -> None:
        """Re-syncing a UDT with an extra field issues ALTER TYPE ... ADD."""
        type_name = f"it_evolve_{variant}"
        await _maybe_await(
            coodie_driver.execute if variant == "sync" else coodie_driver.execute_async,
            f"DROP TYPE IF EXISTS test_ks.{type_name}",
            [],
        )

        class V1(UserType):
            a: str = ""

            class Settings:
                __type_name__ = type_name
                keyspace = "test_ks"

        class V2(UserType):
            a: str = ""
            b: int = 0

            class Settings:
                __type_name__ = type_name
                keyspace = "test_ks"

        sync = (lambda c: c.sync_type()) if variant == "sync" else (lambda c: c.sync_type_async())
        await _maybe_await(sync, V1)
        stmts = await _maybe_await(sync, V2)
        assert stmts == [f'ALTER TYPE test_ks.{type_name} ADD "b" int']
        # Idempotent: nothing left to add
        assert await _maybe_await(sync, V2) == []

    async def test_sync_table_auto_syncs_udts(self, coodie_driver, variant, driver_type) -> None:
        """sync_table() creates referenced (nested) UDTs without explicit sync_type()."""
        if variant == "sync":
            from coodie.sync.document import Document as BaseDoc
        else:
            from coodie.aio.document import Document as BaseDoc

        class AutoDoc(BaseDoc):
            id: Annotated[UUID, PrimaryKey()] = __import__("pydantic").Field(default_factory=uuid4)
            contact: AutoContact | None = None

            class Settings:
                name = f"it_auto_udt_docs_{variant}"
                keyspace = "test_ks"

        await _maybe_await(AutoDoc.sync_table)
        assert {"it_auto_phone", "it_auto_contact"} <= await _type_names(coodie_driver, variant)

        if driver_type == "acsylla":
            return  # acsylla does not support UDT round-trips
        rid = uuid4()
        await _maybe_await(AutoDoc(id=rid, contact=AutoContact(name="Bob", phone=AutoPhone(number="1"))).save)
        fetched = await _maybe_await(AutoDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.contact is not None
        assert fetched.contact.phone is not None
        assert fetched.contact.phone.number == "1"
