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


def calculate_price(sku_item, qty, rule_values):
    result = 0
    if qty and rule_values:
        # quotient calculate price with specials if quotient > 1
        quotient = qty / rule_values[0]
        # remainder calculate price with normal prices
        remainder = qty % rule_values[0]
        result += quotient * rule_values[1] # special price
        result += remainder * PRICES.get(sku_item, None)
        return result
    return None


def checkout(skus):
    final_result = 0

    if skus_is_valid(skus):
        skus_dict = group_count_skus(skus)
        for sku_item, qty in skus_dict.items():
            rule_values = RULES.get(sku_item, None)
            if rule_values:
                result = calculate_price(sku_item, qty, rule_values)
                final_result += result
        return final_result
    else:
        return -1

if __name__ == '__main__':
    print("Expected: 175, got: {}".format(checkout("AAABB")))
    print("Expected: 130, got: {}".format(checkout("AAA")))
    print("Expected: 45, got: {}".format(checkout("BB")))
    print("Expected: -1, got: {}".format(checkout("fBB")))
