#!/usr/bin/env python3
"""Exact evidence for boundary_exclusion.md; Python standard library only."""
import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
from forest_constraints import model, evaluate
from verify import graph, require, hoffman_singleton_edges, check_girth_and_identities

HERE = Path(__file__).resolve().parent


def lower_certificate():
    """Replay only m>4, without either imposed edge bound or disabled assertions."""
    types, edges, equalities, erhs, inequalities, irhs = model(edge_bounds=False)
    data = json.loads((HERE/'forest_lower_certificate.json').read_text())
    size = len(types)+len(edges)
    require((len(types),len(edges),len(equalities),len(inequalities))
            == (72,1638,222,222), 'unrestricted certificate dimensions')
    coefficients = [Fraction(0)]*size
    bound = Fraction(0)
    for name, rows, rhs in [('equality_multipliers',equalities,erhs),
                            ('inequality_multipliers',inequalities,irhs)]:
        seen = set()
        for row, numerator in data[name]:
            require(type(row) is int and 0 <= row < len(rows) and row not in seen,
                    'malformed multiplier index')
            seen.add(row)
            multiplier = Fraction(numerator,data['denominator'])
            require(name == 'equality_multipliers' or multiplier <= 0,
                    'inequality multiplier sign')
            bound += multiplier*rhs[row]
            for column, value in rows[row].items():
                coefficients[column] += multiplier*value
    objective = [Fraction(0)]*size
    allowed = [True]*size
    for i,(degree,neighbors) in enumerate(types):
        if degree == 8:
            objective[i] = Fraction(neighbors[2],2)
            allowed[i] = neighbors[1]+2*neighbors[2] == 5
    error = max([Fraction(0)]+[coefficients[i]-objective[i]
                              for i in range(size) if allowed[i]])
    corrected = bound-428*error
    require(bound == Fraction(data['uncorrected_bound']), 'certificate raw bound')
    require(error == Fraction(data['max_coefficient_error']), 'certificate exact error')
    require(corrected == Fraction(data['corrected_bound'])
            == Fraction(4120933,1000000) and corrected > 4,
            'certificate corrected strict bound')
    return {'variables':size,'equality_rows':len(equalities),
            'inequality_rows':len(inequalities),'edge_bounds_added':False,
            'uncorrected_bound':str(bound),'coefficient_error':str(error),
            'corrected_bound':str(corrected),
            'certificate_sha256':hashlib.sha256((HERE/'forest_lower_certificate.json').read_bytes()).hexdigest()}


def local_checks():
    signs = []
    negatives = set()
    for degree in (6,7):
        for c in range(degree+1):
            for a in range(degree-c+1):
                b = degree-c-a
                eps = b+2*c-(8 if degree == 6 else 7)
                if degree == 6:
                    require((c-3)*eps >= 0, 'six-vertex sign')
                    if c == 5:
                        require(eps >= 2 and (c-3)*eps >= 4, 'five-block positive term')
                elif (c-3)*eps < 0:
                    negatives.add((c,eps))
                signs.append((degree,a,b,c,eps))
    require(negatives == {(1,1),(2,1),(2,2)}, 'complete negative type list')
    for c in range(7):
        r = c-3
        require((c-3)*(c-4)//2+r >= comb(max(r,0)+1,2), 'six charge inequality')
    require(all((c-1)*(c-2)//2 >= 0 for c in range(8)), 'seven charge nonnegativity')
    require(all(a+b < 11 for a,b in product(range(6),repeat=2)), 'c2 epsilon2 exclusion')
    require(24*7+13*16-13*5-17*8-24*7 == 7, 'epsilon sum arithmetic')
    for h in range(3):
        require(5*h+8*(3+h)+7*(5-2*h) == 59-h, 'high epsilon balance')
    for m in range(8):
        require((39+2*m)-3*17 == 2*m-12, 'six surplus')
        require((22-3*m)+(2*m-12) == 10-m, 'charge total')
    return {'local_neighbor_types_checked':len(signs),
            'negative_seven_types_before_c2_epsilon2_exclusion':sorted(map(list,negatives))}


def four_configurations(r):
    """All labeled-block systems, with points normalized by block membership."""
    memberships = [s for k in range(2,r+1) for s in combinations(range(r),k)]
    pair_index = {p:i for i,p in enumerate(combinations(range(r),2))}
    masks = [sum(1 << pair_index[p] for p in combinations(s,2)) for s in memberships]

    def visit(start,used,degrees,chosen):
        union_size = 4*r-sum(len(memberships[i])-1 for i in chosen)
        if union_size <= 13:
            blocks = [set() for _ in range(r)]
            point = 0
            for i in chosen:
                for b in memberships[i]:
                    blocks[b].add(point)
                point += 1
            for b in range(r):
                for _ in range(4-len(blocks[b])):
                    blocks[b].add(point)
                    point += 1
            require(point == union_size, 'point reconstruction')
            yield blocks
        for i in range(start,len(memberships)):
            s = memberships[i]
            if used & masks[i] or any(degrees[b] >= 4 for b in s):
                continue
            ds = degrees.copy()
            for b in s:
                ds[b] += 1
            yield from visit(i+1,used | masks[i],ds,chosen+[i])
    yield from visit(0,0,[0]*r,[])


def check_four_configurations():
    records = []
    for r in range(6):
        count = max_disjoint = max_eligible = with_triple = 0
        stream = hashlib.sha256()
        for blocks in four_configurations(r):
            count += 1
            require(all(len(b) == 4 for b in blocks), 'four-block size')
            require(all(len(a & b) <= 1 for a,b in combinations(blocks,2)),
                    'four-block pair multiplicity')
            pairs = [(a,b) for a,b in combinations(range(r),2) if not blocks[a] & blocks[b]]
            triples = [t for t in combinations(range(r),3)
                       if all(not blocks[a] & blocks[b] for a,b in combinations(t,2))]
            eligible = []
            for a,b in pairs:
                rest = set(range(13))-blocks[a]-blocks[b]
                if any(all(len(set(z) & blocks[c]) <= 1 for c in range(r) if c not in (a,b))
                       for z in combinations(sorted(rest),3)):
                    eligible.append((a,b))
            require(len(pairs) <= 3, 'disjoint-pair upper bound')
            if triples:
                with_triple += 1
                require(len(triples) == 1 and not eligible, 'A1 excludes every eligible A2 pair')
                original = triples[0]
                remainder = set(range(13))-set().union(*(blocks[i] for i in original))
                require(len(remainder) == 1, 'A1 singleton remainder')
                for i in range(r):
                    if i not in original:
                        require(remainder <= blocks[i] and all(len(blocks[i] & blocks[j]) == 1 for j in original),
                                'remaining large block intersects triple')
            max_disjoint = max(max_disjoint,len(pairs))
            max_eligible = max(max_eligible,len(eligible))
            stream.update((json.dumps([sorted(b) for b in blocks],separators=(',',':'))+'\n').encode())
        records.append({'four_blocks':r,'incidence_patterns':count,
                        'max_disjoint_pairs':max_disjoint,'max_eligible_A2_pairs':max_eligible,
                        'patterns_with_A1_triple':with_triple,'incidence_sha256':stream.hexdigest()})
    require([r['incidence_patterns'] for r in records] == [1,1,2,9,71,546], 'complete four-block inventory')
    return records


def small_packings():
    ground = set(range(5))
    pairs = [set(p) for p in combinations(range(5),2)]
    counts = [0]*11
    for mask in range(1 << len(pairs)):
        selected = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        if all(len((ground-a) & (ground-b)) <= 1 for a,b in combinations(selected,2)):
            require(all(not a & b for a,b in combinations(selected,2)), 'Fact I complement identity')
            counts[len(selected)] += 1
    require(counts == [1,10,15]+[0]*8, 'Fact I packing bound and positive controls')
    four = set(range(4))
    for a,b in product(range(4),repeat=2):
        overlap = len((four-{a}) & (four-{b}))
        require(overlap == (3 if a == b else 2), 'Fact II singleton complements')
    triples = [t for t in combinations(range(4),3)]
    require(all(len(set(a) & set(b)) == 2 for a,b in combinations(triples,2)), 'Fact II distinct triple intersection')
    return {'fact_I_counts':counts,'fact_II_ordered_singleton_pairs':16}


def inventories_and_bounds():
    records = []
    # Charges for six c=4,5,6 and seven c=4,5,6,7.
    types = [(6,4,1),(6,5,3),(6,6,6),(7,4,3),(7,5,6),(7,6,10),(7,7,15)]
    for m in (5,6,7):
        budget = 10-m
        inventories = []
        def rec(i,left,counts):
            if i == len(types):
                inventories.append(tuple(counts));return
            for n in range(left//types[i][2]+1):
                rec(i+1,left-n*types[i][2],counts+[n])
        rec(0,budget,[])
        for counts in inventories:
            require(not any(counts[i] for i in (2,4,5,6)), 'forbidden c>=6 or seven c>=5')
            if counts[1] == 0:
                require(counts[0]+counts[3] <= 5 and counts[3] <= 1, 'four-only inventory')
                require(6 < 21-2*m and 4 < 21-2*m, 'four-only strict contradiction')
            else:
                require(counts[1] == 1 and counts[3] == 0 and counts[0] <= 7-m, 'one-five inventory')
                t = counts[0]
                for eps in (2,3):
                    for a1 in range(2*t+1):
                        for a2prime in range(10):
                            if a1+a2prime > 9-eps:
                                continue
                            for a2other in range(2*comb(t,2)+1):
                                require(2*a1+a2prime+a2other < 21-2*m+2*eps,
                                        'one-five capacity contradicts epsilon balance')
        max_t = 7-m
        records.append({'m':m,'charge_budget':budget,'large_inventories':len(inventories),
                        'one_five_max_fours':max_t,
                        'one_five_negative_weight_upper':7+max_t*(max_t+1),
                        'one_five_negative_weight_required':25-2*m})
    require([r['large_inventories'] for r in records] == [12,9,6], 'inventory count')
    return records


def graph_controls():
    hs = hoffman_singleton_edges()
    fixture = json.loads((HERE/'lower_bound_54_185.json').read_text())
    controls = [graph(50,sorted(hs-deleted)) for deleted in (set(),{(0,1)},{(0,1),(2,3)})]
    controls.append(graph(fixture['n'],fixture['edges']))
    result = []
    for G in controls:
        e = check_girth_and_identities(G)
        d = list(map(len,G)); n = len(G); maximum = max(d)
        F = [{u for u in range(n) if u != v and u not in G[v] and not G[u] & G[v]}
             for v in range(n)]
        T = {v for v in range(n) if d[v] == maximum and not F[v]}
        single = double = 0
        for v in range(n):
            deficit = maximum-d[v]
            for t in T:
                actual = sum(t in G[u] for u in F[v])
                require(actual == deficit*(t not in G[v]), 'definition-level cover identity')
            if T and deficit == 1: single += 1
            if T and deficit == 2: double += 1
        result.append({'n':n,'edges':e,'sinks':len(T),'single_cover_rows':single,'double_cover_rows':double})
        if all(x in (6,7,8) for x in d):
            sizes = tuple(d.count(j) for j in (6,7,8))
            ts,es,eq,eb,ub,bb = model(sizes,edge_bounds=False)
            ti = {t:i for i,t in enumerate(ts)}
            vt = [ti[(d[v],tuple(sum(d[u] == j for u in G[v]) for j in (6,7,8)))] for v in range(n)]
            variables = [0]*(len(ts)+len(es)); ei = {p:i+len(ts) for i,p in enumerate(es)}
            for t in vt: variables[t] += 1
            for u in range(n):
                for v in G[u]:
                    if u < v:
                        a,b = sorted((vt[u],vt[v])); variables[ei[a,b]] += 2 if a == b else 1
            require(all(evaluate(r,variables) == b for r,b in zip(eq,eb)), 'certificate equality control')
            require(all(evaluate(r,variables) <= b for r,b in zip(ub,bb)), 'certificate inequality control')
            require(sum(variables) <= n+2*e, 'certificate mass bound control')
    require(sum(x['single_cover_rows'] for x in result) == 50 and
            sum(x['double_cover_rows'] for x in result) == 2, 'nonvacuous cover controls')
    return result


def main():
    result = {'verified':True,'claim':'No order54 size187 girth5 graph has n8=13',
              'remaining_z':list(range(13)),'lower_certificate':lower_certificate(),
              'local_checks':local_checks(),'four_block_patterns':check_four_configurations(),
              'small_packings':small_packings(),'large_inventories':inventories_and_bounds(),
              'graph_controls':graph_controls(),'new_solver_refutations':0,
              'prior_forest_SAT_exclusions_used':False}
    expected = HERE/'boundary_exclusion_expected.json'
    if expected.exists():
        require(json.loads(expected.read_text()) == result, 'expected record differs')
    print(json.dumps(result,indent=2,sort_keys=True))
    return result


if __name__ == '__main__':
    main()
