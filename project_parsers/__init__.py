from .csharp_asmdef_parser.parser import Parser as CSharpAsmdefParser
from .csharp_namespace_parser.parser import Parser as CSharpNamespaceParser
from .python_parser.parser import Parser as PythonParser
from .godot.godot_parser import GodotParser as GodotParser

parsers = {
    "csharp-asmdef": CSharpAsmdefParser,
    "csharp-namespace": CSharpNamespaceParser,
    "python": PythonParser,
    "godot": GodotParser,
}