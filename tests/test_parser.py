import pytest
from typing import Any

from parser import process

@pytest.fixture
def simple_json_string() -> str:
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
    
    return [
        {
            "name": "test_job",
            "tasks": [
                {
                "name": "task1",
                "plugin_args": {
                    "frame_start": 9,
                    "frame_end" : 9
                }
                }
            ]
        },
        {
            "name": "test_job",
            "tasks": [
                {
                "name": "task1",
                "plugin_args": {
                    "frame_start": 10,
                    "frame_end" : 10
                }
                }
            ]
        },
        {
            "name": "test_job",
            "tasks": [
                {
                "name": "task1",
                "plugin_args": {
                    "frame_start": 11,
                    "frame_end" : 11
                }
                }
            ]
        }, 
    ]
    

def test_simple_processing(simple_json_string : str, expected_simple_json_result : list[dict[str, Any]]):
    
    result = process(simple_json_string)
    assert result == expected_simple_json_result, f"Expected {expected_simple_json_result}, but got {result}"
    
    
    
    
    
    
    

