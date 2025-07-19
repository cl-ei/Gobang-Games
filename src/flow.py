import json
import time
from typing import *
from multiprocessing import Process, Queue
from src.core.core import calc_candidate


def calc(q: Queue, table_str: str, first: int):
    table: List[Tuple[int, int]] = [(x, y) for x, y in json.loads(table_str)]
    print(f"enter calc wrapper.")
    result = calc_candidate(table, first)

    print(f"calc done: {result}")
    q.put(result)
    return


class FlowController:
    ROLE_PLAYER = 1
    ROLE_PC = 2

    STATUS_PLAYER = 0
    STATUS_PC = 1
    STATUS_OVER = 2

    def __init__(self):
        self.first = self.ROLE_PLAYER
        self._table = []
        self._winner = None
        self._queue = Queue()
        self._proc = None

        # 0. 玩家走子状态；1. 电脑走子状态; 3. 已角逐出胜负
        self._status = 0

    @property
    def table_string(self) -> str:
        return json.dumps(self._table)

    @property
    def table(self) -> List[Tuple[int, int]]:
        return self._table

    @property
    def winner(self) -> Optional[int]:
        return self._winner

    @property
    def is_busy(self) -> bool:
        return self._proc is not None and self._proc.is_alive()

    def check_winner(self):
        valid_pcs = []
        last_index = len(self._table) - 1
        while last_index >= 0:
            valid_pcs.insert(0, self._table[last_index])
            last_index -= 2

        if len(valid_pcs) < 5:
            return False

        last_x, last_y = valid_pcs[-1]
        stone_set = set(valid_pcs)  # 使用集合提高查找效率

        # 检查四个方向：水平(→/←)、垂直(↑/↓)、左斜(↗/↙)、右斜(↖/↘)
        directions = [
            ((1, 0), (-1, 0)),   # 水平方向
            ((0, 1), (0, -1)),   # 垂直方向
            ((1, 1), (-1, -1)),  # 左斜方向
            ((1, -1), (-1, 1))   # 右斜方向
        ]

        for (dx1, dy1), (dx2, dy2) in directions:
            count = 1  # 包括当前落子位置
            x, y = last_x, last_y
            for _ in range(4):
                x, y = x + dx1, y + dy1
                if (x, y) in stone_set and 0 <= x <= 14 and 0 <= y <= 14:
                    count += 1
                else:
                    break

            x, y = last_x, last_y
            for _ in range(4):
                x, y = x + dx2, y + dy2
                if (x, y) in stone_set and 0 <= x <= 14 and 0 <= y <= 14:
                    count += 1
                else:
                    break

            if count >= 5:
                # 已经产生winner
                if ((len(self._table) % 2 == 0 and self.first == self.ROLE_PLAYER) or
                        (len(self._table) % 2 != 0 and self.first == self.ROLE_PC)):
                    self._winner = self.ROLE_PC
                else:
                    self._winner = self.ROLE_PLAYER
                return True
        return False

    def player_take(self, x, y):
        if self._status != self.STATUS_PLAYER:
            raise RuntimeError("error status")

        if (x, y) in self._table:
            return

        self._table.append((x, y))
        self.check_winner()
        if self.winner is not None:
            self._status = self.STATUS_OVER
            return

        # start pc
        if self._proc is not None:
            if self._proc.is_alive():
                self._proc.terminate()
                self._proc.join()

        self._proc = Process(target=calc, args=(self._queue, self.table_string, self.first))
        self._proc.start()

        self._status = self.STATUS_PC

    def fresh_status(self) -> int:
        if self._status == self.STATUS_PC:
            # 检查是否计算完毕
            if self.is_busy:
                return self._status
            final_step: Tuple[int, int] = self._queue.get()
            self._table.append(final_step)

            # check winner
            self.check_winner()
            if self.winner is not None:
                self._status = self.STATUS_OVER
            else:
                self._status = self.STATUS_PLAYER
        return self._status

    def go_back(self):
        if len(self._table) > 1:
            if self._winner is not None:
                self._winner = None
                self._table.pop(-1)
            else:
                self._table.pop(-1)
                self._table.pop(-1)

    def go_ahead(self):
        pass
