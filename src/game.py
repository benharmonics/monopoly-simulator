from random import randint
from typing import Optional, Callable

from cards import Cards, Card
import spaces
from spaces import Space
import logging
from player import Player


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


class Game:
    def __init__(self, players: int = 4, max_turns: int = 100) -> None:
        self.max_turns = max_turns
        self.players = [Player(i) for i in range(1, players + 1)]
        self.board = spaces.board()
        self.chance_cards = Cards(
            [
                Card(
                    "Advance to Boardwalk",
                    _advance_to(spaces.BOARDWALK, pay_on_pass_go=False),
                ),
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
        )

        self.community_cards = Cards(
            [
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
                Card(
                    "You have won second prize in a beauty contest. Collect $10",
                    _payout(10),
                ),
                Card("You inherit $100", _payout(100)),
            ]
        )

    def run(self) -> None:
        turn_count = 0
        while len(self.players) > 1 and turn_count < self.max_turns:
            turn_count += 1
            for player in self.players:
                self._take_turn(player)
            self.players = [p for p in self.players if p.money > 0]
            logging.info(f"End of turn {turn_count}: {self.players}")
        if turn_count == self.max_turns:
            logging.info(f"Max turn count reached: {turn_count}")
            logging.info(f"Final state: {self.players}")
            return
        logging.info(f"Winner: {self.players} | Turns: {turn_count}")

    def _owned_spaces(self, player: Player) -> list[Space]:
        return list(s for s in self.board if s.owned_by == player.id)

    def _interact_with_space(self, player: Player):
        space = self.board[player.space]
        # Buy unpurchased spaces
        if space.meta.buying_price and not space.owned_by:
            if player.money <= space.meta.buying_price:
                return
            logging.info(
                f"Player {player.id} purchasing {space.meta.name} for {space.meta.buying_price}"
            )
            self._pay(space.meta.buying_price, player)
            space.owned_by = player.id
            return
        # Pay rent
        if space.owned_by and space.owned_by != player.id:
            rent = spaces.rent_value(self.board, space)
            print(f"{space.owned_by=}")
            other = next(p for p in self.players if p.id == space.owned_by)
            self._pay(space.meta.buying_price, player, other)
            logging.debug(
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
                self._pay(200, player)
            case spaces.LUXURY_TAX:
                self._pay(100, player)
            case s if s in list(spaces.CHANCES):
                card = self.chance_cards.draw()
                logging.debug(f"Chance time for Player {player.id}: {card.name}")
                card.effect(player)
            case s if s in list(spaces.COMMUNITY_CHESTS):
                card = self.community_cards.draw()
                logging.debug(f"Chance time for Player {player.id}: {card.name}")
                card.effect(player)

    def _bankrupt(self, player: Player, pay_to: Optional[Player] = None) -> None:
        logging.info(f"Player {player.id} has gone bankrupt and is exiting the game")
        for space in self._owned_spaces(player):
            player.money = 0
            space.owned_by = pay_to.id if pay_to else None
            space.houses = 0
            space.hotel = False
            space.mortgaged = False

    def _pay(
        self, amount: int, player: Player, pay_to: Optional[Player] = None
    ) -> None:
        if player.money <= amount:
            # TODO: try to mortgage properties, etc. to avoid bankruptcy
            if pay_to:
                pay_to.money += player.money
            return self._bankrupt(player, pay_to)
        if pay_to:
            pay_to.money += amount
        player.money -= amount

    def _buy_houses_and_hotels(self, player: Player) -> None:
        # TODO: strategic property-buying
        for space in self._owned_spaces(player):
            self._buy_houses_and_hotels_on_space(player, space)

    def _buy_houses_and_hotels_on_space(self, player: Player, space: Space) -> None:
        # railroads, utilities can be purchased, but houses cannot be built on them
        if not space.meta.building_price:
            return
        assert (
            space.meta.color is not None
        ), "Color should exist on spaces when buying houses/hotels"
        assert (
            space.owned_by is not None
        ), "When buying houses/hotels, space must be owned"
        assert (
            space.owned_by == player.id
        ), "When buying houses/hotels, space must be owned by player"
        if not spaces.player_owns_all_color(
            self.board, space.meta.color, space.owned_by
        ):
            return
        if player.money <= space.meta.building_price or space.hotel:
            return
        player.money -= space.meta.building_price
        if space.houses < 4:
            space.houses += 1
            logging.debug(
                f"Player {player.id} purchased house on {space.meta.name} for ${space.meta.building_price}"
            )
        else:
            space.houses = 0
            space.hotel = True
            logging.debug(
                f"Player {player.id} purchased hotel on {space.meta.name} for ${space.meta.building_price}"
            )

    def _take_turn(self, player: Player, remaining_rolls=3):
        roll1, roll2 = randint(1, 6), randint(1, 6)
        rolled_doubles = roll1 == roll2

        if not rolled_doubles and player.jail_sentence > 0:
            player.jail_sentence -= 1
            logging.debug(
                f"Player {player.id} is in jail and can't  move ({player.jail_sentence} turns remaining)"
            )
            self._buy_houses_and_hotels(player)
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

        self._interact_with_space(player)
        self._buy_houses_and_hotels(player)

        if rolled_doubles:
            if player.jail_sentence != 0:
                self._take_turn(player, remaining_rolls - 1)
            player.jail_sentence = 0
