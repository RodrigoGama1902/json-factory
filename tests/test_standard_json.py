from typing import Any

import pytest

import json_factory

# =====================
# Fixtures
# =====================

@pytest.fixture
def standard_json_string() -> str:
    """A standard JSON string without variable references."""
    return """{
  "name": "test_data",
  "tasks": [
    {
      "name": "task1",
      "priority": 0,
      "group": "string",
      "pool": "string",
      "plugin_name": "string",
      "plugin_args": {
        "frame_start": 1,
        "frame_end" : 1
      }
    }
  ]
}"""


@pytest.fixture
def expected_standard_json_result() -> list[dict[str, Any]]:
    """Expected result after processing the standard JSON string."""
    return [
        {
            "name": "test_data",
            "tasks": [
                {
                    "name": "task1",
                    "priority": 0,
                    "group": "string",
                    "pool": "string",
                    "plugin_name": "string",
                    "plugin_args": {"frame_start": 1, "frame_end": 1},
                }
            ],
        }
    ]


# =====================
# Tests
# =====================

def test_standard_processing(
    standard_json_string: str,
    expected_standard_json_result: list[dict[str, Any]],
):
    """Test the processing of a standard JSON string without variable references."""
    result = json_factory.from_string(standard_json_string)
    assert (
        result == expected_standard_json_result
    ), f"Expected {expected_standard_json_result}, but got {result}"
