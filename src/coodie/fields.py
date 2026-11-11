from dataclasses import dataclass


@dataclass(frozen=True)
class PrimaryKey:
    """Annotated marker: partition key column.

    Use ``partition_key_index`` to define composite partition keys::

        product_id: Annotated[UUID, PrimaryKey(partition_key_index=0)]
        category:   Annotated[str,  PrimaryKey(partition_key_index=1)]
    """

    partition_key_index: int = 0


@dataclass(frozen=True)
class ClusteringKey:
    """Annotated marker: clustering column.

    Args:
        order: ``"ASC"`` (default) or ``"DESC"``.
        clustering_key_index: Position within the clustering key (0-based).
    """

    order: str = "ASC"
    clustering_key_index: int = 0


@dataclass(frozen=True)
class Indexed:
    """Annotated marker: create a secondary index on this column."""

    index_name: str | None = None


@dataclass(frozen=True)
class Counter:
    """Annotated marker: counter column."""


@dataclass(frozen=True)
class BigInt:
    """Annotated marker: maps ``int`` to CQL ``bigint``."""


@dataclass(frozen=True)
class SmallInt:
    """Annotated marker: maps ``int`` to CQL ``smallint``."""


@dataclass(frozen=True)
class TinyInt:
    """Annotated marker: maps ``int`` to CQL ``tinyint``."""


@dataclass(frozen=True)
class VarInt:
    """Annotated marker: maps ``int`` to CQL ``varint``."""


@dataclass(frozen=True)
class Double:
    """Annotated marker: maps ``float`` to CQL ``double``."""


@dataclass(frozen=True)
class Ascii:
    """Annotated marker: maps ``str`` to CQL ``ascii``."""


@dataclass(frozen=True)
class TimeUUID:
    """Annotated marker: maps ``UUID`` to CQL ``timeuuid``."""


@dataclass(frozen=True)
class Time:
    """Annotated marker: maps to CQL ``time``."""


@dataclass(frozen=True)
class Static:
    """Annotated marker: declares a column as ``STATIC``.

    Static columns are shared across all rows within a partition.
    They can only appear on tables that have at least one clustering column.
    """


@dataclass(frozen=True)
class Frozen:
    """Annotated marker: wraps a collection or UDT type with ``frozen<>``."""


@dataclass(frozen=True)
class Duration:
    """Annotated marker: maps a ``CqlDuration`` field to CQL ``duration``."""


@dataclass(frozen=True)
class Discriminator:
    """Annotated marker: discriminator column for polymorphic (single-table inheritance) models."""


@dataclass(frozen=True)
class Vector:
    """Annotated marker: vector column for ANN similarity search.

    Maps ``list[float]`` to the CQL ``vector<float, N>`` type::

        embedding: Annotated[list[float], Vector(dimensions=384)]
    """

    dimensions: int


_VALID_SIMILARITY_FUNCTIONS = frozenset({"COSINE", "DOT_PRODUCT", "EUCLIDEAN"})


@dataclass(frozen=True)
class VectorIndex:
    """Annotated marker: create a SAI vector index on this column.

    Emits ``CREATE CUSTOM INDEX … USING 'vector_index'`` with the
    chosen similarity function (``COSINE``, ``DOT_PRODUCT``, or
    ``EUCLIDEAN``)::

        embedding: Annotated[list[float], Vector(dimensions=384), VectorIndex(similarity_function="COSINE")]
    """

    similarity_function: str = "COSINE"
    index_name: str | None = None

    def __post_init__(self) -> None:
        if self.similarity_function not in _VALID_SIMILARITY_FUNCTIONS:
            raise ValueError(
                f"Invalid similarity_function {self.similarity_function!r}, "
                f"must be one of {sorted(_VALID_SIMILARITY_FUNCTIONS)}"
            )
