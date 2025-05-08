import sys
from pprint import pprint

sys.path.append("src")

import json_factory

json_string = """{
  "name": "test_job_$frame(<0-10>).zfill(5)",
  "plugin_args" : {
    "frame_string" : $frame.zfill(5).to_string(),
    "frame_start" : $frame,
    "frame_end" : $frame
  }
}"""

pprint(json_factory.from_string(json_string))
