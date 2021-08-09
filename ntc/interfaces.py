from typing import Dict, List, Tuple


class CfgSavable:
    """
    Class to indicate that an instance will be saveable by Cfg
    """

    def save_strs(self) -> Tuple[str, str, List[str], Dict[str, str]]:
        """
        Return strings required for saving

        :return: import string, class name, args, kwargs
        """
        return "", self.__class__.__name__, [], {}

    def create_eval_str(self, cls_name, args, kwargs):
        args_str = ",".join([*args, *[f"{key}={value}" for key, value in kwargs.items()]])
        return f"{cls_name}({args_str})"
