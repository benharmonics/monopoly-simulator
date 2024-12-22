from dataclasses import dataclass


@dataclass
class Player:
    id: int
    money: int = 1500
    space: int = 0
    jail_sentence: int = 0
    get_out_of_jail_cards: int = 0
