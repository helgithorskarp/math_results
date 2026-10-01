#!/usr/bin/env python3
"""Independent quotient census and literal full-vertex static certificate audit.

Imports no producer, solver, catalogue, private census or saved star domains.
Only explicit ground maps and complete entrywise coverage are used.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations
from functools import lru_cache
import hashlib, json, random
from pathlib import Path
HERE=Path(__file__).resolve().parent
DEFICITS=(1,)*4+(0,)*7
N=tuple(map(frozenset,((7,8,9),(5,6,9),(4,6,8),(4,5,7),(2,3,9),(1,3,8),(1,2,7),(0,3,6),(0,2,5),(0,1,4))))
POINTS=frozenset(range(10));GROUND=list(combinations(range(5),2));POSITION={p:i for i,p in enumerate(GROUND)}
PAIRS=list(combinations(range(10),2));RED=[p for p in PAIRS if p[1] in N[p[0]]];BLUE=[p for p in PAIRS if p[1] not in N[p[0]]]
STARS=[frozenset(i for i,p in enumerate(GROUND) if t in p) for t in range(5)]
NEIGHBORS=N
STAR_SETS=STARS
def require(ok, message):
    if not ok:
        raise ValueError(message)

def pack(value):
    normalized = json.loads(json.dumps(value))  # JSON object keys are strings.
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))

def digest(value):
    return hashlib.sha256(pack(value).encode()).hexdigest()

def word(points):
    return sum(1 << i for i in points)

def points(mask, n):
    return {i for i in range(n) if mask >> i & 1}

def integer(value, minimum, maximum, name):
    require(type(value) is int and minimum <= value <= maximum, name + " is out of range")

def fields(value, names, name):
    require(type(value) is dict and set(value) == set(names), name + " has malformed fields")

def quotient(v):
 def a(i,j):return v[POSITION[tuple(sorted((i,j)))]]
 return (a(0,3)-a(1,3)-a(0,2)+a(1,2),a(0,4)-a(1,4)-a(0,2)+a(1,2),*(a(0,i)+a(0,j)-a(i,j)-a(0,1)-a(0,2)+a(1,2) for i,j in ((2,3),(2,4),(3,4))))
def setup():
 sets={z:frozenset(i for i in range(10) if z>>i&1) for z in range(1024)}
 vec={z:tuple(int(i in sets[z]) for i in range(10)) for z in sets}
 qs={z:quotient(v) for z,v in vec.items()}
 red={z:frozenset(t for t,(i,j) in enumerate(RED) if i in sets[z] and j in sets[z]) for z in sets}
 blue={z:tuple(int(i in sets[z] and j in sets[z]) for i,j in BLUE) for z in sets}
 require(all((j in N[i])==set(GROUND[i]).isdisjoint(GROUND[j]) for i,j in PAIRS),'literalP mismatch')
 require(all(qs[word(s)]==(0,)*5 for s in STARS) and quotient([5]*10)==(0,)*5,'quotient geometry')
 commonstar=[]
 for i,j in BLUE:
  ts=[t for t,s in enumerate(STARS) if i in s and j in s];require(len(ts)==1,'nonunique blue star');commonstar.append(ts[0])
 low=set()
 for size in (3,4,5):
  for c in combinations(range(10),size):
   c=set(c);z=POINTS-c;k=len(z)
   if any(k-1>8-len(N[i]&c) for i in c):continue
   if any(len(N[i]&z)<k-7 for i in z):continue
   if any(k+1+len(N[i]&c)+len(N[j]&c)>12 for i,j in RED if i in z and j in z):continue
   low.add(word(z))
 table=defaultdict(list);pairs=[];stats=Counter()
 for a in sorted(low):
  for b in sorted(low):
   if a>b or len(sets[a])+len(sets[b])>12:continue
   stats['low_pairs_within_budget']+=1
   if not red[a].isdisjoint(red[b]):continue
   stats['low_pairs_red_capped']+=1
   size=len(sets[a])+len(sets[b]);q=tuple(qs[a][i]+qs[b][i] for i in range(5))
   record=(a,b,red[a]|red[b],tuple(vec[a][i]+vec[b][i] for i in range(10)),tuple(blue[a][i]+blue[b][i] for i in range(len(BLUE))),size,q)
   table[size,q].append(record);pairs.append(record)
 full={k:sorted(word(POINTS-set(c)) for c in combinations(range(10),10-k) if all(len(N[i]&set(c))<=1 for i in c)) for k in (5,6)}
 choices={()}|{(h,) for h in full[5]+full[6]}|{(a,b) for a in full[5] for b in full[5] if a<=b and red[a].isdisjoint(red[b])}
 maps=[]
 for perm in permutations(range(5)):
  image=[POSITION[tuple(sorted((perm[a],perm[b])))] for a,b in GROUND]
  require(all((j in N[i])==(image[j] in N[image[i]]) for i,j in PAIRS),'bad local map')
  images={z:word(image[i] for i in sets[z]) for z in sets}
  maps.append((perm,images))
 remaining=set(choices);cohorts=[];covered=set()
 while remaining:
  h=min(remaining);orbit={tuple(sorted(images[z] for z in h)) for p,images in maps}
  require(orbit<=choices and not covered.intersection(orbit) and h==min(orbit),'invalid full-large cover')
  covered.update(orbit);remaining.difference_update(orbit);cohorts.append((h,len(orbit)))
 require(covered==choices,'missing full-large choice')
 info={'low_size_counts':dict(sorted(Counter(len(sets[z]) for z in low).items())),'low_pair_table':dict(stats),'all_full_large_choices':len(choices),'full_large_cohorts':[(h,n) for h,n in cohorts],'full_large_sizes':{k:len(v) for k,v in full.items()}}
 return sets,vec,qs,red,blue,commonstar,table,pairs,cohorts,maps,info

def one_cohort(highs,data):
 sets,vec,qs,red,blue,commonstar,table,pairs,cohorts,maps,info=data
 surplus=sum(len(sets[h])-4 for h in highs);total=22-surplus
 highred=frozenset().union(*(red[h] for h in highs))
 highvec=tuple(sum(vec[h][i] for h in highs) for i in range(10))
 highblue=tuple(sum(blue[h][i] for h in highs) for i in range(len(BLUE)))
 hq=tuple(sum(qs[h][i] for h in highs) for i in range(5))
 keys=set();stats=Counter()
 for a,b,ar,av,ab,size,q in pairs:
  if not ar.isdisjoint(highred):continue
  demand=total-size
  if not 10<=demand<=12:continue
  stats['first_low_pairs']+=1
  target=tuple(-hq[i]-q[i] for i in range(5))
  for c,d,br,bv,bb,bs,bq in table.get((demand,target),()):
   if b>c:continue
   stats['ordered_quotient_joins']+=1
   if not br.isdisjoint(highred|ar):continue
   stats['red_capped_joins']+=1
   residual=[5-highvec[i]-av[i]-bv[i] for i in range(10)]
   twice=residual[POSITION[0,1]]+residual[POSITION[0,2]]-residual[POSITION[1,2]]
   if twice%2:continue
   mu=(twice//2,)+tuple(residual[POSITION[0,j]]-twice//2 for j in range(1,5))
   if any(not 0<=m<=2 for m in mu) or sum(mu)+len(highs)!=7:continue
   if any(mu[i]+mu[j]!=residual[t] for t,(i,j) in enumerate(GROUND)):continue
   stats['integral_recoveries']+=1
   if any(highblue[i]+ab[i]+bb[i]+mu[commonstar[i]]>3 for i in range(len(BLUE))):continue
   key=((a,b,c,d),tuple(highs),mu);require(key not in keys,'duplicate quotient recovery');keys.add(key)
 return sorted(keys),dict(stats)

def expand(key,maps):
 low,highs,mu=key;out=set()
 for perm,images in maps:
  m=[0]*5
  for t,n in enumerate(mu):m[perm[t]]=n
  out.add((tuple(sorted(images[z] for z in low)),tuple(sorted(images[z] for z in highs)),tuple(m)))
 return out


def validate_key(raw):
    require(type(raw) is list and len(raw)==3,'malformed incidence key')
    lows,highs,mu=raw
    require(type(lows) is list and len(lows)==4,'malformed equal-one-tag rows')
    for z in lows:
        integer(z,0,1023,'low row word')
    require(lows==sorted(lows),'unordered equal-one-tag rows')
    require(type(highs) is list and len(highs)<=2,'malformed full large rows')
    for z in highs:
        integer(z,0,1023,'full large word')
    require(highs==sorted(highs),'unordered full large rows')
    require(type(mu) is list and len(mu)==5,'malformed multiplicities')
    for m in mu:
        integer(m,0,2,'multiplicity')
    require(sum(mu)+len(highs)==7,'incorrect number of full rows')
    return tuple(lows),tuple(highs),tuple(mu)

def rows_from_key(key):
    lows,highs,mu=key
    return list(lows)+list(highs)+[word(s) for s,m in zip(STAR_SETS,mu) for _ in range(m)]

def incidence_census():
    data=setup();keys=set();stats=Counter();cohort_counts=[]
    for index,(highs,n) in enumerate(data[8]):
        found,part=one_cohort(highs,data);stats.update(part)
        expanded=set()
        for key in found:
            expanded.update(expand(key,data[9]))
        require(not keys.intersection(expanded),'overlapping full-large cohorts')
        keys.update(expanded)
        cohort_counts.append({'cohort':index,'canonical_highs':highs,'high_orbit':n,'canonical_keys':len(found),'expanded_keys':len(expanded)})
    patterns=Counter((tuple(sorted(z.bit_count() for z in lows)),tuple(h.bit_count() for h in highs)) for lows,highs,mu in keys)
    report={'incidence_records':len(keys),'incidence_sha256':digest(sorted(keys)),
            'setup':data[10],'census':dict(sorted(stats.items())),
            'cohort_counts':cohort_counts,
            'patterns':[{'low_sizes':l,'high_sizes':h,'records':n} for (l,h),n in sorted(patterns.items())]}
    return keys,report

@lru_cache(maxsize=None)
def orbit(key):
    out=set()
    for perm in permutations(range(5)):
        image=[POSITION[tuple(sorted((perm[a],perm[b])))] for a,b in GROUND]
        require(all((j in NEIGHBORS[i])==(image[j] in NEIGHBORS[image[i]]) for i,j in PAIRS),'invalid local relabeling')
        def move(z):
            return word(image[i] for i in points(z,10))
        lows,highs,mu=key;m=[0]*5
        for t,n in enumerate(mu):
            m[perm[t]]=n
        out.add((tuple(sorted(move(z) for z in lows)),tuple(sorted(move(h) for h in highs)),tuple(m)))
    return frozenset(out)

class LiteralFrame:
    """Full physical vertex sets, including root, A, and all B points."""
    def __init__(self, local, rows, deficits):
        self.local = local
        self.rows = rows
        self.deficits = deficits
        self.n = len(rows)
        self.universe = frozenset(range(11 + self.n))
        self.misses = [points(z, 10) for z in rows]
        self.a_red = [frozenset({0} | {j + 1 for j in local[i]}
                               | {11 + b for b, z in enumerate(self.misses) if i not in z})
                      for i in range(10)]
        self.a_blue = [self.universe - red - {i + 1} for i, red in enumerate(self.a_red)]
        self.full = {}

    def neighborhoods(self, b, star):
        key = (b, star)
        if key not in self.full:
            red = frozenset({i + 1 for i in POINTS - self.misses[b]}
                            | {11 + c for c in points(star, self.n)})
            self.full[key] = red, self.universe - red - {11 + b}
        return self.full[key]

    def domains(self):
        result = []
        for b, (z, delta) in enumerate(zip(self.misses, self.deficits)):
            degree = len(z) - delta
            require(0 <= degree < self.n, "literal outside degree out of range")
            accepted = []
            for picked in combinations([c for c in range(self.n) if c != b], degree):
                star = word(picked)
                red, blue = self.neighborhoods(b, star)
                if all(len(blue & self.a_blue[i]) <= 6 if i in z
                       else len(red & self.a_red[i]) <= 3 for i in range(10)):
                    accepted.append(star)
            result.append(sorted(accepted))
        return result

    def compatible(self, b, x, c, y):
        red_b, blue_b = self.neighborhoods(b, x)
        red_c, blue_c = self.neighborhoods(c, y)
        if ((11 + c) in red_b) != ((11 + b) in red_c):
            return False
        return len(red_b & red_c) <= 3 if (11 + c) in red_b else len(blue_b & blue_c) <= 6

@lru_cache(maxsize=None)
def literal_domains(key):
    # Immutable exact domains, keyed by the complete fixed-tag incidence.
    # Repeated integrity controls never need to rebuild the same geometry.
    frame = LiteralFrame(NEIGHBORS, rows_from_key(key), DEFICITS)
    return tuple(tuple(domain) for domain in frame.domains())

def check_exclusion(frame, stars, exclusion):
    require(type(exclusion) is dict, "exclusion is not an object")
    if exclusion.get("type") == "empty_star":
        fields(exclusion, ("type", "point"), "empty-star certificate")
        b = exclusion["point"]
        integer(b, 0, 10, "empty-star point")
        require(not stars[b], "claimed star domain is nonempty")
        return 0, 0
    fields(exclusion, ("type", "point", "covers"), "star-pair certificate")
    require(exclusion["type"] == "star_pair_cover", "unknown exclusion type")
    require(all(stars), "star-pair cover with an initially empty domain")
    b = exclusion["point"]
    integer(b, 0, 10, "target point")
    require(type(exclusion["covers"]) is list and exclusion["covers"], "empty star cover")
    covered = set()
    against_points = []
    for cover in exclusion["covers"]:
        fields(cover, ("against", "stars"), "unsupported-star cover")
        c, unsupported = cover["against"], cover["stars"]
        integer(c, 0, 10, "support point")
        require(b != c, "self-support obstruction")
        against_points.append(c)
        require(type(unsupported) is list and unsupported, "empty unsupported-star list")
        for x in unsupported:
            integer(x, 0, 2047, "unsupported star")
        require(unsupported == sorted(set(unsupported)), "noncanonical unsupported stars")
        require(set(unsupported) <= set(stars[b]), "claimed star not in complete initial domain")
        require(not covered.intersection(unsupported), "overlapping unsupported-star covers")
        for x in unsupported:
            require(not any(frame.compatible(b, x, c, y) for y in stars[c]),
                    "claimed unsupported star has initial support")
        covered.update(unsupported)
    require(against_points == sorted(set(against_points)), "unordered or duplicate support points")
    require(covered == set(stars[b]), "incomplete initial-star obstruction cover")
    return len(exclusion["covers"]), len(covered)
def verify_certificate(certificate, keys, census_result):
    fields(certificate, ("schema", "order", "red_page_cap", "blue_page_cap", "outside_deficits",
                         "local_graph", "incidence_records", "entries"), "certificate")
    for name, expected in (("schema", 1), ("order", 22), ("red_page_cap", 3), ("blue_page_cap", 6)):
        require(type(certificate[name]) is int and certificate[name] == expected, "wrong " + name)
    require(certificate["outside_deficits"] == list(DEFICITS)
            and all(type(d) is int for d in certificate["outside_deficits"]), "wrong deficiency tags")
    require(certificate["local_graph"] == "KG(5,2)", "wrong local graph")
    require(type(certificate["entries"]) is list and certificate["entries"], "no certificate entries")
    integer(certificate["incidence_records"], len(keys), len(keys), "incidence record count")
    covered = set()
    hist = Counter()
    exclusions = Counter()
    weighted_exclusions = Counter()
    cover_count = unsupported_count = 0
    ordered_keys = []
    for entry in certificate["entries"]:
        fields(entry, ("key", "orbit_size", "domain_sizes", "domains_sha256", "exclusion"), "entry")
        key = validate_key(entry["key"])
        ordered_keys.append(key)
        images = orbit(key)
        require(key == min(images), "representative is not minimal in its local orbit")
        integer(entry["orbit_size"], len(images), len(images), "orbit size")
        require(not (covered & images), "overlapping orbit entries")
        require(images <= keys, "certificate orbit has inadmissible incidence")
        covered.update(images)
        frame = LiteralFrame(NEIGHBORS, rows_from_key(key), DEFICITS)
        stars = literal_domains(key)
        require(entry["domain_sizes"] == [len(domain) for domain in stars]
                and all(type(s) is int for s in entry["domain_sizes"]), "star domain sizes mismatch")
        require(entry["domains_sha256"] == digest(stars), "literal star domains hash mismatch")
        covers, unsupported = check_exclusion(frame, stars, entry["exclusion"])
        cover_count += covers
        unsupported_count += unsupported
        hist[len(images)] += 1
        exclusions[entry["exclusion"]["type"]] += 1
        weighted_exclusions[entry["exclusion"]["type"]] += len(images)
    require(ordered_keys == sorted(set(ordered_keys)), "unordered or duplicate representatives")
    require(covered == keys, "certificate does not cover the complete independent census")
    result = dict(census_result)
    result.update({"orbits": len(ordered_keys), "orbit_size_histogram": dict(sorted(hist.items())),
                   "exclusion_types": dict(sorted(exclusions.items())),
                   "weighted_exclusion_types": dict(sorted(weighted_exclusions.items())),
                   "star_pair_covers": cover_count, "unsupported_stars": unsupported_count,
                   "covered_records_sha256": digest(sorted(covered)),
                   "certificate_sha256": digest(certificate)})
    return result
def geometry_controls():
    require(all(len(n) == 3 for n in NEIGHBORS), "Petersen is not cubic")
    require(all((j in NEIGHBORS[i]) == (set(GROUND[i]).isdisjoint(GROUND[j]))
                for i, j in PAIRS), "literal adjacency/ground-label mismatch")
    require(all(len(NEIGHBORS[i] & NEIGHBORS[j]) == (0 if j in NEIGHBORS[i] else 1)
                for i, j in PAIRS), "Petersen common-neighbor table mismatch")
    independent = [frozenset(s) for s in combinations(range(10), 4)
                   if all(j not in NEIGHBORS[i] for i, j in combinations(s, 2))]
    require(set(independent) == set(STAR_SETS), "independent four-set classification mismatch")
    require(all(t * (t - 1) // 2 >= t - 1 for t in range(5)), "four-column packing identity")
    require(all(sum(i in star and j in star for star in STAR_SETS) == (0 if j in NEIGHBORS[i] else 1) for i,j in PAIRS), 'ground-star pair multiplicity')
    patterns=[list(s) for s in combinations_with_replacement(range(5,8),4) if sum(s)<=22]
    require(patterns==[[5,5,5,5],[5,5,5,6],[5,5,5,7],[5,5,6,6]],'four-low size-budget coverage')
    return {'independent_four_sets':len(independent),'complete_low_size_patterns':patterns,'fixed_tags':[1,1,1,1]}

def primary_control():
    raw = (HERE / "primary21.txt").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == "3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55",
            "primary21 raw fixture hash mismatch")
    matrix = json.loads(raw.decode().split("\n\n")[0])
    require(len(matrix) == 21 and all(len(row) == 21 for row in matrix), "primary21 dimensions")
    red = []
    universe = set(range(21))
    for i in range(21):
        require(matrix[i][i] == 0, "primary21 diagonal")
        require(all(type(matrix[i][j]) is int and matrix[i][j] in (0, 1)
                    and matrix[i][j] == matrix[j][i] for j in range(21)), "primary21 symmetry/entries")
        red.append({j for j in range(21) if j != i and matrix[i][j] == 0})
    blue = [universe - red[i] - {i} for i in range(21)]
    red_pages = [len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]]
    blue_pages = [len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i]]
    require(max(red_pages) == 3 and max(blue_pages) == 6, "primary21 book caps")
    roots = [i for i, n in enumerate(red) if len(n) == 10]
    require(len(roots) == 1, "primary21 unique degree-ten root")
    v = roots[0]
    a, b = sorted(red[v]), sorted(blue[v])
    local = tuple(frozenset(j for j in range(10) if a[j] in red[a[i]]) for i in range(10))
    rows = [word(i for i in range(10) if a[i] not in red[u]) for u in b]
    deficits = [10 - len(red[u]) for u in b]
    actual = [word(j for j in range(10) if b[j] in red[u]) for u in b]
    frame = LiteralFrame(local, rows, deficits)
    domains = frame.domains()
    require(all(actual[i] in domains[i] for i in range(10)), "primary21 actual star rejected")
    require(all(frame.compatible(i, actual[i], j, actual[j]) for i, j in combinations(range(10), 2)),
            "primary21 actual completion rejected")
    damaged = 0
    for i in range(10):
        for j in range(10):
            for h in range(10):
                if len({i, j, h}) != 3 or not actual[i] >> j & 1 or actual[i] >> h & 1:
                    continue
                trial = actual[i] ^ (1 << j) ^ (1 << h)
                require(any(not frame.compatible(i, trial, c, actual[c]) for c in range(10) if c != i),
                        "primary21 asymmetric damaged star accepted")
                damaged += 1
    return {"order": 21, "red_edges": len(red_pages), "blue_edges": len(blue_pages),
            "max_red_pages": max(red_pages), "max_blue_pages": max(blue_pages),
            "actual_stars_accepted": 10, "actual_completion_accepted": 1,
            "asymmetric_degree_preserving_damages_rejected": damaged}

def signed_cut_controls():
    sampler = random.Random(20261001)
    checks = negative_slacks = 0
    for _ in range(32):
        columns = [set(sampler.sample(range(11), 5)) for _ in range(10)]
        rows = [word(i for i in range(10) if b in columns[i]) for b in range(11)]
        b = sampler.randrange(11)
        actual_star = word(c for c in range(11) if c != b and sampler.getrandbits(1))
        frame = LiteralFrame(NEIGHBORS, rows, DEFICITS)
        red, blue = frame.neighborhoods(b, actual_star)
        z = points(rows[b], 10)
        c = POINTS - z
        for i in z:
            pages = len(blue & frame.a_blue[i])
            intersection = len(points(actual_star, 11) & (columns[i] - {b}))
            h = len(NEIGHBORS[i] & c)
            require(intersection == len(z) - 6 + h + (6 - pages), "signed two-column identity")
            checks += 1
            negative_slacks += pages > 6
    require(negative_slacks > 0, "signed controls lack negative blue slack")
    return {"frames": 32, "blue_intersection_identity_checks": checks,
            "negative_blue_slack_cases": negative_slacks}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--expected", type=Path, default=HERE / "expected.json")
    parser.add_argument("--derive", action="store_true", help="omit frozen-summary comparison")
    args = parser.parse_args()
    geometry = geometry_controls()
    keys, census = incidence_census()
    result = verify_certificate(json.loads(args.certificate.read_text()), keys, census)
    result["controls"] = {"geometry": geometry, "primary21": primary_control(),
                          "signed_cut": signed_cut_controls()}
    if not args.derive:
        require(pack(result) == pack(json.loads(args.expected.read_text())["verifier"]),
                "verifier expected-summary mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
