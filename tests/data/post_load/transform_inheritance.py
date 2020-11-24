from ntc import CN

from .transform import cfg


def transform(cfg: CN) -> None:
    if cfg.DICT.X == "Y":
        cfg.DICT.X = "Z"


cfg = cfg.inherit()
cfg.add_transform(transform)
