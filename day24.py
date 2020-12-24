import copy

class Tiles:
    def __init__(self, file):
        self.instructions = []
        self.read_file(file)
        self.black_tile = {}

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            self.instructions.append(line.strip("\n"))

    def read_instructions(self):
        for i in range(len(self.instructions)):
            j = 0
            x, y = (0, 0)
            while j < len(self.instructions[i]):
                if self.instructions[i][j] == "e":
                    x += 2
                    j += 1
                elif self.instructions[i][j:j+2] == "se":
                    x += 1
                    y -= 1
                    j += 2
                elif self.instructions[i][j:j+2] == "sw":
                    x -= 1
                    y -= 1
                    j += 2
                elif self.instructions[i][j] == "w":
                    x -= 2
                    j += 1
                elif self.instructions[i][j:j+2] == "nw":
                    y += 1
                    x -= 1
                    j += 2
                elif self.instructions[i][j:j+2] == "ne":
                    x += 1
                    y += 1
                    j += 2
            if (x, y) in self.black_tile:
                self.black_tile.pop((x,y))
            else:
                self.black_tile[(x, y)] = 1
        return len(self.black_tile)

    def get_extremes(self):
        x = [k[0] for k,v in self.black_tile.items()]
        y = [k[1] for k,v in self.black_tile.items()]
        return min(x), min(y), max(x), max(y)

    def flip_every_day(self, days):
        for day in range(days):
            x_min, y_min, x_max, y_max = self.get_extremes()
            tiles = copy.deepcopy(self.black_tile)
            for x in range(x_min-2, x_max+2):
                for y in range(y_min-2, y_max+2):
                    if (x,y) in self.black_tile and self.adjacent(x,y) > 2:
                        tiles.pop((x, y))
                    elif (x,y) in self.black_tile and self.adjacent(x,y) == 0:
                        tiles.pop((x, y))
                    elif (x,y) not in self.black_tile and self.adjacent(x,y) == 2:
                        tiles[(x, y)] = 1
            self.black_tile = tiles
        return len(self.black_tile)

    def adjacent(self, x, y):
        position = [(x-2, y), (x+2, y), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        adjacent = 0
        for p in position:
            if p in self.black_tile:
                adjacent += 1
        return adjacent


if __name__ == "__main__":
    tiles = Tiles("data/day24.txt")
    print(f"Part 1: {tiles.read_instructions()}")
    print(f"Part 2: {tiles.flip_every_day(100)}")
