
class Tobogan:
    def __init__(self, file):
        self.trees = {}
        self.width = 0
        self.length = 0
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        y = 0
        for line in lines:
            for x in range(len(line)):
                if line[x] == "#":
                    self.trees[x, y] = line[x]
            y += 1
            self.width = len(line)
        self.length = y

    def go_down_slope(self, right, down):
        x = 0
        y = 0
        trees = 0
        while y <= self.length + 1:
            if (x % self.width, y) in self.trees:
                trees += 1
            x += right
            y += down
        return trees

    def check_all_slopes(self):
        a = self.go_down_slope(1, 1)
        print(a)
        b = self.go_down_slope(3, 1)
        print(b)
        c = self.go_down_slope(5, 1)
        print(c)
        d = self.go_down_slope(7, 1)
        print(d)
        e = self.go_down_slope(1, 2)
        print(e)
        return a * b * c * d * e


if __name__ == "__main__":
    toboggan = Tobogan("data/day3.txt")
    print(toboggan.check_all_slopes())


