import sys
import copy
sys.path.insert(0, "/Users/camillevanassel/git/advent-of-code")


class Bugs:
    def __init__(self, file, size):
        self.bugs = {}
        self.layouts = set()
        self.read_file(file)
        self.bugs_levels = {}
        self.size = size
        empty_grid = {}
        for y in range(size):
            for x in range(size):
                empty_grid[(x, y)] = "."
        for i in range(-size, size+1):
            self.bugs_levels[i] = copy.deepcopy(empty_grid)
        self.bugs_levels[0] = copy.deepcopy(self.bugs)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        y = 0
        for line in lines:
            line = line.strip("\n")
            for x in range(len(line)):
                self.bugs[(x, y)] = line[x]
            y += 1

    def get_layout(self):
        layout = 0
        for y in range(5):
            for x in range(5):
                if self.bugs_levels[0].get((x, y)) == "#":
                    layout += 2 ** (y*5 + x)
        return layout

    def watch_bugs(self):
        has_repeated = False
        layout = self.get_layout()
        self.layouts.add(layout)
        while not has_repeated:
            copy_bugs = copy.deepcopy(self.bugs_levels[0])
            for bug in self.bugs_levels[0]:
                if self.bugs_levels[0][bug] == "#" and self.adjacent_bugs(bug, 0) != 1:
                    copy_bugs[bug] = "."
                elif self.bugs_levels[0][bug] == "." and (self.adjacent_bugs(bug, 0) == 1 or self.adjacent_bugs(bug, 0) == 2):
                    copy_bugs[bug] = "#"
            self.bugs_levels[0] = copy_bugs
            layout = self.get_layout()
            if layout in self.layouts:
                return layout
            else:
                self.layouts.add(layout)

    def adjacent_bugs(self, position, level):
        positions = [(position[0] - 1, position[1]), (position[0], position[1] + 1),
                     (position[0], position[1] - 1), (position[0] + 1, position[1])]
        adjacent_bugs = 0
        for p in positions:
            if p in self.bugs_levels[level]:
                if self.bugs_levels[level].get(p) == "#":
                    adjacent_bugs += 1
        return adjacent_bugs

    def adjacent_bugs_recursive(self, position, level):
        if level == self.size:
            return self.adjacent_bugs(position, level)
        adjacent_bugs = self.adjacent_bugs(position, level)
        if position == (2, 1):
            adjacent_bugs += self.get_adjacent_bugs([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], level + 1)
        elif position == (1, 2):
            adjacent_bugs += self.get_adjacent_bugs([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], level + 1)
        elif position == (3, 2):
            adjacent_bugs += self.get_adjacent_bugs([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)], level + 1)
        elif position == (2, 3):
            adjacent_bugs += self.get_adjacent_bugs([(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)], level + 1)
        if level != -self.size:
            if position[0] == 0:
                adjacent_bugs += self.get_adjacent_bugs([(2, 1)], level - 1)
            elif position[0] == 4:
                adjacent_bugs += self.get_adjacent_bugs([(2, 3)], level - 1)
            elif position[1] == 0:
                adjacent_bugs += self.get_adjacent_bugs([(1, 2)], level - 1)
            elif position[1] == 4:
                adjacent_bugs += self.get_adjacent_bugs([(3, 2)], level - 1)
        return adjacent_bugs

    def get_adjacent_bugs(self, positions, level):
        adjacent_bugs = 0
        for p in positions:
            if p in self.bugs_levels[level]:
                if self.bugs_levels[level].get(p) == "#":
                    adjacent_bugs += 1
        return adjacent_bugs

    def watch_bugs_recursive_levels(self, minutes):
        copy_bugs = copy.deepcopy(self.bugs_levels)
        for i in range(minutes):
            for level in range(-self.size, self.size):
                for bug in self.bugs_levels[level]:
                    if bug == (2, 2):
                        continue
                    elif self.bugs_levels[level][bug] == "#" and self.adjacent_bugs_recursive(bug, level) != 1:
                        copy_bugs[level][bug] = "."
                    elif self.bugs_levels[level][bug] == "." and (self.adjacent_bugs_recursive(bug, level) == 1 or
                                                                  self.adjacent_bugs_recursive(bug, level) == 2):
                        copy_bugs[level][bug] = "#"
            self.bugs_levels = copy.deepcopy(copy_bugs)
            self.number_of_bugs()
        return self.number_of_bugs()

    def number_of_bugs(self):
        s = 0
        for i in range(-self.size, self.size):
            for x in range(5):
                for y in range(5):
                    if self.bugs_levels[i][(x, y)] == "#":
                        s += 1
        return s

    def print_bugs(self):
        number_bugs = 0
        for i in range(-5, 6):
            print(f"Depth {i}")
            for y in range(5):
                line = ""
                for x in range(5):
                    line += (self.bugs_levels[i][(x, y)])
                print(line)
            print()
        return number_bugs


if __name__ == "__main__":
    bugs = Bugs("../data/2019/day24.txt", 10)
    # print(bugs.watch_bugs())
    print(bugs.watch_bugs_recursive_levels(10))

