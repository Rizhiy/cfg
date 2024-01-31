from pathlib import Path

import pytest

from pycs import CN

DATA_DIR = Path(__file__).parent / "data" / "warnings"
THIS_FILE = Path(__file__)


def test_transform_with_frozen_schema():
    schema = CN()
    with pytest.warns(
        match=r"Transforming without freezing schema is discouraged, as it frequently leads to bugs",
    ) as records:
        schema.transform()
    assert len(records) == 1
    assert Path(records[0].filename) == THIS_FILE


def test_extend_without_clone():
    with pytest.warns(
        match=r"Extending config file without clone\(\) is discouraged, as it frequently leads to bugs",
    ) as records:
        CN.load(DATA_DIR / "extend_without_clone.py")
    assert len(records) == 1
    assert Path(records[0].filename) == THIS_FILE
