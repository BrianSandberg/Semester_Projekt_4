#Holds information about the game - player moves, connections, wins, ties, etc.

class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def player(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0]
        p2 = self.moves[1]
        winner = -1

        if int(p1) < int(p2) or int(p1) > int(p2):
            winner = 1
        elif int(p1) == int(p2):
            winner = 0

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False


