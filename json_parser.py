import json
import os


def update_file(file_path, project_dict: dict):
	if os.path.exists(file_path):
		read = read_file_as_dict(file_path)
		add_missing_dict_values(project_dict, read)
	
	json_txt = json.dumps(project_dict, indent=4)
	with open(file_path, "w") as file:
		file.write(json_txt)


def read_file_as_dict(file_path) -> dict:
	with open(file_path, "r") as file:
		return json.loads(file.read())


def add_missing_dict_values(to_modify: dict, new_values: dict):
	for key in new_values.keys():
		if key not in to_modify:
			to_modify[key] = new_values[key]

	for key, value in to_modify.items():
		if isinstance(value, list):
			add_missing_dict_values_list(to_modify[key], new_values[key])


def add_missing_dict_values_list(to_modify, new_values):
	for item in to_modify:
		if not isinstance(item, dict):
			return
		
		match_from_new = get_dictionary_with_value_from_list(new_values, "path", item["path"])
		if match_from_new:
			add_missing_dict_values(item, match_from_new)


def get_dictionary_with_value_from_list(l, key, value):
	for item in l:
		if not isinstance(item, dict): continue
		if key in item:
			if item[key] != value: continue
			return item
	return None
