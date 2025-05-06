import json
from dataclasses import dataclass, field
from typing import Any

test_task = """{
  "name": "test_job",
  "tasks": [
    {
      "name": "task1",
      "priority": 0,
      "group": "string",
      "pool": "string",
      "plugin_name": "string",
      "plugin_args": {
        "frame_start": $current_frame(<0-3>),
        "frame_end" : $current_frame
      }
    }
  ]
}"""

VALID_VARIABLE_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz0123456789_"
)

class VariableNotInitializedError(Exception):
    """Custom exception for uninitialized variables."""


class VariableAlreadyInitializedError(Exception):
    """Custom exception for already initialized variables."""


class RangeSizeNotDefinedError(Exception):
    """Custom exception for undefined range size."""


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

def _get_variable_positions(job_task_str: str) -> list[int]:
    """
    Finds all positions of the '$' character in the job task string.

    Args:
        job_task_str (str): The job task string to search.

    Returns:
        list[int]: A list of positions where '$' is found.
    """
    return [i for i, char in enumerate(job_task_str) if char == "$"]


def parse_job_task(job_task_str: str) -> list[dict[str, Any]]:
    """
    Parses a job task string into a dictionary with keys 'job' and 'task'.

    Args:
        job_task_str (str): The job task string to parse.

    Returns:
        dict: A dictionary with keys 'job' and 'task'.
    """
    
    # =====================
    # Initialization
    # =====================

    # Store all variables in the program
    variables = VariableList()
    # The first initialized variable sets the global range size
    declared_range_size : None | int = None
    
    # =====================
    # Parser Init
    # =====================

    # find all $ and its positions in the job task string
    variable_positions = _get_variable_positions(job_task_str)

    # Populate the variable list with all variables found in the job task string
    for var_init_pos in variable_positions:
        var_end_pos = var_init_pos
        for i in range(var_init_pos, len(job_task_str)):
            if not i == var_init_pos: # ignore first character "$"
                if not job_task_str[i].lower() in VALID_VARIABLE_CHARS:
                    break
            var_end_pos += 1

        variable_name = job_task_str[var_init_pos:var_end_pos]

        # check if is a variable initialization
        # Variable initialization has an expression after the variable name
        # e.g: $current_frame(<0-3>)
        if job_task_str[var_end_pos] == "(":

            if variable_name in variables:
                raise VariableAlreadyInitializedError(
                    f"Variable '{variable_name}' was already initialized."
                )

            variable_expr = job_task_str[var_end_pos + 1 :]
            if ")" in variable_expr:
                variable_expr = variable_expr.split(")")[0]
            else:
                raise VariableNotInitializedError(
                    f"Variable '{variable_name}' was declared but not initialized."
                )

            range_value = []
            if variable_expr.startswith("<") and variable_expr.endswith(">"):
                # Extract the range size from the variable expression
                range_size_str = variable_expr.split("<")[1].split(">")[0]
                try:
                    # solve range
                    range_start = int(range_size_str.split("-")[0])
                    range_end = int(range_size_str.split("-")[1])

                    if declared_range_size is None:
                        declared_range_size = range_end - range_start + 1
                    else:
                        if declared_range_size != range_end - range_start + 1:
                            raise RangeSizeNotDefinedError(
                                "Range size is not defined. Please check the variable declarations."
                            )

                    range_value = [
                        int(x) for x in range(range_start, range_end + 1)
                    ]

                except ValueError as exc:
                    raise VariableNotInitializedError(
                        f"Variable '{variable_name}' has an invalid range size."
                    ) from exc
            
            var_end_pos += len(variable_expr) + 2  # +2 for the parentheses

            variables.append(
                Variable(
                    init=True,
                    name=variable_name,
                    start_loc=var_init_pos,
                    end_loc=var_end_pos,
                    range=range_value,
                )
            )
        else:
            if not variables.is_initialized(variable_name):
                raise VariableNotInitializedError(
                    f"Variable '{variable_name}' was declared but not initialized."
                )

            variables.append(
                Variable(
                    init=False,
                    name=variable_name,
                    start_loc=var_init_pos,
                    end_loc=var_end_pos,
                )
            )

        print(f"variable_declaration: {variable_name}")

    # now replace the variables in the job task string with their values
    if not declared_range_size:
        raise RangeSizeNotDefinedError(
            "Range size is not defined. Please check the variable declarations."
        )

    generated_tasks: list[dict[str, Any]] = []

    for i in range(declared_range_size):
        task_raw = job_task_str
        loc_offset = 0
        for variable in variables:
            
            variable_value = variables.get_variable_range(variable)[i]

            start_loc = variable.start_loc + loc_offset
            end_loc = variable.end_loc + loc_offset

            task_raw = (
                task_raw[:start_loc] + str(variable_value) + task_raw[end_loc:]
            )

            loc_offset += (start_loc - end_loc) + len(str(variable_value))

        generated_tasks.append(json.loads(task_raw))

    return generated_tasks


if __name__ == "__main__":
    job_task = test_task
    parsed_job_task = parse_job_task(job_task)
    
    print(parsed_job_task)
