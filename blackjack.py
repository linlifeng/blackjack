# coding=utf-8

import random

suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
numbers = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}
deck = []
for suit in suits:
    for number in numbers:
        deck.append(number + ' of ' + suit)

# these part was copied from a stackoverflow question.
class Card(object):
    card_values = {
        'Ace': 11,  # value of the ace is high until it needs to be low
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10
    }

    def __init__(self, suit, rank):
        """
        :param suit: The face of the card, e.g. Spade or Diamond
        :param rank: The value of the card, e.g 3 or King
        """
        self.suit = suit.capitalize()
        self.rank = rank
        self.points = self.card_values[rank]

def ascii_version_of_card(*cards):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
    keep it as a list so that the dealer can add a hidden card in front of the list
    """
    return_string = True
    # we will use this to prints the appropriate icons for each card
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', '♦', '♥', '♣']

    # create an empty list of list, each sublist is a line
    lines = [[] for i in range(9)]

    for index, card in enumerate(cards):
        # "King" should be "K" and "10" should still be "10"
        if card.rank == '10':  # ten is the only one who's rank is 2 char long
            rank = card.rank
            space = ''  # if we write "10" on the card that line will be 1 char to long
        else:
            rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
            space = ' '  # no "10", we use a blank space to will the void
        # get the cards suit in two steps
        suit = suits_name.index(card.suit)
        suit = suits_symbols[suit]

        # add the individual card on a line by line basis
        lines[0].append('┌─────────┐')
        lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {}{}│'.format(space, rank))
        lines[8].append('└─────────┘')

    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))

    # hidden cards do not use string
    if return_string:
        return '\n'.join(result)
    else:
        return result


def ascii_version_of_hidden_card(*cards):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """
    # a flipper over card. # This is a list of lists instead of a list of string becuase appending to a list is better then adding a string
    lines = [['┌─────────┐'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['└─────────┘']]

    # store the non-flipped over card after the one that is flipped over
    cards_except_first = ascii_version_of_card(*cards[1:], return_string=False)
    for index, line in enumerate(cards_except_first):
        lines[index].append(line)

    # make each line into a single list
    for index, line in enumerate(lines):
        lines[index] = ''.join(line)

    # convert the list into a single string
    return '\n'.join(lines)

## end copied code

class Deck(object):
    def __init__(self, cards):
        self.cards = cards
        self.size = len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop()
        # print(card)
        # print(len(self.cards))
        return card


class Hand(Deck):
    def hit(self, card):
        self.cards.append(card)

    def score(self):
        total_score = 0
        ace = False
        for card in self.cards:
            number, suit = card.split(' of ')
            value = numbers[number]
            total_score += value
            if number == 'Ace':
                ace = True

        if ace:
            alt_score = total_score + 10
            if alt_score <= 21:
                total_score = alt_score

        return total_score

    def display(self):
        card_objects = []
        for card in self.cards:
            number, suit = card.split(' of ')
            card_object = Card(suit, number)
            card_objects.append(card_object)

        print(ascii_version_of_card(*tuple(card_objects)))


def check_end(dealer_hand, player_hands):
    # end if anyone got blackjack
    for player_hand in player_hands:
        if player_hand.score() == 21:
            return True

    # end if dealer busted
    if dealer_hand.score() > 21:
        return True

    # end if anyone busted
    for player_hand in player_hands:
        if player_hand.score() > 21:
            return True


def compare_hand(dealer_hand, player_hands):
    results = []
    for player_hand in player_hands:
        if player_hand.score() > 21 and dealer_hand.score() > 21:
            results.append("Draw")
        elif player_hand.score() > 21:
            results.append("Player Busted!")
        elif dealer_hand.score() > 21:
            results.append("Player Won! Dealer Busted.")
        elif player_hand.score() > dealer_hand.score():
            results.append("Player Won")
        elif player_hand.score() < dealer_hand.score():
            results.append("Player Lost")
        else:
            results.append("Draw")
    return results


if __name__ == '__main__':
    deck = Deck(deck)
    # print(deck.cards)
    deck.shuffle()

    # dealing
    player_hand = Hand([])
    dealer_hand = Hand([])

    card = deck.deal()
    player_hand.hit(card)
    card = deck.deal()
    dealer_hand.hit(card)
    card = deck.deal()
    player_hand.hit(card)
    card = deck.deal()
    dealer_hand.hit(card)

    # playing
    # print("player:", player_hand.cards, player_hand.score())
    print("Player's Hand:")
    player_hand.display()
    # print("dealer:", dealer_hand.cards, dealer_hand.score())
    print("Dealer's Hand:")
    dealer_hand.display()

    end = check_end(dealer_hand, [player_hand])
    while not end:
        choice = raw_input("Hit[H] or Pass[P]?")
        if choice.upper() == 'H':
            print("player hits")
            card = deck.deal()
            player_hand.hit(card)
            end = check_end(dealer_hand, [player_hand])

        if choice.upper() == 'P':
            # player pass, dealer continue hitting until win or bust
            print("player holds.")
            while dealer_hand.score() < player_hand.score():
                card = deck.deal()
                dealer_hand.hit(card)
                print("dealer:", dealer_hand.cards, dealer_hand.score())
                end = check_end(dealer_hand, [player_hand])
            end = True

        # print("player:", player_hand.cards, player_hand.score())
        print("Player's Hand:")
        player_hand.display()
        # print("dealer:", dealer_hand.cards, dealer_hand.score())
        print("Dealer's Hand:")
        dealer_hand.display()

    # results:
    results = compare_hand(dealer_hand, [player_hand])
    # print("player:", player_hand.cards, player_hand.score())
    print("Player's Hand:")
    player_hand.display()
    # print("dealer:", dealer_hand.cards, dealer_hand.score())
    print("Dealer's Hand:")
    dealer_hand.display()
    print("*******")
    print(results[0])
    print("*******")

