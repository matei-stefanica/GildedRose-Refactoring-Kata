from enum import StrEnum
from abc import abstractmethod, ABC

BASE_DECREASE = -1
BASE_INCREASE = 1
MILK_DECAYING_FACTOR = 1.1
BASE_UPPER_QUALITY_BOUND = 50
BASE_LOWER_QUALITY_BOUND = 0
BRIE_DEVELOPMENT_FACTOR = 2
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
            item.update()

class Item(ABC):
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality
        self.bound_quality_custom(BASE_LOWER_QUALITY_BOUND, BASE_UPPER_QUALITY_BOUND)

    def bound_quality_custom(self, lowerBound, upperBound):
        self.quality = min(upperBound, max(self.quality, lowerBound))

    def modify_quality(self, value):
        self.quality += value

    @abstractmethod
    def update():
        pass

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class BaseItem(Item):
    def update(self):
        if self.sell_in > BASE_LOWER_QUALITY_BOUND:
            self.modify_quality(BASE_DECREASE)
        else:
            self.modify_quality(PAST_SELLIN_MULTIPLIER * BASE_DECREASE)
        self.bound_quality_custom(BASE_LOWER_QUALITY_BOUND, BASE_UPPER_QUALITY_BOUND)
        self.sell_in -= DAILY_DECREMENT

class BrieItem(Item):
    def update(self):
        if self.sell_in > BASE_LOWER_QUALITY_BOUND:
            self.modify_quality(BASE_INCREASE)
        else:
            self.modify_quality(BRIE_DEVELOPMENT_FACTOR * BASE_INCREASE)
        self.bound_quality_custom(BASE_LOWER_QUALITY_BOUND, BASE_UPPER_QUALITY_BOUND)
        self.sell_in -= DAILY_DECREMENT

class TicketsItem(Item):    
    def update(self):
        if self.sell_in <= BASE_LOWER_QUALITY_BOUND:
            self.quality = BASE_LOWER_QUALITY_BOUND
        else:
            if self.sell_in > TICKETS_FIRST_INCREASE_THRESHOLD:
                self.modify_quality(BASE_INCREASE)
            elif self.sell_in > TICKETS_SECOND_INCREASE_THRESHOLD:
                self.modify_quality(TICKETS_FIRST_QUALITY_MODIFIER)
            elif self.sell_in > BASE_LOWER_QUALITY_BOUND:
                self.modify_quality(TICKETS_SECOND_QUALITY_MODIFIER)
        self.bound_quality_custom(BASE_LOWER_QUALITY_BOUND, BASE_UPPER_QUALITY_BOUND)
        self.sell_in -= DAILY_DECREMENT

class ConjuredItem(Item):
    
    def update(self):
        if self.sell_in > BASE_LOWER_QUALITY_BOUND:
            self.modify_quality(CONJURED_MULTIPLIER * BASE_DECREASE)
        else:
            self.modify_quality(CONJURED_MULTIPLIER * PAST_SELLIN_MULTIPLIER * BASE_DECREASE)
        self.bound_quality_custom(BASE_LOWER_QUALITY_BOUND, BASE_UPPER_QUALITY_BOUND)
        self.sell_in -= DAILY_DECREMENT

class BadItem(Item):
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
        self.bound_quality_custom(BAD_ITEM_LOWER_BOUND, BASE_UPPER_QUALITY_BOUND)

    def update(self):
        if self.sell_in > BASE_LOWER_QUALITY_BOUND:
            self.modify_quality(BASE_DECREASE)
        else:
            self.modify_quality(PAST_SELLIN_MULTIPLIER * BASE_DECREASE)
        self.bound_quality_custom(BAD_ITEM_LOWER_BOUND, BASE_UPPER_QUALITY_BOUND)
        self.sell_in -= DAILY_DECREMENT

class MilkItem(Item):
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
        self.bound_quality_custom(MILK_LOWER_BOUND, BASE_UPPER_QUALITY_BOUND)

    def update(self):
        if self.sell_in > BASE_LOWER_QUALITY_BOUND:
            self.modify_quality(BASE_DECREASE)
        else:
            self.quality -= int(-BASE_DECREASE * pow(MILK_DECAYING_FACTOR, abs(self.sell_in)))
        self.bound_quality_custom(MILK_LOWER_BOUND, BASE_UPPER_QUALITY_BOUND)
        self.sell_in -= DAILY_DECREMENT

class SulfurasItem(Item):
    def update(self):
        pass
