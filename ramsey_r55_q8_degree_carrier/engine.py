#!/usr/bin/env python3
"""One exact q8 marginal sweep; dictionary polynomial convolution."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb, factorial, isqrt
from pathlib import Path
import argparse, hashlib, json, time


@lru_cache(None)
def domain(left, right, root=False):
    # A forbidden five-set has a vertices on the left and 5-a on the right.
    forbidden = []
    for a in range(1, 5):
        b = 5-a
        for color in (0, 1):
            if (a >= 2 and left != color) or (b >= 2 and right != color):
                continue
            for rows in combinations(range(4), a):
                for cols in combinations(range(4), b):
                    mask = sum(1 << (4*i+j) for i in rows for j in cols)
                    forbidden.append((mask, mask if color else 0))
    states = []
    for word in range(1 << 16):
        if any(word & mask == value for mask, value in forbidden):
            continue
        if root:
            columns = [sum(((word >> (4*i+j)) & 1) << i for i in range(4))
                       for j in range(4)]
            if columns != sorted(columns, reverse=True):
                continue
        states.append(word)
    return tuple(states)


@lru_cache(None)
def spectrum(left, right, root, side, selected):
    out = Counter()
    for word in domain(left, right, root):
        if side == 0:
            values = [((word >> (4*i)) & 15).bit_count() for i in selected]
        else:
            values = [sum((word >> (4*i+j)) & 1 for i in range(4)) for j in selected]
        out[tuple(values)] += 1
    return out


def multiply(a, b):
    out = Counter()
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            out[i+k, j+l] += x*y
    return out


def block_marginal(r, block, selected):
    colors = [int(i < r) for i in range(8)]
    polynomials = []
    dimensions = []
    for other in range(8):
        if block == other:
            continue
        i, j = sorted((block, other))
        d = domain(colors[i], colors[j], i == 0)
        polynomials.append(spectrum(colors[i], colors[j], i == 0,
                                    int(block == j), selected))
        dimensions.append(len(d))
    words = range(15) if colors[block] else range(1, 16)
    star = Counter(tuple((word >> i) & 1 for i in selected) for word in words)
    polynomials.extend([star]*11)
    dimensions.extend([15]*11)
    poly = Counter({(0, 0): 1})
    for p in polynomials:
        poly = multiply(poly, p)
    fixed_degree = 3 * colors[block]
    accepted = sum(count for (i, j), count in poly.items()
                   if 18 <= fixed_degree+i <= 24 and 18 <= fixed_degree+j <= 24)
    total = 1
    for size in dimensions:
        total *= size
    if sum(poly.values()) != total:
        raise ValueError("marginal total mismatch")
    return {"selected": list(selected), "accepted": accepted, "total": total}


def core_marginal(r):
    poly = [1]
    for block in range(8):
        star = Counter(w.bit_count() for w in (range(15) if block < r else range(1,16)))
        out = [0]*(len(poly)+4)
        for i, count in enumerate(poly):
            for j, weight in star.items():
                out[i+j] += count*weight
        poly = out
    if sum(poly) != 15**8:
        raise ValueError("core marginal total mismatch")
    counts = [sum(poly[max(0,18-d):max(0,25-d)]) for d in range(11)]
    return {"accepted_by_fixed_degree": counts, "maximum": max(counts),
            "total": 15**8}


def per_core(r):
    a, b = r-1, 8-r
    return 1998**a * 1931**b * 37823**(comb(a,2)+comb(b,2)) * 35714**(a*b) * 15**88


def fraction(p):
    return {"numerator": p.numerator, "denominator": p.denominator}


def ordered_transfer(classes):
    rows = []
    carrier = 0
    bound = Fraction(0)
    for row in classes:
        r = row['r']; a, b = r-1, 8-r
        sequences = 1998**a * 1931**b
        multisets = comb(1998+a-1,a) * comb(1931+b-1,b)
        distinct = comb(1998,a) * comb(1931,b)
        orders = factorial(a)*factorial(b)
        rest, remainder = divmod(row['per_task_carrier'], sequences)
        if remainder:
            raise ValueError('nonintegral remaining carrier')
        selected = [x['best']['selected'] for x in row['blocks']]
        if (any(selected[i] != selected[1] for i in range(1,r)) or
                any(selected[i] != selected[r] for i in range(r,8))):
            raise ValueError('degree event not invariant under whole-block sorting')
        upper = Fraction(**row['probability_upper'])
        sorted_bound = upper*Fraction(sequences,orders*multisets) + Fraction(multisets-distinct,multisets)
        sorted_size = multisets*rest
        rows.append({'r':r,'root_sequences':sequences,'root_multisets':multisets,
                     'distinct_root_multisets':distinct,'label_orders':orders,
                     'remaining_coordinate_count':rest,'sorted_per_task_carrier':sorted_size,
                     'sorted_fraction_bound':fraction(sorted_bound),
                     'current_task_factor16':16*sorted_bound<=1})
        carrier += 546356*sorted_size
        bound += 546356*sorted_size*sorted_bound
    return {'source':'h3887','classes':rows,'sorted_q8_carrier':carrier,
            'sorted_retained_upper':fraction(bound),'declared_gate_factor16':16*bound<=carrier}


def calculate():
    result = []
    for r in range(5, 9):
        blocks = []
        p2 = Fraction(1)
        # Blocks of the same nonroot color have identical marginal families;
        # nonetheless instantiate all eight blocks, with explicit edge direction.
        for block in range(8):
            choices = [block_marginal(r, block, selected)
                       for selected in combinations(range(4),2)]
            best = min(choices, key=lambda x: Fraction(x["accepted"],x["total"]))
            p2 *= Fraction(best["accepted"], best["total"])
            blocks.append({"block": block, "choices": choices, "best": best})
        core = core_marginal(r)
        p2 *= Fraction(core["maximum"], core["total"])**11
        # Upper rational approximation is used only in the aggregate count.
        scale = 1 << 40
        bound = isqrt((p2.numerator*scale*scale)//p2.denominator)
        if bound*bound*p2.denominator < p2.numerator*scale*scale:
            bound += 1
        upper = Fraction(bound, scale)
        if upper*upper < p2:
            raise ValueError("invalid rational square-root upper bound")
        result.append({"r": r, "blocks": blocks, "core": core,
                       "probability_squared_upper": fraction(p2),
                       "probability_upper": fraction(upper),
                       "per_task_carrier": per_core(r),
                       "each_task_factor16": 256*p2.numerator <= p2.denominator})
        print(json.dumps({"r":r,"probability_upper_display_only":float(upper),
                          "each_task_factor16":result[-1]["each_task_factor16"]}), flush=True)
    carrier = 546356 * sum(row["per_task_carrier"] for row in result)
    upper_total = sum(546356*row["per_task_carrier"]*Fraction(**{
        "numerator":row["probability_upper"]["numerator"],
        "denominator":row["probability_upper"]["denominator"]}) for row in result)
    return {"q":8,"core_count":546356,"tasks":2185424,"classes":result,
            "carrier":carrier,"retained_upper_rational":fraction(upper_total),
            "parent_source":"h3873", "parent_factor16":16*upper_total <= carrier,
            "ordered_transfer":ordered_transfer(result),
            "new_q10_decisions":0,"new_q7r5_decisions":0}


def main():
    p=argparse.ArgumentParser();p.add_argument("out",type=Path);a=p.parse_args()
    start=time.monotonic();out=calculate()
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"declared_gate_factor16":out["ordered_transfer"]["declared_gate_factor16"],
                      "elapsed_seconds":time.monotonic()-start,
                      "carrier_bit_length":out["carrier"].bit_length()}),flush=True)


if __name__ == "__main__":
    main()
