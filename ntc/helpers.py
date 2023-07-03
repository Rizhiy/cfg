from __future__ import annotations

import sys
from pathlib import Path

from nt_utils.cli import autocli

from ntc.node import CN


def get_output_dir(cfg: CN, mkdir=True, base_dir=Path("output")) -> Path:
    output_dir = base_dir / cfg.NAME
    if mkdir:
        output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@autocli
def _get_output_dir_cli(cfg_path: str, mkdir=True, base_dir=Path("output")) -> None:
    cfg = CN.load(cfg_path)
    dir_ = get_output_dir(cfg, mkdir=mkdir, base_dir=base_dir)
    sys.stdout.write(str(dir_))
