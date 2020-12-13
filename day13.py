import math


class Bus:
    def __init__(self, file):
        self.time = 0
        self.bus_ids = []
        self.bus_ids_pos = {}
        self.max_bus = 0
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        self.time = int(file1.readline().strip())
        l = file1.readline().strip().split(",")
        self.bus_ids = [int(x) for x in l if x != "x"]
        for i in range(len(l)):
            if l[i] != "x":
                self.bus_ids_pos[i] = int(l[i])
        self.max_bus = len(l)

    def find_departure_time(self):
        min_time = 10000000000
        min_bus = 0
        for bus in self.bus_ids:
            d = math.ceil(self.time/bus)
            time = d*bus
            if time < min_time:
                min_time = time
                min_bus = bus
        return min_bus * (min_time - self.time)

    def chinese_Remainder(self):
        N = math.prod(self.bus_ids)
        y = [int(N/x) for x in self.bus_ids]
        a = [- k for k,x in self.bus_ids_pos.items()]
        z = []
        for i in range(len(y)):
            z.append(self.modular_inverse(y[i], self.bus_ids[i]))

        x = 0
        for i in range(len(y)):
            x += a[i]*y[i]*z[i]
        return self.modulo(x, N)

    @staticmethod
    def modulo(n, m):
        return ((n % m) + m) % m;

    @staticmethod
    def modular_inverse(x, p):
        return pow(x, p - 2, p)


if __name__ == "__main__":
    bus = Bus("data/day13.txt")
    print(f"Part 1: {bus.find_departure_time()}")
    print(f"Part 2: {bus.chinese_Remainder()}")

