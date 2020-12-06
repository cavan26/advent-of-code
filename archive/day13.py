import sys
sys.path.insert(0, "/Users/camillevanassel/git/advent-of-code")

from archive.day2 import IntcodeMachine
import time
import sys


class GameArcade:
    def __init__(self):
        self.machine = IntcodeMachine("data/2019/day13.txt")
        self.tiles = {}
        self.max_X = 0
        self.max_Y = 0
        self.score = 0
        self.ball = (0, 0)
        self.paddle = (0, 0)
        self.machine_player = Player()

    def get_tiles(self):
        self.machine.intcode_list[0] = 2
        output = self.machine.add_input([])
        self.process_output(output)

    def process_output(self, output):
        i = 0
        while i < len(output):
            if output[i] > self.max_X:
                self.max_X = output[i]
            if output[i + 1] > self.max_Y:
                self.max_Y = output[i + 1]
            if output[i] == -1 and output[i+1] == 0:
                self.score = output[i+2]
            if output[i+2] == 3:
                self.paddle = (output[i], output[i+1])
            elif output[i+2] == 4:
                self.ball = (output[i], output[i + 1])
            self.tiles[(output[i], output[i + 1])] = output[i + 2]
            i += 3

    def get_number_blocks(self):
        return sum([x == 2 for x in self.tiles.values()])

    def display_game(self):
        sys.stdout.flush()
        sys.stdout.write(f" SCORE: {self.score} \n")
        line = ""
        for y in range(self.max_Y + 1):
            for x in range(self.max_X + 1):
                if self.tiles[(x, y)] == 0:
                    line += "  "
                elif self.tiles[(x, y)] == 1:
                    line += "W "
                elif self.tiles[(x, y)] == 2:
                    line += "B "
                elif self.tiles[(x, y)] == 3:
                    line += "T "
                elif self.tiles[(x, y)] == 4:
                    line += "0 "
            line += "\n"
        sys.stdout.write(line)

    def play(self):
        playing = True
        while playing:
            key = self.get_move_machine()
            if key == "q":
                output = self.machine.add_input([-1])
            elif key == "d":
                output = self.machine.add_input([1])
            elif key == "s":
                output = self.machine.add_input([0])
            else:
                continue
            self.process_output(output)
            self.display_game()
            time.sleep(0.1)
            if self.ball[1] >= self.paddle[1]:
                playing = False
                print("You lost the game...")
            if self.get_number_blocks() == 0:
                playing = False
                print(f"FINAL SCORE: {self.score}")

    @staticmethod
    def get_move_keyboard():
        return input("Move the cursor")

    def get_move_machine(self):
        return self.machine_player.move(self.ball, self.paddle)


class Player:
    def __init__(self):
        self.previous_position_ball = (0, 0)
        self.position_ball = (0, 0)
        self.paddle = (0, 0)

    def get_direction(self):
        return self.position_ball[0] - self.previous_position_ball[0]

    def get_future_position(self):
        multiplier = self.paddle[1] - self.position_ball[1]
        return self.position_ball[0] + multiplier * self.get_direction()

    def move(self, new_position_ball, new_position_paddle):
        self.paddle = new_position_paddle
        self.previous_position_ball = self.position_ball
        self.position_ball = new_position_ball

        if self.paddle[1] == self.position_ball[1] + 1:
            if self.paddle[0] - self.position_ball[0] == 1:
                return "q"
            elif self.paddle[0] - self.position_ball[0] == -1:
                return "d"

        if self.paddle[0] == self.get_future_position():
            return "s"
        elif self.paddle[0] > self.get_future_position():
            return "q"
        elif self.paddle[0] < self.get_future_position():
            return "d"


if __name__ == "__main__":
    game = GameArcade()
    game.get_tiles()
    game.display_game()
    game.play()