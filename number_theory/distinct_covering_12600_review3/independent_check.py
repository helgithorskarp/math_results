#!/usr/bin/env python3
"""Independent adaptive covering certificate audit on period12600.

No target code imports. Branch completeness uses gcd stabilizer signatures;
uniform bounds use the current prefix period; box data uses literal remainders;
pair entries use unions of positive-support labels and exact weight bit planes.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import gcd, lcm
from pathlib import Path
import sys
from time import monotonic

HERE = Path(__file__).resolve().parent
N = 12600
CERT_HASH = "332bccfc80087837a8f9b370d4b45c7e8726eb63f75a3b523b7135760e7cf8e0"


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

def pair_values(weights,m,n):
    """All unions on labels of positive support points; no CRT intersection."""
    items = sorted(weights.items())
    planes = [0] * max((w.bit_length() for _,w in items),default=0)
    left, right = [0]*m, [0]*n
    for i,(x,w) in enumerate(items):
        bit = 1 << i
        left[x % m] |= bit
        right[x % n] |= bit
        for j in range(len(planes)):
            if (w >> j) & 1:
                planes[j] |= bit
    values = []
    for a in range(m):
        for b in range(n):
            union = left[a] | right[b]
            values.append(sum((union & plane).bit_count() << j
                              for j,plane in enumerate(planes)))
    return values


def histogram(weights,m):
    values = [0] * m
    for x,w in weights.items():
        values[x % m] += w
    return values


def lift_maximum(L,P,U,m):
    g = gcd(P,m)
    counts = Counter(x % g for x in U)
    return L // lcm(P,m) * max(counts.values(),default=0)


class Incomplete(RuntimeError):
    pass


class Audit:
    def __init__(self,data,seconds=180,max_nodes=1600,capture_pairs=False):
        demand(type(data["schema"]) is int and data["schema"] == 2 and
               type(data["L"]) is int and data["L"] == N and
               type(data["minimum"]) is int and data["minimum"] == 8 and
               data["root_anchors"] == [[8,0]],"wrong global theorem header")
        self.nodes,self.vectors = data["nodes"],data["vectors"]
        demand(self.nodes,"empty tree")
        self.eligible = tuple(m for m in divisors(N) if m >= 8)
        self.deadline = monotonic()+seconds
        self.budget = max_nodes
        self.capture_pairs = capture_pairs
        self.prefixes,self.vector_uses = {},Counter()
        def unfold(i,A):
            demand(type(i) is int and 0 <= i < len(self.nodes) and
                   i not in self.prefixes,"missing/cyclic/shared node")
            demand(len({m for m,_ in A}) == len(A) and
                   all(m in self.eligible and type(a) is int and 0 <= a < m
                       for m,a in A),"invalid prefix")
            self.prefixes[i] = A
            node = self.nodes[i]
            demand(type(node) is list and node and type(node[0]) is int and
                   node[0] in (0,1,2),"open or invalid node")
            if node[0] == 2:
                demand(len(node) == 3 and type(node[1]) is int and
                       node[1] in self.eligible and node[1] not in dict(A) and
                       node[2],"invalid expansion")
                for child in node[2]:
                    demand(type(child) is list and len(child) == 2 and
                           type(child[0]) is int and 0 <= child[0] < node[1],
                           "invalid child")
                    unfold(child[1],A+((node[1],child[0]),))
            elif node[0] == 1:
                demand(len(node) == 5 and type(node[1]) is int and
                       0 <= node[1] < len(self.vectors),"invalid weight reference")
                self.vector_uses[node[1]] += 1
            else:
                demand(len(node) == 3,"invalid uniform record")
        unfold(0,((8,0),))
        demand(set(self.prefixes) == set(range(len(self.nodes))) and
               set(self.vector_uses) == set(range(len(self.vectors))),
               "unused proof material")
        self.counts,self.periods = Counter(),Counter()
        self.branch_phases = self.positive_phases = self.zero_phases = 0
        self.signature_orbits = self.pair_phases = self.boxes = self.points = 0
        self.max_weight = self.max_depth = 0
        self.events,self.pair_events,self.pair_entries = [],[],[]
        self.cut_margins = []

    def time_check(self):
        if monotonic() > self.deadline:
            raise Incomplete("fixed independent time budget; no exclusion")

    def state(self,A):
        P = lcm(*(m for m,_ in A))
        U = tuple(x for x in range(P) if all(x % m != a for m,a in A))
        demand(U,"a covering prefix refutes exclusion")
        B = tuple(m for m in self.eligible if m not in dict(A))
        return P,U,B

    def weighted(self,i,A,B,node):
        _,vi,stored_D,stored_C,pairs = node
        weights = decode(N,self.vectors[vi])
        demand(weights and all(all(x % m != a for m,a in A) for x in weights),
               "covered or empty weight support")
        self.points += len(weights)
        self.boxes += len(self.vectors[vi])
        self.max_weight = max(self.max_weight,max(weights.values()))
        occupied = set()
        for pair in pairs:
            demand(type(pair) is list and len(pair) == 2 and pair[0] != pair[1] and
                   all(type(m) is int and m in B and m not in occupied for m in pair),
                   "invalid repeated or absent resource")
            occupied.update(pair)
        caps = [(m,max(histogram(weights,m))) for m in B if m not in occupied]
        C = sum(v for _,v in caps)
        for m,n in pairs:
            self.time_check()
            values = pair_values(weights,m,n)
            cap = max(values)
            C += cap
            digest = sha256(("".join(str(v)+"," for v in values)).encode()).hexdigest()
            self.pair_phases += len(values)
            self.pair_events.append([i,m,n,digest])
            if self.capture_pairs:
                self.pair_entries.append([i,m,n,values])
        D = sum(weights.values())
        demand(type(stored_D) is int and type(stored_C) is int and
               (D,C) == (stored_D,stored_C) and D > C,"false strict weighted cut")
        self.counts["weighted"] += 1
        self.counts["grouped_weighted"] += bool(pairs)
        self.cut_margins.append(Fraction(D-C,max(weights.values())))
        self.events.append([i,"weighted",D,C])

    def run(self):
        if len(self.nodes) > self.budget:
            raise Incomplete("fixed independent node budget insufficient; no exclusion")
        for count,i in enumerate(sorted(self.prefixes)):
            self.time_check()
            if count >= self.budget:
                raise Incomplete("fixed independent node budget; no exclusion")
            A,node = self.prefixes[i],self.nodes[i]
            self.max_depth = max(self.max_depth,len(A))
            P,U,B = self.state(A)
            self.periods[P] += 1
            if node[0] == 2:
                m,children = node[1:]
                g = gcd(P,m)
                buckets = Counter(x % g for x in U)
                positive,zero = set(),set()
                for a in range(m):
                    signature = phase_signature(m,a,A)
                    (positive if buckets.get(a % g,0) else zero).add(signature)
                    self.branch_phases += 1
                    if buckets.get(a % g,0):
                        self.positive_phases += 1
                    else:
                        self.zero_phases += 1
                demand(positive and positive.isdisjoint(zero),
                       "empty positive frontier or noninvariant gain")
                child_signatures = []
                phases = []
                for a,j in children:
                    demand(buckets.get(a % g,0)>0,"zero-gain child")
                    child_signatures.append(phase_signature(m,a,A))
                    phases.append(a)
                demand(len(set(phases)) == len(phases) and
                       len(set(child_signatures)) == len(child_signatures) and
                       set(child_signatures) == positive,
                       "missing/repeated/extra positive phase orbit")
                self.signature_orbits += len(positive)
                self.counts["expanded"] += 1
                self.events.append([i,"expanded",m,phases])
            elif node[0] == 0:
                D = N // P * len(U)
                # Group equal gcds, rather than scanning the target's full period.
                coefficients = Counter()
                for m in B:
                    coefficients[gcd(P,m)] += N // lcm(P,m)
                C = sum(scale*max(Counter(x % g for x in U).values())
                        for g,scale in coefficients.items())
                demand(all(type(v) is int for v in node[1:]) and
                       (D,C) == tuple(node[1:]) and D > C,"false strict uniform cut")
                self.counts["uniform"] += 1
                self.cut_margins.append(Fraction(D-C))
                self.events.append([i,"uniform",D,C])
            else:
                self.weighted(i,A,B,node)
        demand(len(self.events) == len(self.nodes),"incomplete event coverage")
        margin = min(self.cut_margins)
        return {"reviewer":"six-reviewer-3","role":"reviewer",
            "status":"COMPLETE INDEPENDENT PERIOD12600 EXCLUSION",
            "certificate_sha256":CERT_HASH,"period":N,"minimum":8,
            "eligible_moduli":len(self.eligible),"nodes":len(self.nodes),
            "node_counts":dict(sorted(self.counts.items())),
            "vectors":len(self.vectors),"vector_usage_counts":dict(Counter(self.vector_uses.values())),
            "maximum_prefix_length":self.max_depth,
            "current_prefix_periods":dict(sorted(self.periods.items())),
            "actual_branch_phases":self.branch_phases,
            "positive_branch_phases":self.positive_phases,
            "zero_gain_branch_phases":self.zero_phases,
            "positive_signature_orbits":self.signature_orbits,
            "pair_groups":len(self.pair_events),"pair_phase_tuples":self.pair_phases,
            "literal_boxes":self.boxes,"positive_weight_points":self.points,
            "maximum_weight":self.max_weight,
            "minimum_certified_uncovered_points_ratio":[margin.numerator,margin.denominator],
            "zero_open_leaves":True,
            "events_sha256":sha256(json.dumps(sorted(self.events),separators=(",",":")).encode()).hexdigest(),
            "pair_events_sha256":sha256(json.dumps(sorted(self.pair_events),separators=(",",":")).encode()).hexdigest()}


def controls(data):
    orbits = 0
    for p,depth in ((2,3),(3,2),(5,1),(7,1)):
        maps = tree_maps(p,depth)
        marked = [(p**e,a) for e in range(1,depth+1) for a in range(p**e)]
        for length in range(3):
            for A in product(marked,repeat=length):
                group = [f for f in maps if all(f[b] % m == b for m,b in A)]
                for e in range(1,depth+1):
                    m = p**e
                    actual = {frozenset(f[a] % m for f in group) for a in range(m)}
                    signatures = {}
                    for a in range(m):
                        signatures.setdefault(phase_signature(m,a,A),set()).add(a)
                    demand(actual == {frozenset(v) for v in signatures.values()},
                           "stabilizer signature control fails")
                    orbits += 1
    maxima_cases = phase_lifts = 0
    for L in (12,60):
        for P in (2,3,4,6):
            for mask in range(1 << P):
                U = tuple(x for x in range(P) if mask >> x & 1)
                actual = {x for x in range(L) if x % P in U}
                for m in divisors(L):
                    literal = [len(actual & set(range(a,L,m))) for a in range(m)]
                    demand(lift_maximum(L,P,U,m) == max(literal),
                           "current-period uniform lift maximum fails")
                    maxima_cases += 1
                    phase_lifts += m
    pair_cases = pairs = 0
    for L in (12,24,60):
        for fixture in range(3):
            weights = {x:(0 if fixture == 0 else (x*x+3*x+fixture) % 5)
                       for x in range(L)}
            weights = {x:w for x,w in weights.items() if w}
            for m,n in combinations([d for d in divisors(L) if d >= 2],2):
                literal = [sum(w for x,w in weights.items()
                               if x % m == a or x % n == b)
                           for a in range(m) for b in range(n)]
                demand(pair_values(weights,m,n) == literal,"small full pair entries fail")
                pair_cases += 1
                pairs += len(literal)
    witness = ((2,0),(3,0),(4,1),(6,1),(12,11))
    positive_prefixes = dominated_pairs = 0
    for depth in range(len(witness)+1):
        A = witness[:depth]
        U = {x for x in range(12) if all(x % m != a for m,a in A)}
        C = sum(max(sum(x % m == a for x in U) for a in range(m))
                for m,_ in witness[depth:])
        demand(len(U) <= C,"actual cover incorrectly excluded")
        positive_prefixes += 1
        covered = set(range(12))-U
        for m in divisors(12):
            if m in dict(A) or not U:
                continue
            zero = [a for a in range(m) if not U & set(range(a,12,m))]
            gaining = [a for a in range(m) if U & set(range(a,12,m))]
            for a,b in product(zero,gaining):
                demand(covered | set(range(a,12,m)) <=
                       covered | set(range(b,12,m)),"zero phase replacement loses coverage")
                dominated_pairs += 1
    rejected = 0
    clone = lambda:json.loads(json.dumps(data))
    def rejects(action,exceptions=(ValueError,)):
        nonlocal rejected
        try:
            action()
        except exceptions:
            rejected += 1
        else:
            raise ValueError("malformed or incomplete certificate accepted")
    bad = clone()
    bad["L"] = 12608
    rejects(lambda:Audit(bad))
    bad = clone()
    bad["root_anchors"] = [[8,1]]
    rejects(lambda:Audit(bad))
    bad = clone()
    bad["nodes"][0] = [3]
    rejects(lambda:Audit(bad))
    bad = clone()
    bad["nodes"][0][2] = []
    rejects(lambda:Audit(bad))
    bad = clone()
    bad["nodes"][0][2][0][1] = 0
    rejects(lambda:Audit(bad))
    bad = clone()
    bad["nodes"].append([0,1,0])
    rejects(lambda:Audit(bad))
    fake = {"schema":2,"L":N,"minimum":8,"root_anchors":[[8,0]],
            "vectors":[],"nodes":[[0,1,0]]}
    rejects(lambda:Audit(fake).run())
    fake = {"schema":2,"L":N,"minimum":8,"root_anchors":[[8,0]],
            "vectors":[[[1,1,1,1,1]]],"nodes":[[1,0,1,0,[]]]}
    rejects(lambda:Audit(fake).run())
    fake["vectors"] = [[[2,2,2,2,1]]]
    fake["nodes"][0][4] = [[9,10],[10,12]]
    rejects(lambda:Audit(fake).run())
    rejects(lambda:decode(N,[[1,1,1,1,0]]))
    rejects(lambda:decode(N,[[1,1,1,1,1],[1,1,1,1,2]]))
    rejects(lambda:Audit(data,seconds=0).run(),exceptions=(Incomplete,))
    return {"full_stabilizer_orbit_cases":orbits,"uniform_lift_maxima":maxima_cases,
        "literal_uniform_phase_values":phase_lifts,"full_pair_cases":pair_cases,
        "literal_pair_phase_values":pairs,"genuine_cover_prefixes":positive_prefixes,
        "zero_gain_dominance_pairs":dominated_pairs,"malformed_and_incomplete_rejections":rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate",type=Path,default=HERE.parent/
                        "distinct_covering_min8_12600_exclusion/certificate.json")
    parser.add_argument("--seconds",type=int,default=180)
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--compare",type=Path,
                        help="optional entrywise separate target-checker capture")
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    demand(sha256(raw).hexdigest() == CERT_HASH,"public certificate bytes differ")
    data = json.loads(raw)
    audit = Audit(data,args.seconds,capture_pairs=bool(args.compare))
    actual = audit.run()
    if args.compare:
        reference = json.loads(args.compare.read_text())
        demand(sorted(audit.events) == sorted(reference["events"]),
               "entrywise node events disagree")
        demand(sorted(audit.pair_entries) == sorted(reference["pair_entries"]),
               "entrywise pair tables disagree")
    actual["controls"] = controls(data)
    encoded = json.dumps(actual,sort_keys=True,indent=2)+"\n"
    if args.write:
        (HERE/"expected.json").write_text(encoded)
    else:
        demand(json.loads((HERE/"expected.json").read_text()) == json.loads(encoded),
               "own expected evidence mismatch")
    print(encoded,end="")


if __name__ == "__main__":
    main()
