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


@unique
class RoleColor(Enum):
    black = "black"
    white = "white"


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
    5: [
        (0b110101010101, 8000000),      # 'aaaaa'
        (0b110101010001, 300000),       # 'aaa?a'
        (0b110100010101, 3000),         # 'a?aaa'
        (0b110101010100, 2500),         # 'aaaa?'
        (0b110001010101, 2500),         # '?aaaa'
        (0b110101000101, 2600),         # 'aa?aa'
        (0b110100000101, 600),          # 'a??aa'
        (0b110101000001, 600),          # 'aa??a'
        (0b110101010000, 500),          # 'aaa??'
        (0b110000010101, 500),          # '??aaa'
        (0b110100010001, 550),          # 'a?a?a'
        (0b110101000000, 150),          # 'aa???'
        (0b110000000101, 150),          # '???aa'
    ],
    6: [
        (0b11000101010100, 300000),     # '?aaaa?'
        (0b11000100010100, 800),        # '?a?aa?'
        (0b11000101000100, 800),        # '?aa?a?'
        (0b11000100000100, 200),        # '?a??a?'
    ],
    7: [
        (0b1100000101010000, 3000),     # '??aaa??'
        (0b1100000100010000, 250),      # '??a?a??'
    ],
    8: [
        (0b110000000101000000, 650),    # '???aa???'
    ]
}
TABLE_SIZE = 15


class Core(object):
    def __init__(self, table, last_pos):
        """

        :param table: chess pieces map
        :param last_pos: the last chess pieces position.
        """
        self.table = table
        self.last_pos = last_pos
        x, y = last_pos & 0b1111, last_pos >> 4
        last_role = (table[y] >> (x << 1)) & 3
        self.last_role = last_role
        if last_role == 1:
            self._next = RoleColor.white
        elif last_role == 2:
            self._next = RoleColor.black
        else:
            raise ValueError("Bad table")

    def find_winner(self):
        pass

    def get_empty_pos(self):
        empty_pos = []
        for y in range(len(self.table)):
            line = self.table[y]
            for x in range(TABLE_SIZE):
                if line >> (x << 1) & 3 == 0:
                    empty_pos.append((x, y))
        return empty_pos

    def analysiz_a_dot(self, x, y):
        if (x, y) == (8, 7):
            self.analysis_a_line(1, 1, 1)
        return None

    def analysis_a_line(self, line, x_position, dot_value_for_self, line_size=TABLE_SIZE):
        this_line = 0b0000000000100001000000100010000
        #             5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0
        dot_value_for_self = 2
        x_position = 7

        r_map = 0b1101
        bit_length = 1
        for x_offset in range(x_position + 1, line_size):
            dot = this_line >> (x_offset << 1) & 3
            if dot == 0:
                r_map <<= 2
                bit_length += 1
            elif dot == dot_value_for_self:
                r_map = (r_map << 2) | 1
                bit_length += 1
            else:
                break
        print("-> ", bin(r_map))
        for _ in range(1, x_position + 1):
            x_offset = x_position - _
            if x_offset < 0:
                break
            dot = this_line >> (x_offset << 1) & 3
            if dot == 0:
                r_map |= 3 << ((bit_length + 1) << 1)
                r_map &= ~(3 << (bit_length << 1))
                bit_length += 1
            elif dot == dot_value_for_self:
                r_map |= 3 << ((bit_length + 1) << 1)
                r_map &= ~(2 << (bit_length << 1))
                bit_length += 1
            else:
                break
        print("r_map: ", bin(r_map))
        return r_map

    def distribute_calcul_task(self, empty_pos):
        for pos in empty_pos:
            self.analysiz_a_dot(*pos)

    def get_result(self):
        empty_pos = self.get_empty_pos()

        empty_pos_check = []
        for x in range(TABLE_SIZE):
            for y in range(TABLE_SIZE):
                if (x, y) not in empty_pos:
                    empty_pos_check.append((x, y))

        self.distribute_calcul_task(empty_pos=empty_pos)
        return ""


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

    def pc_take(self, pos):
        if not pos:
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

    def calcul(self):
        table = self.zip_table()
        x, y = self.table[-1]
        core = Core(table=table, last_pos=(y << 4) + (x & 0b1111))
        result = core.get_result()


def test():
    mgr = GameManager()
    mgr.player_take((7, 8))
    mgr.pc_take((7, 7))
    mgr.player_take((11, 7))
    mgr.calcul()
    # mgr.pc_take()
    print("susscess")
