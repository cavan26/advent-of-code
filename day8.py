import copy

class Accumulator:
    def __init__(self, file):
        self.accumulator = 0
        self.program = {}
        self.visited_position = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        i = 0
        for line in lines:
            instruction = line.strip().split(" ")[0]
            number = int(line.strip().split(" ")[1].replace("+", ""))
            self.program[i] = (instruction, number)
            i += 1

    def run_prgram(self):
        i = 0
        while i not in self.visited_position:
            self.visited_position.append(i)
            if self.program[i][0] == "acc":
                self.accumulator += self.program[i][1]
                i += 1
            elif self.program[i][0] == "jmp":
                i += self.program[i][1]
            elif self.program[i][0] == "nop":
                i += 1

    def terminates(self, program) -> bool:
        i = 0
        visited_position = []
        terminated = False
        while i not in visited_position:
            if i == len(program) - 1:
                terminated =  True
            visited_position.append(i)
            if program[i][0] == "acc":
                self.accumulator += self.program[i][1]
                i += 1
            elif program[i][0] == "jmp":
                i += self.program[i][1]
            elif program[i][0] == "nop":
                i += 1
            if terminated:
                return True
        return False

    def try_all_combination(self):
        for i in self.program:
            new_program = copy.deepcopy(self.program)
            if new_program[i][0] == "acc":
                continue
            elif new_program[i][0] == "jmp":
                print(f"Position {i}: change jmp into nop")
                new_program[i] = ("nop", new_program[i][1])
            elif new_program[i][0] == "nop":
                print(f"Position {i}: change nop into jmp")
                new_program[i] = ("jmp", new_program[i][1])
            self.accumulator = 0
            if self.terminates(new_program):
                print(self.accumulator)


if __name__ == "__main__":
    accumulator = Accumulator("data/day8.txt")
    print(accumulator.program)
    accumulator.try_all_combination()