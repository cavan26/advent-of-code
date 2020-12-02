
class PasswordChecker:
    def __init__(self, file):
        self.policy = []
        self.password = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        for line in file1.readlines():
            bounds = line.split(" ")[0]
            self.policy.append([int(bounds.split("-")[0]), int(bounds.split("-")[1]), line.split(" ")[1][:-1]])
            self.password.append(line.split(" ")[2])

    def check_pawwords(self):
        correct_password = 0
        for i in range(len(self.password)):
            count = 0
            for letter in self.password[i]:
                if letter == self.policy[i][2]:
                    count += 1
            if self.policy[i][1] >= count >= self.policy[i][0]:
                correct_password += 1
            else:
                print(self.policy[i])
                print(self.password[i])
        print(correct_password)

    def check_password_part_2(self):
        correct_password = 0
        for i in range(len(self.password)):
            passport = self.password[i]
            if passport[self.policy[i][1]-1] == self.policy[i][2] and passport[self.policy[i][0]-1] == self.policy[i][2]:
                continue
            elif passport[self.policy[i][1]-1] == self.policy[i][2] or passport[self.policy[i][0]-1] == self.policy[i][2]:
                correct_password += 1

        print(correct_password)


if __name__ == "__main__":
    checker = PasswordChecker("data/day2.txt")
    checker.check_password_part_2()