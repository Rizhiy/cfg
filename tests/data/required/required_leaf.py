from ntc import CL

from ..base_cfg import cfg

cfg = cfg.clone()
cfg.REQUIRED = CL(None, str, required=True)
