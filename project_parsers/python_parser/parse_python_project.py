import argparse
import os

from .folder import Folder
import json_parser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path")
    parser.add_argument("output_path")
    args = parser.parse_args()
    parse(args.project_path, args.output_path)


def parse(project_path, output_path):
    if not os.path.exists(project_path):
        print(f"File \"{project_path}\" does not exist")
        return

    root = Folder(project_path)
    d = root.as_dict()
    json_parser.update_file(output_path, d)


if __name__ == "__main__":
    main()