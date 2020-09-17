import ast
import astor
import inspect
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def import_module(module_path: Path) -> ModuleType:
    # TODO: resolve it generally, not for tests
    spec = importlib.util.spec_from_file_location("tests" + "." + "data", module_path.parent / "__init__.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    spec = importlib.util.spec_from_file_location("tests" + "." + "data" + "." + module_path.stem, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def merge_module(module: ModuleType, output_path: Path, clean: bool = True) -> None:
    if clean:
        output_path.unlink(missing_ok=True)

    module_path = Path(module.__file__)
    # raise RuntimeError(_merge_source(module))

    with module_path.open() as module_file:
        _append_to_file(output_path, f"# START --- {module_path} ---\n")
        for line in module_file:
            if line.startswith("from "):
                import_members = line.strip().split(" ")
                if import_members[3] == "cfg":
                    imported_module = importlib.import_module(import_members[1], package=module.__package__)
                # if imported_module.__spec__.loader.is_package(imported_module.__spec__.name):
                #     pass
                # else:
                # if not _is_builtin_module(imported_module):
                    merge_module(imported_module, output_path, clean=False)
                else:
                    _append_to_file(output_path, line)
            # if "import " not in line:
            else:
                _append_to_file(output_path, line)
        _append_to_file(output_path, f"# END --- {module_path} ---\n")


def _merge_source(module: ModuleType) -> ast.AST:
    module_path = Path(module.__file__)

    with module_path.open() as module_file:
        source = module_file.read()
        ast_node = ast.parse(source)
        ast.fix_missing_locations(ast_node)
        raise RuntimeError(astor.to_source(ast_node))


def _is_module_package(module: ModuleType) -> bool:
    return module.__spec__.loader.is_package(module.__spec__.name)


def _is_builtin_module(module: ModuleType) -> bool:
    for path_dir in sys.path[1:]:
        if module.__file__.startswith(path_dir):
            return True
    return False


def _append_to_file(output_path: Path, data: str) -> None:
    with output_path.open("a") as output_file:
        output_file.write(data)
