# https://github.com/ameroyer/advent_of_code_2019/blob/master/day05.ipynb

def run_program(intcode, inputs):
    counter = 0
    output_value = None
    while intcode[counter] != 99:
        codes = "%05d" % intcode[counter]
        codes = [int(codes[0]), int(codes[1]), int(codes[2]), int(codes[3:])]
        opcode = codes[-1]
        assert codes[0] == 0
        # Outputs
        if opcode == 4:
            output_value = intcode[intcode[counter + 1]]
            counter += 2
        # Inputs
        elif opcode == 3:
            assert codes[1] == codes[2] == 0
            intcode[intcode[counter + 1]] = inputs.pop()
            counter += 2
        else:
            x, y = intcode[counter + 1:counter + 3]
            x = intcode[x] if codes[2] == 0 else x
            y = intcode[y] if codes[1] == 0 else y
            # addition and multiplication
            if opcode in [1, 2]:
                intcode[intcode[counter + 3]] = x + y if opcode == 1 else x * y
                counter += 4
            # Comparison result
            elif opcode == 7:
                intcode[intcode[counter + 3]] = int(x < y)
                counter += 4
            elif opcode == 8:
                intcode[intcode[counter + 3]] = int(x == y)
                counter += 4
            # Jump if eq
            elif (opcode == 5 and x != 0) or (opcode == 6 and x == 0):
                counter = y
            # Jump instruction that failed their test
            else:
                counter += 3
    return output_value


def get_diagnostic_code(program, inputs):
    return run_program([x for x in program], inputs)


with open("test/input/input5.txt", 'r') as f:
    inputs = list(map(int, f.read().split(',')))

print("Diagnostic code:", get_diagnostic_code(inputs, [1]))
print("Extended diagnostic code:", get_diagnostic_code(inputs, [5]))
