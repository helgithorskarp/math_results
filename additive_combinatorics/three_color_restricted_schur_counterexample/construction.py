"""Seven intervals and compact two-value extension witnesses; integer-only."""


def parameters(k):
    if type(k) is not int or k < 2:
        raise ValueError("k must be an integer at least 2")
    low = k * (k + 2)
    high = k * low
    first = high + k * k + k - 1
    stop = k * (k + 1) * (k + 2) - 2
    return low, high, first, stop


def coloring(k):
    """Return k, endpoint and inclusive [left, right, color] blocks."""
    low, high, first, stop = parameters(k)
    return {
        "k": k,
        "N": stop - 1,
        "blocks": [
            [1, k, 0],
            [k + 1, k * (k + 1), 1],
            [k * (k + 1) + 1, low - 1, 0],
            [low, high, 2],
            [high + 1, high + k - 1, 0],
            [high + k, first - 1, 1],
            [first, stop - 1, 0],
        ],
    }


def extension_witnesses(k, target):
    """Forbid blue and green on F..Q, and also red at Q.

    A term [value, multiplicity] denotes that many copies of the value.
    The target itself is prospective, so only summands are looked up.
    """
    low, _, first, stop = parameters(k)
    if type(target) is not int or not first <= target <= stop:
        raise ValueError("target must be an integer in [F,Q]")
    result = [
        {"color": 1, "terms": [[k + 1, k - 1],
                                [target - (k - 1) * (k + 1), 1]],
         "sum": target},
        {"color": 2, "terms": [[low, k - 1],
                                [target - (k - 1) * low, 1]],
         "sum": target},
    ]
    if target == stop:
        result.append({"color": 0, "terms": [[1, k - 1], [first, 1]],
                       "sum": target})
    return result
