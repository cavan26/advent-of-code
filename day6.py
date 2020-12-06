
class Questions:
    def __init__(self, file):
        self.groups = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        group = {}
        number_of_passengers = 0
        for line in lines:
            if line == "\n":
                self.groups.append(len({k:v for k,v in group.items() if v==number_of_passengers}))
                group = {}
                number_of_passengers = 0
            else:
                number_of_passengers += 1
                line = line.strip("\n")
                for char in line:
                    group[char] = group.setdefault(char, 0) + 1
        self.groups.append(len({k: v for k, v in group.items() if v == number_of_passengers}))

    def get_numbers(self):
        print(self.groups)
        return sum(self.groups)


if __name__ == "__main__":
    quest = Questions("data/day6.txt")
    print(quest.get_numbers())

