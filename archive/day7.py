from day2 import IntcodeMachine
from itertools import permutations


class Amplifier():
    def __init__(self, number_amplifier, phase_setting_sequence):
        self.number_amplifiers = number_amplifier
        self.phase_setting_sequence = phase_setting_sequence
        self.amplifiers: list[IntcodeMachine] = []
        self.still_running = True

    def run_amplifiers(self):
        input = [self.phase_setting_sequence[0], 0]

        for i in range(1, self.number_amplifiers):
            output = self.get_output(input)
            input = [self.phase_setting_sequence[i]] + output

        return self.get_output(input)

    @staticmethod
    def get_output(input) -> list[int]:
        machine = IntcodeMachine("data/archive/day7.txt")
        return machine.add_input(input)

    def create_amplifier(self,  input) -> list[int]:
        self.amplifiers.append(IntcodeMachine("data/archive/day7.txt"))
        return self.amplifiers[-1].add_input(input)

    def create_amplifiers(self) -> list[int]:
        output = [0]
        has_halted = False
        for i in range(self.number_amplifiers):
            input = [self.phase_setting_sequence[i]] + output
            output = self.create_amplifier(input)
            if self.amplifiers[i].is_stopped:
                has_halted = True
        return output, has_halted

    def run_loop(self, output):
        has_halted = False
        for i in range(self.number_amplifiers):
            input =  output
            output = self.amplifiers[i].add_input(input)
            if self.amplifiers[i].is_stopped:
                has_halted = True
        return output, has_halted

    def run_amplifiers_feedback_loop(self):
        output, has_halted = self.create_amplifiers()
        while not has_halted:
            output, has_halted = self.run_loop(output)
        return output


def amplification_circuit():
    phase_settings = [0, 1, 2, 3, 4]
    config = []
    max_amplifier = 0

    for phase_settings_permutation in list(permutations(phase_settings)):
        amplifiers = Amplifier(5, phase_settings_permutation)
        output = amplifiers.run_amplifiers()[0]
        if output > max_amplifier:
            max_amplifier = output
            config = phase_settings_permutation

    print(f"The max amplification is {max_amplifier} for config {config}")


def amplification_circuit_feedback_loop():
    phase_settings = [5, 6, 7, 8, 9]
    config = []
    max_amplifier = 0

    for phase_settings_permutation in list(permutations(phase_settings)):
        amplifiers = Amplifier(5, phase_settings_permutation)
        output = max(amplifiers.run_amplifiers_feedback_loop())
        if output > max_amplifier:
            max_amplifier = output
            config = phase_settings_permutation

    print(f"The max amplification is {max_amplifier} for config {config}")


if __name__ == "__main__":
    amplification_circuit_feedback_loop()
