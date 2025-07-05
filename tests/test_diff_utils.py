from mcp_config_hub import diff_utils

def test_generate_config_diff_no_diff():
    a = {"x": 1, "y": 2}
    b = {"x": 1, "y": 2}
    diff = diff_utils.generate_config_diff(a, b, "tool")
    assert diff is None

def test_generate_config_diff_with_diff():
    a = {"x": 1, "y": 2}
    b = {"x": 1, "y": 3}
    diff = diff_utils.generate_config_diff(a, b, "tool")
    assert diff is not None
    assert "-  \"y\": 2" in diff
    assert "+  \"y\": 3" in diff

def test_has_changes_true():
    a = {"x": 1}
    b = {"x": 2}
    assert diff_utils.has_changes(a, b)

def test_has_changes_false():
    a = {"x": 1}
    b = {"x": 1}
    assert not diff_utils.has_changes(a, b)
