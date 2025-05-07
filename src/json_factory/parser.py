import json
from typing import Any

from .constants import VALID_VARIABLE_CHARS
from .entities import Variable, VariableList, VariableReference
from .exceptions import (
    RangeSizeNotDefinedError,
    VariableAlreadyInitializedError,
    VariableNotInitializedError,
)


def _get_variable_positions(json_string: str) -> list[int]:
    """Find all $ and its positions in the json_string."""
    return [i for i, char in enumerate(json_string) if char == "$"]


def _parse_variable_expression(
    variable_expr: str,
) -> tuple[list[Any], None | Exception]:
    """Parse the variable expression and return the range value."""

    range_value = []

    # Parse "[]" operator
    # e.g: $current_frame([0,2,5,6]) -> [0, 2, 5, 6]
    if variable_expr.startswith("[") and variable_expr.endswith("]"):
        # Extract the range size from the variable expression
        range_size_str = variable_expr.split("[")[1].split("]")[0]
        try:
            range_value = [int(x) for x in range_size_str.split(",")]
        except ValueError as exc:
            return [], exc
    # Parse "<>" operator

    # e.g:
    # $current_frame(<3>) -> [0, 1, 2, 3]
    # $current_frame(<0-3>) -> [0, 1, 2, 3]
    # $current_frame(<0-10>{2}) -> [0, 2, 4, 6, 8, 10] # With step 2
    if variable_expr.startswith("<") and variable_expr.endswith(">"):
        # Extract the range size from the variable expression
        range_size_str = variable_expr.split("<")[1].split(">")[0]
        try:
            # Check if a step is provided (e.g., <0-10>{2})
            if "{" in range_size_str and "}" in range_size_str:
                range_part, step_str = range_size_str.split("{")
                step = int(step_str.strip("}"))
            else:
                range_part = range_size_str
                step = 1  # Default step

            # Check if the range part is a single number (e.g., <3>)
            if "-" not in range_part:
                range_start = 0
                range_end = int(range_part)
            else:
                # Extract the start and end for ranges (e.g., <0-3>)
                range_start = int(range_part.split("-")[0])
                range_end = int(range_part.split("-")[1])

            # Generate the range with the step
            range_values = [x for x in range(range_start, range_end + 1, step)]

            return range_values, None
        except ValueError as exc:
            return [], exc

    return range_value, None


def from_string(json_string: str) -> list[dict[str, Any]]:
    """Process the json_string with custom syntax and return a list
    of the generated jsons as python dict.

    Args:
        json_string (str): The JSON string to process.
    Returns:
        list[dict[str, Any]]: A list of generated JSON objects as Python dictionaries.
    """

    # =====================
    # Initialization
    # =====================

    # Store all variables in the program
    declared_variables: list[Variable] = VariableList()
    # The first initialized variable sets the global range size
    # if no variable is initialized, the range size is 1 and the standard json
    # will be returned
    declared_range_size: None | int = 1

    # =====================
    # Parser Init
    # =====================

    # find all $ and its positions in the job task string
    variable_positions = _get_variable_positions(json_string)

    # Populate the variable list with all variables found in the job task string
    for var_init_pos in variable_positions:
        var_end_pos = var_init_pos
        for i in range(var_init_pos, len(json_string)):
            if not i == var_init_pos:  # ignore first character "$"
                if not json_string[i].lower() in VALID_VARIABLE_CHARS:
                    break
            var_end_pos += 1

        variable_name = json_string[var_init_pos:var_end_pos]

        # check if is a variable initialization
        # Variable initialization has an expression after the variable name
        # e.g: $current_frame(<0-3>)
        if json_string[var_end_pos] == "(":

            if variable_name in declared_variables:
                raise VariableAlreadyInitializedError(
                    f"Variable '{variable_name}' was already initialized."
                )

            variable_expr = json_string[var_end_pos + 1 :]
            if ")" in variable_expr:
                variable_expr = variable_expr.split(")")[0]
            else:
                raise VariableNotInitializedError(
                    f"Variable '{variable_name}' was declared but not initialized."
                )
            range_value, exc = _parse_variable_expression(variable_expr)
            if not range_value and exc:
                raise VariableNotInitializedError(
                    f"Variable '{variable_name}' has an invalid range size."
                ) from exc

            # Defines the global range size from the first initialized variable
            if declared_range_size == 1 and range_value:
                declared_range_size = len(range_value)
            else:
                # If the global range size is already defined,
                # check if the current variable has the same size
                # if not raise an error
                if declared_range_size != len(range_value):
                    raise RangeSizeNotDefinedError(
                        f"Variable has a range size({range_value}) that does not match the global range({declared_range_size})."
                    )

            var_end_pos += len(variable_expr) + 2  # +2 for the parentheses
            declared_variables.append(
                Variable(
                    name=variable_name,
                    range=range_value,
                    declaration=VariableReference(var_init_pos, var_end_pos),
                )
            )
        else:
            variable_data = declared_variables.get_variable(variable_name)
            if not variable_data:
                raise VariableNotInitializedError(
                    f"Variable '{variable_name}' was declared but not initialized."
                )
            variable_data.add_reference(
                VariableReference(var_init_pos, var_end_pos)
            )

    # =====================
    # Generate each json
    # =====================

    generated_jsons: list[dict[str, Any]] = []

    for i in range(declared_range_size):
        generated_json_string = json_string

        # After each variable replacement, the string length changes
        # so we need to keep track of the offset to replace the variable correctly
        loc_offset = 0

        for variable in declared_variables:
            variable_value = variable.get_range_value_from_index(i)

            # Replace each reference with the variable value for the
            # current range index
            for reference in variable.references:

                start_loc = reference.start_loc + loc_offset
                end_loc = reference.end_loc + loc_offset

                generated_json_string = (
                    generated_json_string[:start_loc]
                    + str(variable_value)
                    + generated_json_string[end_loc:]
                )

                loc_offset += (start_loc - end_loc) + len(str(variable_value))

        generated_jsons.append(json.loads(generated_json_string))

    return generated_jsons
