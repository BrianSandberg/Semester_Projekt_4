from enum import *
from random import *

fullDeck = []

class Card(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Color(Enum):
    SPADES = "spades"
    CLUBS = "clubs"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"

class PlayingCard:
    def __init__(self, value, color):
        self.card = value
        self.color = color

def createDeck():
    for color in Color:
        for card in Card:
            fullDeck.append(PlayingCard(Card(card), Color(color)))
    return fullDeck

def drawCard(deck):
    randomCard = randint(0, len(deck)-1)
    return deck.pop(randomCard)

def getCard():
    testCard = drawCard(fullDeck)
    return testCard.card.value