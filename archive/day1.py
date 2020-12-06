import math


def fuel_required(mass: int) -> int:
    fuel = math.floor(mass/3) - 2
    if fuel < 0:
        return 0
    return fuel


def fuel_required_extended(mass: int) -> int:
    total_fuel = 0
    fuel = fuel_required(mass)
    while fuel != 0:
        total_fuel += fuel
        fuel = fuel_required(fuel)
    return total_fuel


def fuel_required_modules() -> int:
    sum_fuel = 0
    f = open("archive-day1/input.txt", "r")
    for module in f:
        sum_fuel += fuel_required_extended(int(module))
    return sum_fuel


if __name__ == "__main__":
    print(fuel_required_modules())