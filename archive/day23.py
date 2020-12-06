from day2 import IntcodeMachine

class Network:
    def __init__(self):
        self.computers = [IntcodeMachine("data/archive/day23.txt") for i in range(50)]
        self.queues = {}
        self.nat = []
        self.Y = None

    def boot_up_computers(self):
        for i in range(50):
            output = self.computers[i].add_input([i])
            self.add_output_to_queue(output)

    def add_output_to_queue(self, output):
        while len(output) != 0:
            if output[0] == 255:
                self.nat = output[1:3]
            elif output[0] in self.queues:
                self.queues[output[0]].extend([output[1], output[2]])
            else:
                self.queues[output[0]] = [output[1], output[2]]
            output = output[3:]

    def read_from_queues(self):
        if self.is_network_idle() and len(self.nat) != 0:
            if 0 in self.queues:
                self.queues[0].extend(self.nat[0:2])
            else:
                self.queues[0] = self.nat[0:2]
            if self.nat[1] == self.Y:
                return self.Y
            self.Y = self.nat[1]
        for i in range(50):
            if i not in self.queues or len(self.queues[i]) == 0:
                output = self.computers[i].add_input([-1])
                self.add_output_to_queue(output)
            else:
                while len(self.queues[i]) > 0:
                    output = self.computers[i].add_input(self.queues[i][:2])
                    self.queues[i] = self.queues[i][2:]
                    self.add_output_to_queue(output)

    def is_network_idle(self):
        return all(len(value) == 0 for value in self.queues.values())

    def part_1(self):
        while 255 not in self.queues:
            self.read_from_queues()
        print(self.queues)

    def part_2(self):
        Y = None
        while Y is None:
            Y = self.read_from_queues()
        print(Y)

if __name__ == "__main__":
    network = Network()
    network.boot_up_computers()
    network.part_2()