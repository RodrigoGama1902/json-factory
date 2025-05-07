class VariableNotInitializedError(Exception):
    """Custom exception for uninitialized variables."""


class VariableAlreadyInitializedError(Exception):
    """Custom exception for already initialized variables."""


class RangeSizeNotDefinedError(Exception):
    """Custom exception for undefined range size."""
