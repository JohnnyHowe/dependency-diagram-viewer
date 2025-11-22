from pathlib import Path


def ignore_path(path: str):
    parts = Path(path).parts

    for part in parts:
        if ignore_path_part(part):
            return True
        
    return False


def ignore_path_part(part: str):
    if part.startswith("."): 
        return True
    return False