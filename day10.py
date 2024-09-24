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
            if letter in "#X":
                asteroid_map.add((j, i))
    return asteroid_map


def neighbours(monitoring_station: tuple, layer: int) -> set:
    nb = set()
    i, j = monitoring_station

    for x in range(i - layer, i + layer + 1):
        nb.add((x, j - layer))
        nb.add((x, j + layer))
    for y in range(j - layer, j + layer + 1):
        nb.add((i - layer, y))
        nb.add((i + layer, y))
    return nb


def list_visible_asteroids(asteroid_map: set, monitoring_station: tuple, grid_size: int) -> set:
    for layer in range(1, grid_size):
        nb = neighbours(monitoring_station, layer)
        for asteroid in nb:
            if asteroid in asteroid_map:
                vector = (asteroid[0] - monitoring_station[0], asteroid[1] - monitoring_station[1])
                gcd_ = math.gcd(vector[0], vector[1])  # reduce for example vector (4,2) to (2,1)
                vector = (int(vector[0] / gcd_), int(vector[1] / gcd_))
                for i in range(1, grid_size):
                    x, y = (asteroid[0] + i * vector[0], asteroid[1] + i * vector[1])
                    if abs(x) > grid_size or abs(y) > grid_size:
                        break
                    elem_to_remove = (x, y)
                    asteroid_map.discard(elem_to_remove)
    return asteroid_map


def compute_part_one(file_name: str) -> int:
    # loop over asteroids and find the best one
    # get asteroid
    # get neighbours in first layer
    # remove asteroid in line of sight
    # move to second layer and repeat
    # count map

    inputs = read_input_file(file_name)
    asteroid_map = transform_input(inputs)
    asteroid_map_org = asteroid_map.copy()
    grid_size = max(len(inputs), len(inputs[0])) + 1
    max_detected_asteroids = 0
    best_monitoring_station = (0, 0)
    for monitoring_station in asteroid_map_org:
        asteroid_map = asteroid_map_org.copy()

        # DONE optimize search grid; if outside grid, search can stop.
        # DONE make function: list_visible_asteroids(map, station) -> map
        asteroid_map = list_visible_asteroids(asteroid_map, monitoring_station, grid_size)

        detected_asteroids = len(asteroid_map) - 1
        if detected_asteroids > max_detected_asteroids:
            max_detected_asteroids = detected_asteroids
            best_monitoring_station = monitoring_station

    print(f'{best_monitoring_station= }, {max_detected_asteroids= }')

    return max_detected_asteroids


def compute_part_two(file_name: str) -> int:
    # in this specific puzzle, the answer is found in the first laser sweep
    # if that was not the case, we have to move the laser and second, third, etc. time
    # each time removing the already vaporized asteroids from the map.
    inputs = read_input_file(file_name)
    asteroid_map = transform_input(inputs)
    asteroid_map_org = asteroid_map.copy()
    grid_size = max(len(inputs), len(inputs[0])) + 1
    max_detected_asteroids = 0
    best_monitoring_station = (0, 0)
    for monitoring_station in asteroid_map_org:
        asteroid_map = asteroid_map_org.copy()
        asteroid_map = list_visible_asteroids(asteroid_map, monitoring_station, grid_size)

        detected_asteroids = len(asteroid_map) - 1
        if detected_asteroids > max_detected_asteroids:
            max_detected_asteroids = detected_asteroids
            best_monitoring_station = monitoring_station
            max_asteroids = asteroid_map.copy()

    # sort the asteroids on angle using 90-atan2(-y, x); starting pointing up, clockwise
    max_asteroids = sorted(max_asteroids,
                           key=lambda p: (math.pi / 2 - math.atan2(-p[1] + best_monitoring_station[1],
                                                                   p[0] - best_monitoring_station[0])) % (2 * math.pi))
    max_asteroids.remove(best_monitoring_station)
    i = 0
    for asteroid in max_asteroids:
        i += 1
        if i in [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299]:
            print(i, asteroid, (-math.atan2(-asteroid[1] + best_monitoring_station[1],
                                            asteroid[0] - best_monitoring_station[0]) + math.pi / 2) % (2 * math.pi))
            if i == 200:
                answer_200 = 100 * asteroid[0] + asteroid[1]

    return answer_200


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input10.txt')}")
    print(f"Part II: {compute_part_two('test/input/input10.txt')}")
