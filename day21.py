from day2 import IntcodeMachine

class Springdroid:
    def __init__(self):
        self.computer = IntcodeMachine("data/day21.txt")

    def convert_to_ASCII(self, program):
        ascii_list = []
        for c in program:
            ascii_list.append(ord(c))
        return ascii_list

    def get_output(self, program):
        input = self.convert_to_ASCII(program)
        output = self.computer.add_input(input)
        if output[-1] > 255:
            print(''.join(chr(i) for i in output[:-1]))
            return output[-1]
        print(''.join(chr(i) for i in output))


if __name__ == "__main__":
    robot = Springdroid()
    # damage_walk = robot.get_output("NOT A J\nNOT B T\nAND D T\nOR T J\nNOT C T\nAND D T\nOR T J\nWALK\n")
    damage_run = robot.get_output("NOT C T\nNOT F J\nAND D T\nAND T J\nNOT A T\nOR T J\nNOT B T\nAND D T\nOR T J\n"
                                  "NOT C T\nAND D T\nAND H T\nOR T J\nRUN\n")
    print(damage_run)