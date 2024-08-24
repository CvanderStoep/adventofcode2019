def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def process_input(inputs: list) -> list:
    intcode = inputs[0]
    intcode = list(map(int, intcode.split(',')))
    return intcode


def process_opcode1(counter, intcode):
    location1 = intcode[counter + 1]
    location2 = intcode[counter + 2]
    location3 = intcode[counter + 3]
    intcode[location3] = intcode[location1] + intcode[location2]
    counter += 4
    return intcode, counter


def process_opcode2(counter, intcode):
    location1 = intcode[counter + 1]
    location2 = intcode[counter + 2]
    location3 = intcode[counter + 3]
    intcode[location3] = intcode[location1] * intcode[location2]
    counter += 4
    return intcode, counter


def process_opcode4(counter, intcode):
    location1 = intcode[counter + 1]
    output_value = intcode[location1]
    counter += 2

    return output_value, counter


def process_parameter(counter, opcode, intcode):
    return None


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    intcode = process_input(inputs)
    counter = 0
    opcode = intcode[counter]
    input_value = 1
    output_value = None
    while opcode != 99:
        location1 = intcode[counter + 1]

        if opcode == 3:
            intcode[location1] = input_value
            counter += 2
        elif opcode == 4:
            output_value, counter = process_opcode4(counter, intcode)
        elif opcode == 1:
            intcode, counter = process_opcode1(counter, intcode)
        elif opcode == 2:
            intcode, counter = process_opcode2(counter, intcode)
        else:
            mode1 = opcode // 100 % 10
            mode2 = opcode // 1000 % 10
            opcode = opcode % 100
            location2 = intcode[counter + 2]
            location3 = intcode[counter + 3]

            if opcode == 4:
                output_value, counter = process_opcode4(counter, intcode)
                opcode = intcode[counter]
                continue

            if mode1 == 0:
                first = intcode[location1]
            else:
                first = location1
            if mode2 == 0:
                second = intcode[location2]
            else:
                second = location2
            if opcode == 1:
                intcode[location3] = first + second
                counter += 4
            elif opcode == 2:
                intcode[location3] = first * second
                counter += 4
            else:
                print('not implemented')
                print(f'{opcode= }')
        opcode = intcode[counter]
    print(f'{output_value= }')
    return output_value


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
    print(f"Part I: {compute_part_one('test/input/input5.txt')}")
    # print(f"Part II: {compute_part_two('test/input/input5.txt')}")
