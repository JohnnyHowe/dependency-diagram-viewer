import json
import os
import re


def update_file(file_path, new_project_dict: dict):
	if os.path.exists(file_path):
		old = _read_file_as_dict(file_path)
		_merge_projects(new_project_dict, old)
	
	json_txt = json.dumps(new_project_dict, indent=4)
	with open(file_path, "w") as file:
		file.write(json_txt)


def _read_file_as_dict(file_path) -> dict:
	with open(file_path, "r") as file:
		return json.loads(file.read())


def _merge_projects(new: dict, old: dict):
	new_items = _get_all_items(new)
	old_items = _get_all_items(old)

	for item in new_items:
		match = _get_match(item, old_items)
		if match:
			_overwrite_diagram_only_data(item, match)


log = False
def _get_match(item: dict, all_items):
	log = "craftingmanager" in item["path"].lower()
	if log: print(f"\nLooking for match for {item}")
	candidates = []
	for item2 in all_items:
		if item["name"] == item2["name"]:
			candidates.append(item2)

	if log:
		print("Found no candidates!")
	if len(candidates) == 0:
		return None

	# sort candidates by how similar path is from root
	scores = []
	for candidate in candidates:
		key = "full_name" if ("full_name" in item and "full_name" in candidate) else "path"
		scores.append(_get_similarity_heuristic(item[key], candidate[key]))
	
	index_of_max = scores.index(max(scores))
	return candidates[index_of_max]	


def _get_similarity_heuristic(path1: str, path2: str):
	split_pattern = r"[\.\/\\]"
	parts1 = re.split(split_pattern, path1)
	parts2 = re.split(split_pattern, path2)

	score = 0

	max_iteration = min(len(parts1), len(parts2))
	for i in range(max_iteration):
		if parts1[i] == parts2[i]:
			score += 1
		else:
			break

	for i in range(max_iteration):
		if parts1[-i] == parts2[-i]:
			score += 1
		else:
			break

	max_score = len(path1) + len(path2)
	score = score / max_score

	if log:
		print(path1, path2, score)

	return score


def _overwrite_diagram_only_data(to_change: dict, other: dict):
	for key in other.keys():
		if key not in ["name", "full_name", "path", "folders", "scripts", "dependencies"]:
			to_change[key] = other[key]


def _get_all_items(d: dict) -> list[dict]:
	items = [d]
	for item in d.get("folders", []) + d.get("scripts", []):
		items += _get_all_items(item)
	return items