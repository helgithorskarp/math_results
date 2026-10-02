#!/usr/bin/env python3
"""Separate column, colored-neighborhood and Cartesian-product checker."""
from collections import Counter
from copy import deepcopy
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import hashlib
import json
import sys
import time

SCOPE = "specified one-nine leaf; red degrees 9^4,10^18; cross-repeated omission"
UNIVERSE = frozenset(range(22))


def canonical(value):
    return json.dumps(value,separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def guard(start):
    if time.monotonic()-start > 30:
        raise RuntimeError("30s phase guard: incomplete checking is not an exclusion")


def unique_object(items):
    answer = {}
    for key,value in items:
        if key in answer:
            raise ValueError("duplicate JSON field")
        answer[key] = value
    return answer


def graph(columns,sy_columns=None):
    red = [set() for _ in range(16)]
    def edge(i,j):
        red[i].add(j)
        red[j].add(i)
    for j in (1,2,*range(3,11)):
        edge(0,j)
    for j in (2,11,12):
        edge(1,j)
    for j in range(9,16):
        edge(2,j)
    for i,j in ((0,4),(4,3),(3,1),(1,2),(2,5),(5,0)):
        edge(i+3,j+3)
    for sx,points in ((9,(3,5)),(10,(2,4))):
        for point in points:
            edge(sx,point+3)
    for i,column in enumerate(columns):
        for t in range(3):
            if column & (1 << t):
                edge(i+3,t+13)
    for sy,ts in ((11,(1,2)),(12,(0,1))):
        for t in ts:
            edge(sy,t+13)
    if sy_columns is not None:
        for i,column in enumerate(sy_columns):
            for s in range(2):
                if column & (1 << s):
                    edge(i+3,s+11)
    return red


def necessary(neighbors,vertices,degrees,outside_size):
    universe = set(vertices)
    red = {i:neighbors[i]&universe for i in vertices}
    blue = {i:universe-red[i]-{i} for i in vertices}
    ranks = {i:degrees[i]-len(red[i]) for i in vertices}
    if any(q < 0 or q > outside_size for q in ranks.values()):
        raise ValueError("outside rank out of range")
    for ix,i in enumerate(vertices):
        for j in vertices[ix+1:]:
            if j in red[i]:
                if len(red[i]&red[j])+max(0,ranks[i]+ranks[j]-outside_size) > 3:
                    return False
            elif len(blue[i]&blue[j])+max(0,outside_size-ranks[i]-ranks[j]) > 6:
                return False
    return True


def x_domain():
    vertices14 = tuple(i for i in range(16) if i not in (11,12))
    vertices16 = tuple(range(16))
    sy_choices = []
    for columns in product(range(4),repeat=6):
        ranks = tuple(sum(bool(c & (1 << s)) for c in columns) for s in range(2))
        if any(rank not in (3,4) for rank in ranks):
            continue
        masks = tuple(sum(int(bool(columns[i] & (1 << s))) << i for i in range(6))
                      for s in range(2))
        sy_choices.append((columns,tuple(4-rank for rank in ranks),masks))
    if len(sy_choices) != 1225:
        raise ValueError("entire 4096-word SY column domain")
    answer = []
    for r in range(2):
        start = time.monotonic()
        for columns in product((3,5,6,7),(3,5,6,7),range(1,8),range(1,8),range(1,8),range(1,8)):
            ranks = tuple(sum(bool(c & (1 << t)) for c in columns) for t in range(3))
            if ranks[0] not in (3,4) or ranks[1] not in (3,4) or ranks[2] not in (2,3):
                continue
            low_t = (4-ranks[0],4-ranks[1],3-ranks[2])
            c = columns+((6,5) if r == 0 else (5,6))
            neighbors = graph(c)
            degrees = (10,10,9,*([10]*10),*(10-l for l in low_t))
            if not necessary(neighbors,vertices14,degrees,8):
                continue
            for sy_columns,low_s,masks in sy_choices:
                lows = low_t+low_s
                if sum(lows) > 3:
                    continue
                beta = tuple((4 if i < 2 else 3)-columns[i].bit_count()
                             -sum(bool(sy_columns[i] & (1 << s)) for s in range(2))
                             for i in range(6))
                if any(b < 0 or b > 2 for b in beta):
                    continue
                neighbors = graph(c,sy_columns)
                degrees = (10,10,9,*([10]*8),*(10-l for l in low_s),*(10-l for l in low_t))
                if not necessary(neighbors,vertices16,degrees,6):
                    continue
                q = (0,6,0,*(3+b for b in beta),4,4,2,2,3,2,3)
                if tuple(degrees[i]-len(neighbors[i]) for i in range(16)) != q:
                    raise ValueError("literal actual-rank bridge")
                if sum(beta) != 1+sum(lows):
                    raise ValueError("literal cut bridge")
                answer.append((r,lows,c,masks[0],masks[1],beta))
            guard(start)
        guard(start)
    answer.sort()
    return answer


def row(mask):
    return frozenset(16+j for j in range(6) if mask & (1 << j))


def complete(vertex,neighbors,mask):
    red = frozenset(neighbors[vertex]) | row(mask)
    return red,UNIVERSE-red-{vertex}


def valid(i,j,left,right,neighbors):
    color = 0 if j in neighbors[i] else 1
    return len(left[color]&right[color]) <= (3 if color == 0 else 6)


def known(xs):
    answer = []
    for _,lows,c,s0,s1,beta in xs:
        sy_columns = tuple(((s0 >> i)&1)+2*((s1 >> i)&1) for i in range(6))
        neighbors = graph(c,sy_columns)
        degree = (10,10,9,*([10]*8),10-lows[3],10-lows[4],*(10-lows[t] for t in range(3)))
        answer.append((neighbors,degree))
    return answer


def y_domain(xs,bases):
    start = time.monotonic()
    # Transpose all six nonzero T-column words: cover is imposed here.
    triples = []
    for columns in product(range(1,8),repeat=6):
        ranks = tuple(sum(bool(c & (1 << t)) for c in columns) for t in range(3))
        if ranks == (3,2,3):
            triples.append(tuple(sum(int(bool(columns[j] & (1 << t))) << j
                                     for j in range(6)) for t in range(3)))
    triples.sort()
    ranks = {n:tuple(m for m in range(64) if m.bit_count() == n) for n in (2,3)}
    answer = []
    for index,(neighbors,degrees) in enumerate(bases):
        for intersection,b in ((2,51),(3,23)):
            sx = (complete(9,neighbors,15),complete(10,neighbors,b))
            if not valid(9,10,*sx,neighbors):
                raise ValueError("canonical actual SX pair is invalid")
            tr = [{m:complete(13+t,neighbors,m) for m in ranks[(3,2,3)[t]]}
                  for t in range(3)]
            allowed = [frozenset(m for m,n in tr[t].items()
                                 if all(valid(9+s,13+t,sx[s],n,neighbors) for s in range(2)))
                       for t in range(3)]
            sy = [{m:complete(11+s,neighbors,m) for m in ranks[2]} for s in range(2)]
            for ts in triples:
                if any(ts[t] not in allowed[t] for t in range(3)):
                    continue
                whole_t = tuple(tr[t][ts[t]] for t in range(3))
                if any(not valid(13+i,13+j,whole_t[i],whole_t[j],neighbors)
                       for i,j in combinations(range(3),2)):
                    continue
                choices = [tuple(m for m,n in sy[s].items()
                                 if all(valid(9+z,11+s,sx[z],n,neighbors) for z in range(2))
                                 and all(valid(11+s,13+t,n,whole_t[t],neighbors) for t in range(3)))
                           for s in range(2)]
                for p,q in product(*choices):
                    if valid(11,12,sy[0][p],sy[1][q],neighbors):
                        answer.append((index,intersection,*ts,p,q))
            guard(start)
    answer.sort()
    return answer


def endpoint_masks(frame):
    _,intersection,t0,t1,t2,p,q = frame
    return (15,51 if intersection == 2 else 23,p,q,t0,t1,t2)


def row_domain(xs,ys,bases):
    start = time.monotonic()
    option_cache = {}
    endpoint_cache = {}
    answer = []
    for index,frame in enumerate(ys):
        xi = frame[0]
        neighbors,degrees = bases[xi]
        masks = endpoint_masks(frame)
        if xi not in option_cache:
            option_cache[xi] = [tuple((m,complete(3+i,neighbors,m)) for m in range(64)
                                    if m.bit_count() == degrees[3+i]-len(neighbors[3+i]))
                               for i in range(6)]
        ep = []
        for e,m in enumerate(masks):
            key = (xi,e,m)
            if key not in endpoint_cache:
                endpoint_cache[key] = complete(9+e,neighbors,m)
            ep.append(endpoint_cache[key])
        candidates = []
        for i in range(6):
            choices = []
            for mask,whole in option_cache[xi][i]:
                if all(valid(3+i,9+e,whole,ep[e],neighbors) for e in range(7)):
                    choices.append(mask)
            candidates.append(tuple(choices))
        if all(candidates):
            answer.append((index,tuple(candidates)))
        guard(start)
    return answer


def join_domain(xs,ys,rows,bases):
    start = time.monotonic()
    pair_cache = {}
    answer = []
    for yi,candidates in rows:
        frame = ys[yi]
        xi = frame[0]
        neighbors,degrees = bases[xi]
        if xi not in pair_cache:
            options = [{m:complete(3+i,neighbors,m) for m in range(64)
                        if m.bit_count() == degrees[3+i]-len(neighbors[3+i])}
                       for i in range(6)]
            pair_cache[xi] = {(i,j):frozenset((a,b) for a,left in options[i].items()
                                            for b,right in options[j].items()
                                            if valid(3+i,3+j,left,right,neighbors))
                              for i,j in combinations(range(6),2)}
        pairs = pair_cache[xi]
        ep = endpoint_masks(frame)
        for chosen in product(*candidates):
            if any((chosen[i],chosen[j]) not in table for (i,j),table in pairs.items()):
                continue
            outside = (0,63,0,*chosen,*ep)
            low_y = 0
            correct = True
            for j in range(6):
                inside_degree = 4-sum(bool(m & (1 << j)) for m in ep[2:])
                outside_degree = sum(bool(m & (1 << j)) for m in outside)
                actual_degree = inside_degree+outside_degree
                if actual_degree not in (9,10):
                    correct = False
                    break
                if actual_degree == 9:
                    low_y |= 1 << j
            if not correct or low_y.bit_count() != 3-sum(xs[xi][1]):
                continue
            answer.append((yi,chosen,low_y))
        guard(start)
    answer.sort()
    return answer


def witnesses(xs,ys,joins,bases):
    start = time.monotonic()
    answer = []
    tags = Counter()
    for index,(yi,cross,low_y) in enumerate(joins):
        frame = ys[yi]
        neighbors = [set(n) for n in bases[frame[0]][0]]+[set() for _ in range(6)]
        for i,mask in enumerate((0,63,0,*cross,*endpoint_masks(frame))):
            for j in row(mask):
                neighbors[i].add(j)
                neighbors[j].add(i)
        witness = None
        for i,j in combinations(range(22),2):
            if j not in neighbors[i]:
                continue
            pages = sorted(neighbors[i]&neighbors[j])
            if len(pages) >= 4:
                witness = (index,i,j,tuple(pages[:4]))
                break
        if witness is None:
            raise ValueError("a necessary partial graph has no known-edge red book")
        _,i,j,pages = witness
        if len({i,j,*pages}) != 6 or len(pages) != 4:
            raise ValueError("literal book points are not distinct")
        if any(p not in neighbors[i] or p not in neighbors[j] for p in pages):
            raise ValueError("a required red page edge is absent")
        if any(n in range(16,22) for p in range(16,22) for n in neighbors[p]):
            raise ValueError("unknown internal-Y edges entered a witness")
        answer.append(witness)
        tags[(tuple(xs[frame[0]][1]),low_y)] += 1
        guard(start)
    return answer,sorted((l,low_y,n) for (l,low_y),n in tags.items())


def regenerate():
    xs = x_domain()
    bases = known(xs)
    ys = y_domain(xs,bases)
    rows = row_domain(xs,ys,bases)
    joins = join_domain(xs,ys,rows,bases)
    books,tags = witnesses(xs,ys,joins,bases)
    flags = tuple(l for l in product(range(2),repeat=5) if sum(l) <= 3)
    by_tag = Counter((item[0],item[1]) for item in xs)
    coverage = [{"repeated_SX":r,"low_T0_T1_T2_SY0_SY1":l,
                 "ordinary_Y_low_count":3-sum(l),
                 "labeled_ordinary_Y_choices":comb(6,3-sum(l)),
                 "X_interfaces":by_tag[r,l]} for r in range(2) for l in flags]
    values = {"X":xs,"Y_endpoints":ys,"XY_rows":rows,"XY_joins":joins,"red_books":books}
    return {"schema":1,"agent":"six-books-1","role":"researcher","scope":SCOPE,
            "normalized_repeated_SX_choices":2,"flag_words_per_core":len(flags),
            "labeled_low_placements_per_core":sum(comb(6,3-sum(l)) for l in flags),
            "tag_coverage":coverage,"canonical_ordered_SX_pairs":((15,51),(15,23)),
            "labeled_SX_pair_orbit_sizes":(90,120),
            "counts":{name:len(value) for name,value in values.items()},
            "domain_sha256":{name:digest(value) for name,value in values.items()},
            "domains":values,"join_tag_histogram":tags,
            "unblocked_partial_joins":len(joins)-len(books),
            "internal_Y_edges_used_in_witnesses":0}


def summary(record):
    answer = {key:value for key,value in record.items() if key != "domains"}
    answer["red_book_witnesses"] = record["domains"]["red_books"]
    return answer


def accept(text,expected):
    value = json.loads(text,object_pairs_hook=unique_object)
    if canonical(value) != canonical(expected):
        raise ValueError("complete independently regenerated record differs")


def controls(record):
    universe = set(range(6))
    subsets = tuple({i for i in range(6) if mask & (1 << i)} for mask in range(64))
    for a,b in product(subsets,repeat=2):
        if len(a&b) < max(0,len(a)+len(b)-6):
            raise ValueError("red outside minimum")
        if len((universe-a)&(universe-b)) < max(0,6-len(a)-len(b)):
            raise ValueError("blue outside minimum")
    fours = tuple(m for m in range(64) if m.bit_count() == 4)
    for intersection,prototype,size in ((2,(15,51),90),(3,(15,23),120)):
        images = set()
        for p in permutations(range(6)):
            images.add(tuple(sum(1 << p[j] for j in range(6) if m & (1 << j)) for m in prototype))
        target = {(a,b) for a,b in product(fours,repeat=2) if (a&b).bit_count() == intersection}
        if len(images) != size or images != target:
            raise ValueError("complete ordered SX orbit transport")
    frozen = json.loads(canonical(record))
    def damage(change):
        bad = deepcopy(frozen)
        change(bad)
        bad["counts"] = {name:len(value) for name,value in bad["domains"].items()}
        bad["domain_sha256"] = {name:digest(value) for name,value in bad["domains"].items()}
        return canonical(bad)
    damages = [
        damage(lambda r:r.__setitem__("scope","all 22-point hosts")),
        damage(lambda r:r.__setitem__("normalized_repeated_SX_choices",1)),
        damage(lambda r:r.__setitem__("labeled_low_placements_per_core",109)),
        damage(lambda r:r["tag_coverage"].pop()),
        damage(lambda r:r["tag_coverage"][0].__setitem__("X_interfaces",1)),
        damage(lambda r:r["domains"]["X"].pop()),
        damage(lambda r:r["domains"]["X"].append(deepcopy(r["domains"]["X"][0]))),
        damage(lambda r:r["domains"]["X"][0][2].__setitem__(6,7)),
        damage(lambda r:r["domains"]["Y_endpoints"].pop()),
        damage(lambda r:r["domains"]["Y_endpoints"][0].__setitem__(1,2)),
        damage(lambda r:r["domains"]["XY_rows"][0][1][0].pop()),
        damage(lambda r:r["domains"]["XY_joins"][0].__setitem__(2,1)),
        damage(lambda r:r["domains"]["red_books"][0][3].__setitem__(0,0)),
        damage(lambda r:r.__setitem__("internal_Y_edges_used_in_witnesses",1)),
        canonical(frozen)[:-1]+',"schema":1}',
        canonical(frozen)+' false',
    ]
    for text in damages:
        try:
            accept(text,record)
        except (ValueError,json.JSONDecodeError):
            continue
        raise ValueError("a damaged whole record was accepted")
    return {"six_point_subset_pairs":4096,"SX_orbit_transports":1440,
            "known_red_book_witnesses":len(record["domains"]["red_books"]),
            "rejected_damages":len(damages)}


if __name__ == "__main__":
    result = regenerate()
    if len(sys.argv) == 2 and sys.argv[1] == "--emit":
        print(canonical(result))
    elif len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        accept(Path(__file__).with_name("EXPECTED.json").read_text(),summary(result))
        print(canonical(controls(result)))
    elif len(sys.argv) == 3 and sys.argv[1] == "--check-full":
        accept(Path(sys.argv[2]).read_text(),result)
        print(canonical({"verified":True,"counts":result["counts"]}))
    elif len(sys.argv) == 2:
        accept(Path(sys.argv[1]).read_text(),summary(result))
        print(canonical({"verified":True,"counts":result["counts"]}))
    else:
        raise SystemExit("usage: verify.py EXPECTED.json | --emit | --self-test | --check-full PATH")
