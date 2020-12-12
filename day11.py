import collections
import copy

class SeatAllocation:
    def __init__(self, file):
        self.seats = collections.OrderedDict()
        self.max_x = 0
        self.max_y = 0
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        i = 0
        for line in lines:
            line = line.strip("\n")
            for j in range(len(line)):
                if line[j] == "L":
                    self.seats[(i, j)] = "L"
                elif line[j] == "#":
                    self.seats[(i, j)] = "#"
            i += 1
        self.max_x = i
        self.max_y = len(line) - 1

    def iterations(self):
        current_state = list(self.seats.values())
        previous_state = []

        while previous_state != current_state:
            new_seating_plan = copy.deepcopy(self.seats)
            for seat in self.seats:
                if self.seats[seat] == "L" and self.is_surrounded_new_rule(seat) == 0:
                    new_seating_plan[seat] = "#"
                elif self.seats[seat] == "#" and self.is_surrounded_new_rule(seat) >= 5:
                    new_seating_plan[seat] = "L"
            self.seats = new_seating_plan
            previous_state = current_state
            current_state = list(self.seats.values())
        return self.occupied_seats()

    def is_surrounded(self, position):
        positions = [(position[0] - 1, position[1]), (position[0] - 1, position[1] + 1),
                     (position[0] - 1, position[1] - 1), (position[0], position[1] + 1),
                     (position[0], position[1] - 1), (position[0] + 1, position[1]),
                     (position[0] + 1, position[1] - 1), (position[0] + 1, position[1] + 1)]
        taken_seat = 0
        for p in positions:
            if p in self.seats:
                if self.seats[p] == "#":
                    taken_seat += 1
        return taken_seat

    def is_surrounded_new_rule(self, position):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        taken_seat = 0

        for direction in directions:
            d = direction
            pos = (position[0] + d[0], position[1] + d[1])
            iter = 1
            while 0 <= pos[0] <= self.max_x and 0 <= pos[1] <= self.max_y:
                if pos in self.seats:
                    if self.seats[pos] == "#":
                        taken_seat += 1
                    break
                iter += 1
                d = [x*iter for x in direction]
                pos = (position[0] + d[0], position[1] + d[1])

        return taken_seat

    def occupied_seats(self):
        occupied = 0
        for seat in self.seats:
            if self.seats[seat] == "#":
                occupied += 1
        return occupied


if __name__ == "__main__":
    seat_allocation = SeatAllocation("data/day11.txt")
    print(seat_allocation.iterations())