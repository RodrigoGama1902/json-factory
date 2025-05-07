from typing import Any

import pytest

import json_factory


@pytest.fixture
def simple_json_string() -> str:
    """A simple JSON string with a variable reference."""
    return """{
  "name": "test_job",
  "tasks": [
    {
      "name": "task1",
      "plugin_args": {
        "frame_start": $current_frame(<9-11>),
        "frame_end" : $current_frame
      }
    }
  ]
}"""


@pytest.fixture
def expected_simple_json_result() -> list[dict[str, Any]]:
    """Expected result after processing the simple JSON string."""
    return [
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "task1",
                    "plugin_args": {"frame_start": 9, "frame_end": 9},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "task1",
                    "plugin_args": {"frame_start": 10, "frame_end": 10},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "task1",
                    "plugin_args": {"frame_start": 11, "frame_end": 11},
                }
            ],
        },
    ]


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


def test_simple_processing(
    simple_json_string: str, expected_simple_json_result: list[dict[str, Any]]
):
    """ "Test the processing of a simple JSON string with variable references."""
    result = json_factory.from_string(simple_json_string)
    assert (
        result == expected_simple_json_result
    ), f"Expected {expected_simple_json_result}, but got {result}"


def test_standard_processing(
    standard_json_string: str,
    expected_standard_json_result: list[dict[str, Any]],
):
    """Test the processing of a standard JSON string without variable references."""
    result = json_factory.from_string(standard_json_string)
    assert (
        result == expected_standard_json_result
    ), f"Expected {expected_standard_json_result}, but got {result}"
