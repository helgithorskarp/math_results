#!/usr/bin/env python3
"""Independent binary-cap covering audit; no target implementation imports.

Only the pinned public weights.json is read as data. GCD signatures enumerate
anchor phase orbits, exact fractions sum unrestricted resources, and weighted
bit planes count literal phase sets.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product, permutations
import json
from math import gcd, lcm
from pathlib import Path
import sys
from time import monotonic

HERE = Path(__file__).resolve().parent
WEIGHT_HASH = "19fd557cc1a658c0f4b2f29fc8ffaf0d3084846c24f28e5a3234aff41087e70a"
ANCHORS = (8,9,10,12,15,16,18,20,24,25,30,36,40,45)


def demand(ok, message):
    if not ok:
        raise ValueError(message)

@lru_cache(None)
def factor(n):
    factors = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            power = 1
            while n % p == 0:
                n //= p
                power *= p
            factors.append((p, power))
        p += 1
    if n > 1:
        factors.append((n, n))
    return tuple(factors)

@lru_cache(None)
def divisors(n):
    # Generate from prime powers, rather than the target's paired-divisor scan.
    values = [1]
    for p, power in factor(n):
        powers = [1]
        while powers[-1] < power:
            powers.append(powers[-1] * p)
        values = [a * b for a in values for b in powers]
    return tuple(sorted(values))

def phase_signature(m, a, A):
    return tuple(gcd(a - b, power)
                 for n, b in A for _, power in factor(gcd(m,n)))

def orbit_representatives(m, A):
    found = set()
    for a in range(m):
        signature = phase_signature(m,a,A)
        if signature not in found:
            found.add(signature)
            yield a

def canonical(A):
    """Transport a signature representative to the certificate's coordinates.

    Names are attached to ORIGINAL prime-tree nodes. First appearance fixes
    marked children; arbitrary unmarked children can extend the bijection.
    This is an alignment bridge, not the orbit-enumeration algorithm.
    """
    names, answer = {}, []
    for m, a in A:
        coordinates = []
        for p, power in factor(m):
            small, image = 1, 0
            while small < power:
                labels = names.setdefault((p,small,a % small),{})
                digit = a // small % p
                if digit not in labels:
                    labels[digit] = len(labels)
                image += small * labels[digit]
                small *= p
            coordinates.append((power,image))
        residue, base = 0, 1
        for power, image in coordinates:
            residue += base * ((image-residue) * pow(base,-1,power) % power)
            base *= power
        demand(base == m and 0 <= residue < m, "bad alignment CRT")
        answer.append((m,residue))
    return tuple(answer)

def decode(L,boxes):
    """Decode literal remainders, using one axis to enumerate candidate points."""
    periods = [q for _,q in factor(L)]
    weights = {}
    for box in boxes:
        demand(len(box) == len(periods)+1 and
               type(box[-1]) is int and box[-1] > 0, "invalid box weight")
        for mask,period in zip(box[:-1],periods):
            demand(type(mask) is int and 0 < mask < (1 << period),
                   "invalid axis mask")
        axis = min(range(len(periods)),
                   key=lambda j: box[j].bit_count() * (L // periods[j]))
        period = periods[axis]
        for residue in range(period):
            if not (box[axis] >> residue) & 1:
                continue
            for n in range(residue,L,period):
                if all((box[j] >> (n % periods[j])) & 1
                       for j in range(len(periods)) if j != axis):
                    demand(n not in weights, "overlapping weight boxes")
                    weights[n] = box[-1]
    return weights

def tree_maps(p,depth):
    nodes = [(p**e,r) for e in range(depth) for r in range(p**e)]
    perms = list(permutations(range(p)))
    maps = []
    for choices in product(perms,repeat=len(nodes)):
        labeling = dict(zip(nodes,choices))
        maps.append(tuple(sum(p**e * labeling[p**e,x % (p**e)][x // (p**e) % p]
                              for e in range(depth)) for x in range(p**depth)))
    return maps


def exponent(n,p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def period(depth):
    return 720 if depth < 10 else 3600


@lru_cache(None)
def resources(Q,placed=(),minimum=8):
    """Derive each gcd coefficient from independent prime exponent sums."""
    demand(Q in (720,3600) and len(set(placed)) == len(placed) and
           all(m >= minimum and Q % m == 0 for m in placed),
           "invalid placed resources")
    out = {}
    for g in divisors(Q):
        value = Fraction(1)
        for p in (2,3,5):
            e,E = exponent(g,p),exponent(Q,p)
            if e == E:
                value *= (sum(Fraction(1,p**t) for t in range(5-E))
                          if p == 2 else Fraction(p,p-1))
        value -= int(g < minimum) + int(g in placed)
        scaled = 8 * value
        demand(value >= 0 and scaled.denominator == 1,"invalid tail coefficient")
        if scaled:
            out[g] = int(scaled)
    return out


@lru_cache(None)
def phase_masks(Q,g):
    return tuple(sum(1 << x for x in range(a,Q,g)) for a in range(g))


def maxima(Q,weights,groups):
    """Exact weighted bit planes intersect literal progression masks."""
    demand(all(type(x) is int and 0 <= x < Q and
               type(w) is int and w > 0 for x,w in weights.items()),
           "invalid positive point weights")
    planes = [0] * max((w.bit_length() for w in weights.values()),default=0)
    for x,w in weights.items():
        bit = 1 << x
        for j in range(len(planes)):
            if w >> j & 1:
                planes[j] |= bit
    total,largest = sum(weights.values()),max(weights.values(),default=0)
    result = {}
    for g in groups:
        demand(Q % g == 0,"invalid phase modulus")
        if g == 1:
            result[g] = total
        elif g == Q:
            result[g] = largest
        else:
            result[g] = max(sum((mask & plane).bit_count() << j
                                for j,plane in enumerate(planes))
                            for mask in phase_masks(Q,g))
    return result


def positive_tail_cut(Q,D,C,values,resource):
    demand(D > 0 and resource.get(Q,0) > 0 and values.get(Q,0) > 0,
           "missing positive demand or omitted infinite tail")
    return C <= 8 * D


def weighted(Q,A,boxes):
    weights = decode(Q,boxes)
    demand(weights and all(all(x % m != a for m,a in A) for x in weights),
           "weight on a covered point or zero demand")
    resource = resources(Q,tuple(m for m,_ in A))
    values = maxima(Q,weights,resource)
    D,C = sum(weights.values()),sum(resource[g]*values[g] for g in resource)
    demand(positive_tail_cut(Q,D,C,values,resource),"invalid weighted cut")
    return weights,D,C,values


class Incomplete(RuntimeError):
    pass


def read_weights(data):
    demand(data["format_version"] == 1 and data["axes_by_period"] ==
           {"720":[16,9,5],"3600":[16,9,25]},"invalid certificate header")
    result = {}
    for phases,Q,boxes in data["certificates"]:
        demand(1 <= len(phases) <= len(ANCHORS) and Q == period(len(phases)) and
               all(type(a) is int and 0 <= a < m for m,a in zip(ANCHORS,phases)),
               "invalid weighted prefix")
        A = tuple(zip(ANCHORS,phases))
        demand(canonical(A) == A,"noncanonical weighted prefix")
        key = tuple(phases)
        demand(key not in result,"duplicate weighted prefix")
        result[key] = Q,boxes
    return result


def event_set_hash(events):
    return sha256(("".join(json.dumps(event,separators=(",",":"))+"\n"
                          for event in sorted(events))).encode()).hexdigest()


def prove(data,seconds=120,max_nodes=4000):
    records = read_weights(data)
    used,events,equalities = set(),[],[]
    nodes,uniform,weighted_cuts = ([0] * 15 for _ in range(3))
    deadline = monotonic() + seconds
    phase_changes = boxes_count = point_count = max_weight = 0
    def visit(A):
        nonlocal phase_changes,boxes_count,point_count,max_weight
        demand(len(A) <= len(ANCHORS),"invalid depth")
        if sum(nodes) >= max_nodes or monotonic() > deadline:
            raise Incomplete("fixed independent node/time budget: no proof conclusion")
        depth = len(A)
        Q = period(depth)
        nodes[depth] += 1
        weights = {x:1 for x in range(Q) if all(x % m != a for m,a in A)}
        resource = resources(Q,tuple(m for m,_ in A))
        D = len(weights)
        values = maxima(Q,weights,resource)
        C = sum(resource[g] * values[g] for g in resource)
        aligned = canonical(A)
        phases = tuple(a for _,a in aligned)
        tag = None
        if positive_tail_cut(Q,D,C,values,resource):
            uniform[depth] += 1
            tag = "uniform"
        elif phases in records:
            recorded_Q,boxes = records[phases]
            demand(recorded_Q == Q and phases not in used,"bad reused weight")
            used.add(phases)
            weights,D,C,values = weighted(Q,aligned,boxes)
            boxes_count += len(boxes)
            point_count += len(weights)
            max_weight = max(max_weight,max(weights.values()))
            weighted_cuts[depth] += 1
            tag = "weighted"
        if tag:
            events.append([tag,Q,phases,D,C,sorted(values.items())])
            if C == 8 * D:
                equalities.append((Q,aligned,weights))
            return
        demand(depth < len(ANCHORS),"uncut terminal assignment")
        m = ANCHORS[depth]
        images = set()
        for a in orbit_representatives(m,A):
            image = canonical(A+((m,a),))[-1][1]
            demand(image not in images,"distinct orbits aligned together")
            images.add(image)
            phase_changes += a != image
            visit(A+((m,a),))
    visit(())
    demand(used == set(records),"unused weight records")
    result = {"reviewer":"six-reviewer-3","role":"reviewer",
        "status":"COMPLETE INDEPENDENT BINARY-CAP EXCLUSION",
        "weights_sha256":WEIGHT_HASH,"anchors":list(ANCHORS),
        "nodes_per_depth":nodes,"uniform_cuts_per_depth":uniform,
        "weighted_cuts_per_depth":weighted_cuts,"nodes":sum(nodes),
        "uniform_cuts":sum(uniform),"weighted_cuts":sum(weighted_cuts),
        "equality_cuts":len(equalities),"uncut_leaves":0,
        "weight_boxes":boxes_count,"positive_weight_points":point_count,
        "maximum_weight":max_weight,
        "nonidentical_phase_representatives":phase_changes,
        "proof_event_set_sha256":event_set_hash(events)}
    return result,events,equalities


@lru_cache(None)
def finite_resource(Q,A,B,C,minimum=8):
    """Scan actual moduli in a finite exponent box, not a geometric formula."""
    result = defaultdict(Fraction)
    for a,b,c in product(range(5),range(B+1),range(C+1)):
        n = 2**a * 3**b * 5**c
        if n >= minimum and n not in A:
            g = gcd(Q,n)
            result[g] += Fraction(g,n)
    return result


def controls(data,equalities,events):
    orbit_cases = 0
    for p,depth in ((2,3),(3,2)):
        group = tree_maps(p,depth)
        possible = [(p**e,a) for e in range(1,depth+1) for a in range(p**e)]
        for length in range(3):
            for A in product(possible,repeat=length):
                stabilizer = [f for f in group if all(f[b] % m == b for m,b in A)]
                for e in range(1,depth+1):
                    m = p**e
                    actual = {frozenset(f[a] % m for f in stabilizer) for a in range(m)}
                    groups = defaultdict(set)
                    for a in range(m):
                        groups[phase_signature(m,a,A)].add(a)
                    demand(actual == {frozenset(v) for v in groups.values()},
                           "incorrect stabilizer signature")
                    orbit_cases += 1
    coefficient_cases = equality_cases = 0
    for Q in (720,3600):
        h = exponent(Q,5)
        for depth in range(15):
            if period(depth) != Q:
                continue
            placed = ANCHORS[:depth]
            infinite = resources(Q,placed)
            for B,C in product(range(2,5),range(h,h+3)):
                finite = finite_resource(Q,placed,B,C)
                for g in divisors(Q):
                    finite_formula = Fraction(1)
                    for p,E,bound in ((2,4,4),(3,2,B),(5,h,C)):
                        if exponent(g,p) == E:
                            finite_formula *= sum(Fraction(1,p**t)
                                                  for t in range(bound-E+1))
                    finite_formula -= int(g < 8) + int(g in placed)
                    demand(finite.get(g,0) == finite_formula <=
                           Fraction(infinite.get(g,0),8),
                           "finite tail coefficient disagrees")
                    coefficient_cases += 1
    for Q,A,weights in equalities:
        h = exponent(Q,5)
        values = maxima(Q,weights,divisors(Q))
        infinite = resources(Q,tuple(m for m,_ in A))
        D = sum(weights.values())
        demand(sum(infinite.get(g,0)*values[g] for g in values) == 8*D,
               "not an equality fixture")
        for B,C in product(range(2,5),range(h,h+3)):
            finite = finite_resource(Q,tuple(m for m,_ in A),B,C)
            bound = sum(finite.get(g,0)*values[g] for g in values)
            u,v = Fraction(1,3**(B-1)),Fraction(1,5**(C-h+1))
            deficit = Fraction(15,8) * (u+v-u*v) * values[Q]
            demand(D-bound >= deficit > 0,"finite equality tail deficit fails")
            equality_cases += 1
    density_cases = 0
    for tag,Q,phases,D,scaled,rows in events:
        h = exponent(Q,5)
        values = dict(rows)
        for B,C in ((2,2),(3,2),(2,3),(4,4)):
            finite = finite_resource(Q,ANCHORS[:len(phases)],B,C)
            bound = sum(finite.get(g,0)*value for g,value in rows)
            u,v = Fraction(1,3**(B-1)),Fraction(1,5**(C-h+1))
            deficit = Fraction(15,8) * (u+v-u*v)
            demand(D-bound >= deficit*values[Q],
                   "terminal finite density deficit fails")
            global_gap = Fraction(1,1920) * (
                Fraction(1,3**(B-1))+Fraction(1,5**(C-1))-
                Fraction(1,3**(B-1)*5**(C-1)))
            demand(deficit/Q >= global_gap > 0,"uniform density bound fails")
            density_cases += 1
    literal_phases = literal_maxima = 0
    for Q in (12,60):
        for fixture in range(3):
            weights = {x:(x*x+3*x+fixture) % 7 for x in range(Q)}
            weights = {x:w for x,w in weights.items() if w}
            groups = divisors(Q)
            actual = maxima(Q,weights,groups)
            for g in groups:
                literal = [sum(w for x,w in weights.items() if x % g == a)
                           for a in range(g)]
                demand(actual[g] == max(literal),"literal weighted maximum fails")
                literal_phases += g
                literal_maxima += 1
    transport_phases = 0
    for fixture in range(3):
        w = {x:(x*x+fixture) % 5 for x in range(12)}
        for n in divisors(60):
            g = gcd(12,n)
            for a in range(n):
                literal = sum(w[y % 12] for y in range(a,60,n))
                lifted = 60 // lcm(12,n) * sum(w[x] for x in range(12)
                                              if x % g == a % g)
                demand(literal == lifted,"individual CRT lift count fails")
                transport_phases += 1
    cover = ((2,0),(3,0),(4,1),(6,1),(12,11))
    positive = 0
    for depth in range(len(cover)):
        A = cover[:depth]
        weights = {x:1+x % 7 for x in range(720)
                   if all(x % m != a for m,a in A)}
        res = resources(720,tuple(m for m,_ in A),minimum=2)
        values = maxima(720,weights,res)
        demand(sum(res[g]*values[g] for g in res) > 8*sum(weights.values()),
               "genuine covering prefix falsely excluded")
        positive += 1
    demand(all(any(x % m == a for m,a in cover) for x in range(12)),
           "positive fixture is not a cover")
    rejected = 0
    def rejects(fn,exceptions=(ValueError,)):
        nonlocal rejected
        try:
            fn()
        except exceptions:
            rejected += 1
        else:
            raise ValueError("bad input accepted")
    clone = lambda:json.loads(json.dumps(data))
    bad = clone()
    bad["certificates"].append(bad["certificates"][0])
    rejects(lambda:read_weights(bad))
    bad = clone()
    bad["certificates"][0][0][0] = 1
    rejects(lambda:read_weights(bad))
    phases,Q,boxes = data["certificates"][0]
    A = tuple(zip(ANCHORS,phases))
    rejects(lambda:weighted(Q,A,[[1,1,1,1]]))
    rejects(lambda:weighted(Q,A,[]))
    rejects(lambda:decode(Q,[[1,1,1,1],[1,1,1,2]]))
    rejects(lambda:decode(Q,[[1,1,1,0]]))
    rejects(lambda:decode(Q,[[1 << 16,1,1,1]]))
    rejects(lambda:prove(data,max_nodes=1),exceptions=(Incomplete,))
    rejects(lambda:prove(data,seconds=0),exceptions=(Incomplete,))
    return {"complete_orbit_cases":orbit_cases,
        "finite_coefficient_cases":coefficient_cases,
        "finite_equality_deficit_cases":equality_cases,
        "finite_density_deficit_cases":density_cases,
        "literal_weighted_maxima":literal_maxima,
        "literal_weighted_phases":literal_phases,
        "individual_CRT_lift_phases":transport_phases,
        "genuine_cover_prefixes":positive,
        "malformed_and_incomplete_rejections":rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights",type=Path,default=HERE.parent/
                        "distinct_covering_min8_binary_barrier/weights.json")
    parser.add_argument("--seconds",type=int,default=120)
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--compare-events",type=Path,
                        help="optional entrywise comparison with a separate replay")
    args = parser.parse_args()
    raw = args.weights.read_bytes()
    demand(sha256(raw).hexdigest() == WEIGHT_HASH,"public weights bytes differ")
    data = json.loads(raw)
    result,events,equalities = prove(data,args.seconds)
    if args.compare_events:
        reference = json.loads(args.compare_events.read_text())
        demand(sorted(json.loads(json.dumps(events))) == sorted(reference),
               "entrywise proof events differ")
    result["controls"] = controls(data,equalities,events)
    encoded = json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.write:
        (HERE/"expected.json").write_text(encoded)
    else:
        demand(json.loads((HERE/"expected.json").read_text()) == result,
               "independent expected evidence mismatch")
    print(encoded,end="")


if __name__ == "__main__":
    main()
