import random


# Deck

# Player
# - hit/stand

# Bank
# - withdraw/deposit

# Game
# - deal
#
class Player:
    def __init__(self, name, bank):
        self.name = name
        self.bank = bank


class ConsolePlayer(Player):
    pass


class Dealer(Player):
    pass


class Bank:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        self.balance -= amount
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance


class EndlessBank:
    pass


def play():
    pass


def main():
    # create a list of players and their banks
    player1_bank = Bank(100)
    player1 = ConsolePlayer("Gosia", player1_bank)

    players = [player1]

    # check if we have enough players and if the players have enough money
    allowed_players = []
    for player in players:
        if player.bank > 10:
            allowed_players.append(player)

    if len(allowed_players) == 1:
        dealer_bank = EndlessBank()
        dealer = Dealer("dealer", dealer_bank)
        allowed_players.append(dealer)
    # start the single game
    if len(allowed_players) > 1:
        play()


# pojedyncza gra start
# tworzymy i tasujemy talie
# decydujemy kto zaczyna
# rozdajemy po 2 karty na start
# pytamy gracza co robi
# gracz decyduje
# przeliczamy, sprawdzamy, czy mamy zwiyciezce
# zmieniamy gracza
# ogłaszamy zwyciezce

# pytamy, czy chcą grać
