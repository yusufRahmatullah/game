import re
from typing import List

_space_pat = re.compile(r'\s*,\s*')


def _is_city(text: str) -> bool:
    if len(text) == 1:
        return False
    if '|' in text or '-' in text or '+' in text:
        return False
    return True


def layout_to_arr(layout: List[str]) -> List[List[str]]:
    """Parse layout in yaml as 2d array of string
    example:
    layout in yaml
    - "BpM,-,LH ,-,EH "
    - " | ,+, x ,+, | "
    - "CF ,-,Ht ,-,Ml "

    will return
    [
        [BpM, -, LH, -, EH],
        [|, +, x, +, |],
        [CF, -, HT, -, Ml]
    ]
    """
    res = []
    for row in layout:
        cols = _space_pat.split(row)
        res.append(cols)
    return res


def read_city_from_layout(layout: List[str]) -> list:
    """Read city from layout in yaml as list of string
    and return all cities that contains in layout

    example:
    layout in yaml
    - "BpM,-,LH ,-,EH "
    - " | ,+, x ,+, | "
    - "CF ,-,Ht ,-,Ml "

    will return [BpM, LH, EH, CF, Ht, Ml]
    may raise error if any not unique city
    """
    res = []
    for row in layout:
        cols = _space_pat.split(row)
        for col in cols:
            if _is_city(col):
                res.append(col)
    sorted_res = sorted(res)
    for i in range(1, len(sorted_res)):
        if sorted_res[i-1] == sorted_res[i]:
            raise ValueError(f'Duplicate city: {sorted_res[i]}')
    return res
