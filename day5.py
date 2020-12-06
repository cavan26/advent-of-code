
class BoardingPass:
    def __init__(self, file):
        self.boarding_pass = []
        self.read_file(file)
        self.ids = []
        self.read_place()

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            self.boarding_pass.append(line.strip("\n"))

    def read_place(self):
        print(self.boarding_pass)
        for b in self.boarding_pass:
            row = self.get_row(b[:7])
            seat = self.get_id(b[7:])
            self.ids.append(row * 8 + seat)

    def get_row(self, code):
        code = [1 if x == "B" else 0 for x in code]
        id = 0
        for i in range(len(code)):
            id += code[i] * (2**(6-i))
        return id

    def get_id(self, code):
        code = [1 if x == "R" else 0 for x in code]
        id = 0
        for i in range(len(code)):
            id += code[i] * (2**(2-i))
        return id


if __name__ == "__main__":
    boarding_pass = BoardingPass("data/day5.txt")
    for i in range(70, 938):
        if i not in boarding_pass.ids:
            print(i)



