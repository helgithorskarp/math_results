#!/usr/bin/env python3
"""Verify the finite class evidence and compare alternate exact histograms.

This checks the finite arithmetic, not CFSG, the completeness proof, the
outer-automorphism premises, or correctness of GAP's group representations.
"""
from collections import Counter
from fractions import Fraction
import json
from math import factorial, gcd, lcm
from pathlib import Path
from catalogue import BOUND, catalogue, prime_divisors, prime_power


def require(condition, message):
    if not condition:
        raise ValueError(message)


def phi(n):
    result = n
    for p in prime_divisors(n):
        result = result // p * (p-1)
    return result


def psl2_histogram(q):
    p, f = prime_power(q)
    d = gcd(2, q-1)
    histogram = Counter({1: 1, p: q*q-1})
    for torus_order, torus_number in (((q-1)//d, q*(q+1)//2),
                                     ((q+1)//d, q*(q-1)//2)):
        for e in range(2, torus_order+1):
            if torus_order % e == 0:
                histogram[e] += torus_number * phi(e)
    return histogram


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for first in range(minimum, n+1):
        for rest in partitions(n-first, first):
            yield (first,) + rest


def symmetric_histogram(n, even_only=False):
    histogram = Counter()
    for partition in partitions(n):
        if even_only and (n-len(partition)) % 2:
            continue
        denominator = 1
        for length, number in Counter(partition).items():
            denominator *= length**number * factorial(number)
        histogram[lcm(*partition)] += factorial(n)//denominator
    return histogram


def cyclic_count(histogram):
    return sum((Fraction(number,phi(e)) for e,number in histogram.items()),Fraction())


def verify(stored_catalogue, evidence):
    rows = catalogue()
    require(stored_catalogue == dict(bound=BOUND,rows=rows), "catalogue differs from generator")
    require(sorted(evidence["gap_catalogue_orders"]) == sorted(r["order"] for r in rows),
            "GAP order multiset mismatch")
    needed = [r for r in rows if not r["automatic_exclusion"]]
    counts = evidence["counts"]
    require(len(counts) == len(needed), "incomplete class evidence")
    require([c["name"] for c in counts] == [r["name"] for r in needed],
            "count rows missing, duplicated or reordered")
    exclusions = []
    histogram_checks = []
    for row, item in zip(needed,counts):
        require(item["order"] == row["order"], "wrong group order")
        orders,sizes = item["class_orders"],item["class_sizes"]
        require(len(orders) == len(sizes) and len(orders)>0, "invalid class arrays")
        require(all(type(x) is int and x>0 for x in orders+sizes), "invalid class integer")
        require(all(row["order"]%e==0 for e in orders), "element order does not divide group order")
        require(sum(sizes) == row["order"], "classes do not cover group order")
        histogram = Counter()
        for e,number in zip(orders,sizes):
            histogram[e] += number
        require(histogram[1] == 1, "identity class malformed")
        count = cyclic_count(histogram)
        require(count.denominator == 1 and count == item["cyclic_count"], "cyclic count mismatch")
        if row["family"] == "PSL2":
            require(histogram == psl2_histogram(row["parameter"]), "PSL2 structural histogram mismatch")
            histogram_checks.append(row["name"])
        if row["name"] in ("A5","A6","A7"):
            require(histogram == symmetric_histogram(int(row["name"][1:]),True),
                    "alternating cycle-type histogram mismatch")
        normalized = count / 2**len(row["aut_primes"])
        if row["name"] == "A5":
            require(normalized == 4, "A5 boundary control failed")
        else:
            require(normalized > 6, "a simple row fails the margin")
            exclusions.append(dict(name=row["name"],cyclic_count=int(count),
                                   aut_normalized=str(normalized)))
    s5 = cyclic_count(symmetric_histogram(5))
    require(s5 == 67, "S5 cycle count control failed")
    return dict(catalogue_rows=len(rows), automatic_exclusions=len(rows)-len(needed),
                exact_count_rows=len(needed), non_A5_exact_exclusions=exclusions,
                alternate_PSL2_histograms=histogram_checks,
                alternate_alternating_histograms=["A5","A6","A7"],
                S5_cyclic_count=int(s5), S5_eta=str(s5/8),
                scope="finite arithmetic checked; mathematical imports and independent team check remain")


def main():
    directory=Path(__file__).resolve().parent
    result=verify(json.loads((directory/"catalogue.json").read_text()),
                  json.loads((directory/"evidence.json").read_text()))
    (directory/"verification.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
