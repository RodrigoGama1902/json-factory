import json

from typing import Any

from exceptions import VariableNotInitializedError, VariableAlreadyInitializedError, RangeSizeNotDefinedError
from constants import VALID_VARIABLE_CHARS
from entities import Variable, VariableList

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


def _get_variable_positions(job_task_str: str) -> list[int]:
    """
    Finds all positions of the '$' character in the job task string.

    Args:
        job_task_str (str): The job task string to search.

    Returns:
        list[int]: A list of positions where '$' is found.
    """
    return [i for i, char in enumerate(job_task_str) if char == "$"]


def process(json_string: str) -> list[dict[str, Any]]:
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
    variable_positions = _get_variable_positions(json_string)

    # Populate the variable list with all variables found in the job task string
    for var_init_pos in variable_positions:
        var_end_pos = var_init_pos
        for i in range(var_init_pos, len(json_string)):
            if not i == var_init_pos: # ignore first character "$"
                if not json_string[i].lower() in VALID_VARIABLE_CHARS:
                    break
            var_end_pos += 1

        variable_name = json_string[var_init_pos:var_end_pos]

        # check if is a variable initialization
        # Variable initialization has an expression after the variable name
        # e.g: $current_frame(<0-3>)
        if json_string[var_end_pos] == "(":

            if variable_name in variables:
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

        #print(f"variable_declaration: {variable_name}")

    # now replace the variables in the job task string with their values
    if not declared_range_size:
        raise RangeSizeNotDefinedError(
            "Range size is not defined. Please check the variable declarations."
        )

    generated_tasks: list[dict[str, Any]] = []

    for i in range(declared_range_size):
        task_raw = json_string
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


# if __name__ == "__main__":
#     job_task = test_task
#     parsed_job_task = parse_job_task(job_task)
    
#     print(parsed_job_task)
