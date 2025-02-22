from coco_eval_tools.utils import sort_paths_by_number, parse_eval_line


# --- Test for utils.py ---

def test_sort_paths_by_number():
    # Test with a mix of numbers in the filenames
    paths = [
        "file_2.json",
        "file_10.json",
        "file_1.json",
        "file_20.json"
    ]
    sorted_paths = sort_paths_by_number(paths)
    expected_sorted_paths = [
        "file_1.json",
        "file_2.json",
        "file_10.json",
        "file_20.json"
    ]
    assert sorted_paths == expected_sorted_paths


def test_parse_eval_line():
    # Test valid line
    line = "AP = 0.50"
    key, value = parse_eval_line(line)
    assert key == "AP"
    assert value == 0.50
    
    # Test invalid line
    line = "Invalid Line"
    key, value = parse_eval_line(line)
    assert key is None
    assert value is None



# --- Test for coco_eval_tool.py ---
