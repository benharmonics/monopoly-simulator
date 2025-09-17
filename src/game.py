from random import randint

from chance import ChanceCards
import spaces
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

    def _player_interact_with_space(self, player: Player):
        space = self.board[player.space]
        # Buy unpurchased spaces
        if space.meta.buying_price and not space.owned_by:
            if player.money <= space.meta.buying_price:
                return
            logging.info(
                f"Player {player.id} purchasing {space.meta.name} for {space.meta.buying_price}"
            )
            player.money -= space.meta.buying_price
            space.owned_by = player.id
            return
        # Pay rent
        if space.owned_by and space.owned_by != player.id:
            rent = spaces.rent_value(self.board, space)
            other = next(p for p in self.players if p.id == space.owned_by)
            player.money -= rent
            other.money += rent
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
                player.money -= 200
            case spaces.LUXURY_TAX:
                player.money -= 100
            case s if s in list(spaces.CHANCES):
                card = self.chance_cards.draw()
                logging.info(f"Chance time for Player {player.id}: {card.name}")
                card.effect(player)
            case s if s in list(spaces.COMMUNITY_CHESTS):
                logging.debug(
                    f"Player {player.id} landed on Community Chest [UNIMPLEMENTED]"
                )
                ...

    def _player_turn(self, player: Player, remaining_rolls=3):
        roll1, roll2 = randint(1, 6), randint(1, 6)
        rolled_doubles = roll1 == roll2

        if not rolled_doubles and player.jail_sentence > 0:
            player.jail_sentence -= 1
            logging.debug(
                f"Player {player.id} is in jail and can't  move ({player.jail_sentence} turns remaining)"
            )

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
        logging.debug(f"Player {player.id} landed on space {spaces._space_name(player.space)}")

        self._player_interact_with_space(player)

        # Bankruptcy
        if player.money <= 0:
            logging.info(
                f"Player {player.id} has gone bankrupt and is exiting the game"
            )
            for space in self.board:
                if space.owned_by != player.id:
                    continue
                space.owned_by = None
                space.mortgaged = False
                space.houses = 0
                space.hotel = False
            return

        # Buy houses/hotels
        for space in self.board:
            if space.owned_by != player.id:
                continue
            # railroads, utilities can be purchased, but have no color, and
            if not space.meta.color or not space.owned_by:
                continue
            if not spaces.player_owns_all_color(self.board, space.meta.color, space.owned_by):
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
