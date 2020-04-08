import pytest

def get_var():
    return "got var"

@pytest.fixture(scope="module")
def set_up_first():
    var1 = "set_up_first"
    var3 = get_var()
    fixture_dict = {"var1": var1,
                    "var3": var3}

    yield fixture_dict


@pytest.fixture(scope="module")
def set_up_second(set_up_first):
    var2 = "set_up_second"

    set_up_first.update({"var2": var2})

    yield set_up_first

def get_value_one():
    return "one"

def get_value_two():
    return "two"

def test_one(set_up_second):
    assert set_up_second["var1"] == "set_up_first"

def test_two(set_up_second):
    assert set_up_second["var2"] == "set_up_second"

def test_three(set_up_second):
    assert set_up_second["var3"] == "got var"

def test_four(set_up_second, set_up_first):
    assert set_up_second["var2"] == "set_up_second"

def test_five(set_up_second, set_up_first):
        assert set_up_first["var1"] == "set_up_first"

@pytest.mark.parametrize("value", [get_value_one(), get_value_two(), "three"])
def test_six(value):
    assert "wrong" == value, "Failed on {}".format(value)