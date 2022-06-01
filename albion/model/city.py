import re

_space_pat = re.compile(r'\s*,\s*')
_zone_map = {
    'B': 'Blue',
    'Y': 'Yellow',
    'R': 'Red',
    'Bl': 'Black',
    'x': 'unidentified'
}


class City:
    def __init__(self, city_string: str) -> None:
        """City string contains comma separated value
        This city_string: "Curlew Fen, 4, B, wsc" will be splitted as
        City name, Tier, Zone, resources
        Resources contains word that represents:
        w: wood
        r: stone
        s: skin
        c: cotton
        o: ore
        """
        self._city_string = city_string
        cols = _space_pat.split(city_string)
        name = cols[0]
        self.name = name
        temp = name.split()
        self.first_name = temp[0]

        if len(temp) == 1:
            self.last_name = ''
        else:
            self.last_name = temp[1]

        self.tier = int(cols[1])
        self.zone = cols[2]
        self.zone_name = _zone_map[self.zone]
        self.resource = cols[3]

    def __repr__(self) -> str:
        return f"[{self.zone_name}][T{self.tier}]{self.name} - {self.resource}"
