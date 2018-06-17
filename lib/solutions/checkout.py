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
    "A": [[5, 200], [3, 130],],
    "B": [[2, 45],],
    "E": [[2, "B"],],
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



def calculate_price(sku_item, rule_values, skus, skus_dict, final_result, special):
    if not sku_item and not rule_values:
        return 0
    result = 0
    sku_item_qty = skus_dict.get(sku_item)
    sku_item_price = PRICES.get(sku_item)
    if special:
        for rule in rule_values:
            rule_qty = rule[0]
            if sku_item_qty >= rule_qty:
                rule_price = rule[1]
                if isinstance(rule_price, (int, long)):
                    quotient = sku_item_qty / rule_qty
                    # remainder = sku_item_qty % rule_qty
                    result += quotient * rule_price # special price
                    sku_item_qty = sku_item_qty - rule_qty * quotient
                else:
                    if str(rule_price) in skus:
                        # only apply free item subtraction if there is enough qty in skus
                        free_item_qty = skus_dict.get(rule_price, 0)
                        f_quotient = free_item_qty / rule_qty
                        rule_sku_qty = skus_dict.get(sku_item, 0)
                        f_remainder = free_item_qty - (f_quotient * rule_qty)
                        free_item_disc_price = RULES.get(rule_price, 0)[0][1]
                        sub_q = f_quotient * free_item_disc_price
                        sub_r = f_remainder * PRICES.get(rule_price, 0)
                        result -= sub_q + sub_r
                        # sku_item_qty = 0
                    ret_val = sku_item_qty * PRICES.get(sku_item, 0)
                    result += ret_val
                    # sku_item_qty = sku_item_qty - rule_qty
                    sku_item_qty = 0
        else:
            ret_val = sku_item_qty * sku_item_price
            result += ret_val
            return result
    else:
        ret_val = sku_item_qty * PRICES.get(sku_item, 0)
        result += ret_val
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
                result = calculate_price(sku_item, rule_values, skus, skus_dict, final_result, special=True,)
                final_result += result
            else:
                result = calculate_price(sku_item, rule_values, skus, skus_dict, final_result, special=False)
                final_result += result
        return final_result
    else:
        return -1


if __name__ == '__main__':
    print("Expected: 265, got: {}".format(checkout("AAAEEEBB")))
    print("Expected: 280, got: {}".format(checkout("ABCDEABCDE")))
    print("Expected: 145, got: {}".format(checkout("BEBEEE")))
    print("Expected: 200, got: {}".format(checkout("AAAAA")))
    print("Expected: 250, got: {}".format(checkout("AAAAAA")))
    print("Expected: 300, got: {}".format(checkout("AAAAAAA")))
    print("Expected: 290, got: {}".format(checkout("AAAEEEEB")))
    print("Expected: 160, got: {}".format(checkout("EEEEBB")))
    print("Expected: 160, got: {}".format(checkout("BEBEEE")))
    print("Expected: 400, got: {}".format(checkout("AAAAAAAAAA")))
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
