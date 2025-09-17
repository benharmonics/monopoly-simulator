import logging

import game

def monte_carlo_game_length():
    import matplotlib.pyplot as plt
    import numpy as np

    game_lengths = [game.simulate() for _ in range(1_000)]
    game_lengths = [gl for gl in game_lengths if gl < 100]
    logging.info(f"{np.mean(game_lengths)=}")
    plt.hist(game_lengths)
    plt.title("Monopoly game lengths")
    plt.xlabel("Game length (turns)")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    monte_carlo_game_length()
    #game.simulate(plot=True)
