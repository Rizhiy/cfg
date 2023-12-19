from __future__ import annotations

import re
from pathlib import Path

import pytest

from pycs import CN
from pycs.errors import MissingRequiredError, ModuleError, SchemaError, SchemaFrozenError, TypeMismatchError

DATA_DIR = Path(__file__).parent / "data" / "bad"


def test_bad_type():
    with pytest.raises(TypeMismatchError) as excinfo:
        CN.load(DATA_DIR / "bad_type.py")
    assert (
        str(excinfo.value)
        == "Instance of type <str> expected, but found 1 of type <class 'int'> for CfgLeaf(Good) at cfg.NAME!"
    )


def test_bad_attr():
    with pytest.raises(SchemaFrozenError) as excinfo:
        CN.load(DATA_DIR / "bad_attr.py")
    assert str(excinfo.value) == "Trying to add leaf to node cfg with frozen schema."


def test_bad_class():
    with pytest.raises(TypeMismatchError) as excinfo:
        CN.load(DATA_DIR / "bad_class.py")
    assert re.match(
        r"^Instance of type <tests.data.base_class.BaseClass> expected,"
        r" but found <tests.data.bad.bad_class.BadClass object at 0x[0-9a-f]+>"
        r" of type <class 'tests.data.bad.bad_class.BadClass'>"
        r" for CfgLeaf\(<tests.data.base_class.BaseClass object at 0x[0-9a-f]+>\) at cfg.CLASS!$",
        str(excinfo.value),
    )


def test_bad_node():
    with pytest.raises((TypeMismatchError, SchemaError)) as excinfo:
        CN.load(DATA_DIR / "bad_node.py")
    assert re.match(
        r"^Instance of type <tests.data.base_class.BaseClass> expected,"
        r" but found <tests.data.bad.bad_node.BadClass object at 0x[0-9a-f]+>"
        r" of type <class 'tests.data.bad.bad_node.BadClass'> for CfgLeaf\(None\) at cfg.CLASSES.ONE!$",
        str(excinfo.value),
    )


def test_bad_node_subclass():
    with pytest.raises(TypeMismatchError) as excinfo:
        CN.load(DATA_DIR / "bad_node_subclass.py")
    assert str(excinfo.value) == (
        "Subclass of type <tests.data.base_class.BaseClass> expected,"
        " but found <class 'tests.data.bad.bad_node_subclass.BadSubClass'> of type <class 'type'>"
        " for CfgLeaf(<class 'tests.data.base_class.BaseClass'>) at cfg.SUBCLASS!"
    )


def test_bad_node_required_subclass():
    with pytest.raises(MissingRequiredError) as excinfo:
        CN.load(DATA_DIR / "bad_node_required_subclass.py")
    assert str(excinfo.value) == (
        "Can't set required value to None for CfgLeaf(<class 'tests.data.base_class.BaseClass'>) at cfg.SUBCLASS"
    )


def test_bad_node_nested_subclass():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_node_nested_subclass.py")
    assert str(excinfo.value) == (
        "Required type for CfgLeaf(<class 'tests.data.bad.bad_node_nested_subclass.BadSubClass'>) "
        "at cfg.SUBCLASSES.ONE must be subclass of <class 'tests.data.base_class.BaseClass'>"
    )


def test_bad_node_instance():
    with pytest.raises((TypeMismatchError, SchemaError)) as excinfo:
        CN.load(DATA_DIR / "bad_node_instance.py")
    assert re.match(
        r"^Subclass of type <tests.data.base_class.BaseClass> expected,"
        r" but found <tests.data.bad.bad_node_instance.SubClass object at 0x[0-9a-f]+>"
        r" of type <class 'tests.data.bad.bad_node_instance.SubClass'>"
        r" for CfgLeaf\(None\) at cfg.SUBCLASSES.ONE!$",
        str(excinfo.value),
    )


def test_inheritance_changes_bad():
    with pytest.raises(TypeMismatchError) as excinfo:
        CN.load(DATA_DIR / "inheritance_changes_bad.py")
    assert str(excinfo.value) == (
        "Instance of type <str> expected, but found 2 of type <class 'int'> for CfgLeaf(BAR) at cfg.DICT.BAR!"
    )


def test_bad_inherit():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_inherit_changes.py")
    assert str(excinfo.value) == "Key cfg.CLASSES.ANOTHER cannot contain nested nodes as leaf spec is defined for it."


def test_bad_inherit_subclass():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_inherit_subclass_changes.py")
    assert str(excinfo.value) == (
        "Value of CfgLeaf(None) at cfg.CLASSES.ANOTHER must be an instance of <class 'tests.data.base_class.BaseClass'>"
    )


def test_bad_inherit_instance():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_inherit_instance_changes.py")
    assert re.match(
        r"^Value of CfgLeaf\(<tests.data.bad.bad_inherit_instance.BadClass object at 0x[0-9a-f]+>\) "
        r"at cfg.CLASSES.ANOTHER must be an instance of <class 'tests.data.base_class.BaseClass'>$",
        str(excinfo.value),
    )


def test_bad_inherit_subclass_instance():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_inherit_subclass_instance_changes.py")
    assert re.match(
        r"^Value of CfgLeaf\(<tests.data.base_class.BaseClass object at 0x[0-9a-f]+>\) "
        r"at cfg.SUBCLASSES.ANOTHER must be a type$",
        str(excinfo.value),
    )


def test_bad_inherit_subclass_class():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_inherit_subclass_class_changes.py")
    assert str(excinfo.value) == (
        "Value of CfgLeaf(None) at cfg.CLASSES.ANOTHER must be an instance of <class 'tests.data.base_class.BaseClass'>"
    )


def test_schema_freeze():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_schema.py")
    assert str(excinfo.value) == "Trying to add leaf to node cfg.DICT with frozen schema."


def test_bad_init():
    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_init.py")
    assert str(excinfo.value) == "Changes to config must be started with `cfg = CN(cfg)`"

    with pytest.raises(SchemaError) as excinfo:
        CN.load(DATA_DIR / "bad_init_2.py")
    assert str(excinfo.value) == "Changes to config must be started with `cfg = CN(cfg)`"


def test_bad_cfg_import():
    with pytest.raises(ModuleError) as excinfo:
        CN.load(DATA_DIR / "bad_cfg_import.py")
    assert str(excinfo.value) == "Can't find config definition, please import config schema using absolute path"


def test_bad_import():
    with pytest.raises(ModuleError):
        CN.load(DATA_DIR / "bad_import.py")
