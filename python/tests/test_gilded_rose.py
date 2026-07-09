# -*- coding: utf-8 -*-
import unittest
from gilded_rose import ProductName
from gilded_rose import Item, GildedRose, BaseItem, BrieItem, TicketsItem, ConjuredItem, BadItem, MilkItem, SulfurasItem

class GildedRoseTest(unittest.TestCase):
    def test_name(self):
        items = [BaseItem(ProductName.BASE_ITEM, 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(ProductName.BASE_ITEM, items[0].name)

    def test_updated_properties_normal_item_before_selling(self):
        items = [BaseItem(ProductName.BASE_ITEM, 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

    def test_updated_properties_normal_item_after_sellin_expires(self):
        items = [BaseItem(ProductName.BASE_ITEM, 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(8, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_never_negative(self):
        items = [BaseItem(ProductName.BASE_ITEM, 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_increase_for_aged_brie_before_sellin(self):
        items = [BrieItem(ProductName.BRIE, 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(11, items[0].quality)
        self.assertEqual(0, items[0].sell_in)

    def test_quality_increase_for_aged_brie_after_sellin(self):
        items = [BrieItem(ProductName.BRIE, 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(22, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_not_greater_than_50(self):
        items = [BrieItem(ProductName.BRIE, 0, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_sulfuras_never_changes_properties(self):
        items = [SulfurasItem(ProductName.SULFURAS, 12, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(23, items[0].quality)
        self.assertEqual(12, items[0].sell_in)

    def test_backstage_passes_with_more_than_5_days_but_less_than_10(self):
        items = [TicketsItem(ProductName.TICKETS, 12, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(24, items[0].quality)
        self.assertEqual(11, items[0].sell_in)

    def test_backstage_passes_with_less_than_10_days(self):
        items = [TicketsItem(ProductName.TICKETS, 8, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(25, items[0].quality)
        self.assertEqual(7, items[0].sell_in)

    def test_backstage_passes_with_less_than_5_days(self):
        items = [TicketsItem(ProductName.TICKETS, 4, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(26, items[0].quality)
        self.assertEqual(3, items[0].sell_in)

    def test_backstage_passes_day_of_the_concert(self):
        items = [TicketsItem(ProductName.TICKETS, 0, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_backstage_passes_day_after_concert(self):
        items = [TicketsItem(ProductName.TICKETS, -2, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-3, items[0].sell_in)

    def test_repr(self):
        items = [BaseItem(ProductName.BASE_ITEM, 10, 10)]
        representation = items[0].__repr__()
        self.assertEqual(representation, str(ProductName.BASE_ITEM) + ", 10, 10")

    def test_initial_quality_cant_be_over_50(self):
        items = [BaseItem(ProductName.BASE_ITEM, 5, 58)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(49, items[0].quality)
        self.assertEqual(4, items[0].sell_in)

    def test_negative_sellin_from_the_start(self):
        items = [BaseItem(ProductName.BASE_ITEM, -3, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(18, items[0].quality)
        self.assertEqual(-4, items[0].sell_in)

    def test__brie_quality_upper_bound(self):
        items = [BrieItem(ProductName.BRIE, 0, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test__backstage_tickets_quality_uppber_bound(self):
        items = [TicketsItem(ProductName.TICKETS, 8, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
        self.assertEqual(7, items[0].sell_in)


    def test_quality_cant_be_negative_when_creating_the_object(self):
        items = [BaseItem(ProductName.BASE_ITEM, 20, -3)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(19, items[0].sell_in)

    def test_conjured_doubles_quality_decrease(self):
        items = [ConjuredItem(ProductName.CONJURED, 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(8, items[0].quality)
        self.assertEqual(4, items[0].sell_in)

    def test_bad_item(self):
        items = [BadItem(ProductName.BAD, 2, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].quality)
        self.assertEqual(1, items[0].sell_in)

    def test_bad_item_lower_bound(self):
        items = [BadItem(ProductName.BAD, 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        self.assertEqual(-10, items[0].quality)
        self.assertEqual(-6, items[0].sell_in)

    def test_milk_lower_bound(self):
        items = [MilkItem(ProductName.MILK, 0, 0)]
        gilded_rose = GildedRose(items)
        for i in range(30):
            gilded_rose.update_quality()
        self.assertEqual(-50, items[0].quality)
        self.assertEqual(-30, items[0].sell_in)
        
if __name__ == '__main__':
    unittest.main()