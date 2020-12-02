import re
import copy
from typing import List
from math import gcd

class MoonSystem:
    def __init__(self, file):
        self.position = {}
        self.velocities = {}
        self.initial_position = {}
        self.initial_velocity = {}
        self.initialize_system(file)
        self.number_of_moons = len(self.position)

    def initialize_system(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        i = 0
        for line in lines:
            coordinates = (re.findall(r'-?\d+\.?\d*', line ))
            for coord in coordinates:
                self.position.setdefault(i, []).append(int(coord))
                self.velocities.setdefault(i, []).append(0)
            i += 1
        self.initial_position = copy.deepcopy(self.position)
        self.initial_velocity = copy.deepcopy(self.velocities)

    def reset_system(self):
        self.position = self.initial_position
        self.velocities = self.initial_velocity

    def iteration(self):
        # Update velocity
        for moon in self.position:
            for i in range(len(self.position[moon])):
                dimension = [self.position[x][i] for x in self.position]
                self.velocities[moon][i] += sum(self.compare(self.position[moon][i], dimension))

        # update position
        for i in range(self.number_of_moons):
            for j in range(3):
                self.position[i][j] += self.velocities[i][j]

    @staticmethod
    def compare(a: int, b: List[int]):
        c = []
        for el in b:
            if el == a:
                c.append(0)
            elif el > a:
                c.append(1)
            elif el < a:
                c.append(-1)
        return c

    def run_steps(self, N):
        for i in range(N):
            self.iteration()

    def energy_kin(self, moon):
        energy = 0
        for coord in self.velocities[moon]:
            energy += abs(coord)
        return energy

    def energy_pot(self, moon):
        energy = 0
        for coord in self.position[moon]:
            energy += abs(coord)
        return energy

    def energy_system(self):
        energy_totale = 0
        for i in range(self.number_of_moons):
            energy_totale += self.energy_kin(i)*self.energy_pot(i)
        return energy_totale

    def find_period_moon(self):
        initial_position = {}
        initial_velocity = {}
        for i in range(3):
            initial_position[i] = [self.position[x][i] for x in self.position]
            initial_velocity[i] = [self.velocities[x][i] for x in self.velocities]
        period = 0
        periods = [None] * 3
        while not all([x is not None for x in periods]):
            self.iteration()
            period += 1
            for i in range(3):
                position = [self.position[x][i] for x in self.position]
                velocity = [self.velocities[x][i] for x in self.velocities]
                if position == initial_position[i] and velocity == initial_velocity[i] and periods[i] is None:
                    periods[i] = period
                    print(f"dimension {i}: period {period}")

        return self.lowest_common_denominator(periods)


    def lowest_common_denominator(self, periods):
        lcm = periods[0]
        for i in periods[1:]:
          lcm = lcm*i//gcd(lcm, i)
        return lcm


if __name__ == "__main__":
    # Part 1
    moons = MoonSystem("../data/2019/day12.txt")
    moons.run_steps(1000)
    print(moons.energy_system())
    print(moons.find_period_moon())

