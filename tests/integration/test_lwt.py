"""Integration tests for Lightweight Transactions (LWT) across all operations.

Covers: ``Document.update(if_conditions={...})`` edge-cases (multiple
conditions, LWT result existing-value completeness),
``Document.delete(if_exists=True)``, ``QuerySet.if_not_exists().create()``,
``QuerySet.if_exists().delete()``, ``Document.insert()``,
``QuerySet.update(if_conditions={...})``,
``Document.delete(if_conditions={...})`` conditional deletes,
``QuerySet.delete(if_conditions={...})``,
extended IF operators (``!=``, ``IN``, ``>``, ``<``),
map put (``col__put``), list set-by-index (``col__setindex``),
and ``DELETE col[key] FROM`` via ``delete_columns(collection_elements=...)``.

Basic ``Document.update(if_conditions={...})`` and
``Document.update(if_exists=True)`` integration tests live in
``test_update.py``; this file adds the remaining §1.5 + Phase 4 coverage.

Every test runs twice (sync and async) via the ``variant`` fixture.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from coodie.results import LWTResult
from tests.conftest import _maybe_await

pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio(loop_scope="session"),
]


class TestConditionalUpdateEdgeCases:
    """Edge-case integration tests for Document.update(if_conditions={...})."""

    async def test_update_multiple_if_conditions_applied(self, coodie_driver, Product) -> None:
        """update(if_conditions={k1: v1, k2: v2}) succeeds when ALL conditions match."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="MultiCond", brand="BrandX", price=10.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.update,
            if_conditions={"name": "MultiCond", "brand": "BrandX"},
            price=25.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.price == 25.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_update_multiple_if_conditions_not_applied(self, coodie_driver, Product) -> None:
        """update(if_conditions={k1: v1, k2: v2}) is rejected when any condition fails."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="MultiCond", brand="BrandY", price=10.0)
        await _maybe_await(p.save)

        # name matches but brand does NOT
        result = await _maybe_await(
            p.update,
            if_conditions={"name": "MultiCond", "brand": "WrongBrand"},
            price=999.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is False
        assert result.existing is not None
        assert result.existing.get("brand") == "BrandY"

        # Price unchanged
        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.price == 10.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_update_if_conditions_existing_has_conditioned_columns(self, coodie_driver, Product) -> None:
        """When a conditional update fails, result.existing carries the current column values."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="ExistCheck", brand="BrandZ", price=42.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.update,
            if_conditions={"name": "Wrong"},
            price=1.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is False
        assert result.existing is not None
        # The server should return the actual value of the conditioned column
        assert result.existing.get("name") == "ExistCheck"

        await _maybe_await(Product(id=pid, name="").delete)


class TestConditionalInsert:
    """Integration tests for Document.insert() (INSERT ... IF NOT EXISTS)."""

    async def test_insert_applied_then_not_applied(self, coodie_driver, Product) -> None:
        """insert() returns applied=True first, then applied=False with the existing row."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()

        result = await _maybe_await(Product(id=pid, name="First").insert)
        assert isinstance(result, LWTResult)
        assert result.applied is True

        result = await _maybe_await(Product(id=pid, name="Second").insert)
        assert isinstance(result, LWTResult)
        assert result.applied is False
        assert result.existing is not None
        assert result.existing.get("name") == "First"

        await _maybe_await(Product(id=pid, name="").delete)


class TestConditionalDelete:
    """Integration tests for Document.delete(if_exists=True)."""

    async def test_delete_if_exists_applied(self, coodie_driver, Product) -> None:
        """delete(if_exists=True) succeeds and returns applied=True when the row exists."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="Deletable", price=5.0)
        await _maybe_await(p.save)

        result = await _maybe_await(p.delete, if_exists=True)

        assert isinstance(result, LWTResult)
        assert result.applied is True

        # Row should be gone
        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is None

    async def test_delete_if_exists_not_applied(self, coodie_driver, Product) -> None:
        """delete(if_exists=True) returns applied=False when the row doesn't exist."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        # Do NOT insert — this row doesn't exist
        p = Product(id=pid, name="Ghost")

        result = await _maybe_await(p.delete, if_exists=True)

        assert isinstance(result, LWTResult)
        assert result.applied is False


class TestQuerySetConditionalCreate:
    """Integration tests for QuerySet.if_not_exists().create()."""

    async def test_queryset_create_if_not_exists_applied(self, coodie_driver, Product) -> None:
        """if_not_exists().create() succeeds when the row is absent."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()

        result = await _maybe_await(
            Product.find().if_not_exists().create,
            id=pid,
            name="NewProduct",
            brand="TestBrand",
            category="testing",
            price=15.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        # Verify the row was actually created
        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.name == "NewProduct"
        assert fetched.price == 15.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_queryset_create_if_not_exists_not_applied(self, coodie_driver, Product) -> None:
        """if_not_exists().create() is rejected when the row already exists."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="Existing", price=10.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            Product.find().if_not_exists().create,
            id=pid,
            name="Duplicate",
            brand="DupBrand",
            category="dup",
            price=99.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is False
        # existing should carry the server's current values
        assert result.existing is not None

        # Original row should be unchanged
        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.name == "Existing"
        assert fetched.price == 10.0

        await _maybe_await(Product(id=pid, name="").delete)


class TestQuerySetConditionalUpdate:
    """Integration tests for QuerySet.update(if_conditions={...})."""

    async def test_queryset_update_if_conditions(self, coodie_driver, Product) -> None:
        """update(if_conditions=...) returns applied=True on match, applied=False with the current row otherwise."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        await _maybe_await(Product(id=pid, name="Before").save)

        result = await _maybe_await(Product.find(id=pid).update, if_conditions={"name": "Before"}, name="After")
        assert isinstance(result, LWTResult)
        assert result.applied is True

        result = await _maybe_await(Product.find(id=pid).update, if_conditions={"name": "Before"}, name="Again")
        assert isinstance(result, LWTResult)
        assert result.applied is False
        assert result.existing == {"name": "After"}

        await _maybe_await(Product(id=pid, name="").delete)


class TestQuerySetConditionalDelete:
    """Integration tests for QuerySet.if_exists().delete()."""

    async def test_queryset_delete_if_exists_applied(self, coodie_driver, Product) -> None:
        """if_exists().delete() succeeds when the row exists."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="ToDelete", price=5.0)
        await _maybe_await(p.save)

        result = await _maybe_await(Product.find(id=pid).if_exists().delete)

        assert isinstance(result, LWTResult)
        assert result.applied is True

        # Row should be gone
        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is None

    async def test_queryset_delete_if_exists_not_applied(self, coodie_driver, Product) -> None:
        """if_exists().delete() returns applied=False when the row doesn't exist."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()

        result = await _maybe_await(Product.find(id=pid).if_exists().delete)

        assert isinstance(result, LWTResult)
        assert result.applied is False


# ------------------------------------------------------------------
# Phase 4: Conditional deletes with if_conditions
# ------------------------------------------------------------------


class TestConditionalDeleteWithConditions:
    """Integration tests for Document.delete(if_conditions={...})."""

    async def test_delete_if_conditions_applied(self, coodie_driver, Product) -> None:
        """delete(if_conditions={col: val}) succeeds when the condition matches."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="CondDel", brand="BrandA", price=10.0)
        await _maybe_await(p.save)

        result = await _maybe_await(p.delete, if_conditions={"name": "CondDel"})

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is None

    async def test_delete_if_conditions_not_applied(self, coodie_driver, Product) -> None:
        """delete(if_conditions={col: val}) is rejected when the condition fails."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="CondDel", brand="BrandB", price=20.0)
        await _maybe_await(p.save)

        result = await _maybe_await(p.delete, if_conditions={"name": "WrongName"})

        assert isinstance(result, LWTResult)
        assert result.applied is False
        assert result.existing is not None
        assert result.existing.get("name") == "CondDel"

        # Row should still exist
        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.name == "CondDel"

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_delete_if_conditions_multiple(self, coodie_driver, Product) -> None:
        """delete(if_conditions={k1: v1, k2: v2}) succeeds only when all match."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="Multi", brand="BrandC", price=30.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.delete,
            if_conditions={"name": "Multi", "brand": "BrandC"},
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is None


class TestQuerySetConditionalDeleteWithConditions:
    """Integration tests for QuerySet.delete(if_conditions={...})."""

    async def test_queryset_delete_if_conditions_applied(self, coodie_driver, Product) -> None:
        """QuerySet.delete(if_conditions=...) succeeds when the condition matches."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="QSDel", brand="BrandD", price=40.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            Product.find(id=pid).delete,
            if_conditions={"name": "QSDel"},
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.find_one, id=pid)
        assert fetched is None

    async def test_queryset_delete_if_conditions_not_applied(self, coodie_driver, Product) -> None:
        """QuerySet.delete(if_conditions=...) is rejected when the condition fails."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="QSDel", brand="BrandE", price=50.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            Product.find(id=pid).delete,
            if_conditions={"name": "Wrong"},
        )

        assert isinstance(result, LWTResult)
        assert result.applied is False
        assert result.existing is not None

        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.name == "QSDel"

        await _maybe_await(Product(id=pid, name="").delete)


# ------------------------------------------------------------------
# Phase 4: Extended IF operators in update conditions
# ------------------------------------------------------------------


class TestExtendedIfOperators:
    """Integration tests for extended IF operators (!=, >, <) in update conditions."""

    async def test_update_if_ne_applied(self, coodie_driver, Product) -> None:
        """update(if_conditions={col__ne: val}) succeeds when col != val."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="NeTest", brand="BrandX", price=10.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.update,
            if_conditions={"name__ne": "Other"},
            price=20.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.price == 20.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_update_if_ne_not_applied(self, coodie_driver, Product) -> None:
        """update(if_conditions={col__ne: val}) fails when col == val."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="NeTest", brand="BrandX", price=10.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.update,
            if_conditions={"name__ne": "NeTest"},
            price=20.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is False

        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.price == 10.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_update_if_gt_applied(self, coodie_driver, Product) -> None:
        """update(if_conditions={col__gt: val}) succeeds when col > val."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="GtTest", price=100.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.update,
            if_conditions={"price__gt": 50.0},
            price=200.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.price == 200.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_update_if_lt_applied(self, coodie_driver, Product) -> None:
        """update(if_conditions={col__lt: val}) succeeds when col < val."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="LtTest", price=10.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.update,
            if_conditions={"price__lt": 50.0},
            price=5.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.price == 5.0

        await _maybe_await(Product(id=pid, name="").delete)

    async def test_update_if_in_applied(self, coodie_driver, Product) -> None:
        """update(if_conditions={col__in: [...]}) succeeds when col in list."""
        await _maybe_await(Product.sync_table)
        pid = uuid4()
        p = Product(id=pid, name="InTest", brand="BrandA", price=10.0)
        await _maybe_await(p.save)

        result = await _maybe_await(
            p.update,
            if_conditions={"brand__in": ["BrandA", "BrandB"]},
            price=99.0,
        )

        assert isinstance(result, LWTResult)
        assert result.applied is True

        fetched = await _maybe_await(Product.get, id=pid)
        assert fetched.price == 99.0

        await _maybe_await(Product(id=pid, name="").delete)


# ------------------------------------------------------------------
# Phase 4: Map put and list set-by-index
# ------------------------------------------------------------------


class TestMapPutAndListSetIndex:
    """Integration tests for map put (col__put) and list set-by-index (col__setindex)."""

    async def test_map_put_new_key(self, coodie_driver, ContainerDoc) -> None:
        """doc.update(meta__put=('newkey', 'newval')) inserts a map entry."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        row = ContainerDoc(id=rid, meta={"k1": "v1"})
        await _maybe_await(row.save)

        await _maybe_await(row.update, meta__put=("k2", "v2"))

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.meta.get("k1") == "v1"
        assert fetched.meta.get("k2") == "v2"

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_map_put_overwrite_key(self, coodie_driver, ContainerDoc) -> None:
        """doc.update(meta__put=('k1', 'updated')) overwrites an existing map entry."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        row = ContainerDoc(id=rid, meta={"k1": "v1"})
        await _maybe_await(row.save)

        await _maybe_await(row.update, meta__put=("k1", "updated"))

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.meta.get("k1") == "updated"

        await _maybe_await(ContainerDoc(id=rid).delete)

    async def test_list_setindex(self, coodie_driver, ContainerDoc) -> None:
        """doc.update(items__setindex=(idx, val)) replaces a list element at a given index."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        row = ContainerDoc(id=rid, items=["a", "b", "c"])
        await _maybe_await(row.save)

        await _maybe_await(row.update, items__setindex=(1, "B"))

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert fetched.items == ["a", "B", "c"]

        await _maybe_await(ContainerDoc(id=rid).delete)


# ------------------------------------------------------------------
# Phase 4: DELETE col[key] FROM / DELETE col[idx] FROM
# ------------------------------------------------------------------


class TestDeleteCollectionElements:
    """Integration tests for deleting map entries and list elements via delete_columns."""

    async def test_delete_map_element(self, coodie_driver, ContainerDoc) -> None:
        """delete_columns(collection_elements=[('meta', 'k1')]) removes a map entry."""
        await _maybe_await(ContainerDoc.sync_table)
        rid = uuid4()
        row = ContainerDoc(id=rid, meta={"k1": "v1", "k2": "v2"})
        await _maybe_await(row.save)

        await _maybe_await(row.delete_columns, collection_elements=[("meta", "k1")])

        fetched = await _maybe_await(ContainerDoc.find_one, id=rid)
        assert fetched is not None
        assert "k1" not in fetched.meta
        assert fetched.meta.get("k2") == "v2"

        await _maybe_await(ContainerDoc(id=rid).delete)
