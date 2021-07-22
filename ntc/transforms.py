from pathlib import Path
from typing import Union

import yaml

from .node import CN


def load_from_file(filepath: Union[str, Path]):
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    def _merge(cfg: CN) -> None:
        if not filepath.exists():
            return
        with filepath.open() as f:
            cfg.update(yaml.load(f, Loader=yaml.Loader))

    return _merge
