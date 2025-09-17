from dataclasses import dataclass
from random import randint
from typing import Optional

import spaces
import logging


@dataclass
class Player:
    id: int
    money: int = 1500
    space: int = 0
    jail_sentence: int = 0
    strategy: str = "greedy"


@dataclass
class Space:
    meta: spaces.Meta
    houses: int = 0
    hotel: bool = False
    purchased_by: Optional[int] = None
    mortgaged: bool = False


class Game:
    def __init__(self, players: int = 4) -> None:
        self.players = [Player(i) for i in range(1, players + 1)]
        self.board = [Space(space) for space in spaces.board()]

    def run(self) -> None:
        while len(self.players) > 1:
            for player in self.players:
                self._player_turn(player)
            self.players = [p for p in self.players if p.money > 0]
            logging.info(f"End of turn: {self.players}")
        logging.info(f"Winner: {self.players}")

    def _player_owns_all_color(self, color: str, player_id: int) -> bool:
        color_count = len(
            list(s for s in self.board if s.meta.color == color)
        )
        owned_count = len(
            list(s for s in self.board if s.meta.color == color and s.purchased_by == player_id)
        )
        return color_count == owned_count

    def _rent(self, space: Space) -> int:
        assert space.purchased_by is not None, "Space must be purchased to get rent data"
        assert space.meta.color is not None, "Space must be colored to get rent data"
        match space.houses:
            case 0:
                rent = space.meta.rent
            case 1:
                rent = space.meta.rent_with_one_house
            case 2:
                rent = space.meta.rent_with_two_houses
            case 3:
                rent = space.meta.rent_with_three_houses
            case 4:
                rent = space.meta.rent_with_four_houses
            case _:
                raise AssertionError(
                    f"invalid number of houses on {space.meta.name}: {space.houses}"
                )
        if space.hotel:  # overwrites 0 houses case
            rent = space.meta.rent_with_hotel
        return rent * 2 if self._player_owns_all_color(space.meta.color, space.purchased_by) else rent

    def _player_interact_with_space(self, player: Player):
        space = self.board[player.space]
        # Buy unpurchased spaces
        if space.meta.buying_price and not space.purchased_by:
            if player.money <= space.meta.buying_price:
                return
            logging.info(
                f"Player {player.id} purchasing {space.meta.name} for {space.meta.buying_price}"
            )
            player.money -= space.meta.buying_price
            space.purchased_by = player.id
            return
        # Pay rent
        if space.purchased_by and space.purchased_by != player.id:
            rent = self._rent(space)
            other = next(p for p in self.players if p.id == space.purchased_by)
            player.money -= rent
            other.money += rent
            logging.info(
                f"Player {player.id} payed rent of ${rent} to Player {space.purchased_by} for {space.meta.name}"
            )
        # Special cases
        match player.space:
            case spaces.GO_TO_JAIL:
                logging.debug(f"Player {player.id}, go to jail! (Landed on 'Go To Jail')")
                player.space = spaces.JAIL
                player.jail_sentence = 3
            case s if s in list(spaces.CHANCES):
                logging.debug(f"Player {player.id} chance! [UNIMPLEMENTED]")
                ...

    def _player_turn(self, player: Player, remaining_rolls=3):
        roll1, roll2 = randint(1, 6), randint(1, 6)
        rolled_doubles = roll1 == roll2

        if not rolled_doubles and player.jail_sentence > 0:
            player.jail_sentence -= 1
            logging.debug(f"Player {player.id} is in jail and can't  move ({player.jail_sentence} turns remaining)")

        if rolled_doubles and remaining_rolls < 1:
            logging.debug(f"Player {player.id}, go to jail! (Triple-Doubles)")
            player.space = spaces.JAIL
            return

        inext = sum((player.space, roll1, roll2))
        passed_go = inext >= len(self.board)
        player.space = inext % len(self.board)
        player.money += passed_go * 200
        if passed_go:
            logging.debug(f"Player {player.id} has passed GO and collected $200")
        logging.debug(f"Player {player.id} landed on space {spaces.name(player.space)}")

        self._player_interact_with_space(player)

        # Bankruptcy
        if player.money <= 0:
            logging.info(f"Player {player.id} has gone bankrupt and is exiting the game")
            for space in self.board:
                if space.purchased_by != player.id:
                    continue
                space.purchased_by = None
                space.mortgaged = False
                space.houses = 0
                space.hotel = False
            return

        # Buy houses/hotels
        for space in self.board:
            if space.purchased_by != player.id:
                continue
            assert space.purchased_by is not None and space.meta.color is not None
            if not self._player_owns_all_color(space.meta.color, space.purchased_by):
                continue
            if player.money <= space.meta.building_price or space.hotel:
                continue
            player.money -= space.meta.building_price
            if space.houses < 4:
                space.houses += 1
                logging.info(
                    f"Player {player.id} purchased house on {space.meta.name} for ${space.meta.building_price}"
                )
            else:
                space.houses = 0
                space.hotel = True
                logging.info(
                    f"Player {player.id} purchased hotel on {space.meta.name} for ${space.meta.building_price}"
                )

        if rolled_doubles:
            if player.jail_sentence != 0:
                self._player_turn(player, remaining_rolls - 1)
            player.jail_sentence = 0
