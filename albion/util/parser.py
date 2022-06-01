from model import City
import re

_space_pat = re.compile(r'\s*,\s*')


def parse_cities(cities: dict[str, str]) -> dict[str, City]:
    """Parse cities from yaml and return as dict of City
    example:
    {
        'CF': 'Curlew Fen, 4, B, wsc',
        'HT': 'Haytor, 4, B, wro'
    }

    will returns
    {
        'CF': City('Curlew Fen, 4, B, wsc'),
        'HT': City('Haytor, 4, B, wro')
    }
    """
    res = {}
    for key, value in cities.items():
        res[key] = City(value)
    return res


def parse_layout_to_arr(layout: list[str]) -> list[list[str]]:
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
