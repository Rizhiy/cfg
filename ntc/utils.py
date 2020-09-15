import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def import_module(module_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("tests" + "." + "data", module_path.parent / "__init__.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    spec = importlib.util.spec_from_file_location("tests" + "." + "data" + "." + module_path.stem, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
