from day2 import IntcodeMachine


class PaintingRobot():
    def __init__(self):
        self.machine = IntcodeMachine("data/2019/day11.txt")
        self.x = 0
        self.y = 0
        self.direction = ["UP", "LEFT", "DOWN", "RIGHT"]
        self.color = {}

    def paint_ship(self):
        output = self.machine.add_input([1])
        has_stopped = self.machine.is_halted()

        while not has_stopped:
            self.color[(self.x, self.y)] = output[0]
            self.change_direction(output[1])
            self.update_coordinates()
            output = self.machine.add_input([self.get_color_panel(self.x, self.y)])
            has_stopped = self.machine.is_halted()

    def get_color_panel(self, x, y):
        if (x, y) in self.color:
            return self.color[(x, y)]
        return 0

    def get_number_panels_painted(self):
        return len(self.color)

    def change_direction(self, side: int):
        if side == 1:
            self.direction = self.direction[-1:] + self.direction[:-1]
        elif side == 0:
            self.direction = self.direction[1:] + self.direction[:1]

    def update_coordinates(self):
        if self.direction[0] == "UP":
            self.y += 1
        elif self.direction[0] == "DOWN":
            self.y -= 1
        elif self.direction[0] == "RIGHT":
            self.x += 1
        elif self.direction[0] == "LEFT":
            self.x -= 1

    def get_extremes(self, coord: int):
        coordinate_list = self.color.keys()
        list_sorted = sorted(coordinate_list, key=lambda x: x[coord])
        return list_sorted[0][coord], list_sorted[-1][coord]

    def draw_result(self):
        X = self.get_extremes(0)
        Y = self.get_extremes(1)
        for y in range(Y[1]+1, Y[0]-1, -1):
            line = ""
            for x in range(X[0]-1, X[1]+1):
                color = self.get_color_panel(x, y)
                if color == 0:
                    line += "  "
                else:
                    line += "# "
            print(line)


if __name__ == "__main__":
    painting_machine = PaintingRobot()
    painting_machine.paint_ship()
    painting_machine.draw_result()