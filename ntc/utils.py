import importlib.util
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Set, Union

import yaml

logger = logging.getLogger(__name__)


def import_module(module_path: Union[Path, str]) -> ModuleType:
    if isinstance(module_path, str):
        module_path = Path(module_path)
    package = _load_package(module_path.parent)
    module_name = module_path.stem
    if package:
        module_name = ".".join((package, module_name))

    return _load_module(module_name, module_path)


def merge_cfg_module(
    module: Union[ModuleType, Path, str], output_path: Path, clean: bool = True, imported_modules: Set[str] = None
) -> None:
    if imported_modules is None:
        imported_modules = set()
    module_name = module.__spec__.name
    if module_name in imported_modules:
        return
    if clean:
        output_path.unlink(missing_ok=True)

    module_path = Path(module.__file__)

    with module_path.open() as module_file:
        _append_to_file(output_path, f"# START --- {module_path} ---\n")
        for line in module_file:
            if line.startswith("from "):
                import_members = line.strip().split(" ")
                imported_module = importlib.import_module(import_members[1], package=module.__package__)
                if imported_module.__spec__.name in imported_modules:
                    continue
                if import_members[3] == "cfg":
                    merge_cfg_module(imported_module, output_path, clean=False, imported_modules=imported_modules)
                elif import_members[1].startswith("."):
                    logger.debug(f"Skipping non cfg relative import {line}")
                else:
                    _append_to_file(output_path, line)
            else:
                _append_to_file(output_path, line)
        _append_to_file(output_path, f"# END --- {module_path} ---\n")

    imported_modules.add(module_name)


def add_yaml_str_representer():
    def obj_representer(dumper, data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))

    yaml.add_multi_representer(object, obj_representer)


def _load_module(module_name: str, module_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


def _load_package(package_path: Path) -> str:
    init_path = package_path / "__init__.py"
    if not init_path.exists():
        return ""
    package_name = package_path.stem
    parent_package_name = _load_package(package_path.parent)
    if parent_package_name:
        package_name = ".".join((parent_package_name, package_name))
    _load_module(package_name, init_path)

    return package_name


def _append_to_file(output_path: Path, data: str) -> None:
    with output_path.open("a") as output_file:
        output_file.write(data)
