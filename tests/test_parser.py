

from json_factory.parser import _replace_variable_with_value


def test_replace_variable_with_value():
    
    string_value = "1xe $teste.teste([0,1,2]).test([],,,), , 2xe"
    expected_result = "1xe '2', , 2xe"
    expected_offset = -30
    
    result, offset = _replace_variable_with_value(string_value, 4, "'2'")

    assert offset == expected_offset
    assert result == expected_result