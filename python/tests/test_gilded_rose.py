# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def update_item(self, name, sell_in, quality):
        item = Item(name, sell_in, quality)
        GildedRose([item]).update_quality()
        return item

    def test_normal_item_degrades_by_one_before_sell_by_date(self):
        item = self.update_item("Elixir of the Mongoose", 10, 20)

        self.assertEqual(9, item.sell_in)
        self.assertEqual(19, item.quality)

    def test_normal_item_degrades_by_two_after_sell_by_date(self):
        item = self.update_item("Elixir of the Mongoose", 0, 20)

        self.assertEqual(-1, item.sell_in)
        self.assertEqual(18, item.quality)

    def test_normal_item_quality_never_becomes_negative(self):
        item = self.update_item("Elixir of the Mongoose", 10, 0)

        self.assertEqual(0, item.quality)

    def test_aged_brie_increases_in_quality(self):
        item = self.update_item("Aged Brie", 10, 20)

        self.assertEqual(9, item.sell_in)
        self.assertEqual(21, item.quality)

    def test_aged_brie_increases_twice_after_sell_by_date(self):
        item = self.update_item("Aged Brie", 0, 20)

        self.assertEqual(-1, item.sell_in)
        self.assertEqual(22, item.quality)

    def test_quality_never_exceeds_fifty(self):
        items = [
            Item("Elixir of the Mongoose", 10, 50),
            Item("Aged Brie", 10, 50),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 49),
        ]

        GildedRose(items).update_quality()

        self.assertEqual(49, items[0].quality)
        self.assertEqual(50, items[1].quality)
        self.assertEqual(50, items[2].quality)

    def test_sulfuras_never_changes(self):
        item = self.update_item("Sulfuras, Hand of Ragnaros", 10, 80)

        self.assertEqual(10, item.sell_in)
        self.assertEqual(80, item.quality)

    def test_backstage_pass_increases_by_one_when_more_than_ten_days_remain(self):
        item = self.update_item(
            "Backstage passes to a TAFKAL80ETC concert", 11, 20
        )

        self.assertEqual(10, item.sell_in)
        self.assertEqual(21, item.quality)

    def test_backstage_pass_increases_by_two_with_ten_or_fewer_days_remaining(self):
        item = self.update_item(
            "Backstage passes to a TAFKAL80ETC concert", 10, 20
        )

        self.assertEqual(9, item.sell_in)
        self.assertEqual(22, item.quality)

    def test_backstage_pass_increases_by_three_with_five_or_fewer_days_remaining(self):
        item = self.update_item(
            "Backstage passes to a TAFKAL80ETC concert", 5, 20
        )

        self.assertEqual(4, item.sell_in)
        self.assertEqual(23, item.quality)

    def test_backstage_pass_quality_drops_to_zero_after_concert(self):
        item = self.update_item(
            "Backstage passes to a TAFKAL80ETC concert", 0, 20
        )

        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

if __name__ == '__main__':
    unittest.main()
