import copy


class Game:
    def __init__(self):
        self.cups = [int(x) for x in "389125467"] + list(range(10, 1000001))
        self.min = min(self.cups)
        self.max = max(self.cups)

    def play_game(self):
        current_pos = 0
        cups = copy.deepcopy(self.cups)

        for i in range(10000000):
            if i % 100000 == 0:
                print(i)
            cups = cups * 2
            if current_pos >= len(self.cups):
                current_pos = 0
            cups_to_move = []
            for i in range(0, 3):
                cups_to_move.append(cups.pop(current_pos + 1))

            current_cup = cups[current_pos]
            destination_cup = current_cup - 1 if current_cup - 1 >= self.min else self.max
            while destination_cup in cups_to_move:
                destination_cup -= 1
                if destination_cup < self.min:
                    destination_cup = self.max

            destination_pos = current_pos + cups[current_pos:].index(destination_cup)
            new_cups = cups[:destination_pos+1] + cups_to_move + cups[destination_pos+1:]
            cups = new_cups[len(self.cups):len(self.cups) + current_pos] + new_cups[current_pos:len(self.cups)]
            current_pos += 1

        i = cups.index(1)
        print(cups[i + 1])
        print(cups[i + 2])
        return cups[i + 1]*cups[i + 2]


if __name__ == "__main__":
    game = Game()
    print(game.play_game())