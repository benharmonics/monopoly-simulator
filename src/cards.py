from dataclasses import dataclass
from random import shuffle
import logging
from typing import Callable

import spaces
from player import Player


@dataclass
class Card:
    name: str
    effect: Callable


class Cards:
    def __init__(self, deck: str) -> None:
        if deck != "chance" and deck != "community":
            raise KeyError("Deck must be either 'chance' or 'community'")
        self._cards: list[Card] = (
            _chance_cards if deck == "chance" else _community_cards
        )
        self._discard: list[Card] = []
        shuffle(self._cards)

    def draw(self) -> Card:
        card = self._cards.pop()
        self._discard.append(card)
        if not self._cards:
            self._cards, self._discard = self._discard, self._cards
            shuffle(self._cards)
        return card


def _advance_to(space_i: int, pay_on_pass_go: bool = True) -> Callable:
    def _inner(p: Player) -> None:
        if p.space > space_i and pay_on_pass_go:
            p.money += 200
        p.space = space_i

    return _inner


def _payout(amount: int) -> Callable:
    def _inner(p: Player) -> None:
        p.money += amount

    return _inner


def _go_back_three_spaces(p: Player):
    p.space = (p.space - 3) % len(spaces.board())


def _advance_to_railroad(p: Player):
    railroad = spaces.next_railroad(p.space)
    if p.space > railroad:
        p.money += 200
    p.space = railroad
    logging.debug("TODO: buy railroad")


def _advance_to_utility(p: Player):
    utility = spaces.next_utility(p.space)
    if p.space > utility:
        p.money += 200
    p.space = utility
    logging.debug("TODO: buy utility")


def _receive_get_out_of_jail_free(p: Player):
    p.get_out_of_jail_cards += 1


def _go_to_jail(p: Player):
    p.space = spaces.JAIL
    p.jail_sentence = 3


# TODO: two chance cards require interactions with the board or other players
_chance_cards = [
    Card("Advance to Boardwalk", _advance_to(spaces.BOARDWALK, pay_on_pass_go=False)),
    Card("Advance to Go (Collect $200)", _advance_to(spaces.GO)),
    Card(
        "Advance to Illinois Avenue. If you pass Go, collect $200",
        _advance_to(spaces.ILLINOIS_AVENUE),
    ),
    Card(
        "Advance to St. Charles Place. If you pass Go, collect $200",
        _advance_to(spaces.ST_CHARLES_PLACE),
    ),
    Card(
        "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled",
        _advance_to_railroad,
    ),
    Card(
        "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled",
        _advance_to_railroad,
    ),
    Card(
        "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown.",
        _advance_to_utility,
    ),
    Card("Bank pays you dividend of $50", _payout(50)),
    Card("Get Out of Jail Free", _receive_get_out_of_jail_free),
    Card("Go Back 3 Spaces", _go_back_three_spaces),
    Card(
        "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200",
        _go_to_jail,
    ),
    # ChanceCard("Make general repairs on all your property. For each house pay $25. For each hotel pay $100", ),
    Card("Speeding fine $15", _payout(-15)),
    Card(
        "Take a trip to Reading Railroad. If you pass Go, collect $200",
        _advance_to(spaces.READING_RAILROAD),
    ),
    # ChanceCard("You have been elected Chairman of the Board. Pay each player $50", ),
    Card("Your building loan matures. Collect $150", _payout(150)),
]

# TODO: two community cards require interactions with the board or other players
_community_cards = [
    Card("Advance to Go (Collect $200)", _advance_to(spaces.GO)),
    Card("Bank error in your favor. Collect $200", _payout(200)),
    Card("Doctor’s fee. Pay $50", _payout(-50)),
    Card("From sale of stock you get $50", _payout(50)),
    Card("Get Out of Jail Free", _receive_get_out_of_jail_free),
    Card(
        "Go to Jail. Go directly to jail, do not pass Go, do not collect $200",
        _go_to_jail,
    ),
    Card("Holiday fund matures. Receive $100", _payout(100)),
    Card("Income tax refund. Collect $20", _payout(20)),
    # Card("It is your birthday. Collect $10 from every player", ),
    Card("Life insurance matures. Collect $100", _payout(100)),
    Card("Pay hospital fees of $100", _payout(-100)),
    Card("Pay school fees of $50", _payout(-50)),
    Card("Receive $25 consultancy fee", _payout(25)),
    # Card("You are assessed for street repair. $40 per house. $115 per hotel", ),
    Card("You have won second prize in a beauty contest. Collect $10", _payout(10)),
    Card("You inherit $100", _payout(100)),
]
