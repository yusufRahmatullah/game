from model import (
    Cell,
    BlankCell, CityCell, ConnectionCell,
    get_cell_class
)
import util
from util.decorator import cache
import yaml


class Map:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.layout = util.parse_layout_to_arr(self.data['layout'])
        self.cities = util.parse_cities(self.data['cities'])

        # for caching
        self._cache = {}

    @classmethod
    def parse_yaml(cls, filepath: str) -> 'Map':
        with open(filepath) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        return cls(data)

    def generate_cells(self) -> list[Cell]:
        lc = self._find_longest_city()
        res = []
        for row in self.layout:
            ln = []
            for col in row:
                kls = get_cell_class(col, lc)
                if kls == 'blank':
                    cell = BlankCell(col, lc)
                elif kls == 'connC':
                    cell = ConnectionCell(col, lc)
                else:
                    city = self.cities[col]
                    cell = CityCell(city, lc, col)
                ln.append(cell)
            c = ln[0]
            for i in range(1, len(ln)):
                c.append(ln[i])
            res.append(c)
        return res

    @cache('longest_city')
    def _find_longest_city(self) -> int:
        lc = 0
        for city in self.cities.values():
            n = max(len(city.first_name), len(city.last_name))
            if n > lc:
                lc = n
        self._cache['longest_city'] = lc
        return self._cache['longest_city']


if __name__ == '__main__':
    map: Map
    map = Map.parse_yaml('maps/martlock.yml')
    cells = map.generate_cells()

    cell: Cell
    for cell in cells:
        cell.draw()
