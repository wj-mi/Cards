# -*- coding:utf-8 -*-

"""生成一副扑克，并打乱顺序
    # 0-12 黑２-A  0: 2       1: 3
    # 13-25 红２－Ａ  13: 2    14: 3
    # 26-38 梅２－a
    # 39-51 方２－Ａ
    # 52  小王
    # 53  大王
"""

import random


KING = [52, 53]   # 大  小王


class Cards(object):
    cards = list(range(0, 54))

    def __init__(self):
        """洗牌：生成两个随机数，交换两个位置的牌30次"""
        self._num = 30
        for i in range(0, self._num):
            r1 = random.randrange(0, 54)
            r2 = random.randrange(0, 54)
            if r1 != r2:
                self.cards[r1], self.cards[r2] = self.cards[r2], self.cards[r1]
        laizi = random.randrange(0, 54)
        self.laizi = self.cards[laizi]


def card_gen():
    """生成一副乱序扑克返回， 第二个为本轮 癞子牌"""
    card = Cards()
    return card.cards, card.laizi


if __name__ == '__main__':
    for i in range(0, 10):
        card = Cards()
        print("--------"*4)
        print("card: {}".format(card.cards))
        print("Laizi card: {}".format(card.laizi if card.laizi in KING else card.laizi % 13))


