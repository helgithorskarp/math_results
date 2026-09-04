#!/usr/bin/env python3
"""Exact degree arithmetic and constructive tests of the f=8 normalization."""
from __future__ import annotations

import itertools
import random

N, FIXED, CYCLES = 43, 8, 7


def require(value, message):
    if not value:
        raise AssertionError(message)


def successor(v):
    return v if v < FIXED else FIXED + 5*((v-FIXED)//5) + (v-FIXED+1) % 5


def orbit_key(u, v):
    images = []
    for _ in range(5):
        images.append(tuple(sorted((u, v))))
        u, v = successor(u), successor(v)
    return min(images)


def main():
    feasible = [(k, t) for k in range(8) for t in range(8) if 18 <= 5*k+t <= 24]
    require(feasible == [(3,t) for t in range(3,8)] + [(4,t) for t in range(5)],
            "degree-feasible pairs differ")
    require({(7-k,7-t) for k,t in feasible} == set(feasible), "complement mismatch")
    print("PASS fixed_degree=5k+t feasible_k=3,4 complement_representative_k=3")
    require(len({min(w[s:]+w[:s] for s in range(5))
                 for w in itertools.product((0,1), repeat=5)}) == 8,
            "binary-necklace count differs")
    print("PASS length_five_binary_necklaces=8")

    pairs = list(itertools.combinations(range(N), 2))
    keys = {pair: orbit_key(*pair) for pair in pairs}
    representatives = sorted(set(keys.values()))
    require(len(representatives) == 203, "edge-orbit count differs")
    cycles = [list(range(FIXED+5*c, FIXED+5*c+5)) for c in range(CYCLES)]
    rng = random.Random(50843)
    for k in (3,4):
        for sample in range(50):
            values = {rep:rng.randrange(2) for rep in representatives}
            selected = set(rng.sample(range(CYCLES), k))
            for c, cycle in enumerate(cycles):
                values[keys[0,cycle[0]]] = int(c in selected)
            complement = int(k == 4)

            def original(u,v):
                return values[keys[tuple(sorted((u,v)))]]

            def color(u,v):
                return original(u,v) ^ complement

            def profile(cycle):
                return color(cycle[0],cycle[1]), color(cycle[0],cycle[2])

            red = sorted([c for c in cycles if color(0,c[0])], key=profile)
            blue = sorted([c for c in cycles if not color(0,c[0])], key=profile)
            require(len(red)==3 and len(blue)==4, "wrong prefix partition")
            p = list(range(N))
            for slot, old in zip(cycles, red+blue, strict=True):
                for v,w in zip(slot,old,strict=True):
                    p[v]=w
            for cycle in cycles[1:]:
                old = [p[v] for v in cycle]
                shift = min(range(5), key=lambda s: tuple(
                    color(p[FIXED],old[(r+s)%5]) for r in range(5)))
                for r,v in enumerate(cycle):
                    p[v]=old[(r+shift)%5]
            require(sorted(p)==list(range(N)), "not a permutation")
            require(all(p[v]==v for v in range(FIXED)), "moved a fixed vertex")
            require(all(p[successor(v)]==successor(p[v]) for v in range(N)),
                    "permutation fails to commute")

            def new(u,v):
                return color(p[u],p[v])

            require(all(new(0,c[0])==int(i<3) for i,c in enumerate(cycles)),
                    "prefix failed")
            profiles = [(new(c[0],c[1]),new(c[0],c[2])) for c in cycles]
            require(profiles[:3]==sorted(profiles[:3]) and profiles[3:]==sorted(profiles[3:]),
                    "block profile order failed")
            for c in cycles[1:]:
                word = tuple(new(FIXED,v) for v in c)
                require(word==min(word[s:]+word[:s] for s in range(5)), "phase failed")
            require(all(new(u,v)==new(successor(u),successor(v)) for u,v in pairs),
                    "not invariant after relabeling")
            require(all(new(u,v)==(original(p[u],p[v])^complement) for u,v in pairs),
                    "full edgewise equivalence failed")
    print("PASS arbitrary_colorings=100 all_903_edges_verified=true k3_and_k4_covered=true")


if __name__ == "__main__":
    main()
