# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items
        self.item_updater_factory = ItemUpdaterFactory()

    def update_quality(self):
        for item in self.items:
            self.item_updater_factory.create(item).update_quality()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemUpdater:
    def __init__(self, item):
        self.item = item

    def update_quality(self):
        raise NotImplementedError

    def decrease_quality(self, amount=1):
        self.item.quality = max(0, self.item.quality - amount)

    def increase_quality(self, amount=1):
        self.item.quality = min(50, self.item.quality + amount)


class NormalItem(ItemUpdater):
    def update_quality(self):
        self.decrease_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.decrease_quality()


class AgedBrie(ItemUpdater):
    def update_quality(self):
        self.increase_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.increase_quality()


class Sulfuras(ItemUpdater):
    def update_quality(self):
        pass


class BackstagePass(ItemUpdater):
    def update_quality(self):
        self.increase_quality()
        if self.item.sell_in < 11:
            self.increase_quality()
        if self.item.sell_in < 6:
            self.increase_quality()
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.item.quality = 0


class ConjuredItem(ItemUpdater):
    def update_quality(self):
        self.decrease_quality(2)
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.decrease_quality(2)


class ItemUpdaterFactory:
    def create(self, item):
        if item.name == "Aged Brie":
            return AgedBrie(item)
        if item.name == "Sulfuras, Hand of Ragnaros":
            return Sulfuras(item)
        if item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePass(item)
        if item.name.startswith("Conjured"):
            return ConjuredItem(item)
        return NormalItem(item)
