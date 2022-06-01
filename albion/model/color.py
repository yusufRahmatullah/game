from multiprocessing import cpu_count
from os import stat


class Color:
    _PINK = '\033[95m'
    _BLUE = '\033[94m'
    _CYAN = '\033[96m'
    _GREEN = '\033[92m'
    _YELLOW = '\033[93m'
    _RED = '\033[91m'
    _BOLD = '\033[1m'
    _UNDERLINE = '\033[4m'
    _END = '\033[0m'

    @classmethod
    def wrap(cls, txt: str, col: str, bold:
        bool=False, line: bool=False) -> str:
        ctn = ''
        if bold:
            ctn += cls._BOLD

        if line:
            ctn += cls._UNDERLINE

        col_map = {
            'pink': cls._PINK,
            'blue': cls._BLUE,
            'cyan': cls._CYAN,
            'green': cls._GREEN,
            'yellow': cls._YELLOW,
            'red': cls._RED,
        }
        clr = col_map.get(col, '')

        return ctn + clr + txt + cls._END

