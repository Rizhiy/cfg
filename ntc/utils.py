import importlib.util
import logging
import sys
from pathlib import Path
from types import ModuleType
from typing import Set

import yaml

from .errors import ModuleError

LOGGER = logging.getLogger(__name__)


def import_module(module_path: Path) -> ModuleType:
    package = _load_package(module_path.parent)
    module_name = module_path.stem
    if package:
        module_name = ".".join((package, module_name))

    return _load_module(module_name, module_path)


def merge_cfg_module(module: ModuleType, imported_modules: Set[str] = None) -> None:
    lines = []
    if imported_modules is None:
        imported_modules = set()
    module_name = module.__spec__.name
    if module_name in imported_modules:
        return

    module_path = Path(module.__file__)

    with module_path.open() as module_file:
        module_file = list(module_file)
        if "cfg = CN(cfg)\n" not in module_file:
            raise ModuleError("Can't find config definition, please import config schema using absolute path")
        lines.append(f"# START --- {module_path} ---\n")
        for line_idx, line in enumerate(module_file):
            if line.startswith("from "):
                _, import_path, __, *imports = line.strip().split(" ")
                imported_module = importlib.import_module(import_path, package=module.__package__)
                if imported_module.__spec__.name in imported_modules:
                    continue
                if import_path.startswith("."):
                    if imports == ["cfg"]:
                        lines.extend(merge_cfg_module(imported_module, imported_modules=imported_modules))
                    else:
                        raise ModuleError(f"Only cfg can be imported relatively:\n{module_path}+{line_idx}:{line}")
                else:
                    lines.append(line)
            else:
                lines.append(line)
        lines.append(f"# END --- {module_path} ---\n")

    imported_modules.add(module_name)
    return lines


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


def full_type_name(_type) -> str:
    module = _type.__module__
    class_name = _type.__name__
    if module is None or module == str.__class__.__module__:
        return class_name  # Avoid reporting __builtin__
    else:
        return f"{module}.{class_name}"


def full_class_name(obj) -> str:
    return full_type_name(obj.__class__)
