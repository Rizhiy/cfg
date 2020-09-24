from ntc import CN

from ..base_cfg import cfg


def hook(cfg: CN) -> None:
    print("Hook 1")


cfg = cfg.clone()
cfg.REQUIRED = "Required"

cfg.add_hook(hook)
