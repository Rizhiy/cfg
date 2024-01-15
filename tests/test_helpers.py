from __future__ import annotations

import subprocess  # noqa: S404
from pathlib import Path

import pytest

from pycs import CN
from pycs.helpers import get_output_dir

DATA_DIR = Path(__file__).parent / "data" / "helpers"


@pytest.mark.parametrize(
    ("cfg_path", "output_path"),
    {
        DATA_DIR / "configs" / "subdir" / "simple.py": Path("output") / "subdir" / "simple",
        DATA_DIR / "configs" / "subdir" / "with_name.py": Path("output") / "name",
        DATA_DIR / "simple.py": Path("output") / "simple",
    }.items(),
)
def test_get_output_dir(cfg_path: str, output_path: Path):
    cfg = CN.load(DATA_DIR / cfg_path)
    assert get_output_dir(cfg, mkdir=False) == output_path


def test_get_output_dir_cli():
    path = DATA_DIR / "configs" / "subdir" / "simple.py"
    output = subprocess.check_output(["cfg-output-dir", str(path), "--mkdir"])  # noqa: S603, S607 False positives
    assert output.decode("utf-8").strip() == str(Path("output") / "subdir" / "simple")


def test_get_output_dir_mkdir(tmp_path: Path):
    cfg = CN.load(DATA_DIR / "configs" / "subdir" / "simple.py")
    output_dir = get_output_dir(cfg, base_dir=tmp_path)
    assert output_dir.exists()
