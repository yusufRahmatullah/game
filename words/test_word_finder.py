from word_finder import WordFinder

tcs = {
    'suit*': ['suit', 'suitable', 'suite'],
    '*suit': ['catsuit', 'jesuit'],
    'su_t': ['suet', 'suit'],
    'acesu': ['spacesuit'],
    'sXXn': ['seen', 'soon'],
    '___lBstBc': ['ballistic', 'realistic'],
}

finder = WordFinder()
for word, exps in tcs.items():
    res = finder.regex_find(word)
    for exp in exps:
        assert exp in res, f'got: {res}, exp: {exp}, from {word}'
