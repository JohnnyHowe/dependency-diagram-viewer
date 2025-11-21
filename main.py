from diagram_viewer import DiagramViewer
from project_parsers.python_parser.parse_python_project import parse

parse("./", "./this.json")
DiagramViewer("./this.json")
