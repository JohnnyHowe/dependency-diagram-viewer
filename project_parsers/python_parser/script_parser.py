
import re


def get_imports(file_contents: str):
    imports = []
    for line in file_contents.splitlines():
        line = line.strip()
        if line.startswith(("import", "from")):
            imports.append(_get_full_import_from_line(line))
    return imports


def _get_full_import_from_line(line: str) -> str:
    if line.startswith("import"):
        return line[6:].strip()
    elif line.startswith("from"):
        match = re.match("from (.+) import (.+)", line)
        return match.group(1)


def is_import_path_match(recreated_path, path_from_import):
    #print((recreated_path, path_from_import))
    return recreated_path == path_from_import