from dataclasses import dataclass, field
from typing import Any

from .exceptions import VariableNotInitializedError


@dataclass
class VariableReference:
    """Class representing a variable reference. that is simply an object that holds
    the reference position in the json string, so it can be replaced with the Variable value.
    """

    start_loc: int = 0
    """Start location of the variable reference in the JSON string."""
    end_loc: int = 0
    """End location of the variable reference in the JSON string."""


@dataclass
class Variable:
    """Stores the variable name, its declaration position, and its range value."""

    name: str
    declaration: VariableReference
    range: list[Any] = field(default_factory=list)
    references: list[VariableReference] = field(default_factory=list)

    def __post_init__(self):
        """Add the declaration to the references list."""
        self.references.append(self.declaration)

    def get_range_value_from_index(self, index: int) -> Any:
        """Get the value of the variable at a specific index."""
        if index < 0 or index >= len(self.range):
            raise IndexError("Index out of range.")
        return self.range[index]

    def add_reference(self, reference: VariableReference):
        """Add a reference to the variable."""
        self.references.append(reference)


class VariableList(list):
    """Custom list class to handle Variable objects."""

    def __contains__(self, item):
        if isinstance(item, str):
            return any(var.name == item for var in self)
        return super().__contains__(item)

    def append(self, item: Variable):
        # Optional: prevent duplicates by name
        super().append(item)

    def get_variable(self, name: str) -> Variable:
        """Get a variable by its name."""
        for var in self:
            if var.name == name:
                return var

        raise VariableNotInitializedError(f"Variable '{name}' not found.")
