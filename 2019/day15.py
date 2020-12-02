from day2 import IntcodeMachine
import copy
import sys
import time


class Droid:
    def __init__(self):
        self.machine = IntcodeMachine("data/2019/day15.txt")
        self.map = {}
        self.coord = (0, 0)

    def move(self, direction):
        output = self.machine.add_input([direction])
        if output[0] == 0:
            self.map[self.update_coordinates(direction)] = 0
        elif output[0] == 1:
            self.coord = self.update_coordinates(direction)
            self.map[self.coord] = 1
        elif output[0] == 2:
            self.coord = self.update_coordinates(direction)
        return output[0]

    def update_coordinates(self, direction):
        x = self.coord[0]
        y = self.coord[1]
        if direction == 1:
            y += 1
        elif direction == 2:
            y -= 1
        elif direction == 3:
            x -= 1
        elif direction == 4:
            x += 1
        return x, y

    def already_visited(self, direction):
        if self.update_coordinates(direction) in self.map:
            return True
        return False


class PathFinder:
    def __init__(self):
        self.paths = []
        self.global_map = {}
        self.opposite_direction = {1: 2, 2: 1, 3: 4, 4: 3}
        self.current_pos = (0, 0)
        self.max_path = 0
        self.oxygen_machine = None

    def get_possible_paths(self):
        path = [(0, 0)]
        self.try_direction(1, Droid(), path)
        self.try_direction(2, Droid(), path)
        self.try_direction(3, Droid(), path)
        self.try_direction(4, Droid(), path)

    def try_direction(self, direction, old_droid, path):
        droid = copy.deepcopy(old_droid)
        output = droid.move(direction)
        self.current_pos = droid.coord
        self.draw()
        time.sleep(0.05)
        if output == 0:  # We hit a wall
            self.global_map[droid.update_coordinates(direction)] = 0
        elif output == 1:  # We continue the exploration
            path.append(droid.coord)
            self.global_map[droid.coord] = 1
            for i in range(1, 5):
                if not droid.already_visited(i):
                    self.try_direction(i, droid, copy.deepcopy(path))
        elif output == 2:  # We found the oxygen generator
            self.global_map[droid.coord] = 2
            path.append(droid.coord)
            self.paths.append(path)
            self.oxygen_machine = droid

    def get_smallest_path(self):
        smallest_path = len(sorted(self.paths, key= lambda x: len(x))[0])
        print(f"The droid explored {len(self.paths)} successful path(s): {smallest_path}")
        return smallest_path

    def draw(self):
        X = (-25, 25)
        Y = (-15, 25)
        sys.stdout.flush()
        for y in range(Y[1] + 1, Y[0] - 1, -1):
            line = ""
            for x in range(X[0] - 1, X[1] + 1):
                if x == 0 and y == 0:
                    line += "S"
                elif x == self.current_pos[0] and y == self.current_pos[1]:
                    line += "X"
                else:
                    if (x, y) in self.global_map:
                        if self.global_map[(x, y)] == 0:
                            line += "#"
                        elif self.global_map[(x, y)] == 1:
                            line += "."
                        elif self.global_map[(x, y)] == 2:
                            line += "O"
                    else:
                        line += " "
            sys.stdout.write(line + "\n")

    def get_extremes(self, coord: int):
        coordinate_list = self.global_map.keys()
        list_sorted = sorted(coordinate_list, key=lambda x: x[coord])
        return list_sorted[0][coord], list_sorted[-1][coord]

    def get_farthest_block(self):
        # Start exploring from oxygen machine
        path = [(0, 0)]
        self.oxygen_machine.map = {}
        self.explore_from_oxygen_machine(1, self.oxygen_machine, path)
        self.explore_from_oxygen_machine(2, self.oxygen_machine, path)
        self.explore_from_oxygen_machine(3, self.oxygen_machine, path)
        self.explore_from_oxygen_machine(4, self.oxygen_machine, path)

        print(f"The farthest block is {self.max_path} blocks away from the starting block")
        return self.max_path

    def explore_from_oxygen_machine(self, direction, old_droid, path):
        droid = copy.deepcopy(old_droid)
        output = droid.move(direction)
        if output == 1:  # We continue the exploration
            path.append(droid.coord)
            if len(path) > self.max_path:
                self.max_path = len(path)
            self.global_map[droid.coord] = 1
            for i in range(1, 5):
                if not droid.already_visited(i):
                    self.explore_from_oxygen_machine(i, droid, copy.deepcopy(path))


if __name__ == "__main__":
    path_finder = PathFinder()
    path_finder.get_possible_paths()
    path_finder.get_smallest_path()
    path_finder.get_farthest_block()
