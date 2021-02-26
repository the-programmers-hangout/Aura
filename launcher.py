import logging
import sys

from bot import Aura
from util.config import config

logging.basicConfig(
    level=config["logging"],
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    stream=sys.stdout,
)


def main():
    run_bot()
    pass


def run_bot():
    bot = Aura()
    bot.run()


if __name__ == '__main__':
    main()
