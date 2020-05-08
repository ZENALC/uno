import random
import time
from Card import Card


def prRed(skk, end='\n'): print("\033[91m {}\033[00m".format(skk), end=end)


def prGreen(skk, end='\n'): print("\033[92m {}\033[00m".format(skk), end=end)


def prYellow(skk, end='\n'): print("\033[93m {}\033[00m".format(skk), end=end)


def prLightPurple(skk, end='\n'): print("\033[94m {}\033[00m".format(skk), end=end)


def prPurple(skk, end='\n'): print("\033[95m {}\033[00m".format(skk), end=end)


def prCyan(skk, end='\n'): print("\033[96m {}\033[00m".format(skk), end=end)


def prLightGray(skk, end='\n'): print("\033[97m {}\033[00m".format(skk), end=end)


def prBlack(skk, end='\n'): print("\033[98m {}\033[00m".format(skk), end=end)


class Game:
    COMPUTER_THINK_TIME = 0.25

    def __init__(self, playerCount=2, cardAmount=7, gameRotation=1):
        self.gameRotation = gameRotation  # 1 is clock-wise, -1 is counter-clock-wise
        self.currentCard = None
        self.playerCount = playerCount
        self.wins = [0] * playerCount
        self.cardAmount = cardAmount
        self.playerCards = [Game.draw_cards(self.cardAmount) for _ in range(self.playerCount)]
        self.playerTurn = random.randint(0, self.playerCount - 1)

    def restart_game(self):
        self.playerCards = [Game.draw_cards(self.cardAmount) for _ in range(self.playerCount)]
        self.playerTurn = random.randint(0, self.playerCount - 1)
        self.start_game()

    def validate_move(self, card: Card):
        currentColor = self.currentCard.get_color()
        currentValue = self.currentCard.get_value()
        currentSpecial = self.currentCard.get_special()

        if card.get_color() == currentColor and currentColor is not None:
            return True
        elif card.get_value() == currentValue and currentValue is not None:
            return True
        elif card.get_special() == currentSpecial and currentSpecial is not None:
            return True
        elif card.get_special() == "WILD" or card.get_special() == "WILD DRAW 4":
            return True
        else:
            return False

    def print_score(self):
        for playerIndex in range(self.playerCount):
            print(f"Player {playerIndex} has {self.wins[playerIndex]} wins.")

    def game_over(self):
        for playerCards in self.playerCards:
            if len(playerCards) == 0:
                return self.playerCards.index(playerCards)

    @staticmethod
    def draw_cards(amount: int):
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

    def get_first_card(self):
        firstCard = Game.draw_card()
        while firstCard.get_special() is not None:
            firstCard = Game.draw_card()
        self.currentCard = firstCard

    def print_player_cards(self):
        print(f"Your {len(self.playerCards[0])} cards are:")
        for card in self.playerCards[0]:
            if card.get_color() == "GREEN":
                prGreen(card, end=" | ")
            elif card.get_color() == "RED":
                prRed(card, end=" | ")
            elif card.get_color() == "BLUE":
                prCyan(card, end=" | ")
            elif card.get_color() == "YELLOW":
                prYellow(card, end=" | ")
            else:
                prPurple(card, end=" | ")
        print()

    def print_current_card(self):
        output = f"\nThe current card is {self.currentCard}.\n"
        if self.currentCard.get_color() is not None:
            if self.currentCard.get_color() == "GREEN":
                prGreen(output)
            elif self.currentCard.get_color() == "BLUE":
                prCyan(output)
            elif self.currentCard.get_color() == "RED":
                prRed(output)
            elif self.currentCard.get_color() == "YELLOW":
                prYellow(output)

    def parse_move(self, card: Card, cpu=True):
        self.currentCard = card
        self.playerCards[self.playerTurn].remove(card)
        if card.get_special() == "WILD" or card.get_special() == "WILD DRAW 4":
            colorChoice = None
            if cpu:
                colorChoice = random.choice(Card.POSSIBLE_COLORS[:-1])
            else:
                while colorChoice not in Card.POSSIBLE_COLORS[:-1]:
                    colorChoice = input("What color would you like? Type>>").upper()

            self.currentCard.set_color(colorChoice)

        elif card.get_special() == "REVERSE":
            self.switch_game_rotation()
            print(self.gameRotation)
        elif card.get_special() == "SKIP":
            self.get_next_player()

    def get_computer_move(self):
        print(f"Player {self.playerTurn} is thinking...")
        playerIndex = self.playerTurn
        time.sleep(Game.COMPUTER_THINK_TIME)
        computerCards = self.playerCards[self.playerTurn]
        for card in computerCards:
            if self.validate_move(card):
                self.parse_move(card)
                print(f"Player {playerIndex} has thrown {card} and now has {len(computerCards)} cards.")
                return
        self.playerCards[self.playerTurn].append(Game.draw_card())
        print(f"Player {self.playerTurn} has drawn a card and now has {len(computerCards)} cards.")

    def get_player_move(self):
        while True:
            cardExists = False
            self.print_player_cards()
            throwCard = input("It is your turn. Type a card to throw or 'DRAW' to draw a card>>").upper()
            if throwCard == "DRAW":
                drawnCard = self.draw_card()
                self.playerCards[self.playerTurn].append(drawnCard)
                print(f"You have drawn {drawnCard}.")
                return
            for card in self.playerCards[0]:
                if throwCard in str(card):
                    cardExists = True
                    print(card)
                    if self.validate_move(card):
                        self.parse_move(card, cpu=False)
                        print(f"You have thrown {card}.")
                        return
                    else:
                        print(f"You cannot throw {card}. Please try again.\n")
                        break
            if not cardExists:
                print(f"You do not have {throwCard}.\n")

    def switch_game_rotation(self):
        if self.gameRotation == 1:
            self.gameRotation = -1
        else:
            self.gameRotation = 1

    def get_next_player(self):
        if self.gameRotation == 1:
            if self.playerTurn == self.playerCount - 1:
                self.playerTurn = 0
            else:
                self.playerTurn += 1
        else:
            if self.playerTurn == 0:
                self.playerTurn = self.playerCount - 1
            else:
                self.playerTurn -= 1

    def start_game(self):
        print(f"Players playing: {self.playerCount}")
        print("Shuffling cards...")
        time.sleep(Game.COMPUTER_THINK_TIME)

        print("Drawing cards...")
        time.sleep(Game.COMPUTER_THINK_TIME)

        print(f"\nEach player has been given {self.cardAmount} cards.")
        print(f"Player {self.playerTurn} will start the game.")

        self.get_first_card()
        self.print_current_card()

        while self.game_over() is None:
            if self.playerTurn == 0:
                self.get_player_move()
            else:
                self.get_computer_move()

            self.get_next_player()
            if self.currentCard.get_special() is not None:
                if "DRAW 4" in self.currentCard.get_special():
                    cardsToGive = 4
                    self.playerCards[self.playerTurn] += self.draw_cards(cardsToGive)
                    prRed(f"Player {self.playerTurn} has been given {cardsToGive} cards.")

                elif "DRAW 2" in self.currentCard.get_special():
                    cardsToGive = 2
                    self.playerCards[self.playerTurn] += self.draw_cards(cardsToGive)
                    prRed(f"Player {self.playerTurn} has been given {cardsToGive} cards.")

            self.print_current_card()
            time.sleep(Game.COMPUTER_THINK_TIME)

        self.wins[self.game_over()] += 1
        self.print_score()
        playAgain = None
        while playAgain not in ['Y', 'N']:
            playAgain = input("Would you like to play again? 'Y' or 'N'>>")[0].upper()
            if playAgain == 'Y':
                print("Restarting game...")
                time.sleep(Game.COMPUTER_THINK_TIME)
                self.restart_game()


g = Game(playerCount=2, cardAmount=10)
g.start_game()
