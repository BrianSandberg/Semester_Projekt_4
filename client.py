import pygame
from network import Network
import pickle

pygame.font.init()
from card import *

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Vi laver faktisk ikke et nyt deck her, men bare trækker et random kort hver gang
# Når vi når lidt længere skal vi lave et nyt deck der kan itereres over
createDeck()
getCard = drawCard(fullDeck).card.value
font = pygame.font.SysFont("comicsans", 60)
#card = GetCard()  # Class Test in the class called card... A little confusing

#getCard = getCard()
#cardText = font.render(str(getCard), 1, (0, 0, 0))

#def testdraw():
#    card = GetCard
#    getCard = card.getCard()
#    return getCard



class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 30
        self.height = 30

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        # x and y of mouse position
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        if p == 1:
            text = font.render("Your Move", 1, (0, 255, 255))
            win.blit(text, (80, 200))

        # text = font.render("Opponents", 1, (0, 255, 255))
        # win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        text1 = font.render(move1, 1, (0, 0, 0))
        text2 = font.render(move2, 1, (0, 0, 0))
        # move2 = int(getCard) #game.get_player_move(1)
        if game.bothWent():
            pass
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                 text2 = font.render(move2, 1, (0,0,0))
            # elif game.p2Went:
            #   text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                pass  # text2 = font.render("Waiting...", 1, (0, 0, 0))
        if p1turn:
            if p == 0:
                # win.blit(text2, (100, 350))
                win.blit(text1, (400, 350))
                for btn in btns:
                    btn.draw(win)

            else:
                win.blit(text1, (100, 350))
                # win.blit(text2, (400, 350))
                win.blit((font.render(str(getCard), 1, (255,0,0))), (100,100))
                # print(str(getCard))
        else:
            if p == 1:
                win.blit(text2, (400,350))
                for btn in btns:
                    btn.draw(win)
            else:
                win.blit(text1, (100,350))
                win.blit((font.render(str(getCard), 1, (255,0,0))), (100,100))

    pygame.display.update()


btns = [Button("1", 50, 500, (0, 0, 0)), Button("2", 100, 500, (255, 0, 0)), Button("3", 150, 500, (0, 255, 0)),
        Button("4", 200, 500, (0, 255, 0)),
        Button("5", 250, 500, (0, 255, 0)), Button("6", 300, 500, (0, 255, 0)), Button("7", 350, 500, (0, 255, 0)),
        Button("8", 400, 500, (0, 255, 0)),
        Button("9", 450, 500, (0, 255, 0)), Button("10", 500, 500, (0, 255, 0)), Button("11", 550, 500, (0, 255, 0)),
        Button("12", 600, 500, (0, 255, 0)),
        Button("13", 650, 500, (0, 255, 0))]



def main():
    run = True
    #turnCount variable keeps track of the number of turns - Is responsible for resetting upon reaching 2 consecutive turns
    global turnCount
    global p1turn
    p1turn = False
    turnCount = 0
    #Global variable so it can be accessed outside of the function
    global getCard
    newCard = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        if turnCount == 2:
            turnCount = 0
            newCard = True
        #Updates getCard which is the current card being played in the game
        while newCard:
            getCard = drawCard(fullDeck).card.value
            #if player == 1:
                #print(getCard)
            if p1turn == True:
                p1turn = False
            else:
                p1turn = True
            #pygame.display.update()
            newCard = False




        try:
            if not p1turn:
                if player == 0:
                    n.send(str(getCard))
                    #print(str(getCard))
            else:
                if player == 1:
                    n.send(str(getCard))

        except:
            print("Something went wrong...")
            break

        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():

            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")

            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if game.firstround() == 1:
                turnCount = turnCount + 1
                text = font.render("Guess a higher number", 1, (255,0,0))
            elif game.firstround() == -1:
                turnCount = turnCount + 1
                text = font.render("Guess a lower number", 1, (255,0,0))
            elif game.firstround() == 0:
                turnCount = 0
                text = font.render("Correct guess", 1, (255,0,0))
                newCard= True

            if p1turn and player == 0:
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
                print("penis")
            elif not p1turn and player == 1:
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))


#            font = pygame.font.SysFont("comicsans", 90)
#            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
#                text = font.render("You Won!", 1, (255, 0, 0))
#            elif game.winner() == -1:
#                text = font.render("Tie Game!", 1, (255, 0, 0))
#            else:
#                text = font.render("You Lost...", 1, (255, 0, 0))

#            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

            pygame.display.update()
            pygame.time.delay(2000)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0: #I think it sould be p1turn == True, instead of player, but that doenst work atm
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                              n.send(btn.text)



                        # else:
                        #   if not game.p2Went:
                        #      n.send(str(getCard))

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()