from __future__ import annotations

import datetime as dt

from rizhiy_cfg.interfaces import CfgSavable


class BaseClass:
    def __eq__(self, other):
        return isinstance(other, self.__class__)


class SubClass(BaseClass):
    pass


class SavableClass(CfgSavable, BaseClass):
    def __init__(self, date: dt.date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._date = date

    def save_strs(self):
        cls_name = super().save_strs()[1]
        return f"import datetime\nfrom {__name__} import {cls_name}", cls_name, [repr(self._date)], {}

    def __eq__(self, other):
        return super().__eq__(other) and self._date == other._date
