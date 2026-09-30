#!/usr/bin/env python3
"""Independent adaptive covering certificate audit on periods15840 and18480.

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
TARGET_HASHES = {15840:"ca9b12acac505569435cab36172e9b6a4a6b6d85306b173a52e321fc7db12bbd",
                 18480:"34b14234d1de52640fb4534e668de79b3847f3054b64e90b2fe5c723c28b942f"}


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


def transport_axis(p,P,m,a,b,A):
    """Construct from path constraints, then check the full coordinate action.

    Every earlier cylinder is fixed; the proposed cylinder goes from a to b.
    No normalization, target transport, or externally supplied map is used.
    """
    powers = [1]
    while powers[-1] < P:
        powers.append(powers[-1]*p)
    demand(powers[-1] == P,"coordinate is not a power of its prime")
    constraints = [(gcd(n,P),x,x) for n,x in A]
    constraints.append((gcd(m,P),a,b))
    forced = {}
    for q,x,y in constraints:
        for power in powers[:-1]:
            if power >= q:
                break
            names = forced.setdefault((power,x % power),{})
            old,new = (x // power) % p,(y // power) % p
            demand(old not in names or names[old] == new,"inconsistent path map")
            demand(new not in names.values() or names.get(old) == new,
                   "noninjective path map")
            names[old] = new
    for key,names in forced.items():
        remaining = iter(v for v in range(p) if v not in names.values())
        forced[key] = tuple(names[v] if v in names else next(remaining)
                            for v in range(p))
    identity = tuple(range(p))
    action = tuple(sum(power*forced.get((power,x % power),identity)[(x // power) % p]
                       for power in powers[:-1]) for x in range(P))
    demand(sorted(action) == list(range(P)),"coordinate action not bijective")
    for power in powers:
        images = {}
        for x,y in enumerate(action):
            old,new = x % power,y % power
            demand(old not in images or images[old] == new,
                   "coordinate action breaks a congruence partition")
            images[old] = new
        demand(len(set(images.values())) == power,"coordinate partition not bijective")
    for n,x in A:
        q = gcd(n,P)
        demand(all((r % q == x % q) == (y % q == x % q)
                   for r,y in enumerate(action)),"earlier cylinder not fixed")
    q = gcd(m,P)
    demand(all((r % q == a % q) == (y % q == b % q)
               for r,y in enumerate(action)),"proposed cylinder not transported")
    return action


def prime_eleven_controls():
    cases = maps = 0
    for mask in range(1 << 11):
        A = tuple((11,r) for r in range(11) if (mask >> r) & 1)
        free = {r for r in range(11) if not (mask >> r) & 1}
        signatures = {}
        for a in range(11):
            signatures.setdefault(phase_signature(11,a,A),set()).add(a)
        expected = [{r} for _,r in A] + ([free] if free else [])
        demand({frozenset(v) for v in signatures.values()} ==
               {frozenset(v) for v in expected},"prime-eleven stabilizer control")
        for bucket in signatures.values():
            for a,b in product(bucket,repeat=2):
                transport_axis(11,11,11,a,b,A)
                maps += 1
        cases += 1
    return {"prime_eleven_fixed_point_sets":cases,
            "prime_eleven_full_transport_actions":maps}


def compress_prime_axis(K,q,s,classes,selected=None):
    """Restrict q fibres to s, for labels d or dq (d divides K).

    This elementary restriction is not a search. With q and s prime,
    the allowed labels are exactly all divisors of Kq and Ks respectively.
    """
    demand(all(type(v) is int for v in (K,q,s)) and K >= 1 and
           q >= s >= 2 and gcd(K,q*s) == 1,"invalid fibre sizes")
    selected = tuple(range(s)) if selected is None else tuple(selected)
    demand(len(selected) == s and len(set(selected)) == s and
           all(type(t) is int and 0 <= t < q for t in selected),
           "invalid selected fibres")
    labels = set()
    images = []
    for m,a in classes:
        demand(type(m) is int and type(a) is int and m >= 2 and
               0 <= a < m and m not in labels,"invalid distinct class")
        labels.add(m)
        if K % m == 0:
            images.append((m,a))
        else:
            demand(m % q == 0 and K % (m // q) == 0,"unsupported label")
            if a % q not in selected:
                continue
            d = m // q
            phase = selected.index(a % q)
            residue = a % d + d*((phase-a % d)*pow(d,-1,s) % s)
            images.append((d*s,residue))
    demand(len({m for m,_ in images}) == len(images),"images not distinct")
    return tuple(images)


def compression_controls():
    families = points = covers = rejected = 0
    for K in (4,6,12):
        for q in (5,7,11,13,25):
            for s in (2,3,5,7,11):
                if s > q or gcd(K,q*s) != 1:
                    continue
                labels = sorted({d for d in divisors(K) if d >= 2} |
                                {d*q for d in divisors(K)})
                for fixture in range(4):
                    A = tuple((m,(3*fixture+fixture*m*m+1) % m) for m in labels)
                    selected = tuple(range(q-s,q))[::-1]
                    B = compress_prime_axis(K,q,s,A,selected)
                    for x in range(K):
                        for j,t in enumerate(selected):
                            original = x+K*((t-x)*pow(K,-1,q) % q)
                            image = x+K*((j-x)*pow(K,-1,s) % s)
                            demand(any(original % m == a for m,a in A) ==
                                   any(image % m == a for m,a in B),
                                   "fibre restriction coverage differs")
                            points += 1
                    families += 1
    A = ((2,0),(3,0),(4,1),(6,1),(12,11),(7,6),(14,3),(21,1))
    for selected in ((0,1,2,3,4),(6,4,2,1,0)):
        B = compress_prime_axis(12,7,5,A,selected)
        demand(all(any(x % m == a for m,a in A) for x in range(84)) and
               all(any(x % m == a for m,a in B) for x in range(60)),
               "genuine cover not preserved by fibre restriction")
        covers += 1
    def rejects(action):
        nonlocal rejected
        try:
            action()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid fibre restriction accepted")
    rejects(lambda:compress_prime_axis(4,5,7,((2,0),)))
    rejects(lambda:compress_prime_axis(4,5,2,((2,0),)))
    rejects(lambda:compress_prime_axis(4,5,3,((7,0),)))
    rejects(lambda:compress_prime_axis(4,5,3,((2,0),(2,1))))
    rejects(lambda:compress_prime_axis(4,5,3,((2,-1),)))
    rejects(lambda:compress_prime_axis(4,5,3,((2,0),),(0,1,1)))
    return {"fibre_compression_families":families,"literal_fibre_point_checks":points,
            "genuine_cover_compressions":covers,"invalid_compressions_rejected":rejected}


class Incomplete(RuntimeError):
    pass


class Audit:
    def __init__(self,data,target=15840,seconds=120,max_nodes=600,capture_pairs=False):
        demand(type(target) is int and target in TARGET_HASHES,"unsupported target")
        self.N = target
        demand(type(data["schema"]) is int and data["schema"] == 2 and
               type(data["L"]) is int and data["L"] == self.N and
               type(data["minimum"]) is int and data["minimum"] == 8 and
               data["root_anchors"] == [[8,0]],"wrong global theorem header")
        self.nodes,self.vectors = data["nodes"],data["vectors"]
        demand(self.nodes,"empty tree")
        self.eligible = tuple(m for m in divisors(self.N) if m >= 8)
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
        self.transports = self.axis_actions = self.axis_points = 0
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
        weights = decode(self.N,self.vectors[vi])
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
                representatives = {phase_signature(m,a,A):a for a,_ in children}
                for a in range(m):
                    if buckets.get(a % g,0):
                        b = representatives.get(phase_signature(m,a,A))
                        demand(b is not None,"missing positive phase representative")
                        for p,power in factor(self.N):
                            action = transport_axis(p,power,m,a,b,A)
                            self.axis_actions += 1
                            self.axis_points += len(action)
                        self.transports += 1
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
                D = self.N // P * len(U)
                # Group equal gcds, rather than scanning the target's full period.
                coefficients = Counter()
                for m in B:
                    coefficients[gcd(P,m)] += self.N // lcm(P,m)
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
            "status":f"COMPLETE INDEPENDENT PERIOD{self.N} EXCLUSION",
            "certificate_sha256":TARGET_HASHES[self.N],"period":self.N,"minimum":8,
            "eligible_moduli":len(self.eligible),"nodes":len(self.nodes),
            "node_counts":dict(sorted(self.counts.items())),
            "vectors":len(self.vectors),"vector_usage_counts":dict(Counter(self.vector_uses.values())),
            "maximum_prefix_length":self.max_depth,
            "current_prefix_periods":dict(sorted(self.periods.items())),
            "actual_branch_phases":self.branch_phases,
            "positive_branch_phases":self.positive_phases,
            "zero_gain_branch_phases":self.zero_phases,
            "positive_signature_orbits":self.signature_orbits,
            "explicit_positive_phase_transports":self.transports,
            "whole_coordinate_actions_checked":self.axis_actions,
            "coordinate_points_checked":self.axis_points,
            "pair_groups":len(self.pair_events),"pair_phase_tuples":self.pair_phases,
            "literal_boxes":self.boxes,"positive_weight_points":self.points,
            "maximum_weight":self.max_weight,
            "minimum_certified_uncovered_points_ratio":[margin.numerator,margin.denominator],
            "zero_open_leaves":True,
            "events_sha256":sha256(json.dumps(sorted(self.events),separators=(",",":")).encode()).hexdigest(),
            "pair_events_sha256":sha256(json.dumps(sorted(self.pair_events),separators=(",",":")).encode()).hexdigest()}


def controls(data):
    N = data["L"]
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
    rejects(lambda:Audit(bad,target=N))
    bad = clone()
    bad["root_anchors"] = [[8,1]]
    rejects(lambda:Audit(bad,target=N))
    bad = clone()
    bad["nodes"][0] = [3]
    rejects(lambda:Audit(bad,target=N))
    bad = clone()
    bad["nodes"][0][2] = []
    rejects(lambda:Audit(bad,target=N))
    bad = clone()
    bad["nodes"][0][2][0][1] = 0
    rejects(lambda:Audit(bad,target=N))
    bad = clone()
    bad["nodes"].append([0,1,0])
    rejects(lambda:Audit(bad,target=N))
    fake = {"schema":2,"L":N,"minimum":8,"root_anchors":[[8,0]],
            "vectors":[],"nodes":[[0,1,0]]}
    rejects(lambda:Audit(fake,target=N).run())
    fake = {"schema":2,"L":N,"minimum":8,"root_anchors":[[8,0]],
            "vectors":[[[1]*len(factor(N))+[1]]],"nodes":[[1,0,1,0,[]]]}
    rejects(lambda:Audit(fake,target=N).run())
    fake["vectors"] = [[[2]*len(factor(N))+[1]]]
    fake["nodes"][0][4] = [[9,10],[10,12]]
    rejects(lambda:Audit(fake,target=N).run())
    rejects(lambda:decode(N,[[1]*len(factor(N))+[0]]))
    rejects(lambda:decode(N,[[1]*len(factor(N))+[1],[1]*len(factor(N))+[2]]))
    rejects(lambda:Audit(data,target=N,seconds=0).run(),exceptions=(Incomplete,))
    return {"full_stabilizer_orbit_cases":orbits,"uniform_lift_maxima":maxima_cases,
        "literal_uniform_phase_values":phase_lifts,"full_pair_cases":pair_cases,
        "literal_pair_phase_values":pairs,"genuine_cover_prefixes":positive_prefixes,
        "zero_gain_dominance_pairs":dominated_pairs,"malformed_and_incomplete_rejections":rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target",type=int,choices=tuple(TARGET_HASHES),default=15840)
    parser.add_argument("--certificate",type=Path)
    parser.add_argument("--seconds",type=int,default=120)
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--compare",type=Path,
                        help="optional private entrywise original-checker capture")
    args = parser.parse_args()
    path = args.certificate or HERE.parent/"distinct_covering_min8_15840_18480_exclusions"/f"certificate-{args.target}.json"
    raw = path.read_bytes()
    demand(sha256(raw).hexdigest() == TARGET_HASHES[args.target],"public certificate bytes differ")
    data = json.loads(raw)
    audit = Audit(data,args.target,args.seconds,capture_pairs=bool(args.compare))
    actual = audit.run()
    if args.compare:
        reference = json.loads(args.compare.read_text())
        demand(sorted(audit.events) == sorted(reference["events"]),"entrywise node events disagree")
        demand(sorted(audit.pair_entries) == sorted(reference["pair_entries"]),"entrywise pair entries disagree")
    actual["controls"] = controls(data)
    actual["controls"].update(prime_eleven_controls())
    actual["controls"].update(compression_controls())
    encoded = json.dumps(actual,sort_keys=True,indent=2)+"\n"
    expected = HERE/f"expected-{args.target}.json"
    if args.write:
        expected.write_text(encoded)
    else:
        demand(json.loads(expected.read_text()) == json.loads(encoded),
               "independent expected evidence differs")
    print(encoded,end="")

if __name__ == "__main__":
    main()
