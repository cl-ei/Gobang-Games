import time
import random
from typing import *
from src.core.evaluate import BOARD_SIZE, evaluate, POSITION_WEIGHT


BRANCH_FACTOR = 30
MAX_DEPTH = 3
MAX_TIME = 10000


def debug_print_board(board, candidate_moves):
    debug_bd = [[" " for _ in range(15)] for _ in range(15)]
    for y in range(15):
        for x in range(15):
            board_v = board[y][x]
            if board_v != 0:
                debug_bd[y][x] = {0: " ", 1: "x", 2: "o"}[board_v]
    for x, y in candidate_moves:
        if debug_bd[y][x] != " ":
            raise RuntimeError(f"ERROR candidate_moves: {x}, {y}")
        debug_bd[y][x] = "·"

    print("============= board ================")
    for line in debug_bd:
        print("    " + " ".join(line))
    print("============= ^^^^^ ================")


def calc_candidate(table: List[Tuple[int, int]], first: int) -> Tuple[int, int]:
    """ 计算最有价值的走法 """

    # 即将走子的玩家，也就是说，需要计算对 next_player 最有价值的走法
    # 在这里，player_us 必然等于 2 即 AI
    next_player = player_us = first if len(table) % 2 == 0 else 3 - first
    print(f"\t table: {table}, first: {first}, player_us: {player_us}")

    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i, pos in enumerate(table):
        x, y = pos
        if i % 2 == 0:
            board[y][x] = first
        else:
            board[y][x] = 3 - first

    if len(table) == 0:
        return BOARD_SIZE // 2, BOARD_SIZE // 2  # 天元位置
    elif len(table) == 1:
        x, y = BOARD_SIZE // 2, BOARD_SIZE // 2
        if board[y][x] == 0:
            return x, y
        return random.choice([
            (x, y - 1), (x, y + 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y - 1), (x + 1, y + 1),
            (x - 1, y + 1), (x + 1, y - 1),
        ])

    # 现在需要计算
    """
    # 2. 检查直接获胜位置
    winning_move = find_winning_move(board, player)
    if winning_move:
        return winning_move

    # 3. 检查对方获胜威胁
    blocking_move = find_blocking_move(board, player)
    if blocking_move:
        return blocking_move
    """
    # 获取候选位置（高性能搜索）
    candidate_moves = get_candidate_moves_v2(table)
    debug_print_board(board, candidate_moves[:20])

    print(f"\tget candidate_moves: {len(candidate_moves)}, top K: {candidate_moves}")
    alpha = float('-inf')
    beta = float('inf')
    best_move = None

    # 使用深度受限的Minimax
    for i, move in enumerate(candidate_moves[:min(BRANCH_FACTOR, len(candidate_moves))]):
        x, y = move

        # 模拟落子
        board[y][x] = next_player

        # 模拟落子之后，next_player 会变成对手, 即AI落子后，下一手为 human
        # 此时
        next_player = 3 - next_player

        # 递归搜索
        # 由于己方已经落子，下一轮是对手方，评估对对手最有利的走法。is_max_turn 为 False
        eval_score = minimax(board, MAX_DEPTH - 1, False, player_us, next_player, alpha, beta, (x, y))
        print(f"\t loop: {i} score: {eval_score}, pos: {move}")
        # 回溯
        board[y][x] = 0

        # 更新最佳着法
        if eval_score > alpha:
            alpha = eval_score
            best_move = move

    # 极端情况：选择随机空位
    if best_move is None:
        print("no best move, select random one.")
        empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == 0]
        best_move = random.choice(empty_positions) if empty_positions else (7, 7)
    return best_move


# 辅助函数组
def is_first_move(board):
    """检查是否开局第一步"""
    for row in board:
        for cell in row:
            if cell != 0:
                return False
    return True

def find_winning_move(board, player):
    """查找立即获胜的位置"""
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                board[i][j] = player
                if check_win(board, player, i, j):
                    board[i][j] = 0
                    return (i, j)
                board[i][j] = 0
    return None

def find_blocking_move(board, player):
    """查找需要防守的位置（对方即将获胜）"""
    opponent = 3 - player
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                board[i][j] = opponent
                if check_win(board, opponent, i, j):
                    board[i][j] = 0
                    return (i, j)
                board[i][j] = 0
    return None


def count_consecutive(board, x, y, dx, dy, player) -> int:
    """统计(x,y)沿(dx,dy)方向的连续player棋子数"""
    count = 0
    while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == player:
        count += 1
        x += dx
        y += dy
    return count


def get_candidate_moves(*args):
    return []


def get_candidate_moves_v2(steps: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    生成候选落子点：
    - 搜索己方最后3手的动态邻域
    - 检测对手的冲四/活三威胁
    - 按权重排序（威胁点 > 邻域中心 > 边缘）
    """
    # 0. 初始化棋盘（0=空, 1=玩家1, 2=玩家2）
    board = [[0] * 15 for _ in range(15)]
    for i, (x, y) in enumerate(steps):
        board[y][x] = 1 if i % 2 == 0 else 2  # 假设玩家1先手

    # 1. 提取己方最后3手（倒数第2、4、6手）
    my_moves = []
    for i in range(len(steps)-2, -1, -2):  # 从倒数第二手开始，向前每隔一步取
        my_moves.append(steps[i])
        if len(my_moves) >= 3:
            break
    last_my_moves = my_moves  # 己方最后1~3手

    # 2. 动态邻域范围
    neighbor_radius = 2 if len(steps) < 10 else (3 if len(steps) < 30 else 4)

    # 3. 生成己方邻域候选点
    candidates = set()
    for x, y in last_my_moves:
        for dx in range(-neighbor_radius, neighbor_radius + 1):
            for dy in range(-neighbor_radius, neighbor_radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == 0:
                    candidates.add((nx, ny))

    # 4. 检测对手的威胁（冲四/活三）
    opponent = 1 if len(steps) % 2 == 1 else 2  # 对手是最后落子的一方
    threat_moves = set()

    # 4.1 仅扫描对手最后3手的邻域（避免全盘扫描）
    opponent_moves = [steps[i] for i in range(len(steps)-1, -1, -2)][:3]
    for x, y in opponent_moves:
        for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:  # 横、竖、斜、反斜
            # 检查冲四（xxxx_）
            if count_consecutive(board, x, y, dx, dy, opponent) >= 4:
                nx, ny = x + 4*dx, y + 4*dy
                if 0 <= nx < 15 and 0 <= ny < 15 and board[ny][nx] == 0:
                    threat_moves.add((nx, ny))
                nx, ny = x - dx, y - dy
                if 0 <= nx < 15 and 0 <= ny < 15 and board[ny][nx] == 0:
                    threat_moves.add((nx, ny))
            # 检查活三（xxx_）略，可类似实现

    candidates.update(threat_moves)

    # 5. 按权重排序
    def get_weight(pos):
        if pos in threat_moves:
            return 10000  # 威胁点最高优先级
        # 邻域权重：基础值 + 离己方落子距离
        min_dist = min(max(abs(pos[0] - mx), abs(pos[1] - my)) for mx, my in last_my_moves)
        base_weight = 4 - min_dist  # 中心=4，边缘=1
        return base_weight

    return sorted(candidates, key=get_weight, reverse=True)


# 核心搜索算法
def minimax(board, depth, is_max_turn, player_us, player_next, alpha, beta, last):
    """
    Minimax算法（带Alpha-Beta剪枝）

    player_us: 己方
    player_next: 即将落子方
    alpha: 己方的分数
    beta: 对手分数
    last: player_us的最后一手
    """

    # 终局节点或达到深度限制
    if depth == 0:
        return evaluate(board, player_us)

    # 检查胜负
    winner = check_any_win(board)
    if winner != 0:
        return float('inf') if winner == player_us else float('-inf')

    # 最大化玩家回合（我方）
    if is_max_turn:
        max_eval = float('-inf')
        candidate_moves = get_candidate_moves(board, last)[:BRANCH_FACTOR]

        for move in candidate_moves:
            x, y = move

            # 模拟落子
            board[y][x] = player_next

            # 递归搜索
            eval_score = minimax(board, depth - 1, False, player_us, 3 - player_next, alpha, beta, (x, y))
            max_eval = max(max_eval, eval_score)

            # 回溯
            board[y][x] = 0

            # Alpha-Beta剪枝
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval

    # 最小化玩家回合（对手）
    else:
        min_eval = float('inf')
        candidate_moves = get_candidate_moves(board, last)[:BRANCH_FACTOR]

        for move in candidate_moves:
            x, y = move

            # 模拟落子
            board[y][x] = player_next

            # 递归搜索
            eval_score = minimax(board, depth - 1, True, player_us, 3 - player_next, alpha, beta, (x, y))
            min_eval = min(min_eval, eval_score)

            # 回溯
            board[y][x] = 0

            # Alpha-Beta剪枝
            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval


def check_win(board, player, i, j):
    """检查指定位置落子后是否获胜"""
    # 临时设置
    board[i][j] = player
    won = is_win(board, player)
    board[i][j] = 0
    return won


def check_any_win(board: List[List[int]]) -> int:
    size = 15
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、右下斜、右上斜

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                continue
            current_player = board[i][j]
            for di, dj in directions:
                count = 1
                # 向正方向检查
                ni, nj = i + di, j + dj
                while 0 <= ni < size and 0 <= nj < size and board[ni][nj] == current_player:
                    count += 1
                    ni += di
                    nj += dj
                    if count == 5:
                        return current_player
                # 向反方向检查（优化：只需要检查另一侧）
                ni, nj = i - di, j - dj
                while 0 <= ni < size and 0 <= nj < size and board[ni][nj] == current_player:
                    count += 1
                    ni -= di
                    nj -= dj
                    if count == 5:
                        return current_player
    return 0
