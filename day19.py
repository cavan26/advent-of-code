

class Checker:
    def __init__(self, file):
        self.rules = {}
        self.message = []
        self.read_file(file)
        self.max_length_message = self.get_max_length()
        self.memoiz = {}

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        is_rule = True
        for line in lines:
            line = line.strip("\n")
            if line == "":
                is_rule = False

            elif is_rule:
                l = line.split(":")
                if "\"" in l[1]:
                    self.rules[int(l[0])] = l[1].split("\"")[1]
                else:
                    r = [x.strip() for x in l[1].split("|")]
                    self.rules[int(l[0])] = [x.split(" ") for x in r]
            else:
                self.message.append(line)

    def get_max_length(self):
        max_length = 0
        for message in self.message:
            if len(message) > max_length:
                max_length = len(message)
        return max_length

    def apply_list(self):
        new_rules = self.apply_recurrent(self.rules[0])
        self.rules[0] = new_rules

    def apply_recurrent(self, l):
        new_rules = []
        for sublist in l:
            if isinstance(sublist, list):
                r = [""]
                for i in sublist:
                    if int(i) in self.memoiz:
                        new_list = self.memoiz[int(i)]
                        r = self.list_possibilities(r, new_list)
                    else:
                        if isinstance(self.rules[int(i)], list):
                            new_list = self.apply_recurrent(self.rules[int(i)])
                            self.memoiz[int(i)] = new_list
                            r = self.list_possibilities(r, new_list)
                        else:
                            r = [x + self.rules[int(i)] for x in r]
            else:
                r = sublist
            new_rules.extend(r)
        return new_rules

    def check_size(self, r):
        all_longer = True
        for lists in r:
            if len(lists) < self.max_length_message:
                all_longer = False
        return all_longer



    def list_possibilities(self, r, l):
        new_list = []
        for element in r:
            for new_element in l:
                new_list.append(element + new_element)
        return new_list

    def check_message(self):
        s = 0
        for message in self.message:
            if message in self.rules[0]:
                s += 1
        return s


if __name__ == "__main__":
    check = Checker("data/day19.txt")
    check.apply_list()
    print(check.check_message())
