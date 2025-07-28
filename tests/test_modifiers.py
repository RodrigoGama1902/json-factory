
import json_factory


def test_to_string_modifier():
    
    json_string = """{
        "param1" : $var1(<2>).to_string(),
        "param2" : $var1,
        "param3" : $var2(<5-7>),
        "param4" : $var2.zfill(3).to_string(),
        "param5" : $var2,
        "param6" : $var2.zfill(3).to_int()
    }"""
    
    expected_result = [
        {
            "param1" : "0",
            "param2" : 0,
            "param3" : 5,
            "param4" : "005",
            "param5" : 5,
            "param6" : 5
        },
        {
            "param1" : "1",
            "param2" : 1,
            "param3" : 6,
            "param4" : "006",
            "param5" : 6,
            "param6" : 6
        },
        {
            "param1" : "2",
            "param2" : 2,
            "param3" : 7,
            "param4" : "007",
            "param5" : 7,
            "param6" : 7
        }
    ]
    
    assert json_factory.from_string(json_string) == expected_result