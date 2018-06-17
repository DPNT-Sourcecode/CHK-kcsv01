# noinspection PyUnusedLocal
# skus = unicode string

# +------+-------+----------------+
# | Item | Price | Special offers |
# +------+-------+----------------+
# | A    | 50    | 3A for 130     |
# | B    | 30    | 2B for 45      |
# | C    | 20    |                |
# | D    | 15    |                |
# +------+-------+----------------+
from collections import Counter

PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}


RULES = {
    "A": [3, 130],
    "B": [2, 45],
}


def skus_is_valid(skus):
    """ Validating skus input data. Items have to be in PRICES.
    """
    skus_dict = group_count_skus(skus)
    for sku_item, value in skus_dict.items():
        if not PRICES.get(sku_item, None):
            return False
    return True


def group_count_skus(skus):
    """ Returns key:value pairs from skus items. """
    return Counter(skus)


def checkout(skus):
    if skus_is_valid(skus):
        skus_dict = group_count_skus(skus)
        for sku_item, qty in skus_dict.items():
            rule_values = RULES.get(sku_item, None)


if __name__ == '__main__':
    print("Expected: 175, got: {}".format(checkout("AAABB")))
