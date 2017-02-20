# -*- coding: utf-8 -*-

"""
This file contain the new gobang core calculate method and data structure.
"""
POINT_TABLE = {
    'aaaaa': 8000000,
    '?aaaa?': 300000,
    'aaa?a': 3000,
    'a?aaa': 3000,
    '??aaa??': 3000,
    'aaaa?': 2500,
    '?aaaa': 2500,
    'aa?aa': 2600,
    '?a?aa?': 800,
    '?aa?a?': 800,
    'a??aa': 600,
    'aa??a': 600,
    'aaa??': 500,
    '??aaa': 500,
    '???aa???': 650,
    'a?a?a': 550,
    'aa???': 150,
    '???aa': 150,
    '??a?a??': 250,
    '?a??a?': 200,
}


class Core(object):
    def __init__(self, black, white, current_pos):
        super(Core, self).__init__()
        self.black = black
        self.white = white
        self.current_pos = current_pos

        self._next = 0 if bool(black[current_pos & 0xf] & (current_pos << (current_pos >> 4))) else 1
