from model import City

CityLayout = dict[str, str]


def parse_cities(cities: CityLayout) -> dict[str, City]:
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
