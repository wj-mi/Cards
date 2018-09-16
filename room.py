# -*- coding: utf-8 -*-

"""游戏主逻辑"""


import logging
from DZ.Cards_gen import card_gen
from DZ.DZ_roboot import Users


def game_start(pokers):
    """游戏开始，发牌，确认地主"""
    index = 0
    for user in Users:
        user.cards = pokers[index: index+18]
        index = index+18
        logging.info("{}'s cards: {}".format(user.name, user.cards))


def log_config():
    logging.basicConfig(level=logging.DEBUG,

                        format='%(levelname)s %(asctime)s %(message)s',

                        datefmt='%a, %d %b %Y %H:%M:%S',

                        filename='DZ.log',

                        filemode='w')


def write_log(user, msg, level="info"):
    """暂时写debug  和info 好了"""
    if level == "info":
        logging.info("{}: {}".format(user.name, msg))
    elif level == "debug":
        logging.debug("{}: {}".format(user.name, msg))


def game():
    """ """
    #  记录上家牌型 -1 则重新选择牌型出牌
    pre_type = -1
    for user in Users:
        pass


def main():
    log_config()
    logging.info("New Game start:")
    pokers, laizi = card_gen()
    logging.info("cards: {}".format(pokers))
    logging.info("laizi card: {}".format(laizi))
    # 发牌
    game_start(pokers)
    # 进入打牌
    game()


if __name__ == '__main__':
    main()
