import argparse
import os
from diagram_viewer import DiagramViewer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"File \"{args.path}\" does not exist")
        return

    DiagramViewer(args.path)


if __name__ == "__main__":
    main()