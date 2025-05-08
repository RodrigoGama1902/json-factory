import sys

sys.path.append("src")

import json_factory

json_string = """{
  "name": "test_job",
  "tasks": [
    {
      "name": "task1",
      "plugin_args": {
        "frame_start": $current_frame(<0-3>),
        "frame_end" : $current_frame.zfill(4).to_string()
      }
    }
  ]
}"""

print(json_factory.from_string(json_string))