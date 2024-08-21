import sys


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def process_input(inputs: list) -> list:
    wires = []
    for wire in inputs:
        wire = wire.split(",")
        wires.append(wire)
    return wires


def process_wire_instructions(instruction: str) -> (int, int):
    direction = instruction[0]
    amount = int(instruction[1:])
    dx, dy = 0, 0
    match direction:
        case 'R':
            dx, dy = amount, 0
        case 'U':
            dx, dy = 0, amount
        case 'L':
            dx, dy = -amount, 0
        case 'D':
            dx, dy = 0, -amount

    return dx, dy


def manhattan_distance(coordinate: tuple) -> int:
    return abs(coordinate[0]) + abs(coordinate[1])


def calculate_range(x: int, y: int, dx: int, dy: int) -> (int, int, int, int, int, int):
    if dx >= 0:
        x1, x2, step_x = x, x + dx + 1, 1
    else:
        x1, x2, step_x = x, x + dx - 1, -1
    if dy >= 0:
        y1, y2, step_y = y, y + dy + 1, 1
    else:
        y1, y2, step_y = y, y + dy - 1, -1
    return x1, x2, y1, y2, step_x, step_y


def calculate_wire_path(wire: list) -> set:
    wire_set = set()
    x, y = 0, 0
    for instruction in wire:
        dx, dy = process_wire_instructions(instruction)
        x1, x2, y1, y2, step_x, step_y = calculate_range(x, y, dx, dy)

        for i in range(x1, x2, step_x):
            for j in range(y1, y2, step_y):
                wire_set.add((i, j))
        x += dx
        y += dy

    return wire_set


def calculate_wire_distance_to_intersection(wire: list, intersections: set) -> dict:
    distance_dict = dict()
    x, y = 0, 0
    steps = 0
    for instruction in wire:
        steps -= 1  # correct for double count when starting new direction
        dx, dy = process_wire_instructions(instruction)
        x1, x2, y1, y2, step_x, step_y = calculate_range(x, y, dx, dy)
        for i in range(x1, x2, step_x):
            for j in range(y1, y2, step_y):
                steps += 1
                if (i, j) in intersections:
                    distance_dict.update({(i, j): steps})
        x += dx
        y += dy

    return distance_dict


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    wires = process_input(inputs)
    wire1_set = calculate_wire_path(wires[0])
    wire2_set = calculate_wire_path(wires[1])

    intersections = wire1_set.intersection(wire2_set)
    intersections.remove((0, 0))

    minimum_distance = sys.maxsize
    for intersection in intersections:
        minimum_distance = min(minimum_distance, manhattan_distance(intersection))

    return minimum_distance


def compute_part_two(file_name: str) -> int:
    inputs = read_input_file(file_name)
    wires = process_input(inputs)
    wire1_set = calculate_wire_path(wires[0])
    wire2_set = calculate_wire_path(wires[1])

    intersections = wire1_set.intersection(wire2_set)
    intersections.remove((0, 0))

    distance1_dict = calculate_wire_distance_to_intersection(wires[0], intersections)
    distance2_dict = calculate_wire_distance_to_intersection(wires[1], intersections)

    min_distance = sys.maxsize
    for key, value in distance1_dict.items():
        min_distance = min(min_distance, value + distance2_dict[key])

    return min_distance


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input3.txt')}")
    print(f"Part II: {compute_part_two('test/input/input3.txt')}")
