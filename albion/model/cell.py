from model.color import Color
import re
from model.city import City


class Cell:
    def __init__(self, ctn: list, height: int, repr: str) -> None:
        if len(ctn) != height:
            raise ValueError('Content length should be same as height')

        self.ctn = ctn
        self.height = height
        self.repr = repr

    def append(self, cell: 'Cell'):
        h = self.height
        ch = cell.height

        if h != ch:
            raise ValueError(
                f'Cell height is not same. {h}({self.repr}) vs '
                f'{ch}({cell.repr})'
            )

        new_ctn = []
        for i in range(h):
            new_row = self.ctn[i] + cell.ctn[i]
            new_ctn.append(new_row)
        self.ctn = new_ctn

    def draw(self):
        for c in self.ctn:
            print(c)


class BlankCell(Cell):
    """BlankCell is represented as '...' and '___'
    '...' have w=3, h=2
    '___' have w=longest_city + 4, h=2
    'xxx' have w=3, h=5
    """
    def __init__(self, repr: str, longest_city: int) -> None:
        if repr == '...':
            self.width = 3
            self.height = 2
        elif repr == '___':
            self.width = longest_city + 4
            self.height = 2
        elif repr == 'xxx':
            self.width = 3
            self.height = 5
        else:
            raise ValueError(f'Unknown representation: {repr}')

        self.ctn = []
        self._generate_ctn()
        super().__init__(self.ctn, self.height, repr)

    def _generate_ctn(self):
        spaces = ' ' * (self.width)
        self.ctn = [spaces for i in range(self.height)]


class CityCell(Cell):
    """CityCell is represented as 3-letter city name.
    Width is set from longest_city
    Height always 5
    """
    def __init__(self, city: City, longest_city: int, repr: str) -> None:
        self.city = city
        self.height = 5
        self.width = longest_city

        # think of this
        self.portal = False

        self.ctn = []
        self._generate_ctn()
        super().__init__(self.ctn, self.height, repr)

    def _generate_color(self, text: str) -> str:
        flag = self.city.zone == 'Bl'
        if self.city.tier == 5:
            return Color.wrap(text, 'yellow', bold=flag, line=flag)
        elif self.city.tier >= 6:
            return Color.wrap(text, 'red', bold=flag, line=flag)
        else:
            return Color.wrap(text, 'blue', bold=flag, line=flag)

    def _generate_ctn(self):
        border = '-' * self.width
        self.ctn.append(f'+-{border}-+')

        tier = f'T{self.city.tier}'
        res = f'[{self.city.resource}]'
        col_tier = self._generate_color(tier)

        spaces = ' ' * (self.width - len(tier) - len(res))
        self.ctn.append(f'| {col_tier}{spaces}{res} |')

        fn = self.city.first_name
        ln = self.city.last_name

        if self.portal:
            col_fn = Color.wrap(fn, 'pink', bold=True)
            col_ln = Color.wrap(ln, 'pink', bold=True)
        else:
            col_fn = fn
            col_ln = ln

        spaces = ' ' * (self.width - len(fn))
        self.ctn.append(f'| {col_fn}{spaces} |')

        spaces = ' ' * (self.width - len(ln))
        self.ctn.append(f'| {col_ln}{spaces} |')

        self.ctn.append(f'+-{border}-+')


class ConnectionCell(Cell):
    """Connection between city based on repr (representation)
    <->: Horizontal connection, w=3, h=5
    <--: Left Hor. connection, w=3, h=5
    -->: Right Hor. connection, w=3, h=5
    ---: Long Path, w=longest_city + 4, h=5
    v^v: Vertical connection, 2=longest_city + 4, h=2
    |^|: Up Ver. connection, w=longest_city + 4, h=2
    |v|: Down Ver. connection, w=longest_city + 4, h=2
    |__: Left-Down Corner, w=longest_city + 4, h=5
    __|: Right-Down Corner, w=longest_city + 4, h=5
    |--: Left-Up Corner, w=longest_city + 4, h=5
    --|: Right-Up Corner, w=longest_city + 4, h=5
    """
    cor_pat = ['|__', '__|', '|--', '--|']
    hor_pat = ['<->', '<--', '-->']
    ver_pat = ['v^v', '|^|', '|v|']

    def __init__(self, repr: str, longest_city: int) -> None:
        self.ctn = []
        if repr in self.hor_pat:
            self.width = 3
            self.height = 5
            self._generate_hor_ctn(repr)
        elif repr == '---':
            self.width = longest_city + 4
            self.height = 5
            self._generate_long_path()
        elif repr in self.ver_pat:
            self.width = longest_city + 4
            self.height = 2
            self._generate_ver_ctn(repr)
        elif repr in self.cor_pat:
            self.width = longest_city + 4
            self.height = 5
            self._generate_corner(repr)
        else:
            raise ValueError(f'Unknown representation: {repr}')

        super().__init__(self.ctn, self.height, repr)

    def _generate_hor_ctn(self, repr: str):
        l = repr[0] if repr[0] == '-' else '◄'
        r = repr[2] if repr[2] == '-' else '►'
        sym = f'{l}-{r}'

        self.ctn.append('   ')
        self.ctn.append('   ')
        self.ctn.append(sym)
        self.ctn.append('   ')
        self.ctn.append('   ')

    def _generate_long_path(self):
        spaces = ' ' * (self.width)
        path = '-' * (self.width)

        self.ctn.append(spaces)
        self.ctn.append(spaces)
        self.ctn.append(path)
        self.ctn.append(spaces)
        self.ctn.append(spaces)

    def _generate_ver_ctn(self, repr: str):
        n = self.width - 1
        l = n // 2
        r = n - l
        ls = ' ' * l
        rs = ' ' * r

        up = '▲'
        down = '▼'
        if repr == '|^|':
            down = '|'
        elif repr == '|v|':
            up = '|'

        self.ctn.append(f'{ls}{up}{rs}')
        self.ctn.append(f'{ls}{down}{rs}')

    def _generate_corner(self, repr: str):
        # todo
        n = self.width - 3
        l = n // 2
        r = n - l
        ls = ' ' * l
        rs = ' ' * r
        lp = '-' * l
        rp = '-' * r
        ln = []

        if repr == '|__':
            ln.append(' | ')
            ln.append(' | ')
            ln.append(f'{ls} \-{rp}')
            ln.append('   ')
            ln.append('   ')
        elif repr == '__|':
            ln.append(' | ')
            ln.append(' | ')
            ln.append(f'{lp}-/ {rs}')
            ln.append('   ')
            ln.append('   ')
        elif repr == '|--':
            ln.append('   ')
            ln.append('   ')
            ln.append(f'{ls} /-{rp}')
            ln.append(' | ')
            ln.append(' | ')
        elif repr == '--|':
            ln.append('   ')
            ln.append('   ')
            ln.append(f'{lp}-\ {rs}')
            ln.append(' | ')
            ln.append(' | ')

        for i in range(5):
            if i == 2:
                # middle lane, put content as is
                self.ctn.append(ln[i])
            else:
                self.ctn.append(f'{ls}{ln[i]}{rs}')


_blank_repr = ['...', '___', 'xxx']
_conn_repr = (
    ConnectionCell.cor_pat + ConnectionCell.hor_pat +
    ConnectionCell.ver_pat + ['---']
)
def get_cell_class(repr, longest_city) -> str:
    if repr in _blank_repr:
        return 'blank'
    elif repr in _conn_repr:
        return 'connC'
    else:
        return 'cityC'
