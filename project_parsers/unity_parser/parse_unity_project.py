
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

    parse(args.project_path, args.output_path)


def parse(project_path, output_path):
    proj = Project(project_path)
    write(output_path, proj)
    

if __name__ == "__main__":
    main()