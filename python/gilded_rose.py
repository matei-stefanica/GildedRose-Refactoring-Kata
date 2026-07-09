# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        NORMAL_DECREASE = 1
        NORMAL_INCREASE = 1

        for item in self.items:
            match item.name:
                case "Aged Brie":
                    if item.quality < 50:
                        if item.sell_in > 0:
                            item.quality += NORMAL_INCREASE
                        else:
                            item.quality = min(50, item.quality + NORMAL_INCREASE * 2)
                case "Sulfuras, Hand of Ragnaros":
                    continue
                case "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in <= 0:
                        item.quality = 0
                    else:
                        if item.quality < 50:
                            if item.sell_in > 10:
                                item.quality += NORMAL_INCREASE
                            elif item.sell_in > 5:
                                item.quality = min(50, item.quality + 2)
                            elif item.sell_in > 0:
                                item.quality = min(50, item.quality + 3)
                case _:
                    if item.quality > 0:
                        if item.sell_in > 0:
                            item.quality -= NORMAL_DECREASE
                        else:
                            item.quality -= 2 * NORMAL_DECREASE
                
            item.sell_in -= 1            

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = max(min(quality, 50), 0)

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
