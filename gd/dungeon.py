import matplotlib.pyplot as plt
from randomizer import seedrandom


class CityMap:
    def __init__(self, window_h: int, window_w: int,
    center_x: int=0, center_y: int=0,
    max_h: int=20, max_w: int=20,
    city_prob: float=0.4) -> None:
        self.window_h = window_h
        self.window_w = window_w
        self.center_x = center_x
        self.center_y = center_y
        self.max_h = max_h
        self.max_w = max_w
        self.city_prob = city_prob

    @staticmethod
    def _check_number(field: str, num: int, odd: bool) -> bool:
        modifier = 1 if odd else 0
        valid = num % 2 == modifier
        if not valid:
            exp = 'odd' if odd else 'even'
            raise ValueError(f'{field} is not {exp}: {num}')

    def _validate(self):
        self._check_number('window_h', self.window_h, True)
        self._check_number('window_w', self.window_w, True)
        self._check_number('max_h', self.max_h, False)
        self._check_number('max_w', self.max_w, False)

    def _calculate_real_coor(self, i, j):
        ci = self.window_h // 2
        cj = self.window_w // 2
        di = ci - i
        dj = cj - j
        ri = self.center_y - di
        rj = self.center_x - dj
        return ri, rj

    def _is_city(self, ri, rj):
        # not city candidate
        if ri % 2 == 1 or rj % 2 == 1:
            return False
        # if real center, always return True
        if ri == 0 and rj == 0:
            return True
        # if exceed max radius, return False
        if abs(ri) > abs(self.max_h) or abs(rj) > abs(self.max_w):
            return False

        seed = f'{ri},{rj}'
        prng = seedrandom(seed)
        val = prng()
        return val <= self.city_prob

    def generate_map(self):
        arr = []
        for i in range(self.window_h):
            row = []
            for j in range(self.window_w):
                ri, rj = self._calculate_real_coor(i, j)
                if ri == 0 and rj == 0:
                    row.append(2)
                elif self._is_city(ri, rj):
                    row.append(1)
                else:
                    row.append(0)
            arr.append(row)
        return arr


city_map = CityMap(9, 9)
arr = city_map.generate_map()

maps = [
    CityMap(9, 9, center_x=-3, center_y=-3),
    CityMap(9, 9, center_y=-3),
    CityMap(9, 9, center_x=3, center_y=-3),
    CityMap(9, 9, center_x=-3),
    CityMap(9, 9),
    CityMap(9, 9, center_x=3),
    CityMap(9, 9, center_x=-3, center_y=3),
    CityMap(9, 9, center_y=3),
    CityMap(9, 9, center_x=3, center_y=3),
]

_, axis = plt.subplots(3, 3)
idx = 0
for i in range(3):
    for j in range(3):
        cm = maps[idx]
        idx += 1
        axis[i, j].imshow(cm.generate_map(), cmap='gray')
        axis[i, j].set_title(f'{cm.center_x},{cm.center_y}')
plt.show()
