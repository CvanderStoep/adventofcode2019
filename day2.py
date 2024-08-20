def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def process_input(inputs: list) -> list:
    intcode = inputs[0]
    intcode = list(map(int, intcode.split(',')))
    return intcode


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    intcode = process_input(inputs)
    if len(intcode) > 12:  # only needed for actual puzzle input, test cases are shorter
        intcode[1] = 12
        intcode[2] = 2
    counter = 0
    opcode = intcode[counter]
    while opcode != 99:
        location1 = intcode[counter + 1]
        location2 = intcode[counter + 2]
        location3 = intcode[counter + 3]
        if opcode == 1:
            intcode[location3] = intcode[location1] + intcode[location2]
        if opcode == 2:
            intcode[location3] = intcode[location1] * intcode[location2]
        counter += 4
        opcode = intcode[counter]
    return intcode[0]


def compute_part_two(file_name: str) -> int:
    inputs = read_input_file(file_name)
    target = 19690720
    for noun in range(1, 100):
        for verb in range(1, 100):
            intcode = process_input(inputs)  # resets after each loop
            try:
                if len(intcode) > 12:  # only needed for actual puzzle input, test cases are shorter
                    intcode[1] = noun
                    intcode[2] = verb
                counter = 0
                opcode = intcode[counter]
                while opcode != 99:
                    location1 = intcode[counter + 1]
                    location2 = intcode[counter + 2]
                    location3 = intcode[counter + 3]
                    if opcode == 1:
                        intcode[location3] = intcode[location1] + intcode[location2]
                    if opcode == 2:
                        intcode[location3] = intcode[location1] * intcode[location2]
                    counter += 4
                    opcode = intcode[counter]
                if intcode[0] == target:
                    print(f'{noun= }, {verb= }, {intcode[0]= }')
                    return 100 * noun + verb
            except Exception as e:  # it was not encountered in the puzzle input, but you never know ...
                print(e)


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input2.txt')}")
    print(f"Part II: {compute_part_two('test/input/input2.txt')}")
