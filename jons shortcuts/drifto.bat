set output="C:/Users/Work/Documents/Projects/drifto/drifto.json"

python "project_parsers/unity_parser/parse_unity_project.py" "C:/Users/Work/Documents/Projects/drifto/Assets/Scripts" %output%
python "C:\Users\Work\Documents\Projects\dependency-diagram-viewer\main.py" %output%