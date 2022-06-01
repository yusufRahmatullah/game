offset = 97

def get_file_name(idx: int, folder_dir: str) -> str:
    key = get_key(idx)
    return f'{folder_dir}/{key}.txt'


def get_index(word: str) -> int:
    return ord(word[0]) - offset


def get_key(idx: int) -> str:
    return chr(idx + offset)


def read_file(filename: str) -> list:
    with open(filename) as f:
        ctn = f.read().splitlines()
    return ctn
