import copy


LETTERS_CAPITAL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z']


class KeyFinder:
    def __init__(self, file, part2 = False):
        self.labyrinth = {}
        self.position = (0, 0)
        self.keys = {}
        self.doors = {}
        self.min_total_step = 1000000
        self.paths = {}
        self.random_walks = {}
        self.read_file(file)
        if part2:
            self.change_maze()
        self.find_all_paths()
        self.memoiz = {}

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        y = 0
        for line in lines:
            for x in range(len(line)):
                self.labyrinth[x, y] = line[x]
                if line[x] == "@":
                    self.keys[line[x]] = (x, y)
                    self.position = (x, y)
                    self.labyrinth[x, y] = '.'
                elif line[x] in LETTERS_CAPITAL:
                    self.doors[line[x]] = (x, y)
                elif line[x] in LETTERS:
                    self.keys[line[x]] = (x, y)
            y += 1

    def find_shortest_path(self, obtained_keys: list, current_key):
        if (current_key + ''.join(obtained_keys)) in self.memoiz:
            return self.memoiz[current_key + ''.join(obtained_keys)]

        random_walk = self.random_walks[current_key]
        min_next_step = 100000000
        ordered_keys = []
        for key in random_walk:
            if key not in obtained_keys:
                possible_path = [element[0] for element in random_walk[key] if len(set(element[1]) - set(obtained_keys)) == 0]
                if possible_path:
                    new_step = sorted(possible_path)[0]
                    (next_step, next_ordered_keys) = self.find_shortest_path(sorted(set(obtained_keys).union(set(key))), key)
                    step = next_step + new_step
                    if step < min_next_step:
                        ordered_keys = [key] + next_ordered_keys
                        min_next_step = step

        if min_next_step == 100000000:
            min_next_step = 0

        self.memoiz[current_key + ''.join(obtained_keys)] = (min_next_step, ordered_keys)
        return (min_next_step, ordered_keys)

    def find_all_paths(self):
        for key in self.keys:
            random_walk = RandomWalk(self.labyrinth, self.keys[key])
            self.random_walks[key] = random_walk.start_random_walk()

    def change_maze(self):
        self.keys["@"] = (self.position[0] - 1, self.position[1] + 1)
        self.keys["!"] = (self.position[0] + 1, self.position[1] + 1)
        self.keys["?"] = (self.position[0] + 1, self.position[1] - 1)
        self.keys["%"] = (self.position[0] - 1, self.position[1] - 1)

        self.labyrinth[(self.position[0], self.position[1])] = "#"
        self.labyrinth[(self.position[0] - 1, self.position[1])] = "#"
        self.labyrinth[(self.position[0] + 1, self.position[1])] = "#"
        self.labyrinth[(self.position[0], self.position[1] + 1)] = "#"
        self.labyrinth[(self.position[0], self.position[1] - 1)] = "#"

    def find_shortest_path_part2(self, obtained_keys: list, current_keys: list):
        if (''.join(current_keys) + ''.join(obtained_keys)) in self.memoiz:
            return self.memoiz[''.join(current_keys) + ''.join(obtained_keys)]

        min_next_step = 100000000
        ordered_keys = []
        for i in range(4):
            current_key = current_keys[i]
            random_walk = self.random_walks[current_key]
            for key in random_walk:
                if key not in obtained_keys:
                    possible_path = [element[0] for element in random_walk[key] if len(set(element[1]) - set(obtained_keys)) == 0]
                    if possible_path:
                        new_step = sorted(possible_path)[0]
                        next_keys = copy.deepcopy(current_keys)
                        next_keys[i] = key
                        (next_step, next_ordered_keys) = self.find_shortest_path_part2(sorted(set(obtained_keys).union(set(key))), next_keys)
                        step = next_step + new_step
                        if step < min_next_step:
                            ordered_keys = [key] + next_ordered_keys
                            min_next_step = step

        if min_next_step == 100000000:
            min_next_step = 0

        self.memoiz[''.join(current_keys) + ''.join(obtained_keys)] = (min_next_step, ordered_keys)
        return (min_next_step, ordered_keys)


class RandomWalk:
    def __init__(self, labyrinth, position_initiale):
        self.labyrinth = labyrinth
        self.position_initiale = position_initiale
        self.step_to_key = {}

    def random_walk(self, position, steps, already_visited, doors):
        directions = [(position[0] + 1, position[1]), (position[0] - 1, position[1]),
                      (position[0], position[1] + 1), (position[0], position[1] - 1)]
        for dir in directions:
            new_doors = copy.deepcopy(doors)
            if dir not in already_visited and self.labyrinth[dir] != "#":
                if self.labyrinth[dir] in LETTERS_CAPITAL:
                    new_doors.add(self.labyrinth[dir].lower())
                elif self.labyrinth[dir] in LETTERS:
                    if self.labyrinth[dir] in self.step_to_key:
                        self.step_to_key[self.labyrinth[dir]].append((steps+1, new_doors))
                    else:
                        self.step_to_key[self.labyrinth[dir]] = [(steps+1, new_doors)]
                already_visited[dir] = 1
                position = dir
                self.random_walk(position, steps + 1, already_visited, new_doors)
                already_visited.pop(dir, None)

    def start_random_walk(self):
        self.random_walk(self.position_initiale, 0, {self.position_initiale: 1}, set())
        return self.step_to_key


if __name__ == "__main__":
    # Part 1
    finder = KeyFinder("../data/2019/day18.txt")
    x = finder.find_shortest_path(set(), "@")
    print(x)

    # Part 2
    finder = KeyFinder("../data/2019/day18.txt", True)
    x = finder.find_shortest_path_part2(set(), ["@", "!", "?", "%"])
    print(x)