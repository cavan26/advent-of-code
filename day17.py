import copy

class Cube:
    def __init__(self, file):
        self.cubes = {}
        self.max_x = []
        self.max_y = []
        self.max_z = []
        self.max_w = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        y = 0
        for line in lines:
            line = line.strip("\n")
            for x in range(len(line)):
                self.cubes[(x,y,0, 0)] = line[x]
            y += 1
        self.max_y = [-1, y + 1]
        self.max_x = [-1, len(line) + 1]
        self.max_z = [-1, 1]
        self.max_w = [-1, 1]

    def iteration(self, N):
        for i in range(N):
            cube_copy = copy.deepcopy(self.cubes)
            for x in range(self.max_x[0], self.max_x[1] + 1):
                for y in range(self.max_y[0], self.max_y[1] + 1):
                    for z in range(self.max_z[0], self.max_z[1] + 1):
                        for w in range(self.max_w[0], self.max_w[1] + 1):
                            if (x,y,z,w) not in self.cubes:
                                cube_copy[(x,y,z,w)] = "."
                                self.cubes[(x,y,z,w)] = "."
                            if self.cubes[(x,y,z,w)] == "#" and not (self.surrounded(x,y,z,w) == 2 or self.surrounded(x,y,z,w) == 3):
                                cube_copy[(x,y,z,w)] = "."
                            elif self.cubes[(x,y,z,w)] == "." and self.surrounded(x,y,z,w) == 3:
                                cube_copy[(x,y,z,w)] = "#"

            self.max_x = [self.max_x[0]-1, self.max_x[1]+1]
            self.max_y = [self.max_y[0]-1, self.max_y[1]+1]
            self.max_z = [self.max_z[0]-1, self.max_z[1]+1]
            self.max_w = [self.max_w[0]-1, self.max_w[1]+1]
            self.cubes = cube_copy
        return self.sum_active()

    def sum_active(self):
        print(self.cubes)
        return sum([1 for k, v in self.cubes.items() if v == "#"])


    def surrounded(self, x, y, z, w):
        surrounded = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if i== 0 and j== 0 and k==0 and l==0:
                            continue
                        else:
                            if (x + i, y + j, z + k, w + l) in self.cubes and self.cubes[(x + i, y + j, z + k, w + l)] == "#":
                                surrounded += 1
        return surrounded

if __name__ == "__main__":
    cube = Cube("data/day17.txt")
    print(cube.iteration(6))
