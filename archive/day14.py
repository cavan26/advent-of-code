import math


class FuelConverter:
    def __init__(self, file):
        self.file = file
        self.table = {}
        self.leftovers = {}
        self.read_conversion_table()

    def read_conversion_table(self):
        file1 = open(self.file, 'r')
        lines = file1.readlines()
        for line in lines:
            result = line.split("=>")[1].strip()
            value = {}
            for item in line.split("=>")[0].split(", "):
                value[item.split(" ")[1]] = int(item.split(" ")[0])
            self.table[result.split(" ")[1]] = (int(result.split(" ")[0]), value)

    def get_fuel(self):
        return self.find_number_ore('FUEL', 1)

    def find_number_ore(self, material, number):
        mult = self.table[material][0]
        number_of_operations = math.ceil(number / mult)
        number_of_ore = 0
        for mat in self.table[material][1]:
            quantity = self.table[material][1][mat] * number_of_operations
            if mat == 'ORE':
                number_of_ore += quantity
            else:
                if mat in self.leftovers:
                    leftover = self.leftovers[mat]
                    if self.leftovers[mat] >= quantity:
                        self.leftovers[mat] = self.leftovers[mat] - quantity
                    else:
                        self.leftovers[mat] = 0
                        number_of_ore += self.find_number_ore(mat, quantity - leftover)
                else:
                    number_of_ore += self.find_number_ore(mat, quantity)
        self.add_leftovers(material, number_of_operations*mult - number)
        return number_of_ore

    def run_without_ore(self, material, number):
        mult = self.table[material][0]
        number_of_operations = math.ceil(number / mult)
        for mat in self.table[material][1]:
            print(mat)
            quantity = self.table[material][1][mat] * number_of_operations
            if mat == 'ORE':
                return False
            else:
                if mat in self.leftovers:
                    leftover = self.leftovers[mat]
                    if self.leftovers[mat] >= quantity:
                        self.leftovers[mat] = self.leftovers[mat] - quantity
                    else:
                        self.leftovers[mat] = 0
                        result = self.run_without_ore(mat, quantity - leftover)
                        if result is False:
                            return False
                else:
                    result = self.run_without_ore(mat, quantity)
                    if result is False:
                        return False
        self.add_leftovers(material, number_of_operations * mult - number)
        return True

    def add_leftovers(self, material, left):
        if material in self.leftovers:
            self.leftovers[material] += left
        else:
            self.leftovers[material] = left

    def find_number_fuel(self):
        ore_collected = 1000000000000
        max_fuel = 82892753
        min_fuel = 0
        fuel = round((min_fuel + max_fuel) / 2)

        while max_fuel-min_fuel != 1:
            ore = self.find_number_ore('FUEL', fuel)
            if ore > ore_collected:
                max_fuel = fuel
            elif ore < ore_collected:
                min_fuel = fuel
            elif ore == ore_collected:
                return fuel
            fuel = round((min_fuel + max_fuel) / 2)

        return min_fuel


if __name__ == "__main__":
    fuel_convertor = FuelConverter("../data/2019/day14.txt")
    # Part 1
    print(fuel_convertor.get_fuel())
    # Part 2
    print(fuel_convertor.find_number_fuel())
