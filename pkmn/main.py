from bdb import effective
import json
from itertools import product

types = []
data = {}
data_reverse = {}


def create_types_map():
    with open('types.csv') as f:
        data = f.read().splitlines()

    headers = data[0]
    ctn = data[1:]
    types_header = headers.split(',')[1:]
    types_column = []
    for r in ctn:
        c1 = r.partition(',')[0]
        types_column.append(c1)
    types_map = {}
    for row in ctn:
        cols = row.split(',')
        type_from = cols[0]
        for i, tt in enumerate(cols[1:]):
            type_to = types_header[i]
            key = f'{type_from} -> {type_to}'
            types_map[key] = float(tt)
    with open('types_map.json', 'w') as f:
        json.dump(types_map, f, indent=2)


def read_types_map():
    global data, types

    with open('types_map.json') as f:
        data = json.load(f)

    types_set = set()
    for k in data.keys():
        t1, _t2 = k.split(' -> ')
        types_set.add(t1)
    types = list(types_set)


def create_types_double():
    global data

    data_double = {}

    for tf in types:
        for tt1, tt2 in product(types, types):
            if tt1 == tt2:
                continue
            type_to = f'{tt1},{tt2}'
            type_to_2 = f'{tt2},{tt1}'
            key = f'{tf} -> {type_to}'
            key_2 = f'{tf} -> {type_to_2}'

            tf_to_tt1 = data[f'{tf} -> {tt1}']
            tf_to_tt2 = data[f'{tf} -> {tt2}']
            res = tf_to_tt1 * tf_to_tt2
            data_double[key] = res
            data_double[key_2] = res

    data.update(data_double)
    with open('types_map.json', 'w') as f:
        json.dump(data, f, indent=2)


def read_types_double():
    global data

    with open('types_map.json') as f:
        data = json.load(f)


def create_data_reverse():
    global data_reverse

    for k, v in data.items():
        tf, tt = k.split(' -> ')
        key = f'{tt} -> {tf}'
        data_reverse[key] = v

    with open('types_map_reverse.json', 'w') as f:
        json.dump(data_reverse, f, indent=2)


def read_data_reverse():
    global data_reverse

    with open('types_map_reverse.json') as f:
        data_reverse = json.load(f)


def calculate_most_powerful():
    double_power = {}

    for k, v in data_reverse.items():
        # tf is double types (defense), tt is single type (attack)
        tf, _tt = k.split(' -> ')
        if tf not in double_power:
            double_power[tf] = 0.0
        double_power[tf] += v
    dp_sorted = sorted(
        double_power.items(),
        key=lambda x: x[1]
    )
    print(dp_sorted)


def calculate_most_effective():
    effect = {}

    for k, v in data.items():
        if ',' in k:
            continue
        tf, _tt = k.split(' -> ')
        if tf not in effect:
            effect[tf] = 0.0
        effect[tf] += v
    es = sorted(
        effect.items(),
        key=lambda x: x[1],
        reverse=True,
    )
    print(es)


def describe_type(typ: str):
    null = []
    half = []
    norm = []
    full = []

    for k, v in data.items():
        tf, tt = k.split(' -> ')
        if tf != typ or ',' in tt:
            continue

        if v == 0.0:
            null.append(tt)
        elif v <= 0.5:
            half.append(tt)
        elif v <= 1.0:
            norm.append(tt)
        else:
            full.append(tt)

    print(f'describe type [{typ}]')
    print('nullify types:')
    print(null)
    print('half damage types:')
    print(half)
    print('normal damage types:')
    print(norm)
    print('full damage types:')
    print(full)


def describe_defense_type(typ: str):
    null = []
    half = []
    norm = []
    full = []

    for k, v in data_reverse.items():
        tf, tt = k.split(' -> ')
        if tf != typ or ',' in tt:
            continue

        if v == 0.0:
            null.append(tt)
        elif v <= 0.5:
            half.append(tt)
        elif v <= 1.0:
            norm.append(tt)
        else:
            full.append(tt)

    print(f'describe defense type [{typ}]')
    print('nullify types:')
    print(null)
    print('half damage types:')
    print(half)
    print('normal damage types:')
    print(norm)
    print('full damage types:')
    print(full)


# create_types_map()
# read_types_map()
# create_types_double()
read_types_double()
# create_data_reverse()
read_data_reverse()

# print('most powerful types')
# calculate_most_powerful()
# print('most effective types')
# calculate_most_effective()

# describe_type('ground')
# print('============')
# describe_defense_type('ground')
# print('\n====================================\n')
# describe_type('ice')
# print('============')
# describe_defense_type('ice')

print('\n====================================\n')
describe_defense_type('steel,dragon')
