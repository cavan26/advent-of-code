from day2 import IntcodeMachine

class Droid:
    def __init__(self):
        self.intcode_machine = IntcodeMachine("data/2019/day25.txt")

    def move(self):
        while True:
            instruction = input("=> ")
            input_robot = []
            for char in instruction:
                input_robot.append(ord(char))
            input_robot.append(10)
            print(''.join(chr(i) for i in self.intcode_machine.add_input(input_robot)))


if __name__ == "__main__":
    droid = Droid()
    droid.move()
