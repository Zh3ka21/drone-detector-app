import os
import re

def sort_paths_by_number(paths: list[str]) -> list[str]:
    """
    Sorts a list of paths by the numeric values embedded in the filenames.
    If no number is found in a filename, the path is considered to have a value of infinity
    and will appear at the end of the sorted list.
    
    Parameters:
    - paths (list of str): List of paths to files.
    
    Returns:
    - List of paths sorted by the numeric value found in the filenames.
    """
    def extract_number(path: str) -> int:
        # Find the first number in the path, or return a large value if no number is found
        numbers = re.findall(r'\d+', path)
        return int(numbers[0]) if numbers else float('inf')
    
    return sorted(paths, key=extract_number)

def find_json_files(directory: str):
    """
    Helper function to find all JSON files in a directory.
        
    Parameters:
    - directory (str): Path to the directory to search for JSON files.
        
    Returns:
    - List of paths to JSON files in the directory.
    """
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.json')]

def parse_eval_line(line):
    """
    Parses a line of text in the format "metric = value", extracting the metric name and value.
    
    Parameters:
    - line (str): Line to parse.
    
    Returns:
    - Tuple (str, float): Key-value pair (metric name, value), or (None, None) if parsing fails.
    """
    match = re.match(r'(.+?) = ([\d\.\-]+)', line)
    if match:
        key = match.group(1).strip()
        value = float(match.group(2).strip())
        return key, value
    return None, None


