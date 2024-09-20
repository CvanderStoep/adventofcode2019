def run_program(p, inputs, init_op=0, init_base=0, early_exit=False):
    #Inputs are given in reverse order (pop)
    op = init_op
    relative_base = init_base
    last_diagnostic = []
    while p[op] != 99:
        codes = "%05d" % p[op]
        codes = [int(codes[0]), int(codes[1]), int(codes[2]), int(codes[3:])]
        # inputs
        if codes[-1] == 3:
            assert codes[1] == 0
            p[p[op + 1] + (relative_base if codes[2] == 2 else 0)] = inputs.pop()
            op += 2
        # unary ops
        elif codes[-1] in  [4, 9]:
            # read parameter
            assert codes[1] == 0
            param = p[op + 1]
            if (codes[2] % 2) == 0:
                try:
                    param = p[param + (relative_base if codes[2] == 2 else 0)]
                except IndexError:
                    param = 0
            # output
            if codes[-1] == 4:
                last_diagnostic.append(param)
                if early_exit:
                    print('early exit')
                    return last_diagnostic[-1], 1, op
            # update relative base
            else:
                relative_base += param
            # next instr
            op += 2
        else:
            # read parameters in correct mode
            x, y = p[op + 1:op + 3]
            if (codes[2] % 2) == 0:
                try:
                    x = p[x + (relative_base if codes[2] == 2 else 0)]
                except IndexError:
                    x = 0
            if not (codes[1] % 2):
                try:
                    y = p[y + (relative_base if codes[1] == 2 else 0)]
                except IndexError:
                    y = 0
            # Read target and allocate more memory if needed
            target = p[op + 3] + (relative_base if codes[0] == 2 else 0)
            if target >= len(p):
                p += [0] * (target - len(p) + 1)
            # addition and multiplication
            if codes[-1] in [1, 2]:
                p[target] = x + y if codes[-1] == 1 else x * y
                op += 4
            # Comparison result
            elif codes[-1] == 7:
                p[target] = int(x < y)
                op += 4
            elif codes[-1] == 8:
                p[target] = int(x == y)
                op += 4
            # Jump if eq
            elif (codes[-1] == 5 and x != 0) or (codes[-1] == 6 and x == 0):
                op = y
            # Jump instruction that failed their test
            else:
                op += 3
    return last_diagnostic, 0, op


with open("test/input/input9.txt", 'r') as f:
    inputs = list(map(int, f.read().split(',')))

key = run_program([x for x in inputs], [1])[0][0]
print("Running BOOST in test mode yields key {}".format(key))

key = run_program([x for x in inputs], [2])[0][0]
print("Running BOOST in sensor boost mode yields key {}".format(key))
