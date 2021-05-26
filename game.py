class Game:
    def __init__(self):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.moves = [None, None]

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def roundRules(self):
        p1 = self.moves[0]
        p2 = self.moves[1]

        if int(p1) < int(p2):
            guess = 1
        elif int(p1) > int(p2):
            guess = -1
        else:
            guess = 0
        return guess

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False