import random
from Card import Card


class Game:
    def __init__(self, playerCount=2, cardAmount=7):
        self.playerCount = playerCount
        self.wins = [0] * playerCount
        self.cardAmount = cardAmount
        self.playerCards = [Game.get_random_cards(cardAmount )for _ in range(playerCount)]

    @staticmethod
    def get_random_cards(amount):
        return [Game.get_random_card() for _ in range(amount)]

    @staticmethod
    def get_random_card():
        turnout = random.randint(0, 15)
        possibleColors = Card.POSSIBLE_COLORS[:-1]
        possibleValues = Card.POSSIBLE_VALUES[:-1]
        possibleSpecials = Card.POSSIBLE_SPECIALS[:-3]

        if turnout == 15:
            return Card(special="WILD DRAW 4")
        elif turnout >= 13:
            return Card(special="WILD")
        elif turnout < 9:
            color = random.choice(possibleColors)
            value = random.choice(possibleValues)
            return Card(value, color)
        else:
            color = random.choice(possibleColors)
            special = random.choice(possibleSpecials)
            return Card(None, color, special)


g = Game(playerCount=3, cardAmount=2)
for gx in g.playerCards:
    print(gx)
