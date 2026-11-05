from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import Self

from coodie.cql_builder import build_batch
from coodie.results import LWTResult


class BatchQuery:
    """Batch context manager usable from both sync and async code.

    Accumulates CQL statements and executes them as a single batch on exit.

    Example::

        with BatchQuery() as batch:
            Product(name="A").save(batch=batch)
            Product(name="B").save(batch=batch)

        async with BatchQuery() as batch:
            await Product(name="A").save(batch=batch)
            await Product(name="B").save(batch=batch)

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

    def _build(self) -> tuple[str, list[Any]]:
        return build_batch(
            self._statements,
            logged=self._logged,
            batch_type=self._batch_type,
            timestamp=self._timestamp,
        )

    def _finish(self, rows: list[dict[str, Any]]) -> LWTResult | None:
        from coodie.query import _parse_lwt_result

        self._statements.clear()
        self.result = _parse_lwt_result(rows) if rows and "[applied]" in rows[0] else None
        return self.result

    def execute_sync(self) -> LWTResult | None:
        """Execute the accumulated batch immediately (blocking).

        Returns an :class:`~coodie.results.LWTResult` when the batch contains
        conditional statements, else ``None``.  When a multi-statement
        conditional batch is not applied, the server returns one row per
        statement; only the first row is reported in ``existing``.
        """
        if not self._statements:
            return None
        from coodie.drivers import get_driver

        return self._finish(get_driver().execute(*self._build()))

    async def execute_async(self) -> LWTResult | None:
        """Async version of :meth:`execute_sync`."""
        if not self._statements:
            return None
        from coodie.drivers import get_driver

        return self._finish(await get_driver().execute_async(*self._build()))

    def execute(self) -> LWTResult | None:
        """Execute the accumulated batch immediately."""
        return self.execute_sync()

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
            self.execute_sync()

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
            await self.execute_async()


class AsyncBatchQuery(BatchQuery):
    """Same as :class:`BatchQuery`, except that ``execute()`` is a coroutine.

    Example::

        async with AsyncBatchQuery() as batch:
            await Product(name="A").save(batch=batch)
            await Product(name="B").save(batch=batch)
    """

    __slots__ = ()

    async def execute(self) -> LWTResult | None:  # type: ignore[override]
        """Execute the accumulated batch immediately."""
        return await self.execute_async()
