
class Game:
    def __init__(self):
        self.starting_numbers = [6,3,15,13,1,0]
        self.played_number = {}

    def play_game(self):
        i = 1
        for num in self.starting_numbers[:-1]:
            self.played_number[num] = i
            i += 1
        last_number = self.starting_numbers[-1]

        for iter in range(len(self.starting_numbers) + 1, 30000001):
            if last_number in self.played_number:
                new_number = (iter-1) -  self.played_number[last_number]
            else:
                new_number = 0
            self.played_number[last_number] = iter - 1
            last_number = new_number
        return new_number


if __name__ == "__main__":
    game = Game()
    print(game.play_game())

