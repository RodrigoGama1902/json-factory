from typing import Any

import pytest

import json_factory

# =====================
# Fixtures
# =====================


@pytest.fixture
def list_operator_json_string() -> str:
    """A simple JSON string with a variable reference."""
    return """{
  "name": "test_job",
  "tasks": [
    {
      "name": "task1",
      "plugin_args": {
        "frame_start": $current_frame([0,2,5,6]),
        "frame_end" : $current_frame
      }
    }
  ]
}"""


@pytest.fixture
def expected_list_operator_json_result() -> list[dict[str, Any]]:
    """Expected result after processing the simple JSON string."""
    return [
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "task1",
                    "plugin_args": {"frame_start": 0, "frame_end": 0},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "task1",
                    "plugin_args": {"frame_start": 2, "frame_end": 2},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "task1",
                    "plugin_args": {"frame_start": 5, "frame_end": 5},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "task1",
                    "plugin_args": {"frame_start": 6, "frame_end": 6},
                }
            ],
        },
    ]


# =====================
# Tests
# =====================


def test_list_operator_processing(
    list_operator_json_string: str,
    expected_list_operator_json_result: list[dict[str, Any]],
):
    """Test the processing of a JSON string with list operator."""
    result = json_factory.from_string(list_operator_json_string)
    assert (
        result == expected_list_operator_json_result
    ), f"Expected {expected_list_operator_json_result}, but got {result}"
