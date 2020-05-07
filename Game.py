import random
from Card import Card


class Game:
    def __init__(self, playerCount=2, cardAmount=7):
        self.currentCard = None
        self.playerCount = playerCount
        self.wins = [0] * playerCount
        self.cardAmount = cardAmount
        self.playerCards = [Game.draw_cards(cardAmount) for _ in range(playerCount)]

    @staticmethod
    def draw_cards(amount):
        return [Game.draw_card() for _ in range(amount)]

    @staticmethod
    def draw_card():
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

    @staticmethod
    def print_card():
        cardLength = 5
        cardWidth = 8
        gap = ' '
        for i in range(cardLength):
            if i == 0 or i == cardLength - 1:
                print(cardWidth * "*")
            else:
                print('*' + gap * (cardWidth - 2) + '*')

    def start_game(self):
        firstCard = Game.draw_card()
        while firstCard.get_special() is not None:
            firstCard = Game.draw_card()
        self.currentCard = firstCard
        print(f"The beginning card is {self.currentCard}.")


g = Game(playerCount=3, cardAmount=2)
g.start_game()
