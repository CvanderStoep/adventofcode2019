def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    content = [int(c) for c in content]
    # content = list(map(int, content))

    return content


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    sum_mass = 0
    for mass in inputs:
        mass = mass // 3 - 2
        sum_mass += mass

    a = sum([m//3-2 for m in inputs])
    b = [(lambda f: f//3 - 2)(m) for m in inputs]
    print(f'{sum(b)= }')
    print(f'{a= }')

    return sum_mass


def compute_part_two(file_name: str) -> int:
    inputs = read_input_file(file_name)
    sum_mass = 0
    for mass in inputs:
        mass = mass // 3 - 2
        while mass > 0:
            sum_mass += mass
            mass = mass // 3 - 2

    return sum_mass


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input1.txt')}")
    print(f"Part II: {compute_part_two('test/input/input1.txt')}")
