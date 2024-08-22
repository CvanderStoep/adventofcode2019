def check_number(number: int, part: int) -> bool:
    numbers = [int(c) for c in str(number)]
    if numbers != sorted(numbers):
        return False

    number_string = str(number)
    # doubles = ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99']
    doubles = [str(i) * 2 for i in range(10)]

    if part == 1:
        if any(d in number_string for d in doubles):
            return True
        else:
            return False

    # part 2
    # triples = ['000', '111', '222', '333', '444', '555', '666', '777', '888', '999']
    triples = [str(i) * 3 for i in range(10)]
    if any(d in number_string and t not in number_string for d, t in zip(doubles, triples)):
        return True
    else:
        return False


def compute_part_one_and_two(part: int) -> int:
    valid_numbers = 0
    for number in range(138307, 654504):
        valid = check_number(number, part)
        if valid:
            valid_numbers += 1
    return valid_numbers

    # alternative
    # valid_numbers = sum(map(lambda number: check_number(number, part=1), range(138307, 654504)))


if __name__ == '__main__':
    print(f"Part I: {compute_part_one_and_two(part=1)}")
    print(f"Part II: {compute_part_one_and_two(part=2)}")
