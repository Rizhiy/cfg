from pathlib import Path

from ntc.transforms import load_from_file

from ..base_cfg import cfg

cfg = cfg.inherit()

cfg.add_transform(load_from_file(Path(__file__).parent / "extra.yaml"))
