# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

normal_item = "greatItem"
sulfuras = "Sulfuras, Hand of Ragnaros"
brie = "Aged Brie"
tickets = "Backstage passes to a TAFKAL80ETC concert"


class GildedRoseTest(unittest.TestCase):
    def test_name(self):
        items = [Item(normal_item, 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(normal_item, items[0].name)

    def test_updated_properties_normal_item(self):
        items = [Item(normal_item, 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(normal_item, items[0].name)
        self.assertEqual(9, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

    def test_updated_properties_normal_item_after_sellin_expires(self):
        items = [Item(normal_item, 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(normal_item, items[0].name)
        self.assertEqual(8, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_never_negative(self):
        items = [Item(normal_item, 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(normal_item, items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_increase_for_aged_brie_before_sellin(self):
        items = [Item(brie, 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(brie, items[0].name)
        self.assertEqual(11, items[0].quality)
        self.assertEqual(0, items[0].sell_in)

    def test_quality_increase_for_aged_brie_after_sellin(self):
        items = [Item(brie, 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(brie, items[0].name)
        self.assertEqual(22, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_quality_not_greater_than_50(self):
        items = [Item(brie, 0, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(brie, items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_sulfuras_never_changes_properties(self):
        items = [Item(sulfuras, 12, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(sulfuras, items[0].name)
        self.assertEqual(23, items[0].quality)
        self.assertEqual(12, items[0].sell_in)

    def test_backstage_passes_with_more_than_10_days_but_more_than_5(self):
        items = [Item(tickets, 12, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(tickets, items[0].name)
        self.assertEqual(24, items[0].quality)
        self.assertEqual(11, items[0].sell_in)

    def test_backstage_passes_with_less_than_10_days(self):
        items = [Item(tickets, 8, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(tickets, items[0].name)
        self.assertEqual(25, items[0].quality)
        self.assertEqual(7, items[0].sell_in)

    def test_backstage_passes_with_less_than_5_days(self):
        items = [Item(tickets, 4, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(tickets, items[0].name)
        self.assertEqual(26, items[0].quality)
        self.assertEqual(3, items[0].sell_in)

    def test_backstage_passes_day_of_the_concert(self):
        items = [Item(tickets, 0, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(tickets, items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_backstage_passes_day_after_concert(self):
        items = [Item(tickets, -2, 23)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(tickets, items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-3, items[0].sell_in)

    def test_repr(self):
        items = [Item(normal_item, 10, 10)]
        representation = items[0].__repr__()
        self.assertEqual(representation, normal_item + ", 10, 10")

    def test_initial_quality_cant_be_over_50(self):
        items = [Item(normal_item, 5, 58)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(normal_item, items[0].name)
        self.assertEqual(49, items[0].quality)
        self.assertEqual(4, items[0].sell_in)

    def test_negative_sellin_from_the_start(self):
        items = [Item(normal_item, -3, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(normal_item, items[0].name)
        self.assertEqual(18, items[0].quality)
        self.assertEqual(-4, items[0].sell_in)

    def test__brie_quality_not_greater_than_50_if_it_starts_from_49_and_its_after_sellin_date(self):
        items = [Item(brie, 0, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(brie, items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test__backstage_tickets_quality_not_greater_than_50_if_it_starts_from_49_and_there_are_less_than_10_days_but_more_than_5(self):
        items = [Item(tickets, 8, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(tickets, items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(7, items[0].sell_in)

    def test__backstage_tickets_quality_not_greater_than_50_if_it_starts_from_49_and_there_are_less_than_5_days_left(self):
        items = [Item(tickets, 2, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(tickets, items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(1, items[0].sell_in)
        
if __name__ == '__main__':
    unittest.main()