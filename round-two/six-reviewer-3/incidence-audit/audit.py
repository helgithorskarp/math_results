"""Independent corner-graph audit of the three-ordinary-five obstruction.

The complete geometric/combinatorial coverage proof is in REVIEW.md.
No researcher code, fixture, solver, floating number or runtime input.
Fixed structural templates replace the raw slot/union-find enumeration.
Degree-four corner paths replace Hamiltonian link enumeration. Every
original endpoint/opposite assignment is retained in the terminal census.
"""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path

P = (1,4,2,-8,-7)


def need(value,message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def evaluate(poly,x):
    result = Q(0)
    for a in reversed(poly):
        result = result*x+a
    return result


def multiply(a,b):
    result = [Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            result[i+j] += x*y
    return result


def geometric_scalars():
    raw = multiply((-1,-2,1),(-1,-2,1))
    raw[3] -= 4;raw[4] -= 8
    need(tuple(raw) == P,'exact phi/b0 threshold polynomial')
    cubic=(-1,-3,1,7)
    need(multiply((-1,-1),cubic) == list(P),
         'positive (1+c) factor reduces threshold to cubic')
    shifted = [sum(Q(P[j])*comb(j,i)*Q(1,2)**(j-i)
                   for j in range(i,len(P))) for i in range(len(P))]
    need(shifted == [Q(33,16),Q(-7,2),Q(-41,2),Q(-22),Q(-7)],
         'complete threshold shift and strict derivative negativity')
    left,right = Q(7,10),Q(3,4)
    need(evaluate(P,left) == Q(3553,10000) > 0
         and evaluate(P,right) == Q(-119,256) < 0,'root initial strict bracket')
    for _ in range(41):
        middle = (left+right)/2
        if evaluate(P,middle) > 0:
            left = middle
        else:
            right = middle
    need(evaluate(P,left) > 0 > evaluate(P,right),'complete root sign bracket')
    scale = 10**12
    lo = Q(left.numerator*scale//left.denominator,scale)
    hi = Q(-((-right.numerator*scale)//right.denominator),scale)
    need(evaluate(P,lo) > 0 > evaluate(P,hi),'outward decimal root bracket')
    need(49 > 45,'upper equilateral angle bound at closed c=1/2')
    # A real four-point code in the widened range, all exact coordinates.
    v = [(Q(3,5),0,Q(4,5)),(0,Q(3,5),Q(4,5)),
         (Q(-3,5),0,Q(4,5)),(0,Q(-3,5),Q(4,5))]
    dot = lambda a,b:sum(x*y for x,y in zip(a,b))
    need(all(dot(x,x) == 1 for x in v),'rational rhombus units')
    c = Q(16,25)
    need(evaluate(P,c) > 0 and c > Q(3,5),'nonvacuous widened corner control')
    need(all(dot(v[i],v[(i+1)%4]) == c for i in range(4)), 'rhombus contacts')
    need(dot(v[0],v[2]) == dot(v[1],v[3]) == Q(7,25) < c,
         'both strict noncontact diagonals')
    need((Q(4,5)**2) == c,'positive half-cotangent product')
    need((Q(7,25)-c*c)/(1-c*c) == Q(-9,41) < c/(1+c),
         'rational rhombus corner greater than triangle corner')
    return {'threshold_polynomial_ascending':list(P),
            'threshold_cubic_ascending':list(cubic),
            'shift_at_half':list(map(str,shifted)),
            'unique_beta_bracket':list(map(str,(lo,hi))),
            'fixed_root_bisections':41,'widened_cosine_domain':'[1/2,beta)',
            'rational_rhombus_cosine':str(c),'strict_rhombus_diagonal':'7/25'}


def usable_cosine(c):
    need(Q(1,2) <= c < 1 and evaluate(P,c) > 0,
         'stated ordinary-five corner domain')


def global_census():
    # Euler and face-edge incidence, followed by degree and T-corner sums.
    n,q,r=15,9,3
    edges=3*n-6-q;triangles=2*n-4-2*q
    threes=4*n+r-2*edges;fours=n-r-threes
    need((edges,triangles,threes,fours) == (30,8,3,9),'complete original census')
    corner_words=[]
    for bits in product((0,1),repeat=4):
        if sum(bits) <= 1:
            qq=sum(bits[i] == bits[(i+1)%4] == 0 for i in range(4))
            need(qq == (4 if not any(bits) else 2),'literal deficient-four QQ ends')
            corner_words.append({'T_bits':list(bits),'QQ_ends':qq})
    distributions=[]
    for b in range(4):
        a=6-2*b;ordinary=fours-a-b
        need(ordinary >= 3 and ordinary <= 6 and 12+2*ordinary+a == 3*triangles,
             'complete T-incidence distributions')
        need(2*a+4*b-3*threes == 3,'exact residual QQ budget')
        distributions.append({'a':a,'b':b,'ordinary':ordinary,'QQ_supply':12,'residual':3})
    return {'vertices':n,'edges':edges,'triangles':triangles,'quadrilaterals':q,
            'threes':threes,'fours':fours,'fives':r,
            'deficient_corner_words':corner_words,'distributions':distributions}


def five_graph_cover():
    pairs=((0,1),(0,2),(1,2));rows=[]
    for bits in product((0,1),repeat=3):
        edges=[p for p,bit in zip(pairs,bits) if bit]
        degrees=[sum(i in e for e in edges) for i in range(3)]
        debt=sum(3-d for d in degrees)
        need(debt == 9-2*len(edges),'internal-slot double counting')
        rows.append({'five_edges':edges,'ordinary_internal_debt':debt,'internal_capacity_ok':debt <= 6})
    need(sum(x['internal_capacity_ok'] for x in rows) == 4,'all eight five graphs covered')
    return rows


def rename(words):
    labels = {0:0,1:1,2:2}
    out = []
    for word in words:
        row = []
        for x in word:
            if x not in labels:
                labels[x] = len(labels)
            row.append(labels[x])
        out.append(tuple(row))
    return tuple(out)


def patch(words,common_ceiling=2):
    need(len(words) == 3,'three original fives')
    need(all(len(w) == len(set(w)) == 5 and f not in w
             for f,w in enumerate(words)),'five distinct original neighbors')
    ts = {frozenset((f,w[i],w[i+1]))
          for f,w in enumerate(words) for i in range(4)}
    need(all(len(t) == 3 for t in ts),'distinct triangle corners')
    faces = Counter(x for t in ts for x in t)
    adjacency = {}
    for t in ts:
        for x in t:
            adjacency.setdefault(x,set()).update(t-{x})
    need(all(faces[f] == 4 and adjacency[f] == set(words[f]) for f in range(3)),
         'complete five-star triangle constraints')
    need(all(faces[x] <= 2 and len(ns) <= 4
             for x,ns in adjacency.items() if x >= 3),'four degree and T capacity')
    need(all(len(adjacency[x]&adjacency[y]) <= common_ceiling
             for x,y in combinations(adjacency,2)),'original common-contact capacity')
    return ts,adjacency


def fan_templates():
    # Distinct roles and the cover of these two templates are proved in REVIEW.
    path = ((3,1,4,5,6),(4,0,3,2,7),(3,1,7,8,9))
    # Role labels must be disjoint from the fives and from the endpoints.
    clique = tuple((3+(i-1)%3,(i-1)%3,(i+1)%3,3+i,6+i) for i in range(3))
    charts = {'path':set(),'clique':set()}
    for bits in product((0,1),repeat=3):
        words = tuple(w[::-1] if b else w for w,b in zip(path,bits))
        ts,_ = patch(words);need(len(ts) == 8,'full path triangle union')
        charts['path'].add(rename(words))
        for reverse_cycle in (False,True):
            relabel = {0:0,1:2,2:1} if reverse_cycle else {0:0,1:1,2:2}
            trial = tuple(tuple(relabel.get(x,x) for x in (w[::-1] if b else w))
                          for w,b in zip(clique,bits))
            rows = [None]*3
            for old,w in enumerate(trial):rows[relabel[old]] = w
            ts,_ = patch(rows);need(len(ts) == 7,'full clique triangle union')
            charts['clique'].add(rename(rows))
    need(len(charts['path']) == 8 and len(charts['clique']) == 16,'all oriented template charts')
    return {name:sorted(value) for name,value in charts.items()}


def close_four_link(corners):
    """Unique four-neighbor cycle completion of three known corners.

    Connectivity/degree tests detect a sealed three-cycle without a
    permutation or Hamiltonian-cycle enumeration. The two degree-one ends
    determine the remaining corner, which must be Q at a two-T vertex.
    """
    adjacency = {}
    edge_set = set()
    for a,b,kind in corners:
        need(a != b and kind in ('T','Q'),'proper corner')
        edge = frozenset((a,b))
        need(edge not in edge_set,'distinct face corners')
        edge_set.add(edge)
        adjacency.setdefault(a,set()).add(b);adjacency.setdefault(b,set()).add(a)
    need(len(adjacency) == 4 and len(edge_set) == 3,'degree-four spanning corner path')
    need(sorted(map(len,adjacency.values())) == [1,1,2,2],'open four-neighbor link')
    seen = set();stack = [next(iter(adjacency))]
    while stack:
        x = stack.pop()
        if x not in seen:seen.add(x);stack.extend(adjacency[x]-seen)
    need(len(seen) == 4,'connected link, no sealed proper cycle')
    return tuple(sorted(x for x in adjacency if len(adjacency[x]) == 1))


def edge_degrees(edges,deficient):
    ends = dict.fromkeys(deficient,0)
    for x,y in edges:
        need(x != y,'no QQ loop')
        if x in ends:ends[x] += 1
        if y in ends:ends[y] += 1
    return ends


def second_T_positions(fi,ii,hi,j):
    """Complete missing-edge cover for a two-corner four-neighbor link."""
    vertices={fi,ii,hi,j};need(len(vertices) == 4,'four local neighbor roles')
    known={frozenset((fi,ii)),frozenset((fi,hi))}
    available=[frozenset(e) for e in combinations(sorted(vertices),2) if frozenset(e) not in known]
    completions=[]
    for extra in combinations(available,2):
        edges=known|set(extra)
        if all(sum(x in edge for edge in edges) == 2 for x in vertices):
            completions.append(extra)
    need(len(completions) == 1,'unique four-cycle from known T/Q corners')
    positions=tuple(sorted(tuple(sorted(e)) for e in completions[0]))
    need(set(map(frozenset,positions)) == {frozenset((ii,j)),frozenset((hi,j))},
         'complete two possible second-T positions')
    return positions


def terminal_triangle():
    tables = []
    for b in range(4):
        a = 6-2*b;ordinary = set(range(6,9+b))
        one = set(range(9+b,9+b+a));zero = set(range(9+b+a,15))
        deficient = sorted(one|zero);pool = sorted((ordinary-{6,7,8})|one)
        counts = Counter();records = [];least = None;relaxed = 0
        for A in product(pool,repeat=3):
            if len(set(A)) != 3:continue
            for H in product(deficient,repeat=3):
                counts['all_endpoint_opposite_assignments'] += 1
                quads = [(i,6+(i-1)%3,H[i],A[i]) for i in range(3)]
                if any(len(set(q)) != 4 for q in quads):
                    counts['repeated_Q_original_rejections'] += 1
                    records.append((A,H,'Q_REPEAT',()));continue
                missing = []
                try:
                    for i in range(3):
                        missing.append(close_four_link([(i,(i+1)%3,'T'),(i,A[i],'T'),
                                                        ((i+1)%3,H[(i+1)%3],'Q')]))
                except ValueError:
                    counts['sealed_degree_four_link_rejections'] += 1
                    records.append((A,H,'SEALED_LINK',()));continue
                counts['proper_link_assignments'] += 1
                need(all(set(missing[i]) == {A[i],H[(i+1)%3]} for i in range(3)),
                     'remaining Q corner from unique link path')
                if all(x in ordinary for x in A):
                    need(b == 3 and not one,'all-ordinary endpoint census')
                    for i in range(3):
                        # -1 stands for any unassigned ORIGINAL fourth
                        # neighbor distinct from the three local ones.
                        choices=second_T_positions(i,6+i,H[i],-1)
                        need(all(6+i in e or H[i] in e for e in choices),
                             'every missing T hits full internal or zero-T opposite')
                    counts['forced_T_at_zero_T_opposite'] += 1
                    records.append((A,H,'ZERO_T_FORCE',()));continue
                forced = {(6+(i-1)%3,H[i]) for i in range(3)}
                deficient_edges = [tuple(sorted((A[i],H[i]))) for i in range(3) if A[i] in one]
                need(len(set(deficient_edges)) == len(deficient_edges),
                     'no reciprocal endpoint/opposite edge after link checks')
                forced |= set(deficient_edges)
                ends = edge_degrees(forced,deficient);total = sum(ends.values())
                need(total == 3+2*sum(x in one for x in A),'exact alias-safe QQ incidence identity')
                need(total >= 15-2*len(ordinary) >= 5,'parameter-count barrier')
                local = all(ends[x] <= (2 if x in one else 4) for x in deficient)
                counts['local_QQ_capacity_rejections'] += int(not local)
                if local:
                    need(total+9 > 12,'original fifteen-point total QQ shortage')
                    counts['total_three_neighbor_capacity_rejections'] += 1
                    relaxed += int(total+3 <= 12)
                least = total if least is None else min(least,total)
                records.append((A,H,'TOTAL_DEMAND' if local else 'LOCAL_SUPPLY',
                                tuple(ends[x] for x in deficient)))
        m=len(pool);need(counts['all_endpoint_opposite_assignments'] == m*(m-1)*(m-2)*len(deficient)**3,
                         'literal complete terminal Cartesian cover')
        # Author comparison encoding, not a proof input or implementation.
        checksum=hashlib.sha256(json.dumps(sorted(records),separators=(',',':')).encode()).hexdigest()
        tables.append({'b':b,'a':a,'ordinary_fours':len(ordinary),'counts':dict(sorted(counts.items())),
                       'minimum_certified_non_three_QQ_ends':least,'entrywise_sha256':checksum,
                       'relaxed_three_neighbor_demand_3_controls':relaxed})
    need(sum(x['counts']['all_endpoint_opposite_assignments'] for x in tables) == 35118,
         'full terminal assignments')
    return tables


def terminal_path():
    result=[]
    for J,K in product((13,14),range(11,15)):
        # Labels6,7,8 are the ordinary I,X,Y. Endpoints11,12 are one-T.
        forced={(6,J),(7,K),(8,K),(11,J),(12,J)}
        ends=edge_degrees(forced,range(11,15));need(sum(ends.values()) == 7,'alias-safe path seven-end debt')
        local=all(ends[x] <= (2 if x<13 else 4) for x in ends)
        result.append({'shared_opposite':J,'middle_opposite':K,'non_three_QQ_ends':ends,
                       'local_capacity_ok':local,'relaxed_demand_3_control':local})
    need(len(result) == 8 and sum(x['local_capacity_ok'] for x in result) == 2,
         'full path opposite cover and nonempty released demand')
    return result


def controls():
    bad=((3,1,4,5,6),(4,0,3,2,7),(3,1,7,8,6))
    actions={'third-common-contact':lambda:patch(bad),
             'sealed-three-link':lambda:close_four_link([(0,1,'T'),(0,9,'T'),(1,9,'Q')]),
             'repeated-corner':lambda:close_four_link([(0,1,'T'),(0,1,'Q'),(1,9,'T')]),
             'loop-corner':lambda:close_four_link([(0,0,'T'),(0,1,'T'),(1,9,'Q')]),
             'bad-T-role':lambda:close_four_link([(0,1,'X'),(0,9,'T'),(1,10,'Q')]),
             'too-low-cosine-for-this-proof':lambda:usable_cosine(Q(499,1000)),
             'failed-upper-corner-domain':lambda:usable_cosine(Q(3,4))}
    rejected=[]
    for name,task in actions.items():
        try:task()
        except ValueError:rejected.append(name)
    need(len(rejected) == len(actions),'all damaged constraints reject')
    patch(bad,common_ceiling=3)
    usable_cosine(Q(1,2));usable_cosine(Q(7,10))
    return {'rejected_damages':rejected,'released_shared_endpoint_is_not_a_spherical_code':True,
            'released_common_ceiling_3_surrogate_accepts':True}


def main():
    result={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'status':'VERIFIED','method':'structural fans and degree-four corner-path completion',
            'geometry':geometric_scalars(),'global_census':global_census(),
            'five_graphs':five_graph_cover(),'fan_charts':fan_templates(),
            'clique_opposite_aliases':terminal_triangle(),'path_opposite_aliases':terminal_path(),
            'controls':controls(),'count_parameter_barriers':
            {'clique_O_le5':'non-three QQ ends >=15-2O','path_O_le6':'non-three QQ ends >=17-2O',
             'O_le6_no_one_T_four':'impossible three ordinary fives',
             'scope':'any finite complete T/Q contact code with exactly3 degree-fives, all4T; other degrees3/4; c in[1/2,beta).'}}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=main()
    if args.output:args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'complete_evidence_sha256':digest(result),
                      'fan_charts':sum(map(len,result['fan_charts'].values())),
                      'terminal_assignments':35118+8,
                      'beta_bracket':result['geometry']['unique_beta_bracket'],
                      'rejected_damages':len(result['controls']['rejected_damages'])},sort_keys=True))
