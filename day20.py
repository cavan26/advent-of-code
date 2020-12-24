from collections import defaultdict


class Jigsaw:
    def __init__(self, file):
        self.tiles = {}
        self.borders = defaultdict(list)
        self.read_file(file)
        self.get_borders()

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        y = 0
        for line in lines:
            line = line.strip("\n")
            if line == "":
                self.tiles[tile_number] = tile
                y = 0
            elif line.startswith("Tile"):
                tile_number = int(line.split(":")[0].split(" ")[1])
                tile = {}
            else:
                for x in range(len(line)):
                    tile[x, y] = line[x]
                y += 1
        self.tiles[tile_number] = tile

    def get_borders(self):
        for tile in self.tiles:
            self.borders[tile].append("".join([self.tiles[tile][i, 0] for i in range(10)]))
            self.borders[tile].append("".join([self.tiles[tile][i, 9] for i in range(10)]))
            self.borders[tile].append("".join([self.tiles[tile][9, i] for i in range(10)]))
            self.borders[tile].append("".join([self.tiles[tile][0, i] for i in range(10)]))

    @staticmethod
    def flip(line):
        return "".join([line[i] for i in range(len(line)-1, -1, -1)])

    def get_corners(self):
        corners = []
        for tile in self.tiles:
            other_borders = [self.borders[t] for t in self.borders if t != tile]
            flat_list = [item for sublist in other_borders for item in sublist]
            non_matching = 0
            for borders in self.borders[tile]:
                if borders not in flat_list and self.flip(borders) not in flat_list:
                    non_matching += 1
            if non_matching == 2:
                corners.append(tile)
        r = 1
        for tile in corners:
            r = r*tile
        return r

    def get_image(self):
        return


if __name__ == "__main__":
    jigsaw = Jigsaw("data/day20.txt")
    print(jigsaw.get_corners())
