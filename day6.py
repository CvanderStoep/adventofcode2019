def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def distance_to_com(parents: dict, start: str) -> int:
    if start == 'COM':
        return 0
    else:
        return 1 + distance_to_com(parents, parents[start])


def path_to_com(parents: dict, start: str, destination: str, path: list) -> list:
    if start == destination:
        return []
    else:
        return [start] + path_to_com(parents, start=parents[start], destination=destination, path=path)


def process_input(inputs: list) -> dict:

    parents = dict()
    for line in inputs:
        object1, object2 = line.split(')')
        parents.update({object2: object1})

    return parents


def calculate_number_of_orbits(parents: dict) -> int:
    total_distance = 0
    for key in parents:
        total_distance += distance_to_com(parents, key)

    return total_distance


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    parents = process_input(inputs)
    number_of_orbits = calculate_number_of_orbits(parents)
    return number_of_orbits


def compute_part_two(file_name: str) -> int:
    inputs = read_input_file(file_name)
    parents = process_input(inputs)
    you_path = path_to_com(parents, 'YOU', 'COM', [])
    san_path = path_to_com(parents, 'SAN', 'COM', [])
    while you_path[-1] == san_path[-1]:
        you_path = you_path[:-1]
        san_path = san_path[:-1]

    return len(you_path) + len(san_path) - 2


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input6.txt')}")
    print(f"Part II: {compute_part_two('test/input/input6.txt')}")
