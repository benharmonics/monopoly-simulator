from dataclasses import dataclass
from random import shuffle
import logging
from typing import Callable

import spaces
from player import Player

@dataclass
class ChanceCard:
    name: str
    effect: Callable

class ChanceCards:
    def __init__(self) -> None:
        self._cards: list[ChanceCard] = _chance_cards
        self._discard: list[ChanceCard] = []
        shuffle(self._cards)

    def draw(self) -> ChanceCard:
        card = self._cards.pop()
        self._discard.append(card)
        if not self._cards:
            self._cards, self._discard = self._discard, self._cards
            shuffle(self._cards)
        return card



def _advance_to_boardwalk(p: Player):
    p.space = spaces.BOARDWALK

def _advance_to_go(p: Player):
    p.space = spaces.GO
    p.money += 200

def _advance_to_illinois_ave(p: Player):
    if p.space > spaces.ILLINOIS_AVENUE:
        p.money += 200
    p.space = spaces.ILLINOIS_AVENUE

def _advance_to_st_charles_ave(p: Player):
    if p.space > spaces.ST_CHARLES_PLACE:
        p.money += 200
    p.space = spaces.ST_CHARLES_PLACE

def _advance_to_reading_railroad(p: Player):
    if p.space > spaces.READING_RAILROAD:
        p.money += 200
    p.space = spaces.READING_RAILROAD

def _bank_pays_dividend(p: Player):
    p.money += 50

def _speeding_fine(p: Player):
    p.money -= 15

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

def _building_loan_matures(p: Player):
    p.money += 150

# TODO: two chance cards require interactions with the board or other players
_chance_cards = [
    ChanceCard("Advance to Boardwalk", _advance_to_boardwalk),
    ChanceCard("Advance to Go (Collect $200)", _advance_to_go),
    ChanceCard("Advance to Illinois Avenue. If you pass Go, collect $200", _advance_to_illinois_ave),
    ChanceCard("Advance to St. Charles Place. If you pass Go, collect $200", _advance_to_st_charles_ave),
    ChanceCard("Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled", _advance_to_railroad),
    ChanceCard("Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled", _advance_to_railroad),
    ChanceCard("Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown.", _advance_to_utility),
    ChanceCard("Bank pays you dividend of $50", _bank_pays_dividend),
    ChanceCard("Get Out of Jail Free", _receive_get_out_of_jail_free),
    ChanceCard("Go Back 3 Spaces", _go_back_three_spaces),
    ChanceCard("Go to Jail. Go directly to Jail, do not pass Go, do not collect $200", _go_to_jail),
    #ChanceCard("Make general repairs on all your property. For each house pay $25. For each hotel pay $100", ),
    ChanceCard("Speeding fine $15", _speeding_fine),
    ChanceCard("Take a trip to Reading Railroad. If you pass Go, collect $200", _advance_to_reading_railroad),
    #ChanceCard("You have been elected Chairman of the Board. Pay each player $50", ),
    ChanceCard("Your building loan matures. Collect $150", _building_loan_matures),
]

