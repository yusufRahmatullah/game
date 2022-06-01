import re
import util

class WordFinder:
    def __init__(self, offset: int=97, max_thread: int=8,
        lang: str='en') -> None:

        self.arr = []
        self._indexes = list(range(26))
        self.offset = offset
        self.max_thread = 8
        self.lang = lang
        self._read_arr()

    def _read_arr(self):
        for i in range(26):
            fn = f'{self.lang}/words.txt'
            self.arr = util.read_file(fn)

    def _direct_regex_find(self, word: str) -> list:
        cw = word.replace('_', r'\w')

        # for handling plain word
        # example:
        # suit -> ^\w*suit\w*$
        # will result suit, suitable, jumpsuit, etc
        if '*' not in word and '_' not in word:
            cw = f'^*{cw}*$'
        # for _, it will handling exact length
        # for *, it will wrap with exact position
        # example:
        # suit* -> ^suit\w*$ -> suitcase, suitable, etc
        # *suit -> ^\w*suit$ -> swimsuit, jumpsuit. etc
        else:
            cw = f'^{cw}$'

        cw = cw.replace('*', r'\w*')
        pat = re.compile(cw)
        res = []
        for a in self.arr:
            if pat.match(a):
                res.append(a)
        return res

    def _symbol_regex_find(self, word: str) -> list:
        reg_map = {}
        reg_count = 0
        cws = []

        for c in word:
            if c.isupper():
                if c in reg_map:
                    g = reg_map[c]
                    cws.append(f'\{g}')
                else:
                    reg_count += 1
                    reg_map[c] = reg_count
                    cws.append('(\w)')
            else:
                cws.append(c)
        cw = f"^{''.join(cws)}$"
        return self._direct_regex_find(cw)

    def regex_find(self, word: str) -> list:
        if re.match(r'.*[A-Z].*', word):
            """
            * find word with same blank letter. e.g. sXXn -> seen, soon
            * combine with * and _. e.g. ___lBstBc -> ballistic, realistic
            """
            return self._symbol_regex_find(word)
        else:
            """
            * find word with given prefix. e.g. suit* -> suit, suitable, suite
            * find word with given suffix. e.g. *suit -> catsuit, jesuit
            * find word with exact blank letter. e.g. su_t -> suet, suit
            * find word that contains exact word. e.g. acese -> spacesuit
            """
            return self._direct_regex_find(word)

    def group_find(self, group: str) -> list:
        """Find word that must contains first item on  array,
        and may contains letters that given on 2nd-nth item on array
        """
        groups = re.split(r'\s*,\s*', group)

        points = []
        for word in self.arr:
            point = 0
            for g in groups[1:]:
                if groups[0] in word and g in word:
                    point += 1
            if point > 0:
                points.append((word, point))

        return sorted(points, key=lambda x: x[1], reverse=True)
