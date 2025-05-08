

from json_factory.parser import _replace_variable_with_value, from_string


def test_replace_variable_with_value():
    
    string_value = "1xe $teste.teste([0,1,2]).test([],,,), , 2xe"
    expected_result = "1xe '2', , 2xe"
    
    result = _replace_variable_with_value(string_value, 4, "'2'")

    assert result == expected_result
    
def test_multiple_variables():
    
    json_string = """{
        "param1" : $var1(<2>),
        "param2" : $var1,
        "param3" : $var2(<5-7>),
        "param4" : $var2
    }"""
    
    expected_result = [
        {
            "param1" : 0,
            "param2" : 0,
            "param3" : 5,
            "param4" : 5,  
        },
        {
            "param1" : 1,
            "param2" : 1,
            "param3" : 6,
            "param4" : 6,  
        },
        {
            "param1" : 2,
            "param2" : 2,
            "param3" : 7,
            "param4" : 7,  
        }
    ]
    
    assert from_string(json_string) == expected_result