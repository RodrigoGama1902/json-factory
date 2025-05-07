# json-factory

**json-factory** is a Python package that enables the dynamic creation of multiple JSON objects from a custom syntax. It interprets special markers within JSON strings and expands them to generate data combinations according to defined rules.

Currently, the `<min-max>` operator is supported, allowing you to expand a value within a numeric range.

## ✨ Features

With **json-factory**, you can:

- Define a JSON with special placeholders.
- Use the `json_factory.from_string()` function to generate multiple JSON objects based on the rules.
- Automate the creation of tasks, configurations, or repetitive structures.

## 📦 Installation

```bash
pip install json-factory
````

Or, for local installation:

```bash
git clone https://github.com/RodrigoGama1902/json-factory.git
cd json-factory
pip install .
```

## 🧪 Example Usage

### Input

```json
{
  "name": "test_job",
  "tasks": [
    {
      "name": "task1",
      "plugin_args": {
        "frame_start": $current_frame(<9-11>),
        "frame_end": $current_frame
      }
    }
  ]
}
```

### Generated Output

```python
[
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
```

## 🔧 Custom Syntax

Currently, the following elements are supported:

* **Range placeholder**:
  `$variable_name(<min-max>)`
  Generates multiple instances with values in the specified range.

* **Variable reference**:
  `$variable_name`
  Reuses the current value of a previously defined variable in the same scope.

## 📚 API

```python
import json_factory

json_string = '...'
results = json_factory.from_string(json_string)
```

* `from_string(json_string: str) -> List[dict]`
  Returns a list of dictionaries with the generated JSON objects.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

