

class DeckShuffler:
    def __init__(self, number_of_cards, file):
        self.number_of_cards = number_of_cards
        self.instruction = []
        self.read_instruction(file)

    def deal_into_stack(self, position):
        return self.number_of_cards - position - 1

    def cut_n_cards(self, N, position):
        return (position - N) % self.number_of_cards

    def deal_with_increment_n(self, N, position):
        return (position*N) % self.number_of_cards

    def shuffle(self, position):
        for instruction in self.instruction:
            if instruction[0] == 0:
                position = self.deal_into_stack(position)
            elif instruction[0] == 1:
                position = self.cut_n_cards(instruction[1], position)
            elif instruction[0] == 2:
                position = self.deal_with_increment_n(instruction[1], position)
        return position

    def read_instruction(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        for line in lines:
            if line.startswith("deal into new stack"):
                self.instruction.append((0, 0))
            elif line.startswith("cut"):
                self.instruction.append((1, int(line.split("cut ")[-1].strip())))
            elif line.startswith("deal with increment"):
                self.instruction.append((2, int(line.split("deal with increment ")[-1].strip())))


if __name__ == "__main__":
    shuffler = DeckShuffler(101741582076661, "../data/2019/day22.txt")
    position = 2020
    memoiz = {}
    for i in range(101741582076661):
        print(position)
        # if position in memoiz:
        #     position = memoiz[position]
        # else:
        #     position1 = position
        position = shuffler.shuffle(position)
            # memoiz[position1] = position
    print(position)
