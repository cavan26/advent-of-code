
class Calculator:
    def __init__(self, file):
        self.operation = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            self.operation.append(line.strip("\n"))

    def calculate_line_recursive(self, i, line):
        before = 0
        operation = ""
        while i < len(line):
            if line[i].isdigit():
                if operation == "":
                    before = int(line[i])
                elif operation == "addition":
                    before += int(line[i])
                    operation = ""
                elif operation == "multiplication":
                    if i+2 < len(line) and line[i + 2] == "+":
                        i_new, after = self.calculate_line_recursive(0, self.get_line(line[i:]))
                        i += i_new - 1
                        before = before * after
                    else:
                        before = before * int(line[i])
                    operation = ""
                i += 1
            elif line[i] == "+":
                i += 1
                operation = "addition"
            elif line[i] == "*":
                i += 1
                operation = "multiplication"
            elif line[i] == " ":
                i += 1
            elif line[i] == "(":
                (i, new_before) = self.calculate_line_recursive(i + 1, line)
                if operation == "":
                    before = new_before
                elif operation == "addition":
                    before += new_before
                    operation = ""
                elif operation == "multiplication":
                    if i+1 < len(line) and line[i + 1] == "+":
                        i_new, after = self.calculate_line_recursive(0, self.get_line(line[i + 2:]))
                        after = new_before + after
                        i += i_new + 2
                        before = before * after
                    else:
                        before = before * new_before
                    operation = ""
            elif line[i] == ")":
                return i + 1, before
        return i, before

    def calculate(self):
        results = []
        for operation in self.operation:
            _, before = self.calculate_line_recursive(0, operation)
            results.append(before)
        return sum(results)

    @staticmethod
    def get_line(line):
        open_parenthesis = 0
        for i in range(len(line)):
            if line[i] == "(":
                open_parenthesis += 1
            elif line[i] == ")":
                if open_parenthesis > 0:
                    open_parenthesis -= 1
                else:
                    return line[:i]
            elif line[i] == "*" and open_parenthesis == 0:
                return line[:i - 1]
        return line


if __name__ == "__main__":
    calculator = Calculator("data/day18.txt")
    print(f"Part 2: {calculator.calculate()}")