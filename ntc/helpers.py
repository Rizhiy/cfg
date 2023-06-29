from __future__ import annotations

import sys
from pathlib import Path

from nt_utils.cli import autocli

from ntc import CN


def get_output_dir(cfg: CN) -> Path:
    return Path("output") / cfg.NAME


@autocli
def _get_output_dir_cli(cfg_path: str) -> None:
    cfg = CN.load(cfg_path)
    dir_ = get_output_dir(cfg)
    sys.stdout.write(str(dir_))
