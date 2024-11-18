from collections import deque


def read_maze(file_path):
    with open(file_path, 'r') as file:
        maze = [list(line.strip()) for line in file.readlines()]
    return maze


def find_start(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '@':
                return (x, y)
    return None


def is_valid_move(maze, x, y, keys):
    if 0 <= x < len(maze[0]) and 0 <= y < len(maze):
        cell = maze[y][x]
        if cell == '#' or (cell.isupper() and cell.lower() not in keys):
            return False
        return True
    return False


def bfs_collect_keys(maze, start):
    queue = deque([(start, 0, set())])
    visited = set([(start, frozenset())])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    keys = set('abcdefghijklmnopqrstuvwxyz')

    while queue:
        (x, y), steps, collected = queue.popleft()

        if maze[y][x] in keys:
            collected = collected | {maze[y][x]}

        if len(collected) == len(keys):
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy