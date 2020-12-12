import math

class Ship:
    def __init__(self, file):
        self.instruction = []
        self.read_file(file)
        self.current_x = 0
        self.current_y = 0
        self.current_orientation = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.x_waypoint = 10
        self.y_waypoint = 1

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            line = line.strip("\n")
            self.instruction.append((line[0], int(line[1:])))

    def navigate(self):
        for instruction in self.instruction:
            self.follow_instruction(instruction)
        return abs(self.current_y) + abs(self.current_x)

    def follow_instruction(self, instruction):
        if instruction[0] == "N":
            self.y_waypoint += instruction[1]
        elif instruction[0] == "S":
            self.y_waypoint -= instruction[1]
        elif instruction[0] == "E":
            self.x_waypoint += instruction[1]
        elif instruction[0] == "W":
            self.x_waypoint -= instruction[1]
        elif instruction[0] == "L":
            self.rotate_waypoint(-1*instruction[1])
        elif instruction[0] == "R":
            self.rotate_waypoint(instruction[1])
        elif instruction[0] == "F":
            self.current_x += instruction[1]*self.x_waypoint
            self.current_y += instruction[1]*self.y_waypoint

    @staticmethod
    def rotate(l, n):
        d = int(n / 90)
        return l[d:] + l[:d]

    def rotate_waypoint(self, degres):
        degres = math.radians(degres)
        x = math.cos(degres) * self.x_waypoint + math.sin(degres) * self.y_waypoint
        y = - math.sin(degres) * self.x_waypoint + math.cos(degres) * self.y_waypoint
        self.x_waypoint = round(x)
        self.y_waypoint = round(y)


if __name__ == "__main__":
    ship = Ship("data/day12.txt")
    print(ship.navigate())