
from collections import defaultdict, OrderedDict
from functools import reduce

class Allergens:
    def __init__(self, file):
        self.ingredient = defaultdict(int)
        self.allergen = defaultdict(list)
        self.ingredient_to_allergen = defaultdict(list)
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            line = line.strip("\n").split(" (")
            ingredients = []
            for ingredient in line[0].split(" "):
                self.ingredient[ingredient] += 1
                ingredients.append(ingredient)

            for allergen in line[1].split("contains ")[1].split(")")[0].split(", "):
                for i in ingredients:
                    self.ingredient_to_allergen[i].append(allergen)
                self.allergen[allergen].append(ingredients)

    def find_allergen_to_ingredient(self):
        allergens = [k for k, v in self.allergen.items()]
        list_canonical = {}
        while (len(allergens)) > 0:
            for a in self.allergen:
                if len(self.allergen[a]) > 1:
                    new_list = list(self.intersection(self.allergen[a]))
                    self.allergen[a] = [new_list]
                    if len(new_list) == 1:
                        allergens.remove(a)
                        list_canonical[a] = new_list[0]
                        self.remove_ingredient(new_list[0])
                elif len(self.allergen[a][0]) == 1:
                    allergens.remove(a)
                    list_canonical[a] = self.allergen[a][0][0]
                    self.remove_ingredient(self.allergen[a][0][0])
                elif len(self.allergen[a][0]) == 0:
                    if a in allergens:
                        allergens.remove(a)
                        list_canonical.append(a)

        od = OrderedDict(sorted(list_canonical.items()))
        print(f"Part 1: {sum([v for k,v in self.ingredient.items()])}")
        print(f"Part 2: {','.join([v for k,v in od.items()])}")
        return sum([v for k,v in self.ingredient.items()])

    def remove_ingredient(self, ingredient):
        self.ingredient.pop(ingredient)
        for allergen in self.ingredient_to_allergen[ingredient]:
            for l in self.allergen[allergen]:
                if ingredient in l:
                    l.remove(ingredient)
        self.ingredient_to_allergen.pop(ingredient)

    @staticmethod
    def intersection(l):
        return reduce(set.intersection, [set(l_) for l_ in l])


if __name__ == "__main__":
    allergen = Allergens("data/day21.txt")
    allergen.find_allergen_to_ingredient()