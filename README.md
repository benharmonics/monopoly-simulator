# Monopoly Simulator

A Monte Carlo simulation of the game Monopoly, written in Python.

We attempt to simulate as much of the game as possible, tracking various data e.g. player money.

## Running

You can import the simulator with `import game`, then run a full simulation with `game.simulate()`. The default behavior when running `main.py` is to simulate several thousand games and compute the average game length, but you could run all sorts of statistical analysis - as the game is run, the players' history is recorded and contained in the `Game` class.

To run a single game and access its metadata, create a `Game` object with a given number of players and max turns, then run the simulation with the `run()` method. Note that you should set a reasonable number of max turns because some games can spiral out of control and go on forever if the bank has infinite money (see [Notes on rules](#notes-on-rules) below).

```python
# Simulating a game and plotting the players' money over time

from game import Game

game = Game(player_count=3, max_turns=75)
nturns = game.run()
game.plot()
print(f"The number of turns in this game was {nturns}.")
```

```python
# Equivalently, you can run a simulation in a single step

import game

nturns = game.simulate(player_count=3, max_turns=75, plot=True)
print(f"The number of turns in this game was {nturns}.")
```

## Upcoming Features

- [ ] Mortgages
- [ ] Limit houses/hotels
- [ ] Limit Get Out of Jail Free cards
- [ ] Use Get Out of Jail Free cards when available
- [ ] Track frequency of spaces
- [ ] Manage properties to avoid bankruptcy
- [ ] Player strategies (all players simply play greedily)
- [ ] Record other types of data?

## Notes on rules

- The bank has unlimited money. During normal play, this means you are encouraged to create your own bank notes from paper if the bank runs out of money.
- The Free Parking space does nothing. Many people play a variation of Monopoly where fees paid to the bank get added to a pot, and a player wins the pot when they land on Free Parking. However, this is not an official rule, and it only tends to make the game longer, so it has been omitted here.

