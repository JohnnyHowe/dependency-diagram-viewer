
import argparse
import os

from project import Project
from json_writer import write


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path")
    parser.add_argument("output_path")
    args = parser.parse_args()

    if not os.path.exists(args.project_path):
        print(f"File \"{args.project_path}\" does not exist")
        return

    proj = Project(args.project_path)
    write(args.output_path, proj)

if __name__ == "__main__":
    main()