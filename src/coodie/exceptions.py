class CoodieError(Exception):
    """Base class for all coodie exceptions."""


class DocumentNotFound(CoodieError):
    """Raised when a document lookup returns no results."""


class MultipleDocumentsFound(CoodieError):
    """Raised when a single-document lookup returns more than one result."""


class ConfigurationError(CoodieError):
    """Raised when coodie is not properly configured (e.g. no driver registered)."""


class InvalidQueryError(CoodieError):
    """Raised when a query is constructed incorrectly."""


class MigrationError(CoodieError):
    """Raised when a migration operation fails."""


class BlockingCallWarning(UserWarning):
    """Emitted when a blocking ``*_sync`` call runs inside an event loop on an async-default model."""
