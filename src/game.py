from random import randint
from typing import Optional

from chance import ChanceCards
import spaces
from spaces import Space
import logging
from player import Player


class Game:
    def __init__(self, players: int = 4) -> None:
        self.players = [Player(i) for i in range(1, players + 1)]
        self.board = spaces.board()
        self.chance_cards = ChanceCards()

    def run(self) -> None:
        while len(self.players) > 1:
            for player in self.players:
                self._player_turn(player)
            self.players = [p for p in self.players if p.money > 0]
            logging.info(f"End of turn: {self.players}")
        logging.info(f"Winner: {self.players}")

    def _player_owned_spaces(self, player: Player) -> list[Space]:
        return list(s for s in self.board if s.owned_by == player.id)

    def _player_interact_with_space(self, player: Player):
        space = self.board[player.space]
        # Buy unpurchased spaces
        if space.meta.buying_price and not space.owned_by:
            if player.money <= space.meta.buying_price:
                return
            logging.info(
                f"Player {player.id} purchasing {space.meta.name} for {space.meta.buying_price}"
            )
            self._player_pay(space.meta.buying_price, player)
            space.owned_by = player.id
            return
        # Pay rent
        if space.owned_by and space.owned_by != player.id:
            rent = spaces.rent_value(self.board, space)
            other = next(p for p in self.players if p.id == space.owned_by)
            self._player_pay(space.meta.buying_price, player, other)
            logging.info(
                f"Player {player.id} paid rent of ${rent} to Player {space.owned_by} for {space.meta.name}"
            )
        # Special cases
        match player.space:
            case spaces.GO_TO_JAIL:
                logging.debug(
                    f"Player {player.id}, go to jail! (Landed on 'Go To Jail')"
                )
                player.space = spaces.JAIL
                player.jail_sentence = 3
            case spaces.FREE_PARKING:
                # In some variants, you receive money on this space, but house rules say
                # that this space is effectively a no-op: you don't need to pay rent when
                # landing here, which is the "feature" if this space, per se.
                ...
            case spaces.INCOME_TAX:
                self._player_pay(200, player)
            case spaces.LUXURY_TAX:
                self._player_pay(100, player)
            case s if s in list(spaces.CHANCES):
                card = self.chance_cards.draw()
                logging.info(f"Chance time for Player {player.id}: {card.name}")
                card.effect(player)
            case s if s in list(spaces.COMMUNITY_CHESTS):
                logging.debug(
                    f"Player {player.id} landed on Community Chest [UNIMPLEMENTED]"
                )
                ...

    def _player_bankrupt(self, player: Player, pay_to: Optional[Player] = None) -> None:
        logging.info(f"Player {player.id} has gone bankrupt and is exiting the game")
        for space in self._player_owned_spaces(player):
            space.owned_by = pay_to.id if pay_to else None
            space.houses = 0
            space.hotel = False
            space.mortgaged = False

    def _player_pay(self, amount: int, player: Player, pay_to: Optional[Player] = None) -> None:
        if player.money <= amount:
            return self._player_bankrupt(player, pay_to)
        player.money -= amount
        if pay_to:
            pay_to.money += amount

    def _player_try_buy_houses_and_hotels(self, player: Player) -> None:
        # TODO: strategic property-buying
        for space in self._player_owned_spaces(player):
            self._player_try_buy_houses_and_hotels_on_space(player, space)

    def _player_try_buy_houses_and_hotels_on_space(self, player: Player, space: Space) -> None:
        # railroads, utilities can be purchased, but houses cannot be built on them
        if not space.meta.building_price:
            return
        assert space.meta.color is not None, "Color should exist on spaces when buying houses/hotels"
        assert space.owned_by is not None, "When buying houses/hotels, space must be owned"
        assert space.owned_by == player.id, "When buying houses/hotels, space must be owned by player"
        if not spaces.player_owns_all_color(
            self.board, space.meta.color, space.owned_by
        ):
            return
        if player.money <= space.meta.building_price or space.hotel:
            return
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


    def _player_turn(self, player: Player, remaining_rolls=3):
        roll1, roll2 = randint(1, 6), randint(1, 6)
        rolled_doubles = roll1 == roll2

        if not rolled_doubles and player.jail_sentence > 0:
            player.jail_sentence -= 1
            logging.debug(
                f"Player {player.id} is in jail and can't  move ({player.jail_sentence} turns remaining)"
            )
            self._player_try_buy_houses_and_hotels(player)
            return

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
        logging.debug(
            f"Player {player.id} landed on space {spaces._space_name(player.space)}"
        )

        self._player_interact_with_space(player)
        if player.money <= 0:
            return self._player_bankrupt(player)
        self._player_try_buy_houses_and_hotels(player)

        if rolled_doubles:
            if player.jail_sentence != 0:
                self._player_turn(player, remaining_rolls - 1)
            player.jail_sentence = 0
