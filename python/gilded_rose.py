# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        BASE_DECREASE = 1
        BASE_INCREASE = 1
        MILK_DECAYING_FACTOR = 1.1

        for item in self.items:
            match item.name:
                case "Aged Brie":
                    if item.quality < 50:
                        if item.sell_in > 0:
                            item.quality += BASE_INCREASE
                        else:
                            item.quality = item.quality + BASE_INCREASE * 2
                case "Sulfuras, Hand of Ragnaros":
                    continue
                case "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in <= 0:
                        item.quality = 0
                    else:
                        if item.quality < 50:
                            if item.sell_in > 10:
                                item.quality += BASE_INCREASE
                            elif item.sell_in > 5:
                                item.quality = item.quality + 2
                            elif item.sell_in > 0:
                                item.quality = item.quality + 3
                case "Conjured":
                    if item.sell_in > 0:
                        item.quality -= 2 * BASE_DECREASE
                    else:
                        item.quality -= 4 * BASE_DECREASE
                case "Bad Item":
                    if item.sell_in > 0:
                        item.quality -= BASE_DECREASE
                    else:
                        item.quality -= 2 * BASE_DECREASE
                    item.bound_quality_custom(-10, 50)
                    item.sell_in -= 1   
                    continue
                case "Milk":
                    if item.sell_in > 0:
                        item.quality -= BASE_DECREASE
                    else:
                        item.quality -= int(BASE_DECREASE * pow(MILK_DECAYING_FACTOR, abs(item.sell_in)))
                    item.bound_quality_custom(-50, 50)
                    item.sell_in -= 1   
                    continue
                case _:
                    if item.quality > 0:
                        if item.sell_in > 0:
                            item.quality -= BASE_DECREASE
                        else:
                            item.quality -= 2 * BASE_DECREASE
            item.bound_quality()
            item.sell_in -= 1   

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality
        self.bound_quality()

    def bound_quality(self):
        if self.quality < 0:
            self.quality = 0
        if self.quality > 50:
            self.quality = 50

    def bound_quality_custom(self, lowerBound, upperBound):
        if self.quality < lowerBound:
            self.quality = lowerBound
        if self.quality > upperBound:
            self.quality = upperBound

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
