from ntc import CN

from .transform import cfg as bc


def transform(cfg: CN) -> None:
    if cfg.DICT.FOO == "bar":
        cfg.DICT.FOO = "baz"


cfg = CN(bc, transformers=[transform])
cfg.NAME = "Name"
