# see 2020-day17
import math


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def transform_input(inputs: list) -> set:
    asteroid_map = set()
    for i, line in enumerate(inputs):
        for j, letter in enumerate(line):
            if letter == "#":
                asteroid_map.add((j, i))
    return asteroid_map


def neighbours(asteroid_map: set, i: int, j: int, layer: int) -> set:
    nb = set()
    for x in range(i - layer, i + layer + 1):
        nb.add((x, j - layer))
        nb.add((x, j + layer))
    for y in range(j - layer, j + layer + 1):
        nb.add((i - layer, y))
        nb.add((i + layer, y))
    return nb


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    asteroid_map = transform_input(inputs)
    asteroid_map_org = asteroid_map.copy()
    grid_size = len(inputs) + 1
    max_detected_asteroids = 0
    best_monitoring_station = (0, 0)
    for monitoring_station in asteroid_map_org:
        asteroid_map = asteroid_map_org.copy()

        # DONE optimize search grid; if outside grid, search can stop.
        for layer in range(1, grid_size):
            nb = neighbours(asteroid_map, monitoring_station[0], monitoring_station[1], layer)
            for asteroid in nb:
                if asteroid in asteroid_map:
                    vector = (asteroid[0] - monitoring_station[0], asteroid[1] - monitoring_station[1])
                    gcd_ = math.gcd(vector[0], vector[1])
                    vector = (int(vector[0] / gcd_), int(vector[1] / gcd_))
                    for i in range(1, grid_size):
                        x, y = (asteroid[0] + i * vector[0], asteroid[1] + i * vector[1])
                        if abs(x) > grid_size or abs(y) > grid_size:
                            break
                        elem_to_remove = (x, y)
                        asteroid_map.discard(elem_to_remove)
        number_detected = len(asteroid_map) - 1
        if number_detected > max_detected_asteroids:
            max_detected_asteroids = number_detected
            best_monitoring_station = monitoring_station

    print(f'{best_monitoring_station= }, {max_detected_asteroids= }')

    # loop over asteroids and find the best one
    # get asteroid
    # get neighbours in first layer
    # remove asteroid in line of sight
    # move to second layer and repeat
    # count map
    return max_detected_asteroids


def compute_part_two(file_name: str) -> int:
    inputs = read_input_file(file_name)
    return 2


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input10.txt')}")
    print(f"Part II: {compute_part_two('test/input/input10.txt')}")
