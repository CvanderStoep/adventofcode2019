import math
from collections import defaultdict


def build_graph(inputs):
    reactions = {}
    for line in inputs.splitlines():
        components, product = line.split(' => ')
        components = [x.split(' ') for x in components.split(', ')]
        num, name = product.split(' ')
        reactions[name] = (int(num), tuple(map(lambda x: (int(x[0]), x[1]), components)))
    return reactions


def make_fuel(reactions, num_fuel=1):
    # Save left-overs and total created components over time
    pantry = defaultdict(lambda: 0)
    created = defaultdict(lambda: 0)

    def synthetize(name, required):
        # Compute how many ores are required to produce 'num'
        # or element 'name'
        if name == 'ORE':
            return required
        # Check if element is in pantry
        if pantry[name] > required:
            pantry[name] -= required
            return 0
        # Otherwise, do some experiments
        required -= pantry[name]
        amount, components = reactions[name]
        num_reactions = math.ceil(required / amount)
        # compute ores required for components
        ores = 0
        for c_num, c_name in components:
            c_required = num_reactions * c_num
            ores += synthetize(c_name, c_required)
        # Update leftovers to pantry
        pantry[name] = num_reactions * amount - required
        created[name] = required
        # Update
        return ores

    # Compute number of required ores for 1 FUEL
    return synthetize('FUEL', num_fuel)


## Binary search to find the number of fuel
# given some budget of ores
def find_num_fuel(reactions, ores_budget=1000000000000):
    # Get upper bound
    ores = make_fuel(reactions, 1)
    upper = 2 * ores_budget // ores

    # Binary search
    def search(start, end):
        n = math.ceil((start + end) / 2)
        ores = make_fuel(reactions, n)
        # Return cases
        if ores == ores_budget:
            return n
        if end == start:
            return start
        # Recursive
        if ores == ores_budget:
            return n
        elif ores > ores_budget:
            return search(start, n - 1)
        else:
            return search(n + 1, end)

    return search(1, upper)


with open("test/input/input14.txt", 'r') as f:
    inputs = f.read()

reactions = build_graph(inputs)
print("{} OREs are required to produce 1 FUEL".format(make_fuel(reactions)))
# print("A trillion OREs make a total of {} FUELs".format(find_num_fuel(reactions)))
