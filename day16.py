from collections import defaultdict


class TicketChecker:
    def __init__(self, file):
        self.ticket = []
        self.other_tickets = []
        self.rules = {}
        self.valid_ticket = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        ticket = False
        my_ticket = False
        iter = 0
        for line in lines:
            line = line.strip("\n")
            if line == "":
                continue
            elif ticket:
                self.other_tickets.append([int(x) for x in line.split(",")])
            elif my_ticket:
                self.ticket = [int(x) for x in line.split(",")]
                my_ticket = False
            elif line.startswith("your ticket:"):
                my_ticket = True
            elif line.startswith("nearby tickets"):
                ticket = True
            else:
                rule = []
                for r in line.split(":")[1].strip().split(" or "):
                    rule.extend(range(int(r.split("-")[0]), int(r.split("-")[1]) + 1))
                self.rules[iter] = rule
                iter += 1

    def check_tickets(self):
        values = []
        for rule in self.rules:
            values.extend(self.rules[rule])
        error_rate = 0
        for ticket in self.other_tickets:
            valid = True
            for i in range(len(ticket)):
                if ticket[i] not in values:
                    error_rate += ticket[i]
                    valid = False
            if valid:
                self.valid_ticket.append(ticket)
        return error_rate

    def check_valid_tickets(self):
        rules = defaultdict(list)
        dimension = defaultdict(list)
        for i in range(len(self.valid_ticket[0])):
            dim = [x[i] for x in self.valid_ticket]

            for j in self.rules:
                if all(elem in self.rules[j] for elem in dim):
                    rules[j].append(i)
                    dimension[i].append(j)

        final_rules = {}
        while len(final_rules) != len(rules):
            for rule in rules:
                if len(rules[rule]) == 1:
                    r = rules[rule][0]
                    final_rules[rule] = r
                    for d in dimension[r]:
                        rules[d].remove(r)

        mult = 1
        for i in range(0, 6):
            mult = mult * self.ticket[final_rules[i]]
        return mult


if __name__ == "__main__":
    ticket = TicketChecker("data/day16.txt")
    print(f"Part 1: {ticket.check_tickets()}")
    print(f"Part 2: {ticket.check_valid_tickets()}")