
class JoltDifference:
    def __init__(self, file):
        self.jolts = []
        self.read_file(file)
        self.memoiz = {}
        self.outlets = {}

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            self.jolts.append(int(line.strip()))
        self.jolts = sorted(self.jolts + [0])

    def jolt_diff(self):
        diff_1 = 1
        diff_3 = 1
        for i in range(len(self.jolts) - 1):
            if self.jolts[i+1] - self.jolts[i] == 1:
                diff_1 += 1
            elif self.jolts[i+1] - self.jolts[i] == 3:
                diff_3 += 1
        return diff_1 * diff_3

    def jolt_diff_arrangement(self, current_position):
        if current_position in self.memoiz:
            return self.memoiz[current_position]
        arrangements = 0
        for i in range(1, 4):
            if current_position + i > len(self.jolts) - 1:
                break
            if self.jolts[current_position + i] - self.jolts[current_position] <= 3:
                if current_position + i == len(self.jolts) - 1:
                    arrangements += 1
                    break
                arrangements += self.jolt_diff_arrangement(current_position + i)

        self.memoiz[current_position] = arrangements
        return arrangements


if __name__ == "__main__":
    checker = JoltDifference("data/day10.txt")
    print(f"Part 1: {checker.jolt_diff()}")
    print(f"Part 2: {checker.jolt_diff_arrangement(0)}")
