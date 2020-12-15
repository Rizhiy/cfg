from ntc import CL
from tests.data.base_cfg import cfg

cfg = cfg.inherit()

cfg.DESCRIBED = CL("described", desc="Described leaf")
