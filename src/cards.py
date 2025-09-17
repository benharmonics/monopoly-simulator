from dataclasses import dataclass
from random import shuffle
from typing import Callable


@dataclass
class Card:
    name: str
    effect: Callable


class Cards:
    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards
        self._discard: list[Card] = []
        shuffle(self._cards)

    def draw(self) -> Card:
        card = self._cards.pop()
        self._discard.append(card)
        if not self._cards:
            self._cards, self._discard = self._discard, self._cards
            shuffle(self._cards)
        return card
