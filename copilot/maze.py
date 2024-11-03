from collections import deque


def read_maze(file_path):
    with open(file_path, 'r') as file:
        maze = [list(line.strip()) for line in file.readlines()]
    return maze


def find_start(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == '@':
                return i, j
    return None


def bfs_collect_keys(maze, start):
    rows, cols = len(maze), len(maze[0])
    all_keys = {cell for row in maze for cell in row if cell.islower()}
    queue = deque([(start[0], start[1], frozenset(), 0)])  # (row, col, collected_keys, distance)
    visited = set()
    visited.add((start[0], start[1], frozenset()))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while queue:
        x, y, keys, dist = queue.popleft()

        # Check if we have collected all keys
        if keys == all_keys:
            return dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                cell = maze[nx][ny]
                if cell == '#':
                    continue
                if cell.isupper() and cell.lower() not in keys:
                    continue
                new_keys = keys
                if cell.islower():
                    new_keys = keys | frozenset([cell])
                if (nx, ny, new_keys) not in visited:
                    queue.append((nx, ny, new_keys, dist + 1))
                    visited.add((nx, ny, new_keys))

    return -1  # If no path is found


# Read the maze from the file
file_path = 'maze.txt'
maze = read_maze(file_path)

# Find the starting position
start = find_start(maze)

if start:
    # Find the shortest path to collect all keys
    shortest_path_length = bfs_collect_keys(maze, start)
    if shortest_path_length != -1:
        print(f"The shortest path length to collect all keys is: {shortest_path_length}")
    else:
        print("No path found to collect all keys.")
else:
    print("Starting point '@' not found in the maze.")
