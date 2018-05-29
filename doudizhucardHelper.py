# -*- coding:utf-8 -*-


C2SCardType = {1:3, 2:4, 3:5, 4:2, 5:8, 6:9, 7:6, 8:7 ,9:10, 10:1, 11:11, 12:12, 13:13, 14:14}
#S2CCardType = {2:4, 3:1, 4:2, 5:3, 6:7, 7:8, 8:5, 9:}
#public enum CardsType
#{
#    danzhang = 1, duizi, santiao, zhadan, lianpai, liandui, sandaiyi, sandaier, feiji, wangza, feijidaiyi, feijidaier, sidaier, sidaierdui
#}
C2SCard = [1,2,3,4,5,6,7,8,9,10,11,12,0,
            13*1+1, 13*1+2, 13*1+3, 13*1+4, 13*1+5, 13*1+6, 13*1+7, 13*1+8, 13*1+9, 13*1+10, 13*1+11, 13*1+12, 13*1+0,
            13*2+1,13*2+2,13*2+3,13*2+4,13*2+5,13*2+6,13*2+7,13*2+8,13*2+9,13*2+10,13*2+11,13*2+12,13*2+0,
            13*3+1,13*3+2,13*3+3,13*3+4,13*3+5,13*3+6,13*3+7,13*3+8,13*3+9,13*3+10,13*3+11,13*3+12,13*3+0,
            -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,52,53
        ]
S2CCard = [12, 0, 1,2,3,4,5,6,7,8,9,10,11,
            13*1+12, 13*1+0, 13*1+1,13*1+2,13*1+3,13*1+4,13*1+5,13*1+6,13*1+7,13*1+8,13*1+9,13*1+10,13*1+11,
            13*2+12, 13*2+0, 13*2+1,13*2+2,13*2+3,13*2+4,13*2+5,13*2+6,13*2+7,13*2+8,13*2+9,13*2+10,13*2+11,
            13*3+12, 13*3+0, 13*3+1,13*3+2,13*3+3,13*3+4,13*3+5,13*3+6,13*3+7,13*3+8,13*3+9,13*3+10,13*3+11,
            65, 66
        ]

# # 牌型： 只判断牌型

class cardType:
    NOTHING = 0  # 无法构成牌型
    ROCKET = 1  # 火箭：　双王，最大牌　１
    BOMB = 2    # 炸弹：四张数值相同的牌　２
    SINGLE = 3   # 单牌：　３
    DOUBLE = 4   # 对牌：　４
    THREE = 5    # 三张牌：　５
    THREE_ONE = 6   # 三带一：３n+1 or 3n+一对　６
    THREE_DOUBLE = 7

    SINGLE_SHUN = 8  # 单顺：五张或更多的连续单牌（不包括对２和双王）　７
    DOUBLE_SHUN = 9  # 双顺：三对或更多的连续对牌（不包括２点和双王）　８
    THREE_SHUN = 10  # 三顺：两个或更多的连续三张牌　９
    AIR_PLANE_SINGLE = 11
    AIR_PLANE_DOUBLE = 12  # 飞机带翅膀：三顺＋同等数量的单牌／对牌　   10
    FOUR_TWO_SIGLE = 13
    FOUR_TWO_DOUBLE = 14   # 四代二：４n+两手牌　　４n+3+7/4n+33+77　 11
# 牌型大小：火箭＞炸弹＞
# 单牌大小：大王＞小王＞２＞A>K>Q>J>10>9>8>7>6>5>4>3


# 0-12 黑２-A  0: 2       1: 3
# 13-25 红２－Ａ  13: 2    14: 3
# 26-38 梅２－a
# 39-51 方２－Ａ
# 52  小王
# 53  大王

"""
Q:
getCardType: 可能有几种牌型
"""

BIGKING = 53
LITTLEKING = 52
CARD_TWO = 0


def getCardType(cards, laizi):
    """给定cards,判断传过来的牌型
    [[牌型, 最大单张, 张数, 0/1(包含癞子)], ]
    """
    # 将cards全部转换为2-A
    print('-' * 20)
    print("origin card: {}, laizi: {}".format(cards, laizi))
    normal_cards = []
    for item in cards:
        card = item if item in [BIGKING, LITTLEKING] else item % 13
        normal_cards.append(card)
    print('normal_cards = {}'.format(normal_cards))
    laizi_card = laizi if laizi in [BIGKING, LITTLEKING] else laizi % 13
    return _judge_type(normal_cards, laizi_card)


def _judge_type(cards, laizi):
    """cards_len, laizi_count """
    type_list = []
    cards_len = len(cards)              # 牌的张数
    laizi_count = cards.count(laizi)    # 癞子牌张数
    if cards_len == 1:
        type_list.append([cardType.SINGLE, _find_max(cards), cards_len, laizi_count])
    elif cards_len == 2:
        if cards.count(cards[0]) == 2:  # duizi
            type_list.append([cardType.DOUBLE, _find_max(cards), cards_len, laizi_count])
        elif cards[0] in [BIGKING, LITTLEKING] and cards[1] in [BIGKING, LITTLEKING]:
            type_list.append([cardType.ROCKET, _find_max(cards), cards_len, laizi_count])
        elif laizi_count == 1:   # 有一个癞子牌,当且仅当另一个牌为除大小王之外的牌,可以构成对子
            single_card = [item for item in cards if item != laizi][0]
            if single_card not in [BIGKING, LITTLEKING]:
                type_list.append([cardType.DOUBLE, single_card, cards_len, laizi_count])
            else:
                type_list.append([cardType.NOTHING, _find_max(cards), cards_len, laizi_count])
        else:
            type_list.append([cardType.NOTHING, _find_max(cards), cards_len, laizi_count])
    elif cards_len == 3:
        _three_cards_judge(cards, laizi, type_list)
    elif cards_len == 4:
        _four_cards_judge(cards, laizi, type_list)
    elif cards_len == 5:
        _five_cards_judge(cards, laizi, type_list)
    else:
        _more_cards_judge(cards, laizi, type_list)
    return type_list


def _more_cards_judge(cards, laizi, type_list):
    """6张以上的牌判牌逻辑  4n+1+1, 2n+2+2, 单顺, 双顺, 333444, 333444+1+1, 333444+2n+2M"""
    cards_len = len(cards)
    laizi_count = cards.count(laizi)
    if laizi_count:
        _remove_types_of_card(cards, laizi, laizi_count)
    card_count = _card_counter(cards)  # 二维数组card_count[0, 1, 1, 0]  单牌:[0], 对子:[1] 三个:[1], 四个:[0]
    # 6张以上的牌若包含大小王,不构成任何牌型
    if BIGKING in cards or LITTLEKING in cards:
        type_list.append([cardType.NOTHING, _find_max(cards), cards_len, laizi_count])
        return

    # 依次考虑能否凑成可能牌型
    if not laizi_count:
        if len(card_count[3]) == 1:
            max_card = card_count[3][0]    # _find_card_by_count(cards, 4)
            # 4n+1+1
            if (len(card_count[0]) == 2 and len(card_count[1]) == len(card_count[2]) == 0) or \
                    (len(card_count[1]) == 1 and len(card_count[0]) == len(card_count[2]) == 0):
                type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])
            elif len(card_count[1]) == 2 and len(card_count[0]) == len(card_count[2]) == 0:  # 4n+2+2
                type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])

        # 33334444
        if len(card_count[3]) == 2:
            type_list.append([cardType.FOUR_TWO_DOUBLE, _find_max(card_count[3]), cards_len, laizi_count])

            if CARD_TWO not in cards and abs(card_count[3][0] - card_count[3][1]) == 1:
                type_list.append([cardType.AIR_PLANE_SINGLE, max(card_count[3]), cards_len, laizi_count])
        if CARD_TWO not in cards:

            if len(card_count[1]) == len(card_count[2]) == len(card_count[3]) == 0:  # 全是单牌,且不包含2
                _judge_single_shun_with_laizi(card_count[0], laizi_count, type_list, cards_len)

            _can_make_doubleshun(card_count, 0, type_list, cards_len)
            _can_make_shanshun(card_count, 0, type_list, cards_len)
        _air_and_chibang(card_count, laizi_count, type_list, cards_len)
        # # 飞机带翅膀
        # if len(card_count[2]) >= 2:
        #     plane_num = len(card_count[2])
        #     if _judge_lianxu(card_count[2]) == 0:
        #         max_card = _find_max(card_count[2])
        #         if len(card_count[0]) == plane_num:
        #             type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])
        #         elif len(card_count[1]) == plane_num and len(card_count[0]) == len(card_count[3]) == 0:
        #             type_list.append([cardType.AIR_PLANE_DOUBLE, max_card, cards_len, laizi_count])
    else:
        if laizi_count == 1:
            # 4n + 1+laizi
            if len(card_count[3]) == 1:  # 未考虑4n+2m
                max_card = card_count[3][0]
                if len(card_count[0]) == 1 and len(card_count[1]) == len(card_count[2]) == 0:  # 4n+1+laizi
                    type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])
                elif len(card_count[1]) == 1 and len(card_count[0]) == 1:  # 4n+2m+1+laizi
                    type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])
                # 4n+3m+laizi => 4n+2/3n+3m+1+1
                elif len(card_count[2]) == 1 and len(card_count[0]) == len(card_count[1]) == 0:
                    max_card = max_card if max_card > card_count[2][0] else card_count[2][0]
                    type_list.append([cardType.AIR_PLANE_DOUBLE, max_card, cards_len, laizi_count])
                    if CARD_TWO not in card_count[3]+card_count[2] and abs(card_count[3][0] - card_count[2][0])==1:
                        type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])
            if len(card_count[2]) == 1:    # 3n
                max_card = card_count[2][0]
                # 3n+ laizi+2m
                if len(card_count[1]) == 1 and len(card_count[0]) == len(card_count[3]) == 0:
                    type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])
                    if CARD_TWO not in card_count[2]+card_count[1] and abs(card_count[1][0] - card_count[2][0]) == 1:
                        max_card = card_count[1][0] if card_count[1][0] > card_count[2][0] else card_count[2][0]
                        type_list.append([cardType.THREE_SHUN, max_card, cards_len, laizi_count])
                elif len(card_count[0]) == 2 and len(card_count[1]) == len(card_count[3]) == 0:   # 3n+1+1+laizi
                    type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])
                elif len(card_count[1]) == 2 and len(card_count[0]) == len(card_count[3]) == 0:
                    type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])

            if CARD_TWO not in cards:
                # 全是单牌
                if len(card_count[1]) == len(card_count[2]) == len(card_count[3]) == 0:
                    _judge_single_shun_with_laizi(card_count[0], laizi_count, type_list, cards_len)
                _can_make_doubleshun(card_count, laizi_count, type_list, cards_len)
                _can_make_shanshun(card_count, laizi_count, type_list, cards_len)
            _air_and_chibang(card_count, laizi_count, type_list, cards_len)

        elif laizi_count == 2:
            # TODO 除开单双顺\飞机带翅膀,其余牌型采用穷举
            if len(card_count[3]) == 1:  # 4n
                max_card = card_count[3][0]
                if len(card_count[0]) == len(card_count[1]) == len(card_count[2]) == 0:  #4n+2laizi
                    type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])

                elif len(card_count[0]) == 2 and len(card_count[1]) == len(card_count[2]) == 0:
                    type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])
                    if CARD_TWO not in (max_card, card_count[0][0]) and abs(max_card - card_count[0][0]) == 1:
                        max_card = max_card if max_card > card_count[0][0] else card_count[0][0]
                        type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])
                    elif CARD_TWO not in (max_card, card_count[0][1]) and abs(max_card - card_count[0][1]) == 1:
                        max_card = max_card if max_card > card_count[0][1] else card_count[0][1]
                        type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])
                # 2laizi+4n+2m
                elif len(card_count[1]) == 1 and len(card_count[0]) == len(card_count[2]) == 0:
                    max_card = max_card if max_card > card_count[1][0] else card_count[1][0]
                    type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])
                    if CARD_TWO not in cards and abs(card_count[3][0] - card_count[1][0]) == 1:
                        type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])
            # 3n+3m
            elif len(card_count[2]) == 2 and len(card_count[0]) == len(card_count[1]) == len(card_count[3]) == 0:
                max_card = _find_max(card_count[2])
                type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])
                if CARD_TWO not in cards and abs(card_count[2][0] - card_count[2][1]) == 1:
                    type_list.append([cardType.THREE_ONE, max_card, cards_len, laizi_count])
            # 3n+2n+1+2laizi => 4n+2+2
            elif len(card_count[2]) == 1 and len(card_count[1]) == len(card_count[0]) == 1 and laizi_count == 2:
                type_list.append([cardType.FOUR_TWO_DOUBLE, card_count[2][0], cards_len, laizi_count])
            # 3n+1+2laizi  => 4+1+1
            elif len(card_count[2]) == 1 and len(card_count[0]) == 1 and len(card_count[1]) == len(card_count[3]) == 0:
                type_list.append([cardType.FOUR_TWO_SIGLE, card_count[2][0], cards_len, laizi_count])
            # 2n+2j+2k+2laizi  ==> 4带2对
            elif len(card_count[1]) == 3 and laizi_count == 2 and card_count[0] == card_count[2] == card_count[3]:
                max_card = _find_max(card_count[1])
                type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])
            # 2n+2k+2laizi ==> 4n+1+1 /
            elif len(card_count[1]) == 2 and len(card_count[0]) == len(card_count[2]) == len(card_count[3]) == 0:
                max_card = _find_max(card_count[1])
                type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])
            elif len(card_count[1]) == 1 and len(card_count[0]) == 2 and len(card_count[2]) == len(card_count[3]) == 0:
                type_list.append([cardType.FOUR_TWO_SIGLE, card_count[1][0], cards_len, laizi_count])

            if CARD_TWO not in cards:

                # 顺子判断
                card_set = set(cards)
                card_set = list(card_set)
                card_set_len = len(card_set)
                if len(card_count[1]) == len(card_count[2]) == len(card_count[3]) == 0:
                    _judge_single_shun_with_laizi(card_count[0], laizi_count, type_list, cards_len)
                _can_make_doubleshun(card_count, laizi_count, type_list, cards_len)
                _can_make_shanshun(card_count, laizi_count, type_list, cards_len)
            _air_and_chibang(card_count, laizi_count, type_list, cards_len)

        elif laizi_count == 3:  # 3个癞子
            # 判断4带两手牌的情况 1+1+1+3laizi/ 2n+1+1+3laizi   ,
            # 2+2+1+3laizi/4n+1+3laizi/3n+1+1+3laizi
            # 3liaiz+1+1+1
            if len(card_count[0]) == 3 and len(card_count[1]+card_count[2]+card_count[3]) == 0:
                max_card = max(card_count[0])
                type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])
                card_count[0] = sorted(card_count[0])
                if CARD_TWO not in card_count[0] and (card_count[0][-1] - card_count[0][0]) == 2:
                    type_list.append([cardType.DOUBLE_SHUN, max_card, cards_len, laizi_count])
            # 3laizi+1+2n
            elif len(card_count[0]) == 1 and len(card_count[1]) == 1 and len(card_count[2]+card_count[3]) == 0:
                max_card = _find_max(card_count[0]+card_count[1])
                type_list.append([cardType.FOUR_TWO_SIGLE, max_card, cards_len, laizi_count])

            # 2+2+1+3laizi
            elif len(card_count[0]) == 1 and len(card_count[1]) == 2 and len(card_count[2]) == len(card_count[3]) == 0:
                max_card = max(card_count[0]+card_count[1])
                type_list.append(cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count)
            # 1+4+3laizi
            elif len(card_count[0]) == 1 and len(card_count[3]) == 1 and len(card_count[1]) == len(card_count[2]) == 0:
                max_card = max(card_count[0]+card_count[3])
                type_list.append(cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count)
            # 3n+1+1+3laizi
            elif len(card_count[2]) == 1 and len(card_count[0]) == 2 and len(card_count[1]) == len(card_count[3]) == 0:
                type_list.append([cardType.FOUR_TWO_SIGLE, card_count[2][0], cards_len, laizi_count])

            # -------------开始判断顺子和飞机带翅膀等情况  TODO飞机带翅膀
            if CARD_TWO not in cards:
                # if _judge_lianxu(cards) <= laizi_count:   # 简单过滤 连续牌
                    # 单顺判断
                    # if len(card_count[1]) == len(card_count[2]) == len(card_count[3]) == 0:
                    #     new_cards = sorted(card_count[0])
                    #     cards_gap = new_cards[-1] - new_cards[0]
                    #     cards_gap_tmp = laizi_count + len(new_cards)-1 -cards_gap
                    #     max_card = 12 if new_cards[-1] >= 12 - cards_gap_tmp else new_cards[-1] + cards_gap_tmp
                    #
                    #     type_list.append([cardType.SINGLE_SHUN, max_card, cards_len, laizi_count])
                _judge_single_shun_with_laizi(card_count[0], laizi_count, type_list, cards_len)
                _can_make_doubleshun(card_count, laizi_count, type_list, cards_len)
                _can_make_shanshun(card_count, laizi_count, type_list, cards_len)
            _air_and_chibang(card_count, laizi_count, type_list, cards_len)
        elif laizi_count == 4:   #
            if len(card_count[3]) == 1 and len(card_count[0]) == len(card_count[1]) == len(card_count[2]) == 0:  # 4n+4laizi
                max_card = card_count[3][0] if card_count[3][0] > laizi else laizi
                type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])
                if abs(card_count[3][0] - laizi) == 1:
                    # max_card = card_count[3][0] if card_count[3][0] > laizi else laizi
                    type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])
            # 1+1+4laizi
            elif len(card_count[0]) == 2 and len(card_count[1]) == len(card_count[2]) == len(card_count[3]) == 0:
                type_list.append([cardType.FOUR_TWO_SIGLE, laizi, cards_len, laizi_count])
            # 2n+2m+ 4laizi
            elif len(card_count[1]) == 2 and len(card_count[0]) == len(card_count[2]) == len(card_count[3]) == 0:
                max_card = _find_max(card_count[1]+[laizi])
                type_list.append([cardType.FOUR_TWO_DOUBLE, max_card, cards_len, laizi_count])
                card_count[1] = sorted(card_count[1])
                max_gap = card_count[1][-1] - card_count[1][0]
                if max_gap == 1:
                    max_card = card_count[1][-1] if card_count[1][-1] > 11 else card_count[1][-1] + 1
                    type_list.append([cardType.THREE_SHUN, max_card, cards_len, laizi_count])
                elif max_gap == 2:
                    type_list.append([cardType.THREE_SHUN, max_card, cards_len, laizi_count])
            # ----- 顺子判断
            if CARD_TWO not in cards:

                if _judge_lianxu(cards) < laizi_count:  # 简单过滤 连续牌

                    _judge_single_shun_with_laizi(card_count[0], laizi_count, type_list, cards_len)
                    _can_make_doubleshun(card_count, laizi_count, type_list, cards_len)
                    _can_make_shanshun(card_count, laizi_count, type_list, cards_len)
            _air_and_chibang(card_count, laizi_count, type_list, cards_len)

    if not type_list:
        type_list.append([cardType.NOTHING, _find_max(cards), cards_len, laizi_count])


def _air_and_chibang(card_count, laizi_count, type_list, cards_len):
    """飞机带翅膀"""
    mix_cards = sorted(card_count[0] + card_count[1] + card_count[2] + card_count[3])
    mix_len = len(mix_cards)
    air_cards = []
    one_air = []
    for index in range(mix_len - 2, -1, -1):
        tmp_gap = mix_cards[index+1] - mix_cards[index]
        if tmp_gap == 1 or (tmp_gap == 2 and laizi_count >= 3):  # 存在癞子, 允许间隔1 或2(癞子补足)
            if mix_cards[index+1] in card_count[0] and laizi_count < 2:
                continue
            if not one_air:
                one_air.append(mix_cards[index+1])
                one_air.append(mix_cards[index])
            else:
                one_air.append(mix_cards[index])
        else:
            if one_air:
                air_cards.append(one_air)
            one_air = []
    if one_air:
        air_cards.append(one_air)
    print('------air_cards: {}'.format(air_cards))
    if air_cards:
        # air_cards_len = len(air_cards)
        sub_airs = []
        for one_air in air_cards:   # 每组飞机能否构成飞机带翅膀
            # 若2在构成飞机的牌中，则次不能构成飞机带翅膀
            if CARD_TWO in one_air:
                continue
            sub_air = _try_to_make_air_and_chibang(one_air, laizi_count, card_count, type_list, cards_len)
            if sub_air:
                sub_airs.append(sub_air)
        if sub_airs:
            for one_air in sub_airs:  # 每组飞机能否构成飞机带翅膀
                sub_air = _try_to_make_air_and_chibang(one_air, laizi_count, card_count, type_list, cards_len)


def _try_to_make_air_and_chibang(one_air, laizi_count, card_count, type_list, cards_len):
    sub_air = []
    one_air = sorted(one_air)
    one_air_len = len(one_air)

    # 去除所有癞子牌抵的牌
    more_laizi = laizi_count
    card_one = card_count[0][:]   # 备份原数据
    card_two = card_count[1][:]
    three_number_card = 0
    laizi_air = 0
    for index in range(one_air_len-2, -1, -1):
        if one_air[index+1] in card_one:
            more_laizi -= 2
            card_one.remove(one_air[index+1])
            # three_number_card += 1
        elif one_air[index+1] in card_two:
            more_laizi -= 1
            card_two.remove(one_air[index+1])
        elif one_air[index+1] in card_count[3]:
            card_one.append(one_air[index+1])
            # three_number_card += 1
        three_number_card += 1
        if one_air[index] in card_one:
            more_laizi -= 2
            card_one.remove(one_air[index])
            # three_number_card += 1
        elif one_air[index] in card_two:
            more_laizi -= 1
            card_two.remove(one_air[index])
        elif one_air[index] in card_count[3]:
            card_one.append(one_air[index])
            # three_number_card += 1
        three_number_card += 1
        if one_air[index+1] - one_air[index] == 2:
            more_laizi -= 3
            # air_len = air_len + 1    # 癞子抵一个飞机,飞机数量+1
            laizi_air += 1
            three_number_card += 1
        if more_laizi < 0:  # 若不能凑成飞机,从可能为飞机的列表中移除
            # air_cards.remove(one_air)
            if index == one_air_len-2:
                sub_air = one_air[: index+1]
            continue

        # 可能构成飞机
        else:
            # 除了构成飞机牌的其余牌
            more_cards = len(card_one) + len(card_two) * 2 + more_laizi

            if laizi_air:
                max_card = 12 if one_air[-1] >= 11 else one_air[-1] + 1
            else:
                max_card = one_air[-1]
            if three_number_card == more_cards + more_laizi:
                #
                type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])

            # 翅膀计算
            for one_card in card_count[2]:
                more_cards += 3 if one_card not in one_air else 0
            # more_cards 为除了构成飞机的所有牌
            if three_number_card == more_cards:  #
                type_list.append([cardType.AIR_PLANE_SINGLE, max_card, cards_len, laizi_count])
            # 飞机带双翅膀的情况
            two_chibang = len(card_two)
            for one_card in card_count[2]:
                if one_card not in one_air:
                    two_chibang += 1
                    card_one.append(one_card)
            if more_laizi == len(card_one):
                two_chibang += len(card_one)
            elif more_laizi - len(card_one) > 0 and (more_laizi - len(card_one)) % 2 == 0:
                two_chibang += len(card_one)
                two_chibang += (more_laizi-len(card_one)) / 2

            if three_number_card == two_chibang:
                type_list.append([cardType.AIR_PLANE_DOUBLE, max_card, cards_len, laizi_count])

            if three_number_card > 2 and more_cards < three_number_card:
                sub_air = one_air[: -1]
            continue

    return sub_air


def _can_make_doubleshun(card_count, laizi_count, type_list, cards_len):
    """存在癞子情况下判断能否构成双顺"""
    if len(card_count[2]) == len(card_count[3]) == 0:
        mix_cards = sorted(card_count[0] + card_count[1])
        mix_len = len(mix_cards)
        single_need_laizi = len(card_count[0])
        more_laizi = laizi_count - single_need_laizi
        if single_need_laizi < 0:
            return
        if mix_cards[-1] - mix_cards[0] <= mix_len - 1 + more_laizi/2:  # 连续
            if mix_cards[-1] - mix_cards[0] == mix_len - 1 + more_laizi/2:
                max_card = mix_cards[-1]
            else:
                more_laizi = mix_len - 1 + more_laizi/2 - (mix_cards[-1] - mix_cards[0])
                if more_laizi:
                    max_card = mix_cards[-1] + more_laizi if mix_cards[-1] + more_laizi <= 12 else 12
                else:
                    return
            type_list.append([cardType.DOUBLE_SHUN, max_card, cards_len, laizi_count])


def _can_make_shanshun(cards_count, laizi_count, type_list, cards_len):
    """存在癞子,判断能否构成三顺"""
    new_cards = sorted(cards_count[0]+cards_count[1]+cards_count[2]+cards_count[3])
    more_laizi = laizi_count - len(cards_count[0])*2 - len(cards_count[1])
    more_laizi += 1 if cards_count[3] else 0
    if more_laizi < 0:
        return
    if not new_cards:
        return
    new_cards_len = len(new_cards)
    max_gap = new_cards[-1] - new_cards[0]
    # if more_laizi >= 3 and max_gap <= new_cards_len - 1 + more_laizi/3:
    if (more_laizi >= 3 and max_gap == new_cards_len - 1 + more_laizi/3 and more_laizi - 3 == 0) or \
            (max_gap == new_cards_len - 1 and more_laizi == 0):  # lianxu
        max_card = new_cards[-1]
        type_list.append([cardType.THREE_SHUN, max_card, cards_len, laizi_count])
    elif max_gap == new_cards_len - 1 and more_laizi == 3:   # and more_laizi == 0:  # 三顺有剩余的癞子的
        # max_card = max(cards_count[2])
        tmp_gap = (new_cards_len-1+more_laizi/3) - max_gap
        max_card = 12 if new_cards[-1] >= 12 - tmp_gap else new_cards[-1] + tmp_gap
        type_list.append([cardType.THREE_SHUN, max_card, cards_len, laizi_count])


def _judge_lianxu(cards):
    card_set = set(cards)  # set 会对list排序
    card_set_list = sorted(list(card_set))
    card_set_len = len(card_set_list)
    return card_set_list[-1] - card_set_list[0] - (card_set_len - 1)


def _judge_single_can_be_shun_with_laizi(cards, laizi_count):
    """有癞子情况下嫩否构成单顺"""
    len_set_cards = len(cards)
    if CARD_TWO in cards or BIGKING in cards or LITTLEKING in cards:
        return False
    if cards[len_set_cards - 1] - cards[0] <= len_set_cards - 1 + laizi_count:
        return True


def _judge_single_shun_with_laizi(cards, laizi_count, type_list, cards_len):
    """有癞子情况下嫩否构成单顺"""
    len_set_cards = len(cards)
    cards = sorted(cards)
    if not cards or (len_set_cards +  laizi_count) < 5:
        return
    if cards[-1] - cards[0] <= len_set_cards - 1 + laizi_count:
        # find max_card
        if cards[-1] - cards[0] == len_set_cards - 1:  # 所有单牌连续
            if laizi_count:
                if cards[-1] < 12 - laizi_count:
                    max_card = cards[-1] + laizi_count
                else:
                    max_card = 12
            else:
                max_card = cards[-1]
        else:
            max_card = _find_max(cards)
        type_list.append([cardType.SINGLE_SHUN, max_card, cards_len, laizi_count])


def _five_cards_judge(cards, laizi, type_list):
    """五张牌判牌逻辑   1+2+3+4+5, 3n+2"""
    # 大小王在不能构成有效牌型
    cards_len = len(cards)
    laizi_count = cards.count(laizi)
    if laizi_count:
        _remove_types_of_card(cards, laizi, laizi_count)
    card_count = _card_counter(cards)  # 二维数组card_count[[0], [1], [1], [0]]  单牌:0, 对子:1 三个:1, 四个:0
    if BIGKING in cards or LITTLEKING in cards:
        type_list.append([cardType.NOTHING, _find_max(cards), cards_len, laizi_count])
        return
    # 此时的cards不包含癞子牌
    if len(card_count[1]) == len(card_count[2]) == len(card_count[3]) == 0 and CARD_TWO not in cards:   # 只有单牌
        _judge_single_shun_with_laizi(cards, laizi_count, type_list, cards_len)

    # 3n+2laizi, 3n+2m
    if len(card_count[2]) == 1 and (laizi_count == 2 or len(card_count[1]) == 1):
        max_card = card_count[2][0]  # _find_card_by_count(cards, 3)
        type_list.append([cardType.THREE_DOUBLE, max_card, cards_len, laizi_count])
    # 3n+1+laizi =>3n=2/4n+1
    elif len(card_count[2]) == 1 and len(card_count[0]) == 1 and laizi_count == 1:
        max_card = card_count[2][0]   # _find_card_by_count(cards, 3)
        type_list.append([cardType.THREE_DOUBLE, max_card, cards_len, laizi_count])
        # type_list.append([cardType.FOUR_TWO_SIGLE, max_card])
    elif len(card_count[1]) == 1 and laizi_count == 3:  # 3laizi+2n
        max_card = laizi if laizi > card_count[1][0] else card_count[1][0]
        type_list.append([cardType.THREE_DOUBLE, max_card, cards_len, laizi_count])
        # type_list.append([cardType.FOUR_TWO_SIGLE, card_count[1][0]])  # 4n+1

    elif len(card_count[1]) == 2 and laizi_count == 1:   # 2n+2m+laizi
        type_list.append([cardType.THREE_DOUBLE, _find_max(card_count[1]), cards_len, laizi_count])
    # 2+1+2laizi/3laizi+1+1
    elif len(card_count[1]) == 1 and laizi_count == 2 and len(card_count[0]) == 1:
        max_card = _find_max(card_count[1] + card_count[0])
        type_list.append([cardType.THREE_DOUBLE, max_card, cards_len, laizi_count])
        # type_list.append([cardType.FOUR_TWO_SIGLE, card_count[1][0]])

    elif laizi_count == 3 and len(card_count[0]) == 2:  # 2n+1+2laizi
        max_card = _find_max(card_count[0])
        type_list.append([cardType.THREE_DOUBLE, max_card, cards_len, laizi_count])
        # type_list.append([cardType.FOUR_TWO_SIGLE, max_card])
    elif laizi_count == 3 and len(card_count[1]) == 1:   # 3laizi+2
        max_card = laizi if laizi > card_count[1][0] else card_count[1][0]
        type_list.append([cardType.THREE_DOUBLE, max_card, cards_len, laizi_count])
        # type_list.append([cardType.FOUR_TWO_SIGLE, max_card])
    elif laizi_count == 4 and len(card_count[0]) == 1:
        max_card = laizi if laizi > card_count[0][0] else card_count[0][0]
        # type_list.append([cardType.FOUR_TWO_SIGLE, laizi])
        type_list.append([cardType.THREE_DOUBLE, max_card, cards_len, laizi_count])

    if not type_list:
        type_list.append([cardType.NOTHING, max(cards), cards_len, laizi_count])


def _four_cards_judge(cards, laizi, type_list):
    """四张牌判牌逻辑  maybe: 4n, 3n+1"""
    cards_len = len(cards)
    laizi_count = cards.count(laizi)
    if laizi_count:
        _remove_types_of_card(cards, laizi, laizi_count)
    card_count = _card_counter(cards)  # 四元数组card_count[0, 1, 1, 0]  单牌:0, 对子:1 三个:1, 四个:0
    if len(card_count[3]) == 1:   # 4n
        type_list.append([cardType.BOMB, cards[0], cards_len, laizi_count])
    elif len(card_count[2]) == 1 and (laizi_count == 1 or len(card_count[0]) == 1):   #3n+1, 3n+laizi
        max_card = card_count[2][0]    # _find_card_by_count(cards, 3)
        type_list.append([cardType.THREE_ONE, max_card, cards_len, laizi_count])
        if laizi_count == 1:
            type_list.append([cardType.BOMB, max_card, cards_len, laizi_count])
    elif len(card_count[1]) == 1 and laizi_count == 1 and len(card_count[0]) == 1:
        type_list.append([cardType.THREE_ONE, card_count[1][0], cards_len, laizi_count])
    elif len(card_count[1]) == 1 and laizi_count == 2:  # 2n+2laizi =>3n+1 or 4n
        two_number_card = card_count[1][0]  # _find_card_by_count(cards, 2)
        max_card = two_number_card if two_number_card > laizi else laizi
        type_list.append([cardType.THREE_ONE, max_card, cards_len, laizi_count])
        type_list.append([cardType.BOMB, two_number_card, cards_len, laizi_count])
    elif len(card_count[0]) == 1 and laizi_count == 3:
        max_card = laizi if laizi > card_count[0][0] else card_count[0][0]  # _find_card_by_count(cards, 1)
        type_list.append([cardType.THREE_ONE, max_card, cards_len, laizi_count])
        type_list.append([cardType.BOMB, card_count[0][0], cards_len, laizi_count])
    elif laizi_count == 4:
        type_list.append([cardType.BOMB, laizi, cards_len, laizi_count])
    elif len(card_count[0]) == 2 and laizi_count == 2:
        max_card = _find_max(card_count[0])
        type_list.append([cardType.THREE_ONE, max_card])
    else:
        type_list.append([cardType.NOTHING, _find_max(cards), cards_len, laizi_count])


def _three_cards_judge(cards, laizi, type_list):
    """三张牌判牌逻辑"""
    cards_len = len(cards)
    laizi_count = cards.count(laizi)
    if laizi_count:
        _remove_types_of_card(cards, laizi, laizi_count)
    card_count = _card_counter(cards)    # 四元数组card_count[0, 1, 1, 0]  单牌:0, 对子:1 三个:1, 四个:0
    # 一个三元组, 2n+laizi, 1+2laizi
    if len(card_count[2]) == 1 or (len(card_count[1]) == 1 and laizi_count == 1) or \
            (len(card_count[0]) == 1 and laizi_count == 2):
        if len(card_count[2]) == 1:
            max_card = cards[0]
        elif len(card_count[1]) == 1:
            max_card = card_count[1][0]  # _find_card_by_count(cards, 2)
        else:    # card_count[0] == 1:
            max_card = card_count[0][0]
        type_list.append([cardType.THREE, max_card, cards_len, laizi_count])
    elif laizi_count == 3:
        type_list.append([cardType.THREE, laizi, cards_len, laizi_count])
    else:
        type_list.append([cardType.NOTHING, _find_max(cards), cards_len, laizi_count])


def _find_card_by_count(cards, count):
    """找到cards中 有count个牌的card  """
    card_set = set(cards)
    for card in card_set:
        if cards.count(card) == count:
            return card


def _remove_types_of_card(cards, card, types):
    """从cards中remove cards types次"""
    for i in range(0, types):
        cards.remove(card)


def _card_counter(cards):
    # TODO 可优化为返回二维数组
    """计算有1, 2, 3, 4张牌对应的牌数量, cards 不包含癞子
    返回一个二维数组
    """
    cards_set = set(cards)
    card_count = [[], [], [], []]
    # one_card = two_card = three_card = four_card = 0
    for card in cards_set:
        count = cards.count(card)
        card_count[count-1].append(card)
    return card_count


def _find_max(cards):
    """ cards 中最大单张"""
    max_card = max(cards)
    if max_card in [BIGKING, LITTLEKING]:
        max_card = max_card
    elif CARD_TWO in cards:
        max_card = CARD_TWO
    return max_card


def compareCard(card_type1, card_type2):
    """
    :param card_type1: [牌型, 最大单张, 张数, 是否包含癞子]
    :param card_type2:
    :return:
    2: 牌型不能比较
    0: 相等
    -1: type1>type2
    1: type1<type2
    """
    result = ERROR = 2
    EQUAL = 0
    MAX = 1
    MIN = -1
    unnormal_type = [cardType.ROCKET, cardType.BOMB]
    ## 顺子，飞机带翅膀，四代二 牌型相同的基础上还要求张数相同
    special_card_type = [cardType.SINGLE_SHUN, cardType.DOUBLE_SHUN, cardType.THREE_SHUN,
                         cardType.AIR_PLANE_SINGLE, cardType.AIR_PLANE_DOUBLE, cardType.FOUR_TWO_SIGLE,
                         cardType.FOUR_TWO_DOUBLE]
    type1, type2 = card_type1[0], card_type2[0]
    if type1 == cardType.NOTHING or type2 == cardType.NOTHING:
        return ERROR

    if type1 != type2:
        # 牌型不相等,仅当其中一方为火箭或者炸弹时能比较
        if type1 in unnormal_type or type2 in unnormal_type:
            if type1 == cardType.ROCKET:
                return MIN
            elif type2 == cardType.ROCKET:
                return MAX
            if type2 == cardType.BOMB:
                result = MAX
            elif type1 == cardType.BOMB:
                result = MIN
        else:
            result = ERROR
    else:   # 牌型相等
        if type1 == cardType.BOMB:   # 炸弹判断 先判断级别，在判断大小
            if card_type1[-1] == 0 and card_type2[-1] != 0:
                # 纯癞子＞硬炸弹＞软炸弹
                result = MIN if card_type2[-1] != 4 else MAX   # card2软炸蛋
            elif card_type1[-1] != 0 and card_type2[-1] == 0:
                result = MAX if card_type1[-1] != 4 else MIN   # CARD1[-1] >0 <4 软炸蛋
            elif card_type1[-1] == 4 or card_type2[-1] == 4:
                result = MIN if card_type1[-1] == 4 else MAX
            else:  # 要么都没有癞子，要么都有癞子 判断大小
                if card_type1[1] == card_type2[1]:
                    #  两个都是软炸弹，大小相等
                    result = EQUAL
                else:
                    # result = MAX if card_type1[1] > card_type2[1] else MIN
                    max_card = _find_max([card_type1[1], card_type2[1]])
                    result = MIN if max_card == card_type1[1] else MAX

        # 顺子，飞机带翅膀，四代二 牌型相同的基础上还要求张数相同
        else:    #  type1 in special_card_type:
            # 首先判断张数是否相同
            if card_type1[2] != card_type2[2]:
                result = ERROR
            else:
                if card_type1[1] == card_type2[1]:
                    result = EQUAL
                else:
                    max_card = _find_max([card_type1[1], card_type2[1]])
                    result = MAX if max_card == card_type2[1] else MIN
                    # result = MAX if card_type1[1] > card_type2[1] else MIN

        # 剩余牌型只用判断大小 单牌，对子，　三条，　三带一，三代二
    return result


def test():
    card1 = [0]
    card2 = [12, 12, 12, 1]
    cardType1 = getCardType(card1, 1)
    cardType2 = getCardType(card2, 1)
    print(compareCard(cardType1[0], cardType2[1]))


if __name__ == '__main__':
    cards = [
        # [9, 9, 9, 10, 10, 4, 6, 6],
        # [1, 2, 3, 4, 5],
        # [0, 4, 4],
        # [1, 1, 2, 2, 3, 3],
        # [6, 7, 8, 9, 10, 12, 5],
        # [0, 0],
        # [8],
        # [2, 3, 4, 5, 1, 7, 8, 9, 10],
        # [2, 2, 4, 4, 6, 6, 12, 12],
        # [8, 9, 9, 10, 10, 10, 5, 5],
        # [1, 14, 27, 2, 15, 29, 10, 12],
        # [2,2,2,3,3,4,10, 12],
        # [1, 2, 3, 4, 5, 6, 7, 7, 7, 10, 11, 12],
        # [15, 41, 18, 16, 42, 5, 17, 45],
        # [29, 3, 18, 5, 21, 8],
        #[2, 2, 2, 3, 3, 4, 4, 4, 5],
        # [10, 10, 12, 5, 1, 1],
        [0, 0, 8, 8, 9, 9, 9, 12, 12, 6],
        [2, 2, 3, 3, 3, 5, 5, 4, 4, 6],
        [1, 1, 1, 1, 2, 2, 2, 3, 3, 6],
        [15, 41, 18, 16, 42, 5, 17, 45]

    ]
    laizi = 6
    for card in cards:
        card_type = getCardType(card, laizi)
        print("card type: {}".format(card_type))
    # test()

