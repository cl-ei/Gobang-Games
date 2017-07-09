# -*- coding: utf-8 -*-

"""
This file contain the new gobang core calculate method and data structure.

"""

from enum import Enum, unique
from random import randint


@unique
class Role(Enum):
    computer = "pc"
    player = "player"


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

POINT_TABLE_BIN = {
    0b110101010101: 8000000,        # 'aaaaa'
    0b11000101010100: 300000,       # '?aaaa?'
    0b110101010001: 300000,         # 'aaa?a'
    0b110100010101: 3000,           # 'a?aaa'
    0b1100000101010000: 3000,       # '??aaa??'
    0b110101010100: 2500,           # 'aaaa?'
    0b110001010101: 2500,           # '?aaaa'
    0b110101000101: 2600,           # 'aa?aa'
    0b11000100010100: 800,          # '?a?aa?'
    0b11000101000100: 800,          # '?aa?a?'
    0b110000000101000000: 650,      # '???aa???'
    0b110100000101: 600,            # 'a??aa'
    0b110101000001: 600,            # 'aa??a'
    0b110101010000: 500,            # 'aaa??'
    0b110000010101: 500,            # '??aaa'
    0b110100010001: 550,            # 'a?a?a'
    0b1100000100010000: 250,        # '??a?a??'
    0b11000100000100: 200,          # '?a??a?'
    0b110101000000: 150,            # 'aa???'
    0b110000000101: 150,            # '???aa'
}


class Core(object):
    def __init__(self, black, white, current_pos):
        """

        :param black: chess pieces map of black
        :param white: chess pieces map of white
        :param current_pos: the current chess pieces position.
        """
        super(Core, self).__init__()
        self.black = black
        self.white = white
        self.current_pos = current_pos
        self._next = "w" if bool(black[current_pos & 0xf] & (current_pos << (current_pos >> 4))) else "b"

    def find_winner(self):
        pass

    def get_empty_pos(self):
        pass

    def extract_table_type(self):
        pass

    def get_result(self):
        pass


class GameManager(object):
    def __init__(self):
        super(GameManager, self).__init__()
        self.__step = 0
        self.__table = []  # (7, 7), (7, 8), (8, 8)

    @property
    def table(self):
        return self.__table

    @property
    def winner(self):
        return None

    @property
    def busy(self):
        return False

    def player_take(self, pos):
        if pos in self.table:
            return False

        self.__table.append(pos)
        self.__step += 1
        return True

    def pc_take(self):
        while True:
            pos = (randint(0, 13), randint(0, 13))
            if pos not in self.table:
                break

        self.__step += 1
        self.__table.append(pos)
        pass

    @property
    def step(self):
        return self.__step

    def go_back(self):
        pass

    def go_ahead(self):
        pass

    def zip_table(self):
        table = [0 for _ in range(16)]
        for __ in range(len(self.__table)):
            x, y = self.__table[__]
            bit_pos = (x << 1) + __ % 2
            table[y] |= 1 << bit_pos
        return table

    def unzip_table(self, bin_table):
        table = []
        for y in range(len(bin_table)):
            line = bin_table[y]
            if line:
                for x in range(16):
                    if bin_table[y] & (3 << (x << 1)):
                        table.append((x, y))
        return table


def test():
    mgr = GameManager()

    for i in range(20):
        while True:
            player_s_take = (randint(0, 15), randint(0, 15))
            if player_s_take not in mgr.table:
                break
        mgr.player_take(player_s_take)
        mgr.pc_take()
        table = mgr.table
        print("table:     ", table, )
        print("zip table: ", mgr.unzip_table(mgr.zip_table()))
    print("susscess")
