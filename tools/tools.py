import json

def load_json_file(file_path):
    """
    Load a JSON file with UTF-8 encoding.
    
    Parameters
    ----------
    file_path : str
        The path to the JSON file.
        
    Returns
    -------
    dict
        The loaded JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")