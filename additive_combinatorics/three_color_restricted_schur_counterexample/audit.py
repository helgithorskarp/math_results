"""Definition-level auditors, independent of the construction module.

No interval proof cases or endpoint formulas are imported or assumed.
All arithmetic uses Python arbitrary-precision integers.
"""

from bisect import bisect_left, bisect_right


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_coloring(record):
    require(type(record) is dict and set(record) == {"k", "N", "blocks"},
            "wrong coloring fields")
    k, endpoint, blocks = record["k"], record["N"], record["blocks"]
    require(type(k) is int and k >= 2, "invalid summand count")
    require(type(endpoint) is int and endpoint >= 1, "invalid endpoint")
    require(type(blocks) is list and bool(blocks), "missing blocks")
    next_integer = 1
    for block in blocks:
        require(type(block) is list and len(block) == 3, "bad block")
        lo, hi, color = block
        require(all(type(v) is int for v in block), "noninteger block")
        require(lo == next_integer and lo <= hi <= endpoint,
                "blocks must partition the integer interval in order")
        require(color in (0, 1, 2), "invalid color")
        next_integer = hi + 1
    require(next_integer == endpoint + 1, "incomplete partition")


def color_at(record, value):
    require(type(value) is int and 1 <= value <= record["N"],
            "summand outside coloring")
    for lo, hi, color in record["blocks"]:
        if lo <= value <= hi:
            return color
    raise ValueError("uncolored integer")


def expand(record):
    validate_coloring(record)
    return tuple(c for lo, hi, c in record["blocks"]
                 for _ in range(lo, hi + 1))


def nonconstant_sums(values, count, endpoint):
    """Bit s is set iff s<=endpoint is a nonconstant count-term sum.

    After processing distinct available values, dp[j][d] records all
    sums using j terms and min(2, number of used values)=d. For each new
    value use multiplicity 0..count-j. Each step reads only the previous
    table, so each value's total multiplicity is chosen exactly once.
    Positive summands justify discarding sums larger than endpoint.
    Constant and nonconstant representations can coexist in separate
    states; constant representations are never subtracted from totals.
    """
    require(type(count) is int and count >= 2, "bad count")
    require(type(endpoint) is int and endpoint >= 1, "bad endpoint")
    require(all(type(v) is int and v >= 1 for v in values), "bad values")
    require(len(set(values)) == len(values), "duplicate available values")
    mask = (1 << (endpoint + 1)) - 1
    dp = [[0, 0, 0] for _ in range(count + 1)]
    dp[0][0] = 1
    for value in sorted(values):
        previous = dp
        dp = [row[:] for row in previous]  # multiplicity zero
        for used in range(count):
            for distinct in range(3):
                bits = previous[used][distinct]
                if not bits:
                    continue
                for mult in range(1, min(count - used, endpoint // value) + 1):
                    dp[used + mult][min(2, distinct + 1)] |= (
                        bits << (mult * value)) & mask
    return dp[count][2]


def audit_nonconstant(record):
    colors = expand(record)
    summaries = []
    for color in range(3):
        values = [i for i, c in enumerate(colors, 1) if c == color]
        sums = nonconstant_sums(values, record["k"], record["N"])
        color_bits = sum(1 << v for v in values)
        require(not sums & color_bits, "monochromatic nonconstant sum")
        summaries.append(sums.bit_count())
    return summaries


def audit_two_values(record):
    """Enumerate same-color triples using an arithmetic progression test.

    For x<y, sums with exactly two values are k*x+b*(y-x), 1<=b<k.
    Search all same-color targets in that range and test divisibility.
    """
    colors = expand(record)
    k, endpoint = record["k"], record["N"]
    pairs = 0
    candidate_targets = 0
    for color in range(3):
        values = [i for i, c in enumerate(colors, 1) if c == color]
        for i, x in enumerate(values):
            for y in values[i + 1:]:
                lo, hi = (k - 1) * x + y, x + (k - 1) * y
                if lo > endpoint:
                    break
                pairs += 1
                left, right = bisect_left(values, lo), bisect_right(values, hi)
                for target in values[left:right]:
                    candidate_targets += 1
                    require((target - k * x) % (y - x) != 0,
                            "monochromatic two-value sum")
    return {"pairs": pairs, "candidate_targets": candidate_targets}


def audit_witness(record, witness, original_endpoint=None):
    """Check a two-value reason a prospective target cannot get a color.

    original_endpoint, when supplied, additionally requires that both
    summands belong to the original fixed prefix.
    """
    validate_coloring(record)
    require(type(witness) is dict and
            set(witness) == {"color", "terms", "sum"}, "bad witness fields")
    color, terms, target = witness["color"], witness["terms"], witness["sum"]
    require(type(color) is int and color in (0, 1, 2), "bad witness color")
    require(type(target) is int and 1 <= target <= record["N"] + 1,
            "bad witness target")
    require(type(terms) is list and len(terms) == 2, "not two terms")
    for term in terms:
        require(type(term) is list and len(term) == 2, "bad term")
        require(all(type(v) is int and v > 0 for v in term), "bad multiplicity")
    require(terms[0][0] < terms[1][0] < target, "summand distinctness/order")
    require(sum(mult for value, mult in terms) == record["k"], "wrong count")
    require(sum(value * mult for value, mult in terms) == target, "wrong sum")
    for value, mult in terms:
        require(color_at(record, value) == color, "wrong summand color")
        if original_endpoint is not None:
            require(type(original_endpoint) is int and value <= original_endpoint,
                    "summand beyond original prefix")
