from argparse import ArgumentParser
import logging
import statistics

import matplotlib.pyplot as plt
import numpy as np

import game


def monte_carlo_game_length():
    ngames = 10_000
    game_lengths = [game.simulate() for _ in range(ngames)]
    game_lengths = [gl for gl in game_lengths if gl < 100]
    average = np.mean(game_lengths, dtype=np.float64)
    logging.info(f"{np.mean(game_lengths)=}")
    logging.info(f"{np.median(game_lengths)=}")
    logging.info(f"{statistics.mode(game_lengths)=}")
    plt.hist(
        game_lengths,
        bins=range(min(game_lengths), max(game_lengths) + 1, 1),
        color="c",
        edgecolor="k",
    )
    plt.axvline(
        average.astype(float),
        color="r",
        linestyle="dashed",
        linewidth=1,
        label=f"Average turns ({average})",
    )
    plt.title(f"Monopoly game lengths ({len(game_lengths)} games)")
    plt.xlabel("Game length (turns)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="monopoly-simulator",
        description="Monte Carlo simulation of the game Monopoly for data analysis",
    )
    parser.add_argument(
        "-l", "--loglevel", default="INFO", choices=("INFO", "WARN", "ERROR")
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    monte_carlo_game_length()
    # game.simulate(plot=True)
