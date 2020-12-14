import itertools
import copy

class DockingData:
    def __init__(self, file):
        self.mask = []
        self.instruction = []
        self.read_file(file)
        self.memory = {}

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        i = 0
        for line in lines:
            l = line.strip("\n").split("=")
            if l[0].strip() == "mask":
                self.mask.append(l[1].strip())
                i += 1
            else:
                memory = l[0].split("[")[1].split("]")[0]
                self.instruction.append((memory, l[1].strip(), i-1))

    def apply_operations(self):
        for instruction in self.instruction:
            mask = self.mask[instruction[2]]
            number = str(bin(int(instruction[1])))[2:]
            if len(number) < len(mask):
                number = "0" * (len(mask) - len(number)) + number
            for c in range(0, len(mask)):
                if mask[c] != "X":
                    number = number[:c] + mask[c] + number[c+1:]

            self.memory[instruction[0]] = int(number, 2)

        s = 0
        for mem in self.memory:
           s += self.memory[mem]
        return s

    def second_decoder(self):
        for instruction in self.instruction:
            mask = self.mask[instruction[2]]
            position = str(bin(int(instruction[0])))[2:]
            if len(position) < len(mask):
                position = "0" * (len(mask) - len(position)) + position
            for c in range(len(mask)):
                if mask[c] == "1":
                    position = position[:c] + mask[c] + position[c+1:]
            number_x = sum([1 for x in mask if x == "X"])
            binaries = [list(i) for i in itertools.product([0, 1], repeat=number_x)]
            position_iter = copy.deepcopy(position)
            for i in range(len(binaries)):
                j = 0
                for k in range(len(mask)):
                    if mask[k] == "X":
                        position_iter = position_iter[:k] + str(binaries[i][j]) + position_iter[k+1:]
                        j += 1
                self.memory[int(position_iter, 2)] = int(instruction[1])

        return sum([v for k,v in self.memory.items()])


if __name__ == "__main__":
    data = DockingData("data/day14.txt")
    print(f"Part 1: {data.apply_operations()}")
    print(f"Part 2: {data.second_decoder()}")
