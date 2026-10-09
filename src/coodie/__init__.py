try:
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("coodie")
    except PackageNotFoundError:
        try:
            from coodie._version import __version__  # type: ignore[no-redef]
        except ImportError:
            __version__ = "unknown"
except ImportError:
    __version__ = "unknown"

from coodie.aio import (
    CounterDocument,
    Document,
    MaterializedView,
    QuerySet,
    create_keyspace,
    drop_keyspace,
    execute_raw,
    init_coodie,
)
from coodie.batch import AsyncBatchQuery, BatchQuery
from coodie.exceptions import (
    ConfigurationError,
    CoodieError,
    DocumentNotFound,
    InvalidQueryError,
    MigrationError,
    MultipleDocumentsFound,
)
from coodie.fields import (
    Ascii,
    BigInt,
    ClusteringKey,
    Counter,
    Discriminator,
    Double,
    Duration,
    Frozen,
    Indexed,
    PrimaryKey,
    SmallInt,
    Static,
    Time,
    TimeUUID,
    TinyInt,
    VarInt,
    Vector,
    VectorIndex,
)
from coodie.lazy import LazyDocument
from coodie.results import LWTResult, PagedResult
from coodie.types import CqlDuration
from coodie.usertype import UserType

__all__ = [
    "Ascii",
    "AsyncBatchQuery",
    "BatchQuery",
    "BigInt",
    "ClusteringKey",
    "ConfigurationError",
    "CoodieError",
    "Counter",
    "CounterDocument",
    "CqlDuration",
    "Discriminator",
    "Document",
    "DocumentNotFound",
    "Double",
    "Duration",
    "Frozen",
    "Indexed",
    "InvalidQueryError",
    "LWTResult",
    "LazyDocument",
    "MaterializedView",
    "MigrationError",
    "MultipleDocumentsFound",
    "PagedResult",
    "PrimaryKey",
    "QuerySet",
    "SmallInt",
    "Static",
    "Time",
    "TimeUUID",
    "TinyInt",
    "UserType",
    "VarInt",
    "Vector",
    "VectorIndex",
    "create_keyspace",
    "drop_keyspace",
    "execute_raw",
    "init_coodie",
]
