import argparse
import os

import pygame

from diagram_viewer import DiagramViewer
from project_parsers.unity_parser.json_writer import write
from project_parsers.unity_parser.project import Project
from window_engine.window import Window

project_path = None
output_path = None
diagram_viewer = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path")
    parser.add_argument("output_path")
    args = parser.parse_args()

    global project_path
    project_path = args.project_path
    global output_path
    output_path = args.output_path

    if not os.path.exists(project_path):
        print(f"File \"{project_path}\" does not exist")
        return

    _recreate_diagram_file()
    Window().update_callbacks.add(_on_update)
    _restart_viewer()


def _on_update():
    for event in Window().pygame_events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                _restart()


def _restart():
    _recreate_diagram_file()
    _restart_viewer()


def _recreate_diagram_file():
    proj = Project(project_path)
    write(output_path, proj)


def _restart_viewer():
    global diagram_viewer
    if diagram_viewer:
        diagram_viewer.running = False
    diagram_viewer = DiagramViewer(output_path)


if __name__ == "__main__":
    main()