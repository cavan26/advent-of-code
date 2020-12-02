
class CoinCollector():
    def __init__(self, file):
        self.list_ints = []
        self.read_file(file)
        self.solve()

    def read_file(self, file):
        file1 = open(file, 'r')
        for line in file1.readlines():
            self.list_ints.append(int(line.strip('\n')))

    def solve(self):
        for i in range(len(self.list_ints)):
            for j in range(i+1, len(self.list_ints)):
                for k in range(j, len(self.list_ints)):
                    if self.list_ints[i] + self.list_ints[j] + self.list_ints[k] == 2020:
                        print(f"{self.list_ints[i]} and {self.list_ints[j]} and {self.list_ints[k]}")
                        print(self.list_ints[i] * self.list_ints[j] * self.list_ints[k])

if __name__ == "__main__":
    collector = CoinCollector("data/day1.txt")