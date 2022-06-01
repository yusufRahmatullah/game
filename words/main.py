from argparse import ArgumentParser
import os
import readline  # magic for up arrow on input()
import sys
import time
from word_finder import WordFinder

run = True
cur_res = []


def _find_word_regex(word: str):
    global cur_res

    st = time.perf_counter()
    cur_res = finder.regex_find(word)
    dt = time.perf_counter() - st

    n = len(cur_res)
    if n <= 20:
        print('result:', cur_res)

    print('total:', n)
    print('executed in', dt, 'seconds')


def _find_word_groups(group: str):
    global cur_res

    st = time.perf_counter()
    cur_res = finder.group_find(group)
    dt = time.perf_counter() - st

    n = len(cur_res)
    if n <= 20:
        print('result:', cur_res)

    print('total:', n)
    print('executed in', dt, 'seconds')


def parse_input(word):
    global run

    if ':' == word[0]:
        if len(word) == 1:
            print('undefined function')
            return
        elif word[1:] == 'q' or word[1:] == 'quit':  # quit app
            run = False
        elif word[1:] == 's' or word[1:] == 'show':  # show current result
            print('result:', cur_res)
    elif word[:2] == 'a:':
        _find_word_groups(word[2:])
    else:
        _find_word_regex(word)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-l', '--lang', choices=['en', 'id'], default='en')
    return parser.parse_args()


if __name__ == '__main__':
    max_thread = os.cpu_count()
    args = parse_args()

    finder = WordFinder(max_thread=max_thread, lang=args.lang)
    while run:
        try:
            word = input('> ')
            parse_input(word)
        except KeyboardInterrupt:
            break
    print()
    print('Thanks')
