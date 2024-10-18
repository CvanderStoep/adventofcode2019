def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    content = [int(i) for i in str(content[0])]

    return content


def calculate_pattern(n: int, length: int) -> list:
    n += 1  # zero base

    pattern = [0] * n + [1] * n + [0] * n + [-1] * n
    pattern_length = len(pattern)
    repeat = length // pattern_length + 1
    pattern = pattern * repeat
    return pattern[1:]


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    for phase in range(1, 101):
        if phase % 10 == 0:
            print(phase, end='')
        else:
            print('.', end='')

        new_input = []
        for i in range(len(inputs)):
            pattern = calculate_pattern(i, len(inputs))
            total = 0
            for j in range(len(inputs)):
                total += inputs[j] * pattern[j]
            total = abs(total) % 10
            new_input.append(total)
        inputs = new_input.copy()

    print()
    result = int("".join(map(str, inputs[:8])))
    print(f'{result= }')

    return result


def compute_part_two(file_name: str) -> int:
    return 'not yet implemented'


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input16.txt')}")
    print(f"Part II: {compute_part_two('test/input/input16.txt')}")
