import re
import sys


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def transform_input(inputs: list) -> list:
    image = re.findall(r'\d', inputs[0])
    image = [int(d) for d in image]
    return image


def get_layer(image: list, width: int, height: int, n: int) -> list:
    n = n - 1
    return image[n * width * height: (n + 1) * width * height]


def get_pixel(layer: list, width: int, height: int, x: int, y: int) -> int:
    return layer[y * width + x]


def count_digit(layer: list, d: int) -> int:
    return layer.count(d)


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)
    image = transform_input(inputs)
    width, height = 25, 6
    number_of_layers = int(len(image) / (width * height))
    number_of_zero_digits = sys.maxsize
    for n in range(1, number_of_layers + 1):
        layer = get_layer(image, width, height, n)
        n_zero = count_digit(layer, 0)
        if n_zero < number_of_zero_digits:
            number_of_zero_digits = n_zero
            layer_number = n
    answer = count_digit(get_layer(image, width, height, layer_number), 1) * \
             count_digit(get_layer(image, width, height, layer_number), 2)

    return answer


def print_picture(image: list, height: int, width: int) -> None:
    for y in range(height):
        for x in range(width):
            pixel = image[y * width + x]
            if pixel == 0:
                pixel = ' '
            else:
                pixel = '*'
            print(pixel, end='')
        print()


def combine_image(image: list, height: int, width: int) -> list:
    final_image = []
    for y in range(height):
        for x in range(width):
            n = 1
            layer = get_layer(image, width, height, n)
            pixel = get_pixel(layer, width, height, x, y)
            while pixel == 2:
                n += 1
                layer = get_layer(image, width, height, n)
                pixel = get_pixel(layer, width, height, x, y)
            final_image.append(pixel)
    return final_image


def compute_part_two(file_name: str) -> str:
    inputs = read_input_file(file_name)
    image = transform_input(inputs)
    width, height = 25, 6

    final_image = combine_image(image, height, width)
    print_picture(final_image, height, width)

    return 'see picture above'


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input8.txt')}")
    print(f"Part II: {compute_part_two('test/input/input8.txt')}")
