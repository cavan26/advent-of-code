class IntcodeMachine:
    def __init__(self, file: str):
        self.position = 0
        self.intcode_list = {}
        self.load_intcode(file)
        self.input = []
        self.output = []
        self.is_stopped = False
        self.relative_base_offset = 0

    def load_intcode(self, file):
        my_file = open(file, "r")
        elements = my_file.read().split(",")
        my_file.close()
        for i in range(len(elements)):
            self.intcode_list[i] = int(elements[i])

    def set_intcode(self, pos: int, value: int, mode: int):
        if mode == 2:
            self.intcode_list[pos + self.relative_base_offset] = value
        else:
            self.intcode_list[pos] = value

    def get(self, pos):
        if pos in self.intcode_list:
            return self.intcode_list[pos]
        return 0

    def get_incode(self, pos: int, mode: int):
        if mode == 0:  # position mode
            return self.get(self.get(pos))
        elif mode == 1:  # immediate mode
            return self.get(pos)
        elif mode == 2:  # relative mode
            return self.get(self.get(pos) + self.relative_base_offset)

    def instruction_1(self, code):
        self.set_intcode(self.get_incode(self.position + 3, 1),
                         self.get_incode(self.position + 1, code[1]) + self.get_incode(self.position + 2, code[2]),
                         code[3])
        self.position += 4

    def instruction_2(self, code):
        self.set_intcode(self.get_incode(self.position + 3, 1),
                         self.get_incode(self.position + 1, code[1]) * self.get_incode(self.position + 2, code[2]),
                         code[3])
        self.position += 4

    def instruction_3(self, code):
        self.set_intcode(self.get_incode(self.position + 1, 1), self.input[0], code[1])
        self.input.pop(0)
        self.position += 2

    def instruction_4(self, code):
        output = self.get_incode(self.position + 1, code[1])
        self.position += 2
        return output

    def instruction_5(self, code):
        if self.get_incode(self.position + 1, code[1]) != 0:
            self.position = self.get_incode(self.position + 2, code[2])
        else:
            self.position += 3

    def instruction_6(self, code):
        if self.get_incode(self.position + 1, code[1]) == 0:
            self.position = self.get_incode(self.position + 2, code[2])
        else:
            self.position += 3

    def instruction_7(self, code):
        if self.get_incode(self.position + 1, code[1]) < self.get_incode(self.position + 2, code[2]):
            self.set_intcode(self.get_incode(self.position + 3, 1), 1, code[3])
        else:
            self.set_intcode(self.get_incode(self.position + 3, 1), 0, code[3])
        self.position += 4

    def instruction_8(self, code):
        if self.get_incode(self.position + 1, code[1]) == self.get_incode(self.position + 2, code[2]):
            self.set_intcode(self.get_incode(self.position + 3, 1), 1, code[3])
        else:
            self.set_intcode(self.get_incode(self.position + 3, 1), 0, code[3])
        self.position += 4

    def instruction_9(self, code):
        self.relative_base_offset += self.get_incode(self.position + 1, code[1])
        self.position += 2

    @staticmethod
    def get_instructions(code: int):
        instructions = [code % 100]
        for i in range(2, 5):
            instructions.append(code // 10 ** i % 10)
        return instructions

    def run_machine(self):
        code = self.get_instructions(self.get_incode(self.position, 1))
        while code[0] != 99:
            code = self.get_instructions(self.get_incode(self.position, 1))
            if code[0] == 1:
                self.instruction_1(code)
            elif code[0] == 2:
                self.instruction_2(code)
            elif code[0] == 3:
                if len(self.input) == 0:
                    output = self.output
                    self.output = []
                    return output
                self.instruction_3(code)
            elif code[0] == 4:
                self.output.append(self.instruction_4(code))
            elif code[0] == 5:
                self.instruction_5(code)
            elif code[0] == 6:
                self.instruction_6(code)
            elif code[0] == 7:
                self.instruction_7(code)
            elif code[0] == 8:
                self.instruction_8(code)
            elif code[0] == 9:
                self.instruction_9(code)
            elif code[0] == 99:
                self.is_stopped = True

        return self.output

    def add_input(self, input) -> list[int]:
        self.input = self.input + input
        return self.run_machine()

    def get_output(self):
        return self.output

    def is_halted(self):
        return self.is_stopped


if __name__ == "__main__":
    machine = IntcodeMachine("data/day5.txt")
    print(machine.add_input([5]))


