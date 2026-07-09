from enum import StrEnum

BASE_DECREASE = -1
BASE_INCREASE = 1
MILK_DECAYING_FACTOR = 1.1
BASE_UPPER_QUALITY_BOUND = 50
BASE_LOWER_QUALITY_BOUND = 0
BRIE_DECAY_MULTIPLIER = 2
TICKETS_FIRST_INCREASE_THRESHOLD = 10
TICKETS_SECOND_INCREASE_THRESHOLD = 5
TICKETS_FIRST_QUALITY_MODIFIER = 2
TICKETS_SECOND_QUALITY_MODIFIER = 3
CONJURED_MULTIPLIER = 2
PAST_SELLIN_MULTIPLIER = 2
DAILY_DECREMENT = 1
BAD_ITEM_LOWER_BOUND = -10
MILK_LOWER_BOUND = -50

class ProductName(StrEnum):
    BASE_ITEM = "greatItem"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    BRIE = "Aged Brie"
    TICKETS = "Backstage passes to a TAFKAL80ETC concert"
    CONJURED = "Conjured"
    BAD = "Bad Item"
    MILK = "Milk"

class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            match item.name:
                case "Aged Brie":
                    if item.quality < BASE_UPPER_QUALITY_BOUND:
                        if item.sell_in > BASE_LOWER_QUALITY_BOUND:
                            item.modify_quality(BASE_INCREASE)
                        else:
                            item.modify_quality(BRIE_DECAY_MULTIPLIER * BASE_INCREASE)
                case "Sulfuras, Hand of Ragnaros":
                    continue
                case "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in <= BASE_LOWER_QUALITY_BOUND:
                        item.quality = BASE_LOWER_QUALITY_BOUND
                    else:
                        if item.quality < BASE_UPPER_QUALITY_BOUND:
                            if item.sell_in > TICKETS_FIRST_INCREASE_THRESHOLD:
                                item.modify_quality(BASE_INCREASE)
                            elif item.sell_in > TICKETS_SECOND_INCREASE_THRESHOLD:
                                item.modify_quality(TICKETS_FIRST_QUALITY_MODIFIER)
                            elif item.sell_in > BASE_LOWER_QUALITY_BOUND:
                                item.modify_quality(TICKETS_SECOND_QUALITY_MODIFIER)
                case "Conjured":
                    if item.sell_in > BASE_LOWER_QUALITY_BOUND:
                        item.modify_quality(CONJURED_MULTIPLIER * BASE_DECREASE)
                    else:
                        item.modify_quality(CONJURED_MULTIPLIER * PAST_SELLIN_MULTIPLIER * BASE_DECREASE)
                case "Bad Item":
                    if item.sell_in > BASE_LOWER_QUALITY_BOUND:
                        item.modify_quality(BASE_DECREASE)
                    else:
                        item.modify_quality(PAST_SELLIN_MULTIPLIER * BASE_DECREASE)
                    item.bound_quality_custom(BAD_ITEM_LOWER_BOUND, BASE_UPPER_QUALITY_BOUND)
                    item.sell_in -= DAILY_DECREMENT   
                    continue
                case "Milk":
                    if item.sell_in > BASE_LOWER_QUALITY_BOUND:
                        item.modify_quality(BASE_DECREASE)
                    else:
                        item.quality -= int(-BASE_DECREASE * pow(MILK_DECAYING_FACTOR, abs(item.sell_in)))
                    item.bound_quality_custom(MILK_LOWER_BOUND, BASE_UPPER_QUALITY_BOUND)
                    item.sell_in -= DAILY_DECREMENT   
                    continue
                case _:
                    if item.quality > BASE_LOWER_QUALITY_BOUND:
                        if item.sell_in > BASE_LOWER_QUALITY_BOUND:
                            item.modify_quality(BASE_DECREASE)
                        else:
                            item.modify_quality(PAST_SELLIN_MULTIPLIER * BASE_DECREASE)
            item.bound_quality_custom(BASE_LOWER_QUALITY_BOUND, BASE_UPPER_QUALITY_BOUND)
            item.sell_in -= DAILY_DECREMENT   

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality
        self.bound_quality_custom(BASE_LOWER_QUALITY_BOUND, BASE_UPPER_QUALITY_BOUND)

    def bound_quality_custom(self, lowerBound, upperBound):
        if self.quality < lowerBound:
            self.quality = lowerBound
        if self.quality > upperBound:
            self.quality = upperBound

    def modify_quality(self, value):
        self.quality += value

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
