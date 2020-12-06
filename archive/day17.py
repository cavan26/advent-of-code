from day2 import IntcodeMachine
import sys
import time

ROTATION_MAP = {"N": 0, "E": 1, "S": 2, "W": 3}


class ScaffoldReader:
    def __init__(self):
        self.camera = IntcodeMachine("data/archive/day17.txt")
        self.coord = {}
        self.max_x = 0
        self.max_y = 0
        self.current_direction = ""
        self.robot_position = (0, 0)
        self.get_coordinates()
        self.directions = ["N", "E", "S", "W"]

    def get_coordinates(self):
        output = self.camera.add_input([])
        x = 0
        y = 0
        for el in output:
            if el == 35:
                self.coord[(x, y)] = 1
            if el == 94:
                self.coord[(x, y)] = 3
                self.current_direction = "N"
                self.robot_position = (x, y)
            x += 1
            if x > self.max_x:
                self.max_x = x
            if el == 10:
                y += 1
                x = 0
        self.max_y = y

    def draw_scaffold(self):
        sys.stdout.flush()
        for y in range(self.max_y + 1):
            line = ""
            for x in range(self.max_x + 1):
                if (x, y) in self.coord:
                    if (x, y) == self.robot_position:
                        line += "O"
                    else:
                        line += "#"
                else:
                    line += "."
            sys.stdout.write(line + "\n")

    def get_intersections(self):
        sum = 0
        for y in range(1, self.max_y):
            for x in range(1, self.max_x):
                if (x, y) in self.coord \
                        and (x-1, y) in self.coord \
                        and (x+1, y) in self.coord \
                        and (x, y-1) in self.coord \
                        and (x, y+1) in self.coord:
                    sum += x*y
        print(sum)

    def get_sourroundings(self):
        cardinal_points = [(self.robot_position[0], self.robot_position[1] - 1),
                         (self.robot_position[0] + 1, self.robot_position[1]),
                         (self.robot_position[0], self.robot_position[1] + 1),
                         (self.robot_position[0] - 1, self.robot_position[1])]
        rotation = cardinal_points[ROTATION_MAP[self.current_direction]:] + cardinal_points[:ROTATION_MAP[self.current_direction]]
        return rotation

    def move(self, direction, rotation):
        if direction == 'R':
            self.directions = self.directions[1:] + self.directions[:1]
            self.robot_position = rotation[1]
        elif direction == 'L':
            self.directions = self.directions[-1:] + self.directions[:-1]
            self.robot_position = rotation[-1]
        self.current_direction = self.directions[0]

    def get_path(self):
        path = []
        reached_end = False
        steps = 0
        turn = ""

        while not reached_end:
            rotation = self.get_sourroundings()
            if rotation[0] in self.coord:
                steps += 1
                self.robot_position = rotation[0]
            else:
                if turn != "":
                    path.append(turn + str(steps))
                steps = 1
                if rotation[1] in self.coord:
                    self.move('R', rotation)
                    turn = 'R'
                elif rotation[-1] in self.coord:
                    self.move('L', rotation)
                    turn = 'L'
                else:
                    reached_end = True
            self.draw_scaffold()
            sys.stdout.write(f"PATH : {path} \n")
            time.sleep(0.05)

        return path

    def find_longest_subroutines(self, path):
        subroutines = {}
        for i in range(len(path)):
            for j in range(3, 6):
                if i + j < len(path):
                    if "".join(path[i:i+j]) in subroutines:
                        subroutines["".join(path[i:i+j])] += 1
                    else:
                        subroutines["".join(path[i:i+j])] = 1
        sorted_subroutines = {k: v for k, v in sorted(subroutines.items(), key=lambda item: item[1], reverse=True)}
        print(sorted_subroutines)

    def get_output(self):
        input = []
        input.extend(self.get_input("A,A,B,C,A,C,A,B,C,B"))
        input.extend(self.get_input("R,12,L,8,R,6"))
        input.extend(self.get_input("R,12,L,6,R,6,R,8,R,6"))
        input.extend(self.get_input("L,8,R,8,R,6,R,12"))
        input.append(ord("n"))
        input.append(10)

        self.camera.intcode_list[0] = 2
        output = self.camera.add_input(input)
        print(f"Space dust: {output[-1]}")

    def get_input(self, string):
        splitted_string = string.split(",")
        input = []
        for s in splitted_string:
            if s.isdigit():
                input.append(ord(s[0]))
                if len(s) > 1:
                    input.append(ord(s[1]))
            if s == "A":
                input.append(65)
            elif s == "B":
                input.append(66)
            elif s == "C":
                input.append(67)
            elif s == "R":
                input.append(82)
            elif s == "L":
                input.append(76)
            input.append(44)
        input = input[:-1]
        input.append(10)
        return input


if __name__ == "__main__":
    scaffold = ScaffoldReader()
    scaffold.draw_scaffold()
    # scaffold.get_intersections()
    path = scaffold.get_path()
    scaffold.get_output()
