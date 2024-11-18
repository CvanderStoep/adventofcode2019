import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Read the initial state from a file
def read_initial_state(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    initial_state = []
    for line in lines:
        initial_state.append([1 if char == '#' else 0 for char in line.strip()])
    return np.array(initial_state)


# Initialize the grid with the given input
grid = read_initial_state('test/input/input24.txt')
N = grid.shape[0]

# Set to keep track of seen patterns
seen_patterns = set()


def update(data):
    def get_element(grid, i, j):
        global N
        if i < 0 or i >= N or j < 0 or j >= N:
            return 0
        else:
            return grid[i, j]

    global grid
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            # Count the number of live neighbors
            total = get_element(grid, i, j - 1) + \
                    get_element(grid, i, j + 1) + \
                    get_element(grid, i - 1, j) + \
                    get_element(grid, i + 1, j)
            total = int(total)

            if grid[i, j] == 1:
                if total == 1:
                    new_grid[i, j] = 1
                else:
                    new_grid[i, j] = 0
            else:
                if total == 1 or total == 2:
                    new_grid[i, j] = 1
                else:
                    new_grid[i, j] = 0

    # Convert the new grid to a tuple of tuples for immutability and hashability
    new_pattern = tuple(map(tuple, new_grid.tolist()))
    if new_pattern in seen_patterns:
        print("Pattern repeated. Stopping the algorithm.")
        biodiversity = 0
        for i in range(N):
            for j in range(N):
                if new_grid[i,j] == 1:
                    tile = (i*N) + j + 1
                    biodiversity += 2**(tile-1)
        print(f'{biodiversity= }')
        ani.event_source.stop()
    else:
        seen_patterns.add(new_pattern)

    mat.set_data(new_grid)
    grid = new_grid
    return [mat]


fig, ax = plt.subplots()
mat = ax.matshow(grid, cmap='binary')

ani = animation.FuncAnimation(fig, update, interval=50, save_count=50)
plt.show()
