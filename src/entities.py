from dataclasses import dataclass, field
from typing import Any

from exceptions import VariableNotInitializedError

@dataclass
class Variable:
    """Class representing a variable."""

    init: bool
    name: str
    range: list[Any] = field(default_factory=list)
    start_loc: int = 0
    end_loc: int = 0


class VariableList(list):
    """Custom list class to handle Variable objects."""

    def __contains__(self, item):
        if isinstance(item, str):
            return any(var.name == item for var in self)
        return super().__contains__(item)

    def append(self, item: Variable):
        # Optional: prevent duplicates by name
        super().append(item)

    def get_variable_range(self, item: Variable) -> list[Any]:
        """Get the range of a variable by its name."""
        for var in self:
            if var.init and var.name == item.name:
                return var.range

        raise VariableNotInitializedError(f"Variable '{item.name}' not found.")

    def is_initialized(self, name: str) -> bool:
        """Check if a variable is initialized."""
        return any(var.name == name for var in self)