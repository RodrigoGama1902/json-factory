from typing import Any

import pytest

import json_factory

# =====================
# Fixtures
# =====================


@pytest.fixture
def simple_range_operator_json_string() -> str:
    """A simple JSON string with a variable reference."""
    return """{
  "name": "test_job",
  "tasks": [
        {
            "name": "simple_range",
            "plugin_args": {
                "frame_start": $simple_range(<2>),
                "frame_end" : $simple_range
            }
        }
    ]
}"""


@pytest.fixture
def expected_simple_range_operator_json_result() -> list[dict[str, Any]]:
    """Expected result after processing the simple JSON string."""
    return [
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "simple_range",
                    "plugin_args": {"frame_start": 0, "frame_end": 0},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "simple_range",
                    "plugin_args": {"frame_start": 1, "frame_end": 1},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "simple_range",
                    "plugin_args": {"frame_start": 2, "frame_end": 2},
                }
            ],
        },
    ]


@pytest.fixture
def custom_range_operator_json_string() -> str:
    """A simple JSON string with a variable reference."""
    return """{
  "name": "test_job",
  "tasks": [
        {
            "name": "custom_range",
            "plugin_args": {
                "frame_start": $custom_range(<9-11>),
                "frame_end" : $custom_range
            }
        }
    ]
}"""


@pytest.fixture
def expected_custom_range_operator_json_result() -> list[dict[str, Any]]:
    """Expected result after processing the simple JSON string."""
    return [
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "custom_range",
                    "plugin_args": {"frame_start": 9, "frame_end": 9},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "custom_range",
                    "plugin_args": {"frame_start": 10, "frame_end": 10},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "custom_range",
                    "plugin_args": {"frame_start": 11, "frame_end": 11},
                }
            ],
        },
    ]


@pytest.fixture
def step_range_operator_json_string() -> str:
    """A simple JSON string with a variable reference."""
    return """{
  "name": "test_job",
  "tasks": [
        {
            "name": "step_range",
            "plugin_args": {
                "frame_start": $step_range(<4{2}>),
                "frame_end" : $step_range
            }
        }
    ]
}"""


@pytest.fixture
def expected_step_range_operator_json_result() -> list[dict[str, Any]]:
    """Expected result after processing the simple JSON string."""
    return [
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "step_range",
                    "plugin_args": {"frame_start": 0, "frame_end": 0},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "step_range",
                    "plugin_args": {"frame_start": 2, "frame_end": 2},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "step_range",
                    "plugin_args": {"frame_start": 4, "frame_end": 4},
                }
            ],
        },
    ]


@pytest.fixture
def step_custom_range_operator_json_string() -> str:
    """A simple JSON string with a variable reference."""
    return """{
  "name": "test_job",
  "tasks": [
        {
            "name": "step_custom_range",
            "plugin_args": {
                "frame_start": $step_custom_range(<2-6{2}>),
                "frame_end" : $step_custom_range
            }
        }
    ]
}"""


@pytest.fixture
def expected_step_custom_range_operator_json_result() -> list[dict[str, Any]]:
    """Expected result after processing the simple JSON string."""
    return [
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "step_custom_range",
                    "plugin_args": {"frame_start": 2, "frame_end": 2},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "step_custom_range",
                    "plugin_args": {"frame_start": 4, "frame_end": 4},
                }
            ],
        },
        {
            "name": "test_job",
            "tasks": [
                {
                    "name": "step_custom_range",
                    "plugin_args": {"frame_start": 6, "frame_end": 6},
                }
            ],
        },
    ]


# =====================
# Tests
# =====================


def test_simple_range_operator_processing(
    simple_range_operator_json_string: str,
    expected_simple_range_operator_json_result: list[dict[str, Any]],
):
    """Test the processing of a simple JSON string with variable references."""
    result = json_factory.from_string(simple_range_operator_json_string)
    assert (
        result == expected_simple_range_operator_json_result
    ), f"Expected {expected_simple_range_operator_json_result}, but got {result}"


def test_custom_range_operator_processing(
    custom_range_operator_json_string: str,
    expected_custom_range_operator_json_result: list[dict[str, Any]],
):
    """Test the processing of a simple JSON string with variable references."""
    result = json_factory.from_string(custom_range_operator_json_string)
    assert (
        result == expected_custom_range_operator_json_result
    ), f"Expected {expected_custom_range_operator_json_result}, but got {result}"


def test_step_range_operator_processing(
    step_range_operator_json_string: str,
    expected_step_range_operator_json_result: list[dict[str, Any]],
):
    """Test the processing of a simple JSON string with variable references."""
    result = json_factory.from_string(step_range_operator_json_string)
    assert (
        result == expected_step_range_operator_json_result
    ), f"Expected {expected_step_range_operator_json_result}, but got {result}"


def test_step_custom_range_operator_processing(
    step_custom_range_operator_json_string: str,
    expected_step_custom_range_operator_json_result: list[dict[str, Any]],
):
    """Test the processing of a simple JSON string with variable references."""
    result = json_factory.from_string(step_custom_range_operator_json_string)
    assert (
        result == expected_step_custom_range_operator_json_result
    ), f"Expected {expected_step_custom_range_operator_json_result}, but got {result}"
