from random import choice
from BGFunc import Block, Color


class TTTBoard:

    def __init__(self):
        self.b_list = [0 for _ in range(9)]
        self.run_list = [i for i in range(9)]
        self.check_list = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                           (0, 3, 6), (1, 4, 7), (2, 5, 8),
                           (0, 4, 8), (2, 4, 6)]
        self.corners = [0, 2, 6, 8]
        self.edges = [1, 3, 5, 7]
        self.win = False
        self.play = True
        self.move = 1
        self.blocks = [Block() for _ in range(9)]

    def get_board(self):
        pr_str = ' _____ _____ _____\n'
        for i in range(3):
            pr_str += '|     |     |     |\n|'
            for j in range(3):
                if self.b_list[i * 3 + j] == 0:
                    pr_str += '     |'
                elif self.b_list[i * 3 + j] == 1:
                    pr_str += '  O  |'
                else:
                    pr_str += '  X  |'
            pr_str += '\n|_____|_____|_____|\n'
        return pr_str

    def print_board(self):
        print(self.get_board())

    def x(self, pos):
        self.b_list[pos] = 10
        self.blocks[pos].update_text('X')
        self.blocks[pos].text_color = Color.red
        self.run_list.remove(pos)
        if pos in self.corners:
            self.corners.remove(pos)
        elif pos in self.edges:
            self.edges.remove(pos)

    def o(self, pos):
        self.b_list[pos] = 1
        self.blocks[pos].update_text('O')
        self.blocks[pos].text_color = Color.blue
        self.run_list.remove(pos)
        if pos in self.corners:
            self.corners.remove(pos)
        elif pos in self.edges:
            self.edges.remove(pos)

    def get_tick(self, tup, nb_list=None):
        if nb_list is None:
            nb_list = self.b_list[:]
        tick = []
        for ele in tup:
            tick.append(nb_list[ele])
        return tick

    # Returns a list of winnable moves and empty list if none
    def get_win(self):
        ret_arr = []
        che = self.check_list[:]
        for tup in che:
            tick = self.get_tick(tup)
            if sum(tick) == 20:
                if tick[0] == 0:
                    ret_arr.append(tup[0])
                elif tick[1] == 0:
                    ret_arr.append(tup[1])
                else:
                    ret_arr.append(tup[2])

            if 0 not in tick or sum(tick) == 11:
                self.check_list.remove(tup)

        return ret_arr

    # Returns the only move to avoid losing else False
    def get_danger(self):
        che = self.check_list[:]
        for tup in che:
            tick = self.get_tick(tup)
            if sum(tick) == 2:
                if tick[0] == 0:
                    return tup[0]
                elif tick[1] == 0:
                    return tup[1]
                else:
                    return tup[2]
        return False

    # Returns a list of moves that cause double danger and empty list if none
    def get_double_danger_moves(self):
        ret_arr = []
        for corner in self.corners:
            count = 0
            new_b_list = self.b_list[:]
            new_b_list[corner] = 10
            for tup in self.check_list:
                tick = self.get_tick(tup, new_b_list)
                if sum(tick) == 20:
                    count += 1
            if count == 2:
                ret_arr.append(corner)
        return ret_arr

    def get_bot_move(self):
        dummy_var = self.get_win()
        if dummy_var:
            self.win = True
            self.play = False
            return choice(dummy_var)

        dummy_var = self.get_danger()
        if dummy_var in self.run_list:
            return dummy_var

        dummy_var = self.get_double_danger_moves()
        if dummy_var:
            return choice(dummy_var)

        return False


class AI1(TTTBoard):
    move2 = {
        0: {1: [6], 2: [6, 8], 3: [2], 4: [5, 7], 5: [2, 4, 6], 6: [2, 8], 7: [2, 4, 6], 8: [2, 6]},
        2: {0: [6, 8], 1: [8], 3: [0, 4, 8], 4: [3, 7], 5: [0], 6: [0, 8], 7: [0, 4, 8], 8: [0, 6]},
        6: {0: [2, 8], 1: [0, 4, 8], 2: [0, 8], 3: [8], 4: [1, 5], 5: [0, 4, 8], 7: [0], 8: [0, 2]},
        8: {0: [2, 6], 1: [2, 4, 6], 2: [0, 6], 3: [2, 4, 6], 4: [1, 3], 5: [6], 6: [0, 2], 7: [2]}
    }

    def __init__(self):
        TTTBoard.__init__(self)
        self.move1 = choice([0, 2, 6, 8])
        self.x(self.move1)

    # A function which is called in the main method if play is True
    def play_it(self, pos):
        self.move += 1
        if self.move == 5:
            self.play = False
        self.o(pos)

        if self.move == 2:
            return self.x(choice(AI1.move2[self.move1][pos]))

        move = self.get_bot_move()
        if move:
            return self.x(move)
        if self.corners:
            return self.x(choice(self.corners))
        else:
            return self.x(choice(self.run_list))


class AI2(TTTBoard):

    def __init__(self):
        TTTBoard.__init__(self)
        self.center = False  # This variable is True when the opponent plays center in move 1
        self.move = 0
        self.liberty_move3 = self.corners

    def is_o(self, args):
        for arg in args:
            if self.b_list[arg] != 1:
                return False
        return True

    def get_non_center_move2(self):
        move2 = {
            (0, 8): [1, 3, 5, 7], (2, 6): [1, 3, 5, 7],  # Opposite corner cases
            (1, 7): [0, 2, 6, 8], (3, 5): [0, 2, 6, 8],  # Opposite edge cases
            (1, 3): [0], (1, 5): [2], (7, 3): [6], (7, 5): [8],  # Non-opposite edge cases
        }
        for key in move2:
            if self.is_o(key):
                return choice(move2[key])

        smol_check_list = [(0, 1, 2), (2, 5, 8), (6, 7, 8), (0, 3, 6)]
        for tup in smol_check_list:
            tick = self.get_tick(tup)
            if sum(tick) == 2:
                # One of the corner is empty implies a continuous draw game to the last move
                if tick[0] == 0:
                    return tup[0]
                if tick[2] == 0:
                    return tup[2]

                # The edge is empty introduces a liberty move in move 3
                self.liberty_move3 = self.edges
                return tup[1]

        # The remaining cases
        if self.b_list[0] == 1:
            return 8
        if self.b_list[2] == 1:
            return 6
        if self.b_list[6] == 1:
            return 2
        if self.b_list[8] == 1:
            return 0

    def play_it(self, inp):
        self.o(inp)
        self.move += 1

        if self.move == 1:
            if inp == 4:
                self.center = True
                return self.x(choice([0, 2, 6, 8]))  # The player played the center so the best move is a corner
            self.x(4)  # If the player does not start with center, the engine will

        if self.move == 2 and not self.center:
            return self.x(self.get_non_center_move2())

        if self.move == 2 and self.center:
            move2 = self.get_danger()
            print(move2)
            if move2 in self.run_list:
                return self.x(move2)
            return self.x(choice(self.corners))

        if self.move == 3:
            move3 = self.get_bot_move()
            if move3 in self.run_list:
                return self.x(move3)
            return self.x(choice(self.liberty_move3))

        if self.move == 4:
            move4 = self.get_bot_move()
            if move4 in self.run_list:
                return self.x(move4)
            return self.x(choice(self.run_list))

        if self.move == 5:
            self.play = False