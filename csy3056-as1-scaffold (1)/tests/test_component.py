from src.component import process_value


def test_process_value_returns_input():
    assert process_value("test") == "test"