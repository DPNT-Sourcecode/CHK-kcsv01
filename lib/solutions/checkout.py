# noinspection PyUnusedLocal
# skus = unicode string

# +------+-------+------------------------+
# | Item | Price | Special offers         |
# +------+-------+------------------------+
# | A    | 50    | 3A for 130, 5A for 200 |
# | B    | 30    | 2B for 45              |
# | C    | 20    |                        |
# | D    | 15    |                        |
# | E    | 40    | 2E get one B free      |
# +------+-------+------------------------+
from collections import Counter

PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
}


RULES = {
    "A": [3, 130],
    "B": [2, 45],
    "E": [2, "B"],
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


# def check_free_item(sku_item, qty, rule_values):



def calculate_price(sku_item, qty, rule_values, skus, skus_dict, special):
    if not sku_item and not qty and not rule_values:
        return None
    result = 0
    if special:
        rule_qty = rule_values[0]
        rule_price = rule_values[1]
        # quotient calculate price with specials if quotient > 1
        quotient = qty / rule_qty
        # remainder calculate price with normal prices
        remainder = qty % rule_qty
        if isinstance(rule_price, (int, long)):
            result += quotient * rule_price # special price
            result += remainder * PRICES.get(sku_item, 0)
        else:
            if str(rule_price) in skus:
                # only apply free item subtraction if there is enough qty in skus
                free_item_qty = skus_dict.get(rule_price, 0)
                sub = min(quotient, free_item_qty) * PRICES.get(rule_price, 0)
                result -= sub
            result += qty * PRICES.get(sku_item, 0)

        return result
    else:
        result += qty * PRICES.get(sku_item, 0)
        return result


def checkout(skus, case_sensitive_sku = True):
    """ Calculates skus price with special rules. Considers case sensitivity."""
    final_result = 0
    if not case_sensitive_sku:
        skus = skus.upper()

    if skus_is_valid(skus):
        skus_dict = group_count_skus(skus)
        for sku_item, qty in skus_dict.items():
            rule_values = RULES.get(sku_item, None)
            if rule_values:
                result = calculate_price(sku_item, qty, rule_values, skus, skus_dict, special=True,)
                final_result += result
            else:
                result = calculate_price(sku_item, qty, rule_values, skus, skus_dict, special=False)
                final_result += result
        return final_result
    else:
        return -1


if __name__ == '__main__':
    print("Expected: 250, got: {}".format(checkout("AAAEEEEB")))
    print("Expected: 265, got: {}".format(checkout("AAAEEEBB")))
    print("Expected: 210, got: {}".format(checkout("AAAEE")))
    print("Expected: 250, got: {}".format(checkout("AAAEEE")))
    print("Expected: 250, got: {}".format(checkout("AAAEEEB")))
    print("Expected: 210, got: {}".format(checkout("AAABEE")))
    print("Expected: 290, got: {}".format(checkout("AAABEEEE")))
    print("Expected: -1, got: {}".format(checkout("ABCa")))
    print("Expected: 210, got: {}".format(checkout("AAABBCD")))
    print("Expected: 20, got: {}".format(checkout("C")))
    print("Expected: 15, got: {}".format(checkout("D")))
    print("Expected: -1, got: {}".format(checkout("aaabb")))
    print("Expected: 175, got: {}".format(checkout("AAABB")))
    print("Expected: 130, got: {}".format(checkout("AAA")))
    print("Expected: 45, got: {}".format(checkout("BB")))
    print("Expected: -1, got: {}".format(checkout("fBB")))
