import itertools
import re
from dataclasses import dataclass
import math


@dataclass
class Moon:
    x: int = 0
    y: int = 0
    z: int = 0
    vx: int = 0
    vy: int = 0
    vz: int = 0


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def calculate_gravity(moon1: Moon, moon2: Moon) -> None:
    if moon1.x < moon2.x:
        moon1.vx += 1
        moon2.vx -= 1
    if moon1.x > moon2.x:
        moon2.vx += 1
        moon1.vx -= 1

    if moon1.y < moon2.y:
        moon1.vy += 1
        moon2.vy -= 1
    if moon1.y > moon2.y:
        moon2.vy += 1
        moon1.vy -= 1

    if moon1.z < moon2.z:
        moon1.vz += 1
        moon2.vz -= 1
    if moon1.z > moon2.z:
        moon2.vz += 1
        moon1.vz -= 1

    return


def calculate_velocity(moon: Moon) -> None:
    moon.x += moon.vx
    moon.y += moon.vy
    moon.z += moon.vz

    return


def calculate_potential_energy(moon: Moon) -> int:
    return abs(moon.x) + abs(moon.y) + abs(moon.z)


def calculate_kinetic_energy(moon: Moon) -> int:
    return abs(moon.vx) + abs(moon.vy) + abs(moon.vz)


def transform_input(inputs: list) -> list:
    moons = []
    for m in inputs:
        x = re.findall(r'-?\d+', m)
        x, y, z = int(x[0]), int(x[1]), int(x[2])
        moons.append(Moon(x, y, z))

    return moons


def compute_part_one(file_name: str) -> int:
    inputs = read_input_file(file_name)

    print(inputs)
    moons = transform_input(inputs)
    for step in range(1, 1001):
        for m1, m2 in itertools.combinations(moons, 2):
            calculate_gravity(m1, m2)

        for moon in moons:
            calculate_velocity(moon)

    total_energy = 0
    for moon in moons:
        total_energy += calculate_potential_energy(moon) * calculate_kinetic_energy(moon)

    print(f'{total_energy= }')
    return total_energy


def compute_part_two(file_name: str) -> int:
    inputs = read_input_file(file_name)

    print(inputs)
    moons = transform_input(inputs)
    moonset = set()
    steps = 0
    xcycle, ycycle, zcycle = 0, 0, 0
    while not xcycle or not ycycle or not zcycle:
        for m1, m2 in itertools.combinations(moons, 2):
            calculate_gravity(m1, m2)

        for moon in moons:
            calculate_velocity(moon)

        x_coordinates = tuple(('x', moon.x, moon.vx) for moon in moons)
        y_coordinates = tuple(('y', moon.y, moon.vy) for moon in moons)
        z_coordinates = tuple(('z', moon.z, moon.vz) for moon in moons)

        if not xcycle and x_coordinates in moonset:
            xcycle = steps
            print(f'{xcycle= }')
        else:
            moonset.add(x_coordinates)
        if not ycycle and y_coordinates in moonset:
            ycycle = steps
            print(f'{ycycle= }')
        else:
            moonset.add(y_coordinates)
        if not zcycle and z_coordinates in moonset:
            zcycle = steps
            print(f'{zcycle= }')
        else:
            moonset.add(z_coordinates)
        steps += 1

    print(f'{math.lcm(xcycle, ycycle, zcycle)= }')
    return math.lcm(xcycle, ycycle, zcycle)


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('test/input/input12.txt')}")
    print(f"Part II: {compute_part_two('test/input/input12.txt')}")
