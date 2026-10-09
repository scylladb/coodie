"""UDT serialization and schema benchmarks — coodie vs cqlengine.

These benchmarks compare UDT-related operations: type creation, serialization
(model → dict), and deserialization (dict → model) for User-Defined Types.
"""

from __future__ import annotations

import pytest

# ---------------------------------------------------------------------------
# UDT model_dump() — serialize UserType to dict (no DB)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="udt-serialization")
def test_cqlengine_udt_serialization(benchmark):
    try:
        from cassandra.cqlengine import columns
        from cassandra.cqlengine.usertype import UserType
    except ImportError:
        pytest.skip("cqlengine not available")

    class CqlAddress(UserType):
        __type_name__ = "bench_cql_addr"
        street = columns.Text()
        city = columns.Text()
        state = columns.Text()
        zipcode = columns.Integer()

    addr = CqlAddress(street="123 Main St", city="Springfield", state="IL", zipcode=62704)

    def _serialize():
        # cqlengine UserType serialization
        return {name: getattr(addr, name) for name in ["street", "city", "state", "zipcode"]}

    benchmark(_serialize)


@pytest.mark.benchmark(group="udt-serialization")
def test_coodie_udt_serialization(benchmark):
    from coodie.usertype import UserType

    class CoodieAddress(UserType):
        street: str
        city: str
        state: str
        zipcode: int

    addr = CoodieAddress(street="123 Main St", city="Springfield", state="IL", zipcode=62704)

    def _serialize():
        addr.model_dump()

    benchmark(_serialize)


# ---------------------------------------------------------------------------
# UDT construction — instantiate from dict (no DB)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="udt-instantiation")
def test_cqlengine_udt_instantiation(benchmark):
    try:
        from cassandra.cqlengine import columns
        from cassandra.cqlengine.usertype import UserType
    except ImportError:
        pytest.skip("cqlengine not available")

    class CqlAddress2(UserType):
        __type_name__ = "bench_cql_addr2"
        street = columns.Text()
        city = columns.Text()
        state = columns.Text()
        zipcode = columns.Integer()

    data = {"street": "123 Main St", "city": "Springfield", "state": "IL", "zipcode": 62704}

    def _create():
        CqlAddress2(**data)

    benchmark(_create)


@pytest.mark.benchmark(group="udt-instantiation")
def test_coodie_udt_instantiation(benchmark):
    from coodie.usertype import UserType

    class CoodieAddress2(UserType):
        street: str
        city: str
        state: str
        zipcode: int

    data = {"street": "123 Main St", "city": "Springfield", "state": "IL", "zipcode": 62704}

    def _create():
        CoodieAddress2(**data)

    benchmark(_create)


# ---------------------------------------------------------------------------
# Nested UDT serialization — 2 levels deep (no DB)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="udt-nested-serialization")
def test_cqlengine_nested_udt_serialization(benchmark):
    try:
        from cassandra.cqlengine import columns
        from cassandra.cqlengine.usertype import UserType
    except ImportError:
        pytest.skip("cqlengine not available")

    class CqlPhone(UserType):
        __type_name__ = "bench_cql_phone"
        country_code = columns.Text()
        number = columns.Text()

    class CqlContact(UserType):
        __type_name__ = "bench_cql_contact"
        name = columns.Text()
        phone = columns.UserDefinedType(CqlPhone)

    phone = CqlPhone(country_code="+1", number="555-1234")
    contact = CqlContact(name="Alice", phone=phone)

    def _serialize():
        return {
            "name": contact.name,
            "phone": {"country_code": phone.country_code, "number": phone.number},
        }

    benchmark(_serialize)


@pytest.mark.benchmark(group="udt-nested-serialization")
def test_coodie_nested_udt_serialization(benchmark):
    from coodie.usertype import UserType

    class CoodiePhone(UserType):
        country_code: str
        number: str

    class CoodieContact(UserType):
        name: str
        phone: CoodiePhone

    phone = CoodiePhone(country_code="+1", number="555-1234")
    contact = CoodieContact(name="Alice", phone=phone)

    def _serialize():
        contact.model_dump()

    benchmark(_serialize)


# ---------------------------------------------------------------------------
# DDL generation — build CREATE TYPE statement (no DB)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="udt-ddl-generation")
def test_cqlengine_udt_ddl_generation(benchmark):
    try:
        from cassandra.cqlengine import columns
        from cassandra.cqlengine.usertype import UserType
    except ImportError:
        pytest.skip("cqlengine not available")

    class CqlBenchAddr(UserType):
        __type_name__ = "bench_cql_ddl_addr"
        street = columns.Text()
        city = columns.Text()
        state = columns.Text()
        zipcode = columns.Integer()

    def _generate():
        # cqlengine doesn't expose a public DDL builder for types,
        # so we simulate the field introspection that sync_type performs
        fields = {name: col.db_type for name, col in CqlBenchAddr._fields.items()}
        return f"CREATE TYPE IF NOT EXISTS bench_ks.bench_cql_ddl_addr ({', '.join(f'{k} {v}' for k, v in fields.items())})"

    benchmark(_generate)


@pytest.mark.benchmark(group="udt-ddl-generation")
def test_coodie_udt_ddl_generation(benchmark):
    from coodie.cql_builder import build_create_type
    from coodie.usertype import UserType

    class CoodieBenchAddr(UserType):
        street: str
        city: str
        state: str
        zipcode: int

        class Settings:
            __type_name__ = "bench_coodie_ddl_addr"

    def _generate():
        # coodie's _get_field_cql_types() returns [(field_name, cql_type_str), ...]
        # by resolving Python type annotations to CQL types via the type system
        fields = CoodieBenchAddr._get_field_cql_types()
        return build_create_type("bench_coodie_ddl_addr", "bench_ks", fields)

    benchmark(_generate)
