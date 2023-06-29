from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from ntc import CN
from ntc.helpers import get_output_dir

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
    assert get_output_dir(cfg) == output_path


def test_get_output_dir_cli():
    path = DATA_DIR / "configs" / "subdir" / "simple.py"
    output = subprocess.check_output(["ntc-output-dir", str(path)])
    assert output.decode("utf-8").strip() == str(Path("output") / "subdir" / "simple")
