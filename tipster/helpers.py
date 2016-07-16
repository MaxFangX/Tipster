from fractions import Fraction


def partition_integer_by_weights(integer, split):
    """
    Given an integer and a dictionary of strings and their corresponding weights,
    return a dictionary of their best fit integer partition, including the remainder

    >>> split = {'max': 4, 'philip': 3}
    >>> partition_integer_by_weights(16, **split)
    {'max': 9, 'philip': 6, 'remainder': 1}
    """

    total_weight = 0
    for _, value in split.iteritems():
        total_weight += value

    # Cannot divide by 0, so just put everything into the remainder
    if total_weight == 0:
        result = split.copy()
        result['remainder'] = integer
        return result

    result = {}
    for receiver, weight in split.iteritems():
        portion_of_total = Fraction(weight, total_weight)
        portion = int(integer * portion_of_total)
        result[receiver] = portion

    subtotal = 0
    for _, portion in result.iteritems():
        subtotal += portion

    remainder = integer - subtotal
    if remainder < 0:
        raise Exception("Remainder should never be less than zero")
    result['remainder'] = remainder

    return result
