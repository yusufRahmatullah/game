import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise


def generate_map(noise_func, denom, total=100, offset=None):
    if offset is None:
        offset = (0, 0)

    res = []
    for i in range(total):
        row = []
        for j in range(total):
            ri = (i + offset[0]) / denom
            rj = (j + offset[1]) / denom
            val = noise_func([ri, rj])
            row.append(val)
        res.append(row)
    return res


def show_map(arr, title):
    plt.imshow(arr, cmap='gray')
    plt.title(title)
    plt.show()


class Config:
    def __init__(self, octaves: int, denom: int, size: int, offset=None):
        self._octaves = octaves
        self._denom = denom
        self._size = size
        if offset is None:
            self._offset = (0, 0)
        else:
            self._offset = offset
        self.noise = PerlinNoise(octaves=octaves, seed=69)
        self.title = f'o{octaves}-d{denom}-s{size}-off{offset}'
        self.map = generate_map(self.noise, denom, total=size, offset=self._offset)

    def quantize(self):
        res = []
        for row in self.map:
            row_res = []
            for col in row:
                if col <= 0:
                    row_res.append(0)
                else:
                    row_res.append(1)
            res.append(row_res)
        return res


arr = [
    Config(0.5, 10, 20, offset=(0, 0)),
    Config(1, 10, 20, offset=(0, 0)),
    Config(1.5, 10, 20, offset=(0, 0)),
    Config(2, 10, 20, offset=(0, 0)),
]

figure, axis = plt.subplots(len(arr), 2)

for i in range(len(arr)):
    cfg = arr[i]
    axis[i, 0].imshow(cfg.map, cmap='gray')
    axis[i, 0].set_title(cfg.title)
    axis[i, 1].imshow(cfg.quantize(), cmap='gray')
    axis[i, 1].set_title('[Q]' + cfg.title)

plt.show()
