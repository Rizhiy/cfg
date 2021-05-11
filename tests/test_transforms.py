from pathlib import Path

from ntc import CN

DATA_DIR = Path(__file__).parent / "data" / "transforms"


def test_load_from_file():
    cfg = CN.load(DATA_DIR / "load_from_file_changes.py")
    assert cfg.DICT.FOO == "bar"
