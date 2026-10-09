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


# ---------------------------------------------------------------------------
# Helpers for variant-aware Document subclass creation
# ---------------------------------------------------------------------------


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
        """sync_type() executes CREATE TYPE without error."""
        if variant == "sync":
            stmts = IAddress.sync_type(keyspace="test_ks")
        else:
            stmts = await IAddress.sync_type_async(keyspace="test_ks")
        assert any("it_address" in s for s in stmts)

    async def test_sync_type_nested_dependency_order(self, coodie_driver, variant) -> None:
        """sync_type() on a nested UDT creates dependencies first (IPhone before IContact)."""
        if variant == "sync":
            stmts = IContact.sync_type(keyspace="test_ks")
        else:
            stmts = await IContact.sync_type_async(keyspace="test_ks")
        # IPhone must appear before IContact in emitted statements
        phone_idx = next((i for i, s in enumerate(stmts) if "it_phone" in s), None)
        contact_idx = next((i for i, s in enumerate(stmts) if "it_contact" in s), None)
        assert phone_idx is not None, "it_phone type was not created"
        assert contact_idx is not None, "it_contact type was not created"
        assert phone_idx < contact_idx, "it_phone must be created before it_contact"

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
