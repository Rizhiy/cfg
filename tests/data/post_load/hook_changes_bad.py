from ntc import CN

from .hook import cfg


def hook(cfg: CN) -> None:
    print("Hook bad")


cfg = CN(cfg)
cfg.REQUIRED = "Required"

cfg.add_hook(hook)
