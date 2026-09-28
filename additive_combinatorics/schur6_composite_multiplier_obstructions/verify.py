#!/usr/bin/env python3
"""Verify finite evidence for the displayed composite-modulus arguments."""
import itertools
import json
import math
from pathlib import Path

import construct
import fibres
from check_witnesses import check
from fibres import require


def order(a, modulus):
    require(math.gcd(a,modulus) == 1, "nonunit")
    value, count = a % modulus, 1
    while value != 1:
        value = value*a % modulus
        count += 1
    return count


def arithmetic():
    for p in (7,11,269):
        require(all(p % d for d in range(2,math.isqrt(p)+1)), "nonprime factor")
    require(538 == 2*269 and 539 == 49*11, "factorization")
    units = {n:[a for a in range(1,n) if math.gcd(a,n) == 1] for n in (538,539)}
    orders = {n:{a:order(a,n) for a in values} for n,values in units.items()}
    require(len(units[538]) == 268 and len(units[539]) == 420, "unit-group size")
    require(orders[538][5] == 67 and orders[538][187] == 4, "orders at 538")
    h67 = {pow(5,j,269) for j in range(67)}
    require({1,23,24} <= h67 and 1+23 == 24, "order-67 orbit triple")
    require({a for a,o in orders[538].items() if o in (1,67)} ==
            {pow(5,j,538) for j in range(67)}, "unique order-67 subgroup")
    require(pow(187,2,538) == 537, "order-four square")
    require(orders[539][67] == 3 and 67 % 49 == 18 and 67 % 11 == 1, "order-three CRT")
    require((1+18+18**2) % 49 == 0, "order-three orbit identity")
    require(orders[539][344] == 5 and 344 % 49 == 1 and 344 % 11 == 3, "order-five CRT")
    require((1+3-pow(3,4,11)) % 11 == 0, "order-five orbit identity")
    involutions = [a for a in units[539] if orders[539][a] == 2]
    require(involutions == [197,342,538], "involution list")
    require(197 % 49 == 1 and 342 % 49 == 48, "axis action of involutions")
    h7 = {pow(78,j,539) for j in range(7)}
    require(orders[539][78] == 7 and len(h7) == 7, "order-seven subgroup")
    for prime, generator in [(3,67),(5,344),(7,78)]:
        require({a for a,o in orders[539].items() if o in (1,prime)} ==
                {pow(generator,j,539) for j in range(prime)}, "unique prime-order subgroup")
    for x in range(1,539):
        orbit = {h*x % 539 for h in h7}
        expected = {x} if x % 7 == 0 else {(x+77*j) % 539 for j in range(7)}
        require(orbit == expected, "wrong additive-fibre orbit")
    double_edges = {tuple(sorted((min(x,7-x), min(2*x % 7,7-2*x % 7))))
                    for x in range(1,7)}
    require(double_edges == {(1,2),(1,3),(2,3)}, "three distinct colours on Z/7 axis")
    ramsey = [1]
    for r in range(1,6):
        ramsey.append(r*ramsey[-1]+1)
    require(ramsey == [1,2,5,16,65,326], "triangle recurrence")
    return {"unit_group_orders":{str(n):len(v) for n,v in units.items()},
            "involutions_mod539":involutions, "order7_subgroup":sorted(h7),
            "ramsey_vertex_bounds":ramsey,
            "order67_triple_mod269":[1,23,24]}


def controls(rows):
    # Check the mask operation against literal residues on a deterministic
    # selection including empty, full and reflected subsets.
    masks = [0,1,2,3,15,31,85,341,683,1023,2047]
    for a,b in itertools.product(masks, repeat=2):
        direct = {(x+y)%11 for x in range(11) for y in range(11)
                  if a >> x & 1 and b >> y & 1}
        require(fibres.sumset(a,b) == sum(1 << z for z in direct), "sumset control")
    invalid = [dict(rows[0], word=rows[0]["word"][:-1]),
               dict(rows[0], word="1"+rows[0]["word"][1:]),
               {"name":"doubling_trap", "modulus":5, "colours":1,
                "multiplier":4, "permutation":[0], "word":"0000"}]
    for row in invalid:
        try:
            check(row)
        except ValueError:
            pass
        else:
            raise ValueError("invalid witness accepted")
    return {"literal_sumset_pairs":len(masks)**2, "invalid_witnesses_rejected":len(invalid)}


def run():
    directory = Path(__file__).resolve().parent
    rows = json.loads((directory/"witnesses.json").read_text())
    require(rows == construct.witnesses(), "construction differs from full witnesses")
    return {"status":"VERIFIED_COMPOSITE_MULTIPLIER_RESTRICTIONS",
            "arithmetic":arithmetic(), "fibre_certificate":fibres.run(),
            "witnesses":[check(row) for row in rows], "controls":controls(rows),
            "external_theorem":"Classical S(4)=44, used as stated in PROOF.md"}


if __name__ == "__main__":
    result = run()
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    require(result == expected, "recorded evidence changed")
    print(json.dumps(result, sort_keys=True, indent=2))
