

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class DonutMaze:
    def __init__(self, file):
        self.maze = {}
        self.doors = {}
        self.doors_position = {}
        self.door_coordinates = {}
        self.read_maze(file)
        self.get_doors()
        self.paths = self.find_all_path_to_doors()
        self.max_level = 10000000
        self.memoiz = {}

    def read_maze(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        y = 0
        for line in lines:
            for x in range(len(line)):
                if line[x] != " " and line[x] != "\n":
                    self.maze[x, y] = line[x]
            y += 1

    def get_surroundings(self, x, y, first_letter):
        if (x+1, y) in self.maze and self.maze[(x+1, y)] in LETTERS:
            second_letter = self.maze[(x+1, y)]
            if (x+2, y) in self.maze and self.maze[(x+2, y)] == ".":
                self.set_door_position((x+2, y), first_letter, second_letter)
            if (x-1, y) in self.maze and self.maze[(x-1, y)] == ".":
                self.set_door_position((x-1, y), first_letter, second_letter)

        elif (x, y+1) in self.maze and self.maze[(x, y+1)] in LETTERS:
            second_letter = self.maze[(x, y + 1)]
            if (x, y+2) in self.maze and self.maze[(x, y+2)] == ".":
                self.set_door_position((x, y+2), first_letter, second_letter)
            if (x, y-1) in self.maze and self.maze[(x, y-1)] == ".":
                self.set_door_position((x, y-1), first_letter, second_letter)

    def set_door_position(self, pos, first_letter, second_letter):
        self.door_coordinates[pos] = ''.join(sorted([first_letter, second_letter]))
        if ''.join(sorted([first_letter, second_letter])) in self.doors_position:
            self.doors_position[''.join(sorted([first_letter, second_letter]))].append(pos)
        else:
            self.doors_position[''.join(sorted([first_letter, second_letter]))] = [pos]

    def get_doors(self):
        for position in self.maze:
            if self.maze[position] in LETTERS:
                self.get_surroundings(position[0], position[1], self.maze[position])
        for doors in self.doors_position:
            if len(self.doors_position[doors]) == 2:
                self.doors[self.doors_position[doors][0]] = self.doors_position[doors][1]
                self.doors[self.doors_position[doors][1]] = self.doors_position[doors][0]

    def find_all_path_to_doors(self):
        all_random_walks = {}
        for door in self.doors_position:
            for coord in self.doors_position[door]:
                walk = RandomWalk(self.maze, self.door_coordinates)
                walk.random_walk(coord, 0, {coord: 1})
                if door in all_random_walks:
                    all_random_walks[door].update(walk.step_to_door)
                else:
                    all_random_walks[door] = walk.step_to_door
        return all_random_walks

    def find_shortest_path(self, current_door, doors: list, current_level):
        if (current_door + ''.join(doors)) in self.memoiz:
            return self.memoiz[current_door + ''.join(doors)]

        path = self.paths[current_door]
        min_next_step = 1000000
        min_doors = []
        sorted_path = {k: v for k, v in sorted(path.items(), key=lambda item: item[1][1])}
        for door in sorted_path:
            if current_level == 0 and path[door][1] == -1:
                continue
            if current_level != 0:
                if door == "AA" or door == "ZZ":
                    continue
            new_level = current_level + path[door][1]
            if new_level > self.max_level:
                continue
            if door + str(new_level) not in doors and new_level < 20:
                new_step = path[door][0]
                if door + str(current_level) != "ZZ0":
                    (next_step, next_doors) = self.find_shortest_path(door, doors + [door + str(new_level)], new_level)
                    step = next_step + new_step + 1
                    if step < min_next_step:
                        min_doors = [door] + next_doors
                        min_next_step = step
                else:
                    print("Found one")
                    if new_level < self.max_level:
                        self.max_level = new_level
                        min_next_step = new_step
                    min_doors = ["ZZ0"]
        self.memoiz[(current_door + ''.join(doors))] = (min_next_step, min_doors)
        return min_next_step, min_doors


class RandomWalk:
    def __init__(self, maze, coordinates_doors):
        self.maze = maze
        self.coordinates_doors = coordinates_doors
        self.step_to_door = {}
        self.steps = 100000

    def random_walk(self, position, steps, already_visited):
        directions = [(position[0] + 1, position[1]), (position[0] - 1, position[1]),
                      (position[0], position[1] + 1), (position[0], position[1] - 1)]

        for dir in directions:
            if dir not in already_visited and self.maze[dir] == ".":
                if dir in self.coordinates_doors:
                    if self.coordinates_doors[dir] in self.step_to_door and self.step_to_door[self.coordinates_doors[dir]][0] < steps:
                        continue
                    door_level = -1 if self.is_outward_door(dir) else 1
                    self.step_to_door[self.coordinates_doors[dir]] = (steps + 1, door_level)
                else:
                    already_visited[dir] = 1
                    position = dir
                    self.random_walk(position, steps + 1, already_visited)
                already_visited.pop(dir, None)

    def is_outward_door(self, coordinates):
        max_x = sorted(self.maze.keys(), key=lambda x: x[0], reverse=True)[0][0]
        max_y = sorted(self.maze.keys(), key=lambda x: x[1], reverse=True)[0][1]

        if coordinates[0] == 2 or coordinates[0] == max_x or coordinates[1] == 2 or coordinates[1] == max_y:
            return True
        return False


if __name__ == "__main__":
    ## Part 1
    maze = DonutMaze("../data/2019/day20.txt")
    print(maze.find_shortest_path("AA", ["AA"], 0))



