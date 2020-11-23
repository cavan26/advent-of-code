import numpy as np
import math


class FFT:
    def __init__(self, file):
        self.input = self.read_file(file)
        self.offset = self.get_offset()
        self.input_part_2 = self.repeat_list(self.input, 10000)
        self.input_part_2 = self.input_part_2[self.offset:]
        self.pattern = [0, 1, 0, -1]

    def get_offset(self):
        return int(''.join([str(i) for i in self.input[:7]]))

    def get_pattern(self, n):
        pattern = np.repeat(self.pattern, n)
        mult = math.ceil(len(self.input) / len(pattern)) + 1
        pattern = self.repeat_list(pattern, mult)
        pattern = pattern[1:]
        return pattern[:len(self.input)]

    def get_output(self):
        output = []
        for i in range(len(self.input)):
            pattern = self.get_pattern(i + 1)
            result = np.dot(pattern, self.input)
            output.append(self.get_last_digit(result))
        return output

    def run_phases_part_1(self, n):
        for i in range(n):
            output = self.get_output()
            self.input = output
        return output[:8]

    def run_phases_part_2(self, n):
        for i in range(n):
            output = self.get_output_part_2()
            self.input_part_2 = output
        return output[:8]

    def get_output_part_2(self):
        output = [0] * len(self.input_part_2)
        previous_sum = 0
        for i in range(len(self.input_part_2)-1, -1, -1):
            output[i] = self.get_last_digit(previous_sum + self.input_part_2[i])
            previous_sum = output[i]
        return output

    @staticmethod
    def get_last_digit(result):
        return int(str(result)[-1])

    @staticmethod
    def read_file(file):
        my_file = open(file, "r")
        elements = my_file.read()
        input = []
        for el in str(elements):
            input.append(int(el))
        return input

    @staticmethod
    def repeat_list(list, n):
        repeated_list = []
        for i in range(n):
            repeated_list.extend(list)
        return repeated_list


if __name__ == "__main__":
    fft = FFT("data/day16.txt")
    print(f"Part 1: {fft.run_phases_part_1(100)}")
    print(f"Part 2: {fft.run_phases_part_2(100)}")
