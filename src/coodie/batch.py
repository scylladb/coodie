from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import Self

from coodie.cql_builder import build_batch
from coodie.results import LWTResult


class BatchQuery:
    """Synchronous batch context manager.

    Accumulates CQL statements and executes them as a single batch on exit.

    Example::

        from coodie.sync import BatchQuery

        with BatchQuery() as batch:
            Product(name="A").save(batch=batch)
            Product(name="B").save(batch=batch)

    For conditional batches (``IF NOT EXISTS`` / ``IF ...``) the outcome is
    returned by :meth:`execute` and also kept on ``batch.result``.
    """

    __slots__ = ("_batch_type", "_logged", "_statements", "_timestamp", "result")

    def __init__(
        self,
        logged: bool = True,
        batch_type: str | None = None,
        timestamp: int | None = None,
    ) -> None:
        self._logged = logged
        self._batch_type = batch_type
        self._timestamp = timestamp
        self._statements: list[tuple[str, list[Any]]] = []
        self.result: LWTResult | None = None

    def add(self, stmt: str, params: list[Any]) -> None:
        """Add a CQL statement to the batch."""
        self._statements.append((stmt, params))

    def __enter__(self) -> Self:
        self._statements.clear()
        self.result = None
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is None and self._statements:
            self.execute()

    def execute(self) -> LWTResult | None:
        """Execute the accumulated batch immediately.

        Returns an :class:`~coodie.results.LWTResult` when the batch contains
        conditional statements, else ``None``.  When a multi-statement
        conditional batch is not applied, the server returns one row per
        statement; only the first row is reported in ``existing``.
        """
        if not self._statements:
            return None
        from coodie.drivers import get_driver
        from coodie.sync.document import _parse_lwt_result

        cql, params = build_batch(
            self._statements,
            logged=self._logged,
            batch_type=self._batch_type,
            timestamp=self._timestamp,
        )
        rows = get_driver().execute(cql, params)
        self._statements.clear()
        self.result = _parse_lwt_result(rows) if rows and "[applied]" in rows[0] else None
        return self.result


class AsyncBatchQuery:
    """Asynchronous batch context manager.

    Accumulates CQL statements and executes them as a single batch on exit.

    Example::

        from coodie.aio import AsyncBatchQuery

        async with AsyncBatchQuery() as batch:
            await Product(name="A").save(batch=batch)
            await Product(name="B").save(batch=batch)

    For conditional batches (``IF NOT EXISTS`` / ``IF ...``) the outcome is
    returned by :meth:`execute` and also kept on ``batch.result``.
    """

    def __init__(
        self,
        logged: bool = True,
        batch_type: str | None = None,
        timestamp: int | None = None,
    ) -> None:
        self._logged = logged
        self._batch_type = batch_type
        self._timestamp = timestamp
        self._statements: list[tuple[str, list[Any]]] = []
        self.result: LWTResult | None = None

    def add(self, stmt: str, params: list[Any]) -> None:
        """Add a CQL statement to the batch."""
        self._statements.append((stmt, params))

    async def __aenter__(self) -> Self:
        self._statements.clear()
        self.result = None
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is None and self._statements:
            await self.execute()

    async def execute(self) -> LWTResult | None:
        """Execute the accumulated batch immediately.

        Returns an :class:`~coodie.results.LWTResult` when the batch contains
        conditional statements, else ``None``.  When a multi-statement
        conditional batch is not applied, the server returns one row per
        statement; only the first row is reported in ``existing``.
        """
        if not self._statements:
            return None
        from coodie.drivers import get_driver
        from coodie.sync.document import _parse_lwt_result

        cql, params = build_batch(
            self._statements,
            logged=self._logged,
            batch_type=self._batch_type,
            timestamp=self._timestamp,
        )
        rows = await get_driver().execute_async(cql, params)
        self._statements.clear()
        self.result = _parse_lwt_result(rows) if rows and "[applied]" in rows[0] else None
        return self.result
