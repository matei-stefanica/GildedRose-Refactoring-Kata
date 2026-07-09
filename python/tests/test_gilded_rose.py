# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_name(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)

    def test_updated_properties_normal_item(self):
        items = [Item("foo", 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(9, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

    def test_updated_properties_normal_item_after_sellin_expires(self):
        items = [Item("foo", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(8, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_never_negative(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_increase_for_aged_brie_after_sellin(self):
        items = [Item("Aged Brie", 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", items[0].name)
        self.assertEqual(22, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_increase_for_aged_brie_before_sellin(self):
        items = [Item("Aged Brie", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", items[0].name)
        self.assertEqual(11, items[0].quality)
        self.assertEqual(0, items[0].sell_in)

    #Obs: the gilded rose constructor does not check from the begining if an item
    # has a quality > 50
    def test_quality_not_greater_than_50(self):
        items = [Item("Aged Brie", 0, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_sulfuras_never_changes_properties(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 12, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Sulfuras, Hand of Ragnaros", items[0].name)
        self.assertEqual(23, items[0].quality)
        self.assertEqual(12, items[0].sell_in)

    def test_backstage_passes_with_more_than_10_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 12, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(24, items[0].quality)
        self.assertEqual(11, items[0].sell_in)

    def test_backstage_passes_with_less_than_10_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 8, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(25, items[0].quality)
        self.assertEqual(7, items[0].sell_in)

    def test_backstage_passes_with_less_than_5_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 4, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(26, items[0].quality)
        self.assertEqual(3, items[0].sell_in)

    def test_backstage_passes_day_of_the_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_backstage_passes_day_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", -2, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-3, items[0].sell_in)

    def test_repr(self):
        items = [Item("foo", 10, 10)]
        representation = items[0].__repr__()
        self.assertEqual(representation, "foo, 10, 10")

    
        
if __name__ == '__main__':
    unittest.main()