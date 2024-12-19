import logging
from game import Game


def main():
    logging.basicConfig(level="INFO")
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
