# 棋盘大小
BOARD_SIZE = 15

# 棋型权重（需根据实际棋力调整）
WEIGHTS = {
    'FIVE': 10000000,       # 五连（胜利）
    'LIVE_FOUR': 100000,    # 活四（必胜）
    'FOUR': 10000,          # 冲四
    'DOUBLE_THREE': 5000,   # 双活三
    'LIVE_THREE': 1000,     # 活三
    'SLEEP_THREE': 200,     # 眠三
    'LIVE_TWO': 100,        # 活二
    'SLEEP_TWO': 10,        # 眠二
    'SINGLE': 1             # 单子
}


# 位置权重矩阵（中心价值更高）
POSITION_WEIGHT = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
    [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 8, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
    [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def evaluate(board, player):
    """
    评估棋盘对指定玩家的优势
    :param board: 15x15二维数组，0=空，1=黑棋，2=白棋
    :param player: 当前玩家 (1=黑棋, 2=白棋)
    :return: 评估分数（正值对玩家有利）
    """
    if is_win(board, player):
        return WEIGHTS['FIVE']

    if is_win(board, 3-player):
        return -WEIGHTS['FIVE']

    # 1. 基础位置分数
    score = position_score(board, player)

    # 2. 棋型分数
    pattern_score = 0
    for direction in [(1, 0), (0, 1), (1, 1), (1, -1)]:  # 水平、垂直、对角线
        pattern_score += pattern_evaluation(board, player, direction)
        pattern_score -= pattern_evaluation(board, 3-player, direction)

    # 3. 特殊威胁检测
    threat_score = 0
    # TODO:
    # threat_score = detect_threats(board, player) * WEIGHTS['DOUBLE_THREE']
    # threat_score -= detect_threats(board, 3-player) * WEIGHTS['DOUBLE_THREE']

    return score + pattern_score + threat_score


def is_win(board, player):
    """检查是否获胜"""
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != player:
                continue
            # 检查四个方向
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                count = 1
                for step in range(1, 5):
                    ni, nj = i + dx*step, j + dy*step
                    if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and board[ni][nj] == player:
                        count += 1
                    else:
                        break
                if count >= 5:
                    return True
    return False


def position_score(board, player):
    """位置基础分数评估"""
    score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == player:
                score += POSITION_WEIGHT[y][x]
            elif board[y][x] == 3 - player:
                score -= POSITION_WEIGHT[y][x]
    return score


def pattern_evaluation(board, player, direction):
    """沿指定方向评估棋型"""
    dx, dy = direction
    pattern_score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            # 跳过非该玩家的棋子
            if board[y][x] != player or (y - dy) >= BOARD_SIZE:
                continue

            # 检查这个位置是否是新棋型的起点
            if x - dx < 0 or y - dy < 0 or board[y - dy][x - dx] != player:
                # 沿方向分析棋型
                line = []
                nx, ny = x, y

                # 获取连续线上的棋子
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    line.append(board[ny][nx])
                    nx += dx
                    ny += dy
                    if len(line) >= 6:  # 最多分析6个位置
                        break

                # 评估此棋型
                pattern_score += evaluate_line(line, player)

    return pattern_score


def evaluate_line(line, player):
    """
    评估一段连续的棋子线
    :param line: 连续位置的值列表
    :param player: 当前玩家
    :return: 此线的分数
    """
    length = 0
    open_ends = 0

    # 计算连续棋子长度
    while length < len(line) and line[length] == player:
        length += 1

    # 检查开放端口
    if length < len(line) and line[length] == 0:  # 右端口
        open_ends += 1
    if length > 0 and line[0] == 0:
        open_ends += 1

    # 确定棋型类型
    if length == 5:
        return WEIGHTS['FIVE']  # 五连

    if length == 4:
        if open_ends == 2:
            return WEIGHTS['LIVE_FOUR']  # 活四
        elif open_ends == 1:
            return WEIGHTS['FOUR']  # 冲四

    if length == 3:
        # 活三判断
        if open_ends == 2:
            return WEIGHTS['LIVE_THREE']
        elif open_ends == 1:
            return WEIGHTS['SLEEP_THREE']

    if length == 2 and open_ends > 1:
        # 检查跳活三（如 Oxx_xO）
        if len(line) >= 5:
            if line[4] == 0 and line[0] == 0 and line[1:4] == [player]*3:
                return WEIGHTS['LIVE_THREE'] * 1.5
    return 0


def detect_threats(board, player):
    """检测特殊威胁（如双活三、冲四活三）"""
    threats = 0

    # 遍历整个棋盘
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != 0:
                continue

            # 模拟在此位置落子
            board[y][x] = player

            # 检测双活三威胁
            live_threes = 0
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                if detect_pattern(board, player, x, y, dx, dy, 'LIVE_THREE'):
                    live_threes += 1
                    if live_threes >= 2:
                        threats += 1  # 双活三威胁
                        break

            # 检测冲四活三威胁
            if (detect_pattern(board, player, x, y, 1, 0, 'FOUR') and
                    detect_pattern(board, player, x, y, 0, 1, 'LIVE_THREE')):
                threats += 2

            # 回溯
            board[y][x] = 0

    return threats


def detect_pattern(board, player, x, y, dx, dy, pattern_type):
    """在指定位置检测特定棋型"""
    # 具体实现类似 evaluate_line，但针对特定点
    # 为简化，此处返回布尔值
    # 实际实现需要分析从(i,j)向(dx,dy)方向的棋型
    return False  # 简化示意
