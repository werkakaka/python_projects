import random

class Dice:
    def __init__(self, sides):
        self._sides = sides
        self._value = None

    def roll(self):
        self._value = random.randint(1, self._sides)

    def get_sides(self):
        return self._sides

    def get_value(self):
        return self._value

    def __str__(self):
        return f"Ilość ścianek: {self._sides}, liczba oczek: {self._value}"

player_score = 0
computer_score = 0

dice1 = Dice(6)
dice2 = Dice(6)

while computer_score < 17:
    dice1.roll()
    dice2.roll()
    computer_score += dice1.get_value() + dice2.get_value()

while player_score < 21:
    choice = input("Czy chcesz rzucić kostkami? (tak/nie): ").strip().lower()
    if choice == "nie":
        break
    dice1.roll()
    dice2.roll()
    player_score += dice1.get_value() + dice2.get_value()
    print(f"Twój wynik: {player_score}")

if player_score > 21:
    print("Przegrałeś! Twój wynik przekroczył 21.")
elif computer_score > 21 or player_score > computer_score:
    print("Wygrałeś!")
elif player_score < computer_score:
    print("Przegrałeś!")
else:
    print("Remis!")

print(f"Wynik komputera: {computer_score}, Twój wynik: {player_score}")
