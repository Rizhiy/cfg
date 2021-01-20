from pathlib import Path

import pytest

from ntc import CN, MissingRequired, ModuleError, SchemaError, SchemaFrozenError, TypeMismatch

DATA_DIR = Path(__file__).parent / "data" / "bad"


def test_bad_type():
    with pytest.raises(TypeMismatch):
        CN.load(DATA_DIR / "bad_type.py")


def test_bad_attr():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "bad_attr.py")


def test_bad_class():
    with pytest.raises(TypeMismatch):
        CN.load(DATA_DIR / "bad_class.py")


def test_bad_node():
    with pytest.raises((TypeMismatch, SchemaError)):
        CN.load(DATA_DIR / "bad_node.py")


def test_bad_node_subclass():
    with pytest.raises(TypeMismatch):
        CN.load(DATA_DIR / "bad_node_subclass.py")


def test_bad_node_required_subclass():
    with pytest.raises(MissingRequired):
        CN.load(DATA_DIR / "bad_node_required_subclass.py")


def test_bad_node_nested_subclass():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_node_nested_subclass.py")


def test_bad_node_instance():
    with pytest.raises((TypeMismatch, SchemaError)):
        CN.load(DATA_DIR / "bad_node_instance.py")


def test_inheritance_changes_bad():
    with pytest.raises(TypeMismatch):
        CN.load(DATA_DIR / "inheritance_changes_bad.py")


def test_bad_inherit():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_inherit_changes.py")


def test_bad_inherit_subclass():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_inherit_subclass_changes.py")
    assert str(excinfo.value) == "Leaf must be an instance of <class 'tests.data.base_class.BaseClass'>"


def test_bad_inherit_instance():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_inherit_instance_changes.py")


def test_bad_inherit_subclass_instance():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_inherit_subclass_instance_changes.py")


def test_bad_inherit_subclass_class():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_inherit_subclass_class_changes.py")
    assert str(excinfo.value) == "Leaf must be an instance of <class 'tests.data.base_class.BaseClass'>"


def test_schema_freeze():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_schema.py")


def test_bad_init():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_init.py")
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_init_2.py")


def test_bad_cfg_import():
    with pytest.raises(ModuleError):
        CN.load(DATA_DIR / "bad_cfg_import.py")


def test_bad_import():
    with pytest.raises(ModuleError):
        CN.load(DATA_DIR / "bad_import.py")
