
class CodeReader:
    def __init__(self, file):
        self.codes = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            self.codes.append(int(line.strip()))

    def check_codes(self):
        i = 25
        while i < len(self.codes):
            code = self.codes[i]
            compare = sorted(self.codes[i - 25: i])
            pair_found = False
            for j in range(len(compare)):
                for k in range(j, len(compare)):
                    if compare[j] >= code:
                        break
                    if compare[j] + compare[k] == code:
                        pair_found = True

            if not pair_found:
                return code
            i += 1

    def contiguous_set_numbers(self):
        invalid_number = self.check_codes()
        print(f"Part 1: {invalid_number}")
        for i in range(len(self.codes)):
            sum = self.codes[i]
            j = 1
            while sum <= invalid_number and i +j < len(self.codes):
                sum += self.codes[i+j]
                if sum == invalid_number:
                    print(f"Part 2: {min(self.codes[i:i+j]) + max(self.codes[i:i + j])}")
                    return min(self.codes[i:i+j]) + max(self.codes[i:i + j])
                else:
                    j += 1
            i += 1


if __name__ == "__main__":
    reader = CodeReader("data/day9.txt")
    reader.contiguous_set_numbers()
