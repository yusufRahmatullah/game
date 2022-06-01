from argparse import ArgumentParser
from map import Map


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('filename', nargs='?', default='maps/martlock.yml')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    map = Map.parse_yaml(args.filename)
    cells = map.generate_cells()

    for cell in cells:
        cell.draw()
