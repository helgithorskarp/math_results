#!/usr/bin/env python3
"""Exact family-generated simple-group catalogue for the eta<=6 base gate.

Mathematical completeness, order formulae, small isomorphisms and outer
automorphism formulae are external/structural premises recorded in PROOF.md.
This program enumerates their finite parameters; it does not prove CFSG.
"""
import argparse
import json
from math import factorial, gcd
from pathlib import Path

BOUND = 724052


def prime_power(q):
    for p in range(2, q + 1):
        if q % p == 0:
            n, f = q, 0
            while n % p == 0:
                n //= p
                f += 1
            return (p, f) if n == 1 else None
    return None


def prime_divisors(n):
    answer, p = [], 2
    while p * p <= n:
        if n % p == 0:
            answer.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        answer.append(n)
    return answer


def catalogue():
    rows = {}

    def add(name, order, out_order, family, parameter=None):
        if order > BOUND:
            return
        primes = prime_divisors(order * out_order)
        row = dict(name=name, order=order, out_order=out_order,
                   aut_primes=primes, family=family, parameter=parameter,
                   automatic_exclusion=order > 36 * 4 ** len(primes))
        if name in rows:
            assert rows[name]["order"] == order
            assert rows[name]["out_order"] == out_order
            return
        rows[name] = row

    for q in range(4, 114):
        pf = prime_power(q)
        if pf is None:
            continue
        p, f = pf
        d = gcd(2, q - 1)
        name = {4: "A5", 5: "A5", 7: "L3(2)", 9: "A6"}.get(q, f"L2({q})")
        add(name, q * (q*q - 1) // d, d*f, "PSL2", q)
    for n in (7, 8, 9):
        add(f"A{n}", factorial(n)//2, 2, "alternating", n)
    for q in (3, 4, 5):
        p, f = prime_power(q)
        add(f"L3({q})", q**3*(q*q-1)*(q**3-1)//gcd(3,q-1),
            2*f*gcd(3,q-1), "PSL3", q)
        add(f"U3({q})", q**3*(q*q-1)*(q**3+1)//gcd(3,q+1),
            2*f*gcd(3,q+1), "PSU3", q)
    add("U4(2)", 3**4*(3**2-1)*(3**4-1)//2, 2, "PSp4", 3)
    add("Sz(8)", 8**2*(8**2+1)*(8-1), 3, "Suzuki", 8)
    for name, order, out in (("M11",7920,1), ("M12",95040,2),
                             ("J1",175560,1), ("M22",443520,2),
                             ("J2",604800,2)):
        add(name, order, out, "sporadic")
    result = sorted(rows.values(), key=lambda r: (r["order"], r["name"]))
    assert len(result) == 53
    assert [r["name"] for r in result if set(r["aut_primes"]) -
            set(prime_divisors(r["order"]))] == ["Sz(8)", "L2(32)"]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gap", type=Path, help="Also write GAP record input.")
    args = parser.parse_args()
    rows = catalogue()
    if args.gap:
        records = []
        for r in rows:
            records.append('rec(name:="%s",order:=%d,out_order:=%d,need_count:=%s)' %
                           (r["name"],r["order"],r["out_order"],
                            str(not r["automatic_exclusion"]).lower()))
        args.gap.write_text("baseCatalogue := [\n" + ",\n".join(records) + "];\n")
    print(json.dumps(dict(bound=BOUND, rows=rows), indent=2))


if __name__ == "__main__":
    main()
