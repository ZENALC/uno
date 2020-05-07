class Card:
    POSSIBLE_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None]
    POSSIBLE_COLORS = ["RED", "BLUE", "YELLOW", "GREEN", None]
    POSSIBLE_SPECIALS = ["REVERSE", "SKIP", "DRAW 2", "WILD", "WILD DRAW 4", None]

    def __init__(self, value=None, color=None, special=None):
        """Initialize Card object
        >>> Card(None, "RED", "WILD")
        Traceback (most recent call last):
        ...
        ValueError: WILD cards cannot have a color.
        >>> Card(9, None, "WILD DRAW 4")
        Traceback (most recent call last):
        ...
        ValueError: WILD cards cannot have a value.
        >>> Card(9, "GREEN", "REVERSE")
        Traceback (most recent call last):
        ...
        ValueError: You cannot have a special card with a value.
        >>> Card(None, None, "REVERSE")
        Traceback (most recent call last):
        ...
        ValueError: You cannot have a special card that is not WILD without a color.
        >>> Card(10, "BLUE")
        Traceback (most recent call last):
        ...
        ValueError: 10 is not a valid value.
        >>> Card(9, "ORANGE")
        Traceback (most recent call last):
        ...
        ValueError: ORANGE is not a valid color.
        >>> Card(None, "RED", "DRAW 5")
        Traceback (most recent call last):
        ...
        ValueError: DRAW 5 is not a valid special.
        >>> Card(color="RED")
        Traceback (most recent call last):
        ...
        ValueError: You cannot have a card with a color but no value or special.
        >>> Card()
        Traceback (most recent call last):
        ...
        ValueError: Empty card.
        """
        value = value if value is None else int(value)
        color = color if color is None else color.upper()
        special = special if special is None else special.upper()

        if special == "WILD" or special == "WILD DRAW 4":
            if value:
                raise ValueError("WILD cards cannot have a value.")
            elif color:
                raise ValueError("WILD cards cannot have a color.")
        elif special is not None:
            if value:
                raise ValueError("You cannot have a special card with a value.")
            if not color:
                raise ValueError("You cannot have a special card that is not WILD without a color.")
        if value not in Card.POSSIBLE_VALUES:
            raise ValueError(f"{value} is not a valid value.")
        if color not in Card.POSSIBLE_COLORS:
            raise ValueError(f"{color} is not a valid color.")
        if special not in Card.POSSIBLE_SPECIALS:
            raise ValueError(f"{special} is not a valid special.")
        if color and (value is None and not special):
            raise ValueError(f"You cannot have a card with a color but no value or special.")
        if not value and not special and not color:
            raise ValueError(f"Empty card.")

        self.value = value
        self.color = color
        self.special = special

    def get_value(self):
        """Return the value of card
        >>> Card(5, "BLUE").get_value()
        5
        >>> Card(9, "RED").get_value()
        9
        >>> Card(None, None, "WILD").get_value() is None
        True
        >>> Card(None, None, "WILD DRAW 4").get_value() is None
        True
        >>> Card(None, "GREEN", "REVERSE").get_value() is None
        True
        """
        return self.value

    def get_color(self):
        """Return the color of card
        >>> Card(5, "BLUE").get_color()
        'BLUE'
        >>> Card(9, "RED").get_color()
        'RED'
        >>> Card(None, None, "WILD").get_color() is None
        True
        >>> Card(None, None, "WILD DRAW 4").get_color() is None
        True
        >>> Card(None, "GREEN", "REVERSE").get_color()
        'GREEN'
        """
        return self.color

    def get_special(self):
        """Return the special of card
        >>> Card(5, "BLUE").get_special() is None
        True
        >>> Card(9, "RED").get_special() is None
        True
        >>> Card(None, None, "WILD").get_special()
        'WILD'
        >>> Card(None, None, "WILD DRAW 4").get_special()
        'WILD DRAW 4'
        >>> Card(None, "GREEN", "REVERSE").get_special()
        'REVERSE'
        """
        return self.special

    def set_value(self, value):
        """Set the value of card
        >>> card1 = Card(5, "BLUE")
        >>> card1.set_value(0)
        >>> card1.get_value()
        0
        >>> card2 = Card(5, "GREEN")
        >>> card2.set_value(0)
        >>> card2.get_value()
        0
        >>> card3 = Card(None, "GREEN", "REVERSE")
        >>> card3.set_value(8)
        Traceback (most recent call last):
        ...
        ValueError: A card with a special cannot have a value.
        >>> card3 = Card(3, "GREEN")
        >>> card3.set_value(-5)
        Traceback (most recent call last):
        ...
        ValueError: -5 is not a valid value.
        """
        if self.special:
            raise ValueError("A card with a special cannot have a value.")
        value = value if value is None else int(value)

        if value in Card.POSSIBLE_VALUES:
            self.value = value
        else:
            raise ValueError(f"{value} is not a valid value.")

    def set_color(self, color):
        """Set the color of card
        >>> card1 = Card(5, "BLUE")
        >>> card1.set_color("GREEN")
        >>> card1.get_color()
        'GREEN'
        >>> card2 = Card(5, "RED")
        >>> card2.set_color("YELLOW")
        >>> card2.get_color()
        'YELLOW'
        >>> card3 = Card(None, "GREEN", "REVERSE")
        >>> card3.set_color("BLUE")
        >>> card3.get_color()
        'BLUE'
        >>> card4 = Card(None, None, "WILD")
        >>> card4.set_color("BLUE")
        Traceback (most recent call last):
        ...
        ValueError: You cannot set a color to a WILD card.
        >>> card5 = Card(3, "GREEN")
        >>> card5.set_color("PURPLE")
        Traceback (most recent call last):
        ...
        ValueError: PURPLE is not a valid color.
        """
        if self.special == "WILD" or self.special == "WILD DRAW 4":
            raise ValueError("You cannot set a color to a WILD card.")

        color = color if color is None else color.upper()
        if color in Card.POSSIBLE_COLORS:
            self.color = color
        else:
            raise ValueError(f"{color} is not a valid color.")

    def set_special(self, special):
        """Set the special of card
        >>> card1 = Card(5, "BLUE")
        >>> card1.set_special("REVERSE")
        Traceback (most recent call last):
        ...
        ValueError: You cannot set a special to a card with a value.
        >>> card2 = Card(None, "RED", "REVERSE")
        >>> card2.set_special("SKIP")
        >>> card2.get_special()
        'SKIP'
        >>> card3 = Card(None, "GREEN", "REVERSE")
        >>> card3.set_special("WILD")
        Traceback (most recent call last):
        ...
        ValueError: You cannot change a card with a color to a WILD card.
        >>> card4 = Card(None, "GREEN", "DRAW 2")
        >>> card4.set_special("DRAW 3")
        Traceback (most recent call last):
        ...
        ValueError: DRAW 3 is not a valid special.
        """
        special = special if special is None else special.upper()
        if self.color and (special == "WILD" or special == "WILD DRAW 4"):
            raise ValueError("You cannot change a card with a color to a WILD card.")
        if self.value:
            raise ValueError("You cannot set a special to a card with a value.")
        if special in Card.POSSIBLE_SPECIALS:
            self.special = special
        else:
            raise ValueError(f"{special} is not a valid special.")

    def __str__(self):
        """Return string of card
        >>> card1 = Card(5, "BLUE")
        >>> str(card1)
        'UNO Card: BLUE 5'
        >>> card2 = Card(None, "BLUE", "DRAW 2")
        >>> str(card2)
        'UNO Card: BLUE DRAW 2'
        >>> card3 = Card(None, None, "WILD DRAW 4")
        >>> str(card3)
        'UNO Card: WILD DRAW 4'
        >>> card4 = Card(None, None, "WILD")
        >>> print(card4)
        UNO Card: WILD
        """
        if not self.color:
            return f"UNO Card: {self.special}"
        elif not self.special:
            return f"UNO Card: {self.color} {self.value}"
        elif not self.value:
            return f"UNO Card: {self.color} {self.special}"

    def __repr__(self):
        """Return representation of card
        >>> card1 = Card(5, "BLUE")
        >>> card1.__repr__()
        'Card(5, "BLUE", None)'
        >>> card2 = Card(None, "BLUE", "DRAW 2")
        >>> card2.__repr__()
        'Card(None, "BLUE", "DRAW 2")'
        >>> card2 = Card(None, None, "WILD DRAW 4")
        >>> card2.__repr__()
        'Card(None, None, "WILD DRAW 4")'
        """
        if self.color and self.special:
            return f"Card({self.value}, \"{self.color}\", \"{self.special}\")"
        elif self.special:
            return f"Card({self.value}, {self.color}, \"{self.special}\")"
        elif self.color:
            return f"Card({self.value}, \"{self.color}\", {self.special})"
        else:
            return f"Card({self.value}, {self.color}, {self.special})"


if __name__ == "__main__":
    import doctest
    doctest.testmod()

