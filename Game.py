import os
import random
import time
from Card import Card
from ColorPrint import *


class Game:
    def __init__(self, playerCount=2, cardAmount=7, gameRotation=1, computerThinkTime=1.0):
        self.highScoreFilename = "high_score.txt"  # default file name that contains high score
        self.computerThinkTime = computerThinkTime  # default time.sleep() time to simulate computer thinking
        self.gameRotation = gameRotation  # 1 is clock-wise, -1 is counter-clock-wise
        self.highScore = self.read_high_score()  # read high-score if file exists
        self.beatOldHighScore = False  # boolean to check if high score has beaten in this game instance
        self.newGame = True  # boolean to check if it is a new game
        self.currentCard = None  # current card being played
        self.playerCount = playerCount  # number of players playing the game
        self.wins = [0] * playerCount  # scores for each individual player in the game
        self.cardAmount = cardAmount  # cards to be given throughout the game
        self.playerCards = [Game.draw_cards(self.cardAmount) for _ in range(self.playerCount)]
        # Giving every player cardAmount of random cards
        self.playerTurn = random.randint(0, self.playerCount - 1)
        # Retrieving a random number to decide which player starts the game

    # Prints out current game score for every player.
    def print_score(self):
        prRed("\nCurrent game stats:\n")
        for playerIndex in range(self.playerCount):
            print(f"Player {playerIndex} has {self.wins[playerIndex]} wins.")

    # Prints out winner if game is over.
    def print_winner(self):
        if self.game_over() != 0:
            print(f"Player {self.game_over()} has won the game!")
        else:
            print(f"You have won the game!")

    # Returns specified amount of random cards.
    @staticmethod
    def draw_cards(amount: int):
        return [Game.draw_card() for _ in range(amount)]

    # Returns a random card.
    @staticmethod
    def draw_card():
        turnout = random.randint(0, 15)
        possibleColors = Card.POSSIBLE_COLORS[:-1]  # -1 because the last possible color is None
        possibleValues = Card.POSSIBLE_VALUES[:-1]  # -1 because the last possible value is None
        possibleSpecials = Card.POSSIBLE_SPECIALS[:-3]  # -3 because the last three are None, WILD, and WILD DRAW 4

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

    # Returns a random first card to start the game.
    def get_first_card(self):
        firstCard = Game.draw_card()
        while firstCard.get_special() is not None:
            firstCard = Game.draw_card()
        self.currentCard = firstCard

    # Prints out player cards in color.
    def print_player_cards(self):
        numberOfCards = len(self.playerCards[0])
        if numberOfCards > 1:
            print(f"Your {len(self.playerCards[0])} cards are:")
        else:
            print("Your last card is:")
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

    # Saves high score in filename specified during initialization.
    def save_high_score(self):
        if self.highScore is None or self.wins[0] > self.highScore:
            if not self.beatOldHighScore:
                print("New high score! Congratulations!")
            else:
                print("You are on a streak of high scores! Keep going!")
            self.beatOldHighScore = True
            self.highScore = self.wins[0]
            with open(self.highScoreFilename, 'w') as f:
                f.write(str(self.wins[0]))

    # Reads high score from filename specified during initialization if exists.
    def read_high_score(self):
        if os.path.exists(self.highScoreFilename):
            with open(self.highScoreFilename, 'r') as f:
                high_score = int(f.read())
                print(f"Old high score of {high_score} found.")
                return high_score
        return None

    # Returns most available color from current player's cards.
    def get_most_available_color(self):
        colorScores = {"blue": 0, "green": 0, "red": 0, "yellow": 0}
        for card in self.playerCards[self.playerTurn]:
            if card.get_color() == "BLUE":
                colorScores["blue"] += 1
            elif card.get_color() == "GREEN":
                colorScores["green"] += 1
            elif card.get_color() == "RED":
                colorScores["red"] += 1
            elif card.get_color() == "YELLOW":
                colorScores["yellow"] += 1

        return max(colorScores.items(), key=lambda k: k[1])[0]

    # Prints out arg in color of current card.
    def color_print(self, arg):
        color = self.currentCard.get_color()
        if color == "BLUE":
            prCyan(arg)
        elif color == "RED":
            prRed(arg)
        elif color == "YELLOW":
            prYellow(arg)
        elif color == "GREEN":
            prGreen(arg)

    # Prints out current card being played in color.
    def print_current_card(self):
        if self.newGame:
            output = f"\nThe first card is {self.currentCard}.\n"
            self.newGame = False
        else:
            output = f"\nThe current card is {self.currentCard}.\n"
        self.color_print(output)

    # Validates move given by current player.
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

    # Parses move given by current player.
    def parse_move(self, card: Card, cpu=True):
        self.currentCard = card
        self.playerCards[self.playerTurn].remove(card)
        if card.get_special() == "WILD" or card.get_special() == "WILD DRAW 4":
            colorChoice = None
            if cpu:
                colorChoice = self.get_most_available_color()
                # colorChoice = random.choice(Card.POSSIBLE_COLORS[:-1])
            else:
                while colorChoice not in Card.POSSIBLE_COLORS[:-1]:
                    colorChoice = input("What color would you like? Type>>").upper().strip()

            self.currentCard.set_color(colorChoice)

        elif card.get_special() == "REVERSE":
            if self.playerCount > 2:
                self.switch_game_rotation()
            else:
                self.get_next_player()
        elif card.get_special() == "SKIP":
            self.get_next_player()

    # Parses a card if any type of draw card is thrown.
    def parse_draw_card(self):
        if "DRAW 4" in self.currentCard.get_special():
            cardsToGive = 4
        else:
            cardsToGive = 2

        self.playerCards[self.playerTurn] += self.draw_cards(cardsToGive)
        if self.playerTurn == 0:
            prRed(f"You have been given {cardsToGive} cards.")
        else:
            prRed(f"Player {self.playerTurn} has been given {cardsToGive} cards.")

    # Makes a move for computer.
    def get_computer_move(self):
        print(f"Player {self.playerTurn} is thinking...")
        playerIndex = self.playerTurn
        time.sleep(self.computerThinkTime)
        computerCards = self.playerCards[self.playerTurn]
        for card in computerCards:
            if self.validate_move(card):
                self.parse_move(card)
                if len(self.playerCards[playerIndex]) == 1:
                    self.color_print(f"Player {playerIndex} says UNO!")
                    self.color_print(f"Player {playerIndex} has thrown {card} and now has 1 card left.")
                else:
                    self.color_print(f"Player {playerIndex} has thrown {card} and now has {len(computerCards)} cards left.")
                return
        self.playerCards[self.playerTurn].append(Game.draw_card())
        print(f"Player {self.playerTurn} has drawn a card and now has {len(computerCards)} cards.")

    # Retrieves player move.
    def get_player_move(self):
        playerIndex = self.playerTurn
        saidUno = False
        while True:
            cardExists = False
            self.print_player_cards()
            playerInput = " ".join(input("It is your turn. Type a card to throw, 'UNO' to saw UNO!, "
                                         "'HELP' for instructions, 'PRINT' to print the current card,"
                                         " or 'DRAW' to draw a card>>").upper().split())
            if playerInput == "DRAW":
                drawnCard = self.draw_card()
                self.playerCards[self.playerTurn].append(drawnCard)
                print(f"You have drawn {drawnCard}.")
                return
            elif playerInput == '':
                continue
            elif playerInput == "PRINT":
                self.print_current_card()
            elif playerInput == "HELP":
                Game.get_instructions()
            elif playerInput == "UNO":
                if saidUno:
                    prRed("You have already said UNO!")
                else:
                    prRed("You said UNO!")
                    saidUno = True
            else:
                for card in self.playerCards[0]:
                    if playerInput in str(card):
                        cardExists = True
                        if playerInput == "WILD" and card.get_special() != "WILD":
                            cardExists = False
                            continue
                        if self.validate_move(card):
                            self.parse_move(card, cpu=False)
                            if len(self.playerCards[playerIndex]) == 1 and not saidUno:
                                prRed("You forgot to say UNO! and you have been given two cards.")
                                self.playerCards[self.playerTurn] += self.draw_cards(2)
                            self.color_print(f"You have thrown {card}.")
                            return
                        else:
                            print(f"You cannot throw {card}. Please try again.\n")
                            break
                if not cardExists:
                    print(f"You do not have {playerInput}.\n")

    # Switches game rotation when REVERSE card is thrown.
    def switch_game_rotation(self):
        if self.gameRotation == 1:
            self.gameRotation = -1
        else:
            self.gameRotation = 1

    # Changes playerTurn to next player in queue
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

    # Checks if game is over then returns playerIndex of winner
    def game_over(self):
        for playerCards in self.playerCards:
            if len(playerCards) == 0:
                return self.playerCards.index(playerCards)

    # Prints out startup stuff to simulate cards being shuffled and drawn.
    def startup(self):
        print(f"Players playing: {self.playerCount}")
        print("Shuffling cards...")
        time.sleep(self.computerThinkTime)

        if self.playerCount > 1:
            print("Flipping coins to decide who will start the game...")
        time.sleep(self.computerThinkTime)

        print("Drawing cards...")
        time.sleep(self.computerThinkTime)

        if self.cardAmount > 1:
            print(f"\nEach player has been given {self.cardAmount} card(s).")
        else:
            print(f"\nEach player has been given {self.cardAmount} card.")

        if self.playerTurn != 0:
            print(f"Player {self.playerTurn} will start the game.")
        else:
            print(f"You will start the game.")

        self.get_first_card()
        self.print_current_card()

    # Starts game and keeps looping until game is over.
    def start_game(self):
        self.startup()
        while self.game_over() is None:
            if self.playerTurn == 0:
                self.get_player_move()
            else:
                self.get_computer_move()

            self.get_next_player()
            if self.currentCard.get_special() is not None and "DRAW" in self.currentCard.get_special():
                self.parse_draw_card()

            self.print_current_card()
            time.sleep(self.computerThinkTime)
        self.print_winner()
        self.wins[self.game_over()] += 1
        self.save_high_score()
        self.print_score()
        playAgain = None
        while playAgain not in ['Y', 'N']:
            try:
                playAgain = input("Would you like to play again? 'Y' or 'N'>>")[0].upper().strip()
                if playAgain == 'Y':
                    print("Restarting game...")
                    time.sleep(self.computerThinkTime)
                    self.restart_game()
            except IndexError:
                continue

    # Restarts game by resetting some variables back to false.
    def restart_game(self):
        self.playerCards = [Game.draw_cards(self.cardAmount) for _ in range(self.playerCount)]
        self.playerTurn = random.randint(0, self.playerCount - 1)
        self.newGame = True
        self.start_game()

    # Prints out instructions of the game.
    @staticmethod
    def get_instructions():
        prRed("\n\nWelcome to the game of UNO!\nThe rules are extremely simple.")
        prYellow("The game starts with a random card with some number and some color.")
        prYellow("Your goal is to match the card with a number or a color and finish all your cards.\n"
                 "For instance, if the last thrown card is a BLUE 9, you can either throw a card that is BLUE or a "
                 "card with the number 6.")
        prCyan("Special cards include WILD cards, REVERSE, DRAW 2, and SKIP.")
        prCyan("If someone throws a REVERSE card, the rotation of the game changes.\n"
               "For instance, if the game is going counter-clockwise,"
               "it will then move clockwise.")
        prGreen("If a SKIP is thrown, the next player's move will be skipped.")
        prGreen("If a DRAW 2 is thrown, the next player will draw 2 cards.")
        prRed("There are two types of wild cards - WILD and WILD DRAW 4.")
        prRed("With a WILD card - a player can change the color of the game's current card.")
        prYellow("With a WILD DRAW 4 card, a player can change the color and give 4 cards to the next player.")
        prGreen("And finally, once a player has two cards, and they are about to throw their second last card, "
                "\nThey must say UNO, or else they will be given two cards.")
        prRed("Those are all the rules. Good luck!\n\n")


g = Game(playerCount=3, cardAmount=2, computerThinkTime=0.9)
g.start_game()
