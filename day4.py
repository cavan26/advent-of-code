
class PassportChecker:
    def __init__(self, file):
        self.passport = []
        self.keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        self.read_file(file)
        self.check_passport_valid()

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        passport = {}
        for line in lines:
            if line == "\n":
                self.passport.append(passport)
                passport = {}
            else:
                line = line.replace("\n", "")
                for pairs in line.split(" "):
                    passport[pairs.split(":")[0]] = pairs.split(":")[1]
        self.passport.append(passport)

    def check_passport_valid(self):
        valid = 0
        for passport in self.passport:
            keys_passort = list(passport.keys())
            if not all(item in keys_passort for item in self.keys):
                continue
            if int(passport["byr"]) < 1920 or int(passport["byr"]) > 2002:
                continue
            if int(passport["iyr"]) < 2010 or int(passport["iyr"]) > 2020:
                continue
            if int(passport["eyr"]) < 2020 or int(passport["eyr"]) > 2030:
                continue
            if "cm" in passport["hgt"] and (int(passport["hgt"].split("cm")[0]) < 150 or int(passport["hgt"].split("cm")[0]) >193):
                continue
            elif "in" in passport["hgt"] and (int(passport["hgt"].split("in")[0]) < 59 or int(passport["hgt"].split("in")[0]) >76):
                continue
            elif "in" not in passport["hgt"] and "cm" not in passport["hgt"]:
                continue
            if "#" not in passport["hcl"] and len(passport["hcl"]) != 7:
                continue
            if passport["ecl"] not in ["amb", "blu","brn" ,"gry" ,"grn" ,"hzl" ,"oth"]:
                continue
            if not passport["pid"].isdigit() or len(passport["pid"]) != 9:
                continue
            valid += 1
        print(valid)


if __name__ == "__main__":
    checker = PassportChecker("data/day4.txt")


