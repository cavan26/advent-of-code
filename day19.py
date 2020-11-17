from day2 import IntcodeMachine


class TractorBeam:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.map = {}
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def get_map(self):
        print("Calculating map...")
        (limit_x_min, limit_x_max) = self.check_entire_line(self.min_y)
        print((limit_x_min, limit_x_max))
        for y in range(self.min_y, self.max_y):
            i = 0
            while limit_x_min + i < limit_x_max:
                beam = IntcodeMachine("data/day19.txt")
                output = beam.add_input([limit_x_min + i, y])
                if output[0] == 1:
                    self.map[limit_x_min + i, y] = 1
                    limit_x_min += i
                    break
                elif output[0] == 0:
                    i += 1
            i = 0
            while limit_x_max + i < self.max_x:
                beam = IntcodeMachine("data/day19.txt")
                output = beam.add_input([limit_x_max + i, y])
                if output[0] == 1:
                    self.map[limit_x_max + i, y] = 1
                    i += 1
                elif output[0] == 0:
                    if y <= 2:
                        limit_x_max += 1
                    limit_x_max += i
                    for x in range(limit_x_min, limit_x_max):
                        self.map[x, y] = 1
                    break

    def check_entire_line(self, y):
        limit_x_min = None
        limit_x_max = None
        for x in range(self.min_x, self.max_x):
            beam = IntcodeMachine("data/day19.txt")
            output = beam.add_input([x, y])
            if output[0] == 1 and limit_x_min is None:
                limit_x_min = x
            elif output[0] == 0 and limit_x_min is not None and limit_x_max is None:
                limit_x_max = x
                break
        return limit_x_min, limit_x_max

    def is_line_empty(self, y):
        (limit_x_min, limit_x_max) = self.check_entire_line(y)
        if limit_x_min is None and limit_x_max is None:
            return True
        return False

    def is_attracted(self, x, y):
        beam = IntcodeMachine("data/day19.txt")
        output = beam.add_input([x, y])
        if output[0] == 0:
            return False
        elif output[0] == 1:
            return True

    def get_number_affected_points(self, max_x, max_y):
        sum = 0
        for y in range(max_y):
            line = ""
            for x in range(max_x):
                if self.is_attracted(x, y):
                    sum += 1
                    line += "#"
                else:
                    line += "."
            print(line)

        return sum

    def get_coordinate_ship(self, size):
        coords = []
        for coord in self.map.keys():
            if self.is_ship_fitting(coord, size):
                coords.append(coord)
        return sorted(coords, key=lambda x: self.distance_to_beam(x))[0]

    def is_ship_fitting(self, coord, size):
        for x in range(size):
            for y in range(size):
                if (coord[0]+x, coord[1]+y) not in self.map:
                    return False
        return True

    @staticmethod
    def distance_to_beam(coord):
        return coord[0]**2 + coord[1]**2

    def draw_map(self):
        for y in range(self.min_y, self.max_y):
            line = ""
            for x in range(self.min_x, self.max_x):
                if (x, y) in self.map:
                    line += "#"
                else:
                    line += "."
            print(line)


if __name__ == "__main__":
    beam = TractorBeam(0, 2000, 0, 2000)
    # beam.get_number_affected_points(100, 100)
    beam.get_map()
    # beam.draw_map()
    print(beam.get_coordinate_ship(100))