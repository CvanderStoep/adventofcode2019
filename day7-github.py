import copy
import operator
import itertools
import asyncio


async def compute(instructions, inputs, outputs):
    """
    inputs: async input queue
    outputs: async output queue
    returns: the final state of the "program" and the last output
    """

    def get_input(list, pos, mode):
        n = list[pos]
        if mode == 0:
            return list[n]
        elif mode == 1:
            return n
        else:
            raise Exception("Invalid mode: {}".format(mode))

    my_program = copy.deepcopy(instructions)

    ip = 0   # instruction pointer
    max_ip = len(my_program)
    result = None

    while ip < max_ip:
        output = None

        # modes: 0 = position, 1 = immediate
        opcode = my_program[ip] % 100
        mode1 = my_program[ip] // 100 % 10
        mode2 = my_program[ip] // 1000 % 10
        mode3 = my_program[ip] // 10000 % 10

        if (opcode == 1) or (opcode == 2):
            # add or multiply
            input1 = get_input(my_program, ip + 1,  mode1)
            input2 = get_input(my_program, ip + 2, mode2)
            assert mode3 == 0, "output mode must be zero"
            out_pos = my_program[ip + 3]
            functor = operator.add if opcode == 1 else operator.mul
            output = functor(input1, input2)
            my_program[out_pos] = output
            ip += 4
        elif opcode == 3:
            # input
            assert mode1 == 0, "output mode must be zero"
            input1 = await inputs.get()  # consume an input
            inputs.task_done()
            out_pos = my_program[ip + 1]
            my_program[out_pos] = input1
            ip += 2
        elif opcode == 4:
            # output
            input1 = get_input(my_program, ip + 1, mode1)
            result = input1
            outputs.put_nowait(result)
            # print("Output: {}".format(result))
            ip += 2
        elif (opcode == 5) or (opcode == 6):
            # jump if true, jump if false
            input1 = get_input(my_program, ip + 1, mode1)
            input2 = get_input(my_program, ip + 2, mode2)
            if (opcode == 5) and (input1 != 0):
                ip = input2
            elif (opcode == 6) and (input1 == 0):
                ip = input2
            else:
                ip += 3
        elif (opcode == 7) or (opcode == 8):
            # less-then or equal
            input1 = get_input(my_program, ip + 1,  mode1)
            input2 = get_input(my_program, ip + 2, mode2)
            comparator = operator.lt if opcode == 7 else operator.eq
            assert mode3 == 0, "output mode must be zero"
            # int(True) == 1, int(False) == 0
            out_pos = my_program[ip + 3]
            my_program[out_pos] = int(comparator(input1, input2))
            ip += 4
        elif opcode == 99:
            # halt
            # print("Done")
            ip = max_ip     # the end
        else:
            raise Exception("Invalid opcode: {}".format(opcode))

    return my_program, result


async def run_a_program(plist):
    inputs = [5, 6, 7, 8, 9]
    results = []
    for inputset in itertools.permutations(inputs):
        # create and initialize the queues
        # Q1 - F1 - Q2 - F2 - Q3 - F3 - Q4 - F5 +
        # +--------------------------------------
        queues = []
        for q in range(len(inputs)):
            queues.append(asyncio.Queue())
        for pos in range(len(inputs)):
            # "phases"
            queues[pos].put_nowait(inputset[pos])
        # first value
        queues[0].put_nowait(0)
        # set up the computationsY
        filters = []
        max_queue = len(queues) - 1
        for pos in range(len(inputs)):
            input_q = queues[pos]
            output_q = queues[pos + 1 if pos < max_queue else 0]
            filter = asyncio.create_task(
                compute(plist, input_q, output_q))
            filters.append(filter)
        returns = await asyncio.gather(*filters, return_exceptions=True)
        # value returned by the final filter
        (_, val) = returns[-1]
        results.append((inputset, val))

    def grabber(x):
        return x[1]

    return max(results, key=grabber)


def read_data(filename):
    """py
    Each line is a "program":
    name1:op1,op2,...opX
    """

    alldata = {}

    with open(filename) as f:
        for line in f:
            (name, prog) = line.rstrip().split(':')
            alldata[name] = [int(x) for x in prog.split(',')]

    return alldata


def main():
    data = read_data('test/input/day7-data.txt')

    for pname in ['test1b', 'test2b', 'data']:
        program = data[pname]
        (maxparm, maxvalue) = asyncio.run(run_a_program(program))
        print("{}: {} <- {}".format(pname, maxparm, maxvalue))


if __name__ == "__main__":
    main()