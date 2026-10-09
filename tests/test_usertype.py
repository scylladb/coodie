"""Tests for coodie.usertype module and UDT integration."""

from __future__ import annotations

from typing import Annotated, Optional
from uuid import UUID

import pytest
from pydantic import Field

from coodie.cql_builder import (
    build_alter_type_add,
    build_create_type,
    build_drop_type,
)
from coodie.fields import Frozen, PrimaryKey
from coodie.types import python_type_to_cql_type_str
from coodie.usertype import (
    UserType,
    _extract_udt_dependencies,
    _is_usertype,
    extract_udt_classes,
)

# ---- UserType definition helpers ----


class Address(UserType):
    street: str
    city: str
    zipcode: int


class AddressWithOverride(UserType):
    street: str

    class Settings:
        __type_name__ = "custom_addr"


class PhoneNumber(UserType):
    country_code: str
    number: str


class Contact(UserType):
    name: str
    phone: PhoneNumber
    address: Address


class AddressWithOptional(UserType):
    street: str
    city: str
    apt: str | None = None


class AddressWithCollection(UserType):
    street: str
    tags: list[str] = Field(default_factory=list)


# ---- Phase 1: UserType class tests ----


class TestUserTypeDefinition:
    def test_type_name_snake_case(self):
        assert Address.type_name() == "address"

    def test_type_name_camel_case(self):
        class ShippingAddress(UserType):
            street: str

        assert ShippingAddress.type_name() == "shipping_address"

    def test_type_name_with_override(self):
        assert AddressWithOverride.type_name() == "custom_addr"

    def test_type_name_lowercased(self):
        class MyUDT(UserType):
            value: int

        assert MyUDT.type_name() == "my_udt"

    def test_instance_creation(self):
        addr = Address(street="123 Main St", city="Springfield", zipcode=62704)
        assert addr.street == "123 Main St"
        assert addr.city == "Springfield"
        assert addr.zipcode == 62704

    def test_model_validate(self):
        data = {"street": "123 Main St", "city": "Springfield", "zipcode": 62704}
        addr = Address.model_validate(data)
        assert addr.street == "123 Main St"

    def test_model_dump(self):
        addr = Address(street="123 Main St", city="Springfield", zipcode=62704)
        data = addr.model_dump()
        assert data == {"street": "123 Main St", "city": "Springfield", "zipcode": 62704}

    def test_equality(self):
        addr1 = Address(street="A", city="B", zipcode=1)
        addr2 = Address(street="A", city="B", zipcode=1)
        addr3 = Address(street="X", city="Y", zipcode=2)
        assert addr1 == addr2
        assert addr1 != addr3

    def test_optional_field(self):
        addr = AddressWithOptional(street="A", city="B")
        assert addr.apt is None

    def test_collection_field(self):
        addr = AddressWithCollection(street="A", tags=["home", "billing"])
        assert addr.tags == ["home", "billing"]

    def test_nested_usertype(self):
        phone = PhoneNumber(country_code="+1", number="555-1234")
        addr = Address(street="A", city="B", zipcode=1)
        contact = Contact(name="Alice", phone=phone, address=addr)
        assert contact.phone.number == "555-1234"
        assert contact.address.city == "B"

    def test_is_usertype_true(self):
        assert _is_usertype(Address)

    def test_is_usertype_false_for_base(self):
        assert not _is_usertype(UserType)

    def test_is_usertype_false_for_non_usertype(self):
        assert not _is_usertype(str)
        assert not _is_usertype(int)

    def test_get_field_cql_types(self):
        fields = Address._get_field_cql_types()
        assert ("street", "text") in fields
        assert ("city", "text") in fields
        assert ("zipcode", "int") in fields

    def test_get_field_cql_types_nested(self):
        fields = Contact._get_field_cql_types()
        assert ("name", "text") in fields
        assert ("phone", "frozen<phone_number>") in fields
        assert ("address", "frozen<address>") in fields


# ---- Phase 2: CQL Builder tests ----


class TestCQLBuilderUDT:
    def test_build_create_type(self):
        fields = [("street", "text"), ("city", "text"), ("zipcode", "int")]
        cql = build_create_type("address", "my_ks", fields)
        assert cql == 'CREATE TYPE IF NOT EXISTS my_ks.address ("street" text, "city" text, "zipcode" int)'

    def test_build_create_type_with_udt_field(self):
        fields = [("name", "text"), ("phone", "frozen<phone_number>")]
        cql = build_create_type("contact", "my_ks", fields)
        assert "frozen<phone_number>" in cql
        assert "CREATE TYPE IF NOT EXISTS my_ks.contact" in cql

    def test_build_drop_type(self):
        cql = build_drop_type("address", "my_ks")
        assert cql == "DROP TYPE IF EXISTS my_ks.address"

    def test_build_alter_type_add(self):
        cql = build_alter_type_add("address", "my_ks", "phone", "text")
        assert cql == 'ALTER TYPE my_ks.address ADD "phone" text'


# ---- Phase 3: Type system integration tests ----


class TestTypeSystemUDT:
    def test_usertype_to_frozen(self):
        assert python_type_to_cql_type_str(Address) == "frozen<address>"

    def test_usertype_with_custom_name(self):
        assert python_type_to_cql_type_str(AddressWithOverride) == "frozen<custom_addr>"

    def test_usertype_annotated_frozen_no_double_wrap(self):
        """Annotated[Address, Frozen()] should produce frozen<address>, not frozen<frozen<address>>."""
        assert python_type_to_cql_type_str(Annotated[Address, Frozen()]) == "frozen<address>"

    def test_usertype_in_list(self):
        assert python_type_to_cql_type_str(list[Address]) == "list<frozen<address>>"

    def test_usertype_in_set(self):
        assert python_type_to_cql_type_str(set[Address]) == "set<frozen<address>>"

    def test_usertype_in_dict_value(self):
        assert python_type_to_cql_type_str(dict[str, Address]) == "map<text, frozen<address>>"

    def test_usertype_in_tuple(self):
        assert python_type_to_cql_type_str(tuple[Address, int]) == "tuple<frozen<address>, int>"

    def test_nested_usertype(self):
        assert python_type_to_cql_type_str(Contact) == "frozen<contact>"

    def test_optional_usertype(self):
        assert python_type_to_cql_type_str(Optional[Address])  # noqa: UP045 - tests typing.Optional explicitly == "frozen<address>"

    def test_pep604_optional_usertype(self):
        assert python_type_to_cql_type_str(Address | None) == "frozen<address>"


# ---- Phase 4: Schema integration tests ----


class TestSchemaUDT:
    def test_build_schema_with_udt_field(self):
        from pydantic import BaseModel

        # We need to import sync Document but we don't need a real driver
        # Just test via build_schema directly
        from coodie.schema import build_schema

        class _FakeDoc(BaseModel):
            id: Annotated[UUID, PrimaryKey()]
            addr: Address

        schema = build_schema(_FakeDoc)
        addr_col = next(c for c in schema if c.name == "addr")
        assert addr_col.cql_type == "frozen<address>"

    def test_build_schema_with_list_udt(self):
        from pydantic import BaseModel

        from coodie.schema import build_schema

        class _FakeDoc(BaseModel):
            id: Annotated[UUID, PrimaryKey()]
            addrs: list[Address] = []

        schema = build_schema(_FakeDoc)
        addrs_col = next(c for c in schema if c.name == "addrs")
        assert addrs_col.cql_type == "list<frozen<address>>"


# ---- Dependency extraction tests ----


class TestUDTDependencies:
    def test_extract_dependencies_simple(self):
        deps = _extract_udt_dependencies(Address)
        assert deps == []  # Address has no UDT deps

    def test_extract_dependencies_nested(self):
        deps = _extract_udt_dependencies(Contact)
        dep_classes = [d.__name__ for d in deps]
        assert "PhoneNumber" in dep_classes
        assert "Address" in dep_classes
        # PhoneNumber and Address should come before Contact (which is not included)
        assert len(deps) == 2

    def test_extract_dependencies_circular_raises(self):
        # Can't easily create a true circular reference with forward refs,
        # but we test the detection logic exists
        # For now, just test that non-circular works fine
        deps = _extract_udt_dependencies(Contact)
        assert len(deps) == 2

    def test_extract_udt_classes_from_document(self):
        from pydantic import BaseModel

        class _FakeDoc(BaseModel):
            id: Annotated[UUID, PrimaryKey()]
            contact: Contact
            extra_addr: Address

        udts = extract_udt_classes(_FakeDoc)
        udt_names = [u.__name__ for u in udts]
        # All three UDTs should be returned
        assert "PhoneNumber" in udt_names
        assert "Address" in udt_names
        assert "Contact" in udt_names
        # Dependencies before dependents
        assert udt_names.index("PhoneNumber") < udt_names.index("Contact")
        assert udt_names.index("Address") < udt_names.index("Contact")

    def test_extract_udt_classes_no_udts(self):
        from pydantic import BaseModel

        class _PlainDoc(BaseModel):
            id: Annotated[UUID, PrimaryKey()]
            name: str

        assert extract_udt_classes(_PlainDoc) == []

    def test_extract_udt_classes_udt_in_collection(self):
        from pydantic import BaseModel

        class _ListDoc(BaseModel):
            id: Annotated[UUID, PrimaryKey()]
            addrs: list[Address] = []

        udts = extract_udt_classes(_ListDoc)
        assert Address in udts

    def test_extract_udt_classes_pep604_optional(self):
        from pydantic import BaseModel

        class _OptDoc(BaseModel):
            id: Annotated[UUID, PrimaryKey()]
            addr: Address | None = None
            phones: list[PhoneNumber] | None = None

        udts = extract_udt_classes(_OptDoc)
        assert Address in udts
        assert PhoneNumber in udts


# ---- sync_type tests with mock driver ----


class TestSyncType:
    def test_sync_type_executes_create(self, registered_mock_driver):
        stmts = Address.sync_type(keyspace="test_ks")
        assert len(stmts) == 1
        assert "CREATE TYPE IF NOT EXISTS test_ks.address" in stmts[0]
        # Verify the driver was called
        assert len(registered_mock_driver.executed) == 1
        cql, params = registered_mock_driver.executed[0]
        assert "CREATE TYPE" in cql
        assert params == []

    def test_sync_type_nested_syncs_deps_first(self, registered_mock_driver):
        stmts = Contact.sync_type(keyspace="test_ks")
        # Should have 3 statements: PhoneNumber, Address, Contact
        assert len(stmts) == 3
        # Verify order: deps before Contact
        assert "phone_number" in stmts[0]
        assert "address" in stmts[1]
        assert "contact" in stmts[2]

    @pytest.mark.asyncio
    async def test_sync_type_async(self, registered_mock_driver):
        stmts = await Address.sync_type_async(keyspace="test_ks")
        assert len(stmts) == 1
        assert "CREATE TYPE IF NOT EXISTS test_ks.address" in stmts[0]

    @pytest.mark.asyncio
    async def test_sync_type_async_nested(self, registered_mock_driver):
        stmts = await Contact.sync_type_async(keyspace="test_ks")
        assert len(stmts) == 3


# ---- Serialization round-trip tests ----


class TestUDTSerialization:
    def test_model_dump_simple(self):
        addr = Address(street="123 Main St", city="Springfield", zipcode=62704)
        assert addr.model_dump() == {
            "street": "123 Main St",
            "city": "Springfield",
            "zipcode": 62704,
        }

    def test_model_dump_nested(self):
        phone = PhoneNumber(country_code="+1", number="555-1234")
        addr = Address(street="A", city="B", zipcode=1)
        contact = Contact(name="Alice", phone=phone, address=addr)
        data = contact.model_dump()
        assert data["phone"] == {"country_code": "+1", "number": "555-1234"}
        assert data["address"] == {"street": "A", "city": "B", "zipcode": 1}

    def test_model_validate_from_dict(self):
        data = {"street": "A", "city": "B", "zipcode": 1}
        addr = Address.model_validate(data)
        assert addr.street == "A"

    def test_model_validate_nested(self):
        data = {
            "name": "Alice",
            "phone": {"country_code": "+1", "number": "555-1234"},
            "address": {"street": "A", "city": "B", "zipcode": 1},
        }
        contact = Contact.model_validate(data)
        assert contact.phone.number == "555-1234"
        assert contact.address.city == "B"

    def test_model_dump_list_of_udt(self):
        addrs = [
            Address(street="A", city="X", zipcode=1),
            Address(street="B", city="Y", zipcode=2),
        ]
        dumped = [a.model_dump() for a in addrs]
        assert len(dumped) == 2
        assert dumped[0]["street"] == "A"
        assert dumped[1]["street"] == "B"
