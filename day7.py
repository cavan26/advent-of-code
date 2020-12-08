
class BagScanner:
    def __init__(self, file):
        self.bags = {}
        self.read_file(file)
        self.luggage = 0
        self.parent_luggage = set()
        self.price = 0

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        i = 0
        for line in lines:
            bag = line.split("contain")[0].split("bags")[0].strip()
            contained_bags = []
            for contained in line.split("contain")[1].split(","):
                if "no other bags" in contained:
                    continue
                else:
                    c_bag = ''.join([i for i in contained.split("bag")[0] if not i.isdigit()]).strip()
                    number = ''.join([i for i in contained.split("bag")[0] if i.isdigit()])
                    contained_bags.append((c_bag, number))
            if bag in self.bags:
                self.bags[bag].extends(contained_bags)
            else:
                self.bags[bag] = contained_bags

    def get_gold_luggage(self, luggage, parent_luggage):
        for contained_luggage in self.bags.get(luggage):
            if contained_luggage == "shiny gold":
                self.parent_luggage.add(parent_luggage)
            else:
                self.get_gold_luggage(contained_luggage, parent_luggage)

    def get_gold_luggage_price(self, luggage, mult):
        for contained_luggage in self.bags.get(luggage):
            new_mult = mult * int(contained_luggage[1])
            self.price += new_mult
            self.get_gold_luggage_price(contained_luggage[0], new_mult)


if __name__ == "__main__":
    scanner = BagScanner("data/day7.txt")
    scanner.get_gold_luggage_price("shiny gold", 1)
    print(scanner.price)
