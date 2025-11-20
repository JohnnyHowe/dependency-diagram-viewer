import re
import string


def is_script(file_name):
	return file_name.endswith(".cs")


def load_contents(file_path: string) -> string:
	with open(file_path, "r") as file:
		contents = file.read()
		pattern = r'//.*?$|/\*.*?\*/'
		return re.sub(pattern, '', contents, flags=re.MULTILINE | re.DOTALL)


def get_root_members(contents: string) -> list[tuple]:
	"""
	Parse the text and get all the root members (classes, enums, interfaces, namespaces)
	Return in form [(type, name, contents), ...] 
	"""
	
	pattern = re.compile(
		r'(?:public|internal|private|protected|static\s+)?\s*'
		r'(namespace|class|struct|enum|interface|delegate)\s+([\w\.]+)',
		re.MULTILINE
	)

	members = []
	for match in pattern.finditer(contents):
		member_type = match.group(1)
		member_name = match.group(2)
		contents_start_index = match.end()
		if get_bracket_depth(contents, contents_start_index) != 0: continue
		members.append((member_type, member_name, get_member_contents(contents, contents_start_index)))

	return members


def get_bracket_depth(contents, char_index):
	depth = 0
	for i in range(char_index):
		if contents[i] == "{": depth += 1
		elif contents[i] == "}": depth -= 1
	return depth


def get_member_contents(parent_contents: string, start_character_index) -> string:
	bracket_depth = 0
	has_found_first_bracket = False
	start_bracket_index = -1

	char_index = start_character_index
	while bracket_depth > 0 or not has_found_first_bracket:
		if len(parent_contents) <= char_index:
			print("Not all brackets closed???")
			return ""

		if parent_contents[char_index] == "{":
			bracket_depth += 1
			has_found_first_bracket = True
			if start_bracket_index == -1:
				start_bracket_index = char_index
		elif parent_contents[char_index] == "}":
			bracket_depth -= 1

		char_index += 1

	return strip_empty_lines(parent_contents[start_bracket_index + 1: char_index - 1])


def strip_empty_lines(s: str) -> str:
	lines = s.splitlines()
	
	# Remove empty lines at the start
	while lines and lines[0].strip() == '':
		lines.pop(0)
	
	# Remove empty lines at the end
	while lines and lines[-1].strip() == '':
		lines.pop()
	
	return "\n".join(lines)


def get_dependencies(contents: string, all_member_full_namespaces) -> list:
	used = set()
	for full_namespace in all_member_full_namespaces:
		if depends_on(contents, full_namespace):
			used.add(full_namespace)
	return list(used)


def depends_on(contents: string, full_member_namespace: string) -> bool:
	parts = full_member_namespace.split(".")
	member_name = parts[-1]

	if not member_name in contents:
		return False

	# okay, there's a member in the file with the same member name
	# are we using the member from this namespace?

	full_use_of_member_in_code = member_name
	pattern = re.compile(r"([\w.]*)\." + member_name)
	for match in pattern.finditer(contents):
		if not full_member_namespace.endswith(match.group(0)): continue
		full_use_of_member_in_code = match.group(0)

	# is the full namespace referenced in code?
	if full_member_namespace == full_use_of_member_in_code:
		return True

	# does the partial namespace reference connect to a "using x"?
	namespaces_in_use = get_all_namespaces_in_use(contents)
	for namespace in namespaces_in_use:
		if namespace + "." + full_use_of_member_in_code == full_member_namespace:
			return True

	return False


def get_all_namespaces_in_use(contents):
	pattern = r'\s*using\s+(.*?);' 
	namespaces = [""]
	for match in re.finditer(pattern, contents):
		namespaces.append(match.group(1).strip())
	return namespaces