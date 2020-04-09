import pytest

def static_init(cls):
    """
    This is implements the static init marker that returns a static class with
    static class variables defined in the class' static_init() method.

    :param cls: class that is calling it's static_init
    :return: static instance of the class
    """
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls

@static_init
class TestDataBuilder():
    """
    Statuc class that Builds payloads to be used as the test body in simulated
    HTTP requests from IOEX models

    """

    @classmethod
    def static_init(cls):
        payload = {}
        ret_val = None
        setattr(cls, 'payload', payload)
        setattr(cls, 'ret_val', ret_val)
        payload.update(payload1 = "test_payload1")
        cls.set_ret_val()


    @classmethod
    def set_ret_val(cls):
        cls.ret_val = "expected_ret_val"


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

class TestClass:

    @classmethod
    def setup_class(cls):
        cls.second_val = "set_up_second"

    def test_one(self, set_up_second):
        assert set_up_second["var1"] == "set_up_first"

    def test_two(self, set_up_second):
        assert set_up_second["var2"] == "set_up_second"

    def test_three(self, set_up_second):
        assert set_up_second["var3"] == "got var"

    def test_four(self, set_up_second, set_up_first):
        assert set_up_second["var2"] == "set_up_second"

    def test_five(self, set_up_second, set_up_first):
            assert set_up_first["var1"] == "set_up_first"

    @pytest.mark.parametrize("value1,value2", [("one", get_value_one()),
                                                       ("two", get_value_two()),
                                                       ("three", "three")])
    def test_six(self, value1, value2):
        assert value1 == value2, "Failed on {}".format(value1)

    parameter_values = [("test7", TestDataBuilder.payload["payload1"])]
    @pytest.mark.parametrize("testid, payload", parameter_values)
    def test_seven(self, testid, payload):
        assert payload == "test_payload1", "{} failed".format(testid)

    parameter_values = [("test8", TestDataBuilder.ret_val)]
    @pytest.mark.parametrize("testid, ret_val", parameter_values)
    def test_eight(self, testid, ret_val):
        assert ret_val == "expected_ret_val", "{} failed".format(testid)