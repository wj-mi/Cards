# -*- coding:utf-8 -*-

"""
斗地主机器人：
    三个机器人，自动完成出牌。
    出牌规则：
        1 随机从一个机器人开始出牌。
        2 每次出牌，为第一个出牌时：选择手中牌 张数最多的牌型出，跟牌牌型和张数必须大于头家，且比头家大
    日志记录每一轮出牌
    # 0-12 黑２-A  0: 2       1: 3
    # 13-25 红２－Ａ  13: 2    14: 3
    # 26-38 梅２－a
    # 39-51 方２－Ａ
    # 52  小王
    # 53  大王
"""

from DZ.doudizhucardHelper import cardType


class Robot(object):
    """机器人"""
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.is_dz = False

    def get_cards(self, card):
        """拿牌程序"""
        self.cards.extend(card)

    def find_group(self):
        pass


    def choose_type(self, per_type=-1):
        """choose type of cards to out from handcards.
        return an list of cards
        """
        if per_type == -1:
            # find all group
            self.find_group()


Users = [Robot("robot1"), Robot("robot2"), Robot("robot3")]


if __name__ == '__main__':
    user = Robot("robot")
    user.cards = [0, 11, 50, 3, 23, 5, 31, 7, 53, 9, 48, 13, 24, 8, 12, 15, 16, 17]
    user.find_group()
