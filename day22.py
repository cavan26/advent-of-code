import copy


class CardGame:
    def __init__(self, file):
        self.player1 = []
        self.player2 = []
        self.read_file(file)

    def read_file(self, file):
        file1 = open(file, 'r')
        lines = file1.readlines()
        player2 = False
        for line in lines:
            line = line.strip("\n")
            if line.startswith("Player 2"):
                player2 = True
            elif line.isdigit() and not player2:
                self.player1.append(int(line))
            elif line.isdigit() and player2:
                self.player2.append(int(line))

    def play_game(self):
        while len(self.player1) > 0 and len(self.player2) > 0:
            if self.player1[0] > self.player2[0]:
                self.player1.append(self.player1.pop(0))
                self.player1.append(self.player2.pop(0))
            elif self.player2[0] > self.player1[0]:
                self.player2.append(self.player2.pop(0))
                self.player2.append(self.player1.pop(0))

        if len(self.player1) == 0:
            return self.calculate_score(self.player2)
        else:
            return self.calculate_score(self.player1)

    @staticmethod
    def calculate_score(player):
        score = 0
        for i in range(0, len(player)):
            score += player[i] * (len(player) - i)
        return score

    def check_already_play(self, list1, list2, already_played):
        hash = (",".join([str(x) for x in list1]), ",".join([str(x) for x in list2]))
        if hash in already_played:
            return True, already_played
        else:
            already_played.add(hash)
            return False, already_played

    def play_recursive_game(self, list1, list2):
        already_played = set()
        round = 1
        while len(list1) > 0 and len(list2) > 0:
            b, already_played = self.check_already_play(list1, list2, already_played)
            if b:
                return "1"
            else:
                if len(list1) - 1 >= list1[0] and len(list2) - 1 >= list2[0]:
                    winner = self.play_recursive_game(copy.deepcopy(list1[1:list1[0] + 1]), copy.deepcopy(list2[1:list2[0] + 1]))
                else:
                    if list1[0] > list2[0]:
                        winner = "1"
                    elif list2[0] > list1[0]:
                        winner = "2"

                if winner == "1":
                    list1.append(list1.pop(0))
                    list1.append(list2.pop(0))
                elif winner == "2":
                    list2.append(list2.pop(0))
                    list2.append(list1.pop(0))
            round += 1
        return winner

    def play_game_part_2(self):
        self.play_recursive_game(self.player1, self.player2)
        if len(self.player1) == 0:
            return self.calculate_score(self.player2)
        else:
            return self.calculate_score(self.player1)


if __name__ == "__main__":
    game = CardGame("data/day22.txt")
    print(f"Part 1: {game.play_game()}")
    game = CardGame("data/day22.txt")
    print(f"Part 2: {game.play_game_part_2()}")
