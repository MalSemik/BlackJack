import random


class Player:
    def __init__(self, name, bank):
        self.name = name
        self.bank = bank


class ConsolePlayer(Player):
    pass


class Dealer:
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


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __repr__(self):
        return str(self.value) + self.color

    def get_game_value(self):
        if self.value not in ["A", "K", "Q", "J"]:
            return self.value
        elif self.value in ["K", "Q", "J"]:
            return 10
        else:
            return None


class Deck:
    def __init__(self):
        self.deck = self.create_deck()

    @classmethod
    def create_deck(cls):
        """
        >>> print(Deck.create_deck())
        [2♣, 3♣, 4♣, 5♣, 6♣, 7♣, 8♣, 9♣, 10♣, A♣, K♣, Q♣, J♣, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, 8♦, 9♦, 10♦, A♦, K♦, Q♦, J♦, 2♥, 3♥, 4♥, 5♥, 6♥, 7♥, 8♥, 9♥, 10♥, A♥, K♥, Q♥, J♥, 2♠, 3♠, 4♠, 5♠, 6♠, 7♠, 8♠, 9♠, 10♠, A♠, K♠, Q♠, J♠]
        """
        new_deck = []
        SYMBOLS = ['♣', '♦', '♥', '♠']
        for symbol in SYMBOLS:
            for i in range(2, 11):
                new_deck.append(Card(i, symbol))
            for item in ['A', 'K', 'Q', 'J']:
                new_deck.append(Card(item, symbol))
        return new_deck

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self, quantity=1):
        cards = []
        for i in range(quantity):
            cards.append(self.deck.pop())
        return cards


def move_aces_to_the_end(hand):
    """
    >>> move_aces_to_the_end([Card('A','♦'),Card(4,'♦')])
    [4♦, A♦]
    >>> move_aces_to_the_end([Card('A','♥'),Card(4,'♦'),Card('A','♦'),Card('K','♦')])
    [4♦, K♦, A♥, A♦]
    >>> move_aces_to_the_end([Card(4,'♦'),Card('K','♦')])
    [4♦, K♦]
    """
    sorted_hand = []
    aces = []
    for card in hand:
        if card.value != 'A':
            sorted_hand.append(card)
        else:
            aces.append(card)
    if len(aces) > 0:
        sorted_hand += aces
    return sorted_hand


def count(hand):
    """
    >>> count([Card(4,'♦'),Card('A','♦'),])
    15
    >>> count([Card(4,'♦'),Card('K','♦'),Card('A','♥'),Card('A','♦')])
    16
    >>> count([Card('A','♥'),Card('A','♦')])
    12
    """
    sorted_hand = move_aces_to_the_end(hand)
    counter = 0
    for card in sorted_hand:
        if card.get_game_value() is not None:
            counter += card.get_game_value()
        else:
            if counter + 11 > 21:
                counter += 1
            else:
                counter += 11
    return counter


def get_bet(player):
    bet = int(input(f'How much would you like to bet? (Your current balance is {player.bank.balance})'))
    while bet > player.bank.balance:
        bet = int(input(
            f'You can\'t bet more than you have. How much would you like to bet? (Your current balance is {player.bank.balance})'))
    return bet

def check_if_player_won(player, dealer, player_hand):
    player_hand_value = count(player_hand)
    if player_hand_value == 21:
        return player
    elif player_hand_value < 21:
        return None
    else:
        return dealer


def play(player, dealer):
    deck = Deck()
    deck.shuffle()
    player_hand = deck.draw(2)
    dealer_hand = deck.draw(2)
    print(f'Player\'s hand: {player_hand}, Dealer\'s hand: {dealer_hand[0]}X')

    bet = get_bet(player)
    player_hand_value = count(player_hand)

    decision = ''
    while decision != 's':
        decision = input('Hit or Stand? (h/s)')
        if decision.lower() == 'h':
            player_hand += deck.draw()
            print(f'Player\'s hand: {player_hand}, Dealer\'s hand: {dealer_hand[0]}X')
            player_hand_value = count(player_hand)

            winner = check_if_player_won(player, dealer, player_hand)
            if winner == player:
                print('You win!')
                player.bank.deposit(bet * 2)
            elif winner == dealer:
                print('You loose!')
                player.bank.withdraw(bet)
            else:
                pass
        elif decision.lower() == 's':
            break
        else:
            print('You have to write h or s')
            continue
    dealer_hand_value = count(dealer_hand)
    while dealer_hand_value < 17:
        dealer_hand += deck.draw()
        print(f'Player\'s hand: {player_hand}, Dealer\'s hand: {dealer_hand}')
        dealer_hand_value = count(dealer_hand)
    if dealer_hand_value == 21:
        winner = dealer
        print(f'Player\'s hand: {player_hand}, Dealer\'s hand: {dealer_hand}')
        return winner, bet
    elif dealer_hand_value > 21:
        winner = player
        print(f'Player\'s hand: {player_hand}, Dealer\'s hand: {dealer_hand}')
        return winner, bet
    else:
        if dealer_hand_value > player_hand_value:
            winner = dealer
            print(f'Player\'s hand: {player_hand}, Dealer\'s hand: {dealer_hand}')
            return winner, bet
        else:
            winner = player
            print(f'Player\'s hand: {player_hand}, Dealer\'s hand: {dealer_hand}')
            return winner, bet


def main():
    # create a list of players and their banks
    player1_bank = Bank(100)
    player1 = ConsolePlayer("Gosia", player1_bank)
    dealer = Dealer()

    game = True
    while game:
        if player1_bank.balance > 0:
            play_decision = input('Do you want to play? (Y/N)')
            if play_decision.lower() == 'y':
                winner, bet = play(player1, dealer)
                if winner == player1:
                    print('You win!')
                    player1.bank.deposit(bet * 2)
                else:
                    print('You loose!')
                    player1.bank.withdraw(bet)
            else:
                print('Goodbye then!')
                game = False
        else:
            print('You\'re broke! Go home!')
            game = False


if __name__ == "__main__":
    main()
