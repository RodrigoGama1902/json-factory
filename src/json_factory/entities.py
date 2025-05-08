from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .exceptions import VariableNotInitializedError


class VariableModifierTypes(Enum):
    """Enum for variable modifiers."""

    ZFILL = "zfill"
    """Zero fill modifier."""
    TO_STRING = "to_string"
    """Convert to string modifier."""
    
@dataclass
class VariableModifier(ABC):
    """Class representing a variable modifier."""
    name : str = ""
    args: list[Any] = field(default_factory=list)

@dataclass
class VariableReference:
    """Class representing a variable reference. that is simply an object that holds
    the reference position in the json string, so it can be replaced with the Variable value.
    """

    start_loc: int = 0
    """Start location of the variable reference in the JSON string."""
    end_loc: int = 0
    """End location of the variable reference in the JSON string."""
    modifiers : list[VariableModifier] = field(default_factory=list)
    """List of modifiers applied to the variable."""
    
    def add_modifier(self, modifier: VariableModifier):
        """Add a modifier to the variable reference."""
        self.modifiers.append(modifier)

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
        
    def get_range_value_from_reference(self, index, reference : VariableReference):
        """Get the value of the variable at a specific 
        index with all applied modifiers."""
        
        # Get value from range by index
        if index < 0 or index >= len(self.range):
            raise IndexError("Index out of range.")
        range_value = self.range[index]
        
        # TODO: Modifier logic should not be implemented here, only executed
        # find a way to fix this
        for mod in reference.modifiers:
            if mod.name == "zfill":
                range_value = str(range_value).zfill(int(mod.args[0]))
            if mod.name == "to_string":
                range_value = str(f'"{range_value}"')
            if mod.name == "to_int":
                range_value = int(str(range_value).replace('"', '').replace("'", ""))
                
        return range_value

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