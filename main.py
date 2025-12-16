import argparse
import os
from diagram_viewer import DiagramViewer
from project_parsers.python_parser.parser import Parser as PythonParser
from project_parsers.csharp_namespace_parser.parser import Parser as CSharpParser
from project_parsers.godot.godot_parser import GodotParser

parsers = {
    "python": PythonParser,
    "csharp": CSharpParser,
    "godot": GodotParser,
}


def _main():
    parser_name = argparse.ArgumentParser()
    parser_name.add_argument("parser")
    parser_name.add_argument("project_path")
    parser_name.add_argument("output_path")
    args = parser_name.parse_args()

    if not args.parser in parsers.keys():
        print(f"No parser named \"{args.parser}\". Use one of the following.")
        for parser_name in parsers.keys():
            print("  - " + parser_name)
        return

    if not os.path.exists(args.project_path):
        print(f"Project path \"{args.project_path}\" doesn't exist!")
        return

    parser = parsers[args.parser](args.project_path, args.output_path)
    #parser.update_dependencies_file()
    DiagramViewer(parser)


if __name__ == "__main__":
    _main()