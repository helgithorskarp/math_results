#!/usr/bin/env python3
"""six-reviewer-4 independent local13 Book Ramsey audit.

Local cores use cubic-column subset products, not low-pair recursion.
Slack graphs use labeled-stub pairings, not integer edge/star recursion.
Three/four-low rows are excluded by universal analytic forms; only
zero-low rows use untrusted external vectors and an integer census.
"""
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, product
from math import comb, gcd
from pathlib import Path
import argparse
import hashlib
import json
import sys

P = tuple(combinations(range(6), 2))
INDEX = {e: i for i, e in enumerate(P)}
E = tuple(combinations(range(10), 2))
ESLOT = {e: i for i, e in enumerate(E)}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def compact(obj):
    return (json.dumps(obj, separators=(',', ':'))+'\n').encode()

def frows(mask):
    rows = [0]*6
    for i, (u, v) in enumerate(P):
        if mask >> i & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows

def transform(mask, point):
    return sum(1 << INDEX[tuple(sorted((point[u], point[v])))]
               for i, (u, v) in enumerate(P) if mask >> i & 1)

def census():
    domain = set()
    visits = 0
    for edges in combinations(range(15), 5):
        visits += 1
        mask = sum(1 << i for i in edges)
        rows = frows(mask)
        if max(r.bit_count() for r in rows) <= 3 and all(
                (rows[u] & rows[v]).bit_count() <= 1
                for u, v in P if rows[u] >> v & 1):
            domain.add(mask)
    need(visits == comb(15, 5), 'all fixed-cardinality F edge sets')
    swaps = []
    for i in range(5):
        p = list(range(6))
        p[i], p[i+1] = p[i+1], p[i]
        swaps.append(p)
    unseen = set(domain)
    catalog = []
    while unseen:
        rep = min(unseen)
        todo, orbit = deque([rep]), {rep}
        while todo:
            mask = todo.popleft()
            for p in swaps:
                image = transform(mask, p)
                need(image in domain, 'orbit stays in complete necessary domain')
                if image not in orbit:
                    orbit.add(image)
                    todo.append(image)
        need(orbit <= unseen, 'orbit partition disjoint')
        unseen -= orbit
        rows = frows(rep)
        lam = [3-r.bit_count() for r in rows]
        choices = [tuple(sum(1 << l for l in block)
                         for block in combinations(range(4), amount)) for amount in lam]
        observed = Counter()
        column_tables = 0
        for columns in product(*choices):
            column_tables += 1
            low = [sum(1 << i for i, col in enumerate(columns) if col >> l & 1)
                   for l in range(4)]
            if any(x.bit_count() != 2 for x in low):
                continue
            stars = tuple(tuple(i for i in range(6) if mask >> i & 1) for mask in low)
            if any(rows[u] >> v & 1 for u, v in stars):
                continue
            full = matrix(rep, stars)
            if any(x < 0 for row in full for x in row):
                continue
            observed[tuple(sorted(stars))] += 1
        profiles = []
        for stars, amount in sorted(observed.items()):
            permutations = 24
            for multiplicity in Counter(stars).values():
                divisor = 1
                for i in range(2, multiplicity+1):
                    divisor *= i
                permutations //= divisor
            need(amount == permutations, 'column-product census preserves every ordered low labeling')
            profiles.append({'stars': stars, 'ordered_low_multiplicity': amount})
        catalog.append({'F_mask': rep, 'orbit_size': len(orbit), 'lambda': lam,
                        'column_tables': column_tables, 'profiles': profiles})
    return domain, visits, catalog

def matrix(mask, stars):
    f = frows(mask)
    local = [sum(1 << (4+i) for i in star) for star in stars]
    local += [sum(1 << (4+j) for j in range(6) if f[i] >> j & 1) |
              sum(1 << l for l, star in enumerate(stars) if i in star) for i in range(6)]
    h = [x.bit_count() for x in local]
    need(h == [2]*4+[3]*6, 'literal local degree sequence')
    return [[h[i]+2 if i == j else h[i]+h[j]-(5 if local[i] >> j & 1 else 2)-
             (local[i] & local[j]).bit_count() for j in range(10)] for i in range(10)]

def row_data(mask, stars, row):
    s0 = matrix(mask, stars)
    a = [int(i in row) for i in range(10)]
    base = [[s0[i][j]-a[i]*a[j] for j in range(10)] for i in range(10)]
    degrees = [sum(r)-4*r[i] for i, r in enumerate(base)]
    lam = [3-r.bit_count() for r in frows(mask)]
    expected = [2-2*a[i] for i in range(4)] + [2+lam[i]-2*a[4+i] for i in range(6)]
    need(degrees == expected and min(degrees) >= 0 and sum(degrees) == 16,
         'independent incident-degree bridge')
    need(sum(base[i][i] for i in range(10)) == 40, 'ten remaining row lengths four')
    return base, tuple(degrees)

def qform(mat, q):
    return sum(mat[i][i]*q[i]*q[i] for i in range(10)) + 2*sum(
        mat[i][j]*q[i]*q[j] for i, j in E)

def row_cover(catalog):
    zero, analytic, counts = [], [], Counter()
    for core in catalog:
        mask = core['F_mask']
        for profile in core['profiles']:
            stars = profile['stars']
            s0 = matrix(mask, stars)
            for row in combinations(range(10), 6):
                if any(s0[i][j] < 1 for i, j in combinations(row, 2)):
                    continue
                k = sum(i < 4 for i in row)
                counts[k] += 1
                need(k in (0,3,4), 'all selected-row low counts covered')
                base, degrees = row_data(mask, stars, row)
                data = {'F_mask': mask, 'stars': stars, 'row': row,
                        'slack_degrees': degrees}
                if k == 0:
                    need(row == tuple(range(4,10)), 'unique zero-low row')
                    zero.append(data)
                elif k == 3:
                    q = [2 if i in row else -3 for i in range(4)]+[0]*6
                    p = [4*x-1 for x in q]
                    potential = [25 if i < 4 and i not in row else 1 for i in range(10)]
                    need(qform(base,q) == 0 and sum(q[i]*degrees[i] for i in range(10)) == -6,
                         'three-low universal zero-form support')
                    need(all(2*p[i]*p[j] == potential[i]+potential[j] for i,j in E
                             if degrees[i] and degrees[j] and base[i][j]),
                         'three-low quadratic slack coefficients equal incident-degree potentials')
                    need(qform(base,p)-sum(c*d for c,d in zip(potential,degrees)) == -32,
                         'three-low constant negative polynomial')
                    data.update({'low_count': k, 'vector': p, 'degree_potentials':potential,
                                 'universal_form': -32})
                    analytic.append(data)
                else:
                    x = min(i for i in range(6) if 4+i not in row)
                    q = [3 if x in stars[l] else -9 for l in range(4)] + [8 if i == x else 0 for i in range(6)]
                    need(all(degrees[l] == 0 for l in range(4)), 'four-low has no incident low slack')
                    need(all(q[i]*q[j] == 0 for i,j in E if degrees[i] and degrees[j]),
                         'four-low quadratic slack polynomial vanishes')
                    need(qform(base,q) == -112, 'four-low universal negative form')
                    data.update({'low_count': k, 'vector': q, 'degree_potentials':[0]*10,
                                 'universal_form': -112})
                    analytic.append(data)
    return zero, analytic, counts

def odd_factorial(n):
    value = 1
    for i in range(1,n+1,2):
        value *= i
    return value

@lru_cache(maxsize=8)
def paired_stubs(degrees):
    labels = tuple(i for i, count in enumerate(degrees) for _ in range(count))
    need(len(labels) == 16, 'sixteen distinct incident stubs')
    slots = [[-1 if labels[i] == labels[j] else ESLOT[tuple(sorted((labels[i],labels[j])))]
              for j in range(16)] for i in range(16)]
    weights = [0]*45
    graphs = set()
    accounted = loopless = 0
    def visit(left):
        nonlocal accounted, loopless
        if not left:
            accounted += 1
            loopless += 1
            graphs.add(bytes(weights))
            return
        firstbit = left & -left
        first = firstbit.bit_length()-1
        others = left ^ firstbit
        candidates = others
        descendants = odd_factorial(left.bit_count()-3)
        while candidates:
            secondbit = candidates & -candidates
            candidates ^= secondbit
            second = secondbit.bit_length()-1
            edge = slots[first][second]
            if edge == -1:
                accounted += descendants
                continue
            weights[edge] += 1
            visit(others ^ secondbit)
            weights[edge] -= 1
    visit((1 << 16)-1)
    need(accounted == odd_factorial(15) == 2027025, 'all perfect labeled matchings accounted for')
    for graph in graphs:
        total = [0]*10
        for (u,v), w in zip(E,graph):
            total[u] += w
            total[v] += w
        need(tuple(total) == degrees, 'terminal multigraph degree recovery')
    print('stub domain complete '+str(degrees)+' graphs='+str(len(graphs)),file=sys.stderr,flush=True)
    return tuple(sorted(graphs)), loopless

def project(q):
    need(len(q) == 10 and all(type(x) is int for x in q) and any(q), 'integer witness dimensions')
    total = sum(q)
    p = [10*x-total for x in q]
    divisor = gcd(*p)
    need(divisor > 0, 'constant vector cannot prove a negative form')
    p = [x//divisor for x in p]
    if next(x for x in p if x) < 0:
        p = [-x for x in p]
    need(sum(p) == 0, 'primitive zero-sum projection')
    return p

def run(path, export=None, compare=None):
    domain, visits, catalog = census()
    zero, analytic, row_counts = row_cover(catalog)
    cert = json.loads(path.read_text())
    need(cert.get('dimension') == 10, 'certificate ambient dimension')
    pools = {}
    for record in cert['records']:
        index = record['index']
        need(type(index) is int and index not in pools and record['vectors'], 'distinct nonempty certificate records')
        pools[index] = [project(q) for q in record['vectors']]
    need(set(range(len(zero))) <= set(pools), 'every independently generated zero-low configuration has witnesses')
    cases, selected, all_hash = [], [], hashlib.sha256()
    stub_domains = {}
    witness_hash = hashlib.sha256()
    for index, case in enumerate(zero):
        base, degrees = row_data(case['F_mask'],case['stars'],case['row'])
        graphs, loopless = paired_stubs(degrees)
        stub_domains[degrees] = {'degrees':degrees,'accounted_labeled_matchings':2027025,
                                'loopless_labeled_matchings':loopless,'weighted_multigraphs':len(graphs)}
        states = []
        for graph in graphs:
            if any(w > base[u][v] for (u,v),w in zip(E,graph)):
                continue
            states.append(tuple((u,v,w) for (u,v),w in zip(E,graph) if w))
        digest, used, maxform = hashlib.sha256(), set(), None
        pool = pools[index]
        plans = [(4*sum(x*x for x in q),tuple((i,j,2*q[i]*q[j]) for i,j in E if q[i] and q[j])) for q in pool]
        for edges in sorted(states):
            r = [x[:] for x in base]
            for u,v,w in edges:
                r[u][v] -= w
                r[v][u] -= w
            need(all(r[i][i] == 4 and sum(r[i]) == 16 for i in range(10)), 'residual uniform diagonal and constant mode')
            need(all(x >= 0 for row in r for x in row), 'residual necessary entry capacities')
            chosen = None
            for vi,(constant,terms) in enumerate(plans):
                value = constant+sum(r[i][j]*w for i,j,w in terms)
                if value < 0:
                    chosen = vi,value
                    break
            need(chosen is not None, 'every necessary residual matrix has a negative zero-sum integer form')
            vi,value = chosen
            used.add(vi)
            maxform = value if maxform is None else max(value,maxform)
            data = compact([index,edges,r])
            digest.update(data)
            all_hash.update(data)
            witness_hash.update(compact([index,edges,pool[vi],value]))
        chosen_pool = [pool[i] for i in sorted(used)]
        selected.append({'index':index,'vectors':chosen_pool})
        cases.append(dict(case,index=index,states=len(states),state_matrix_sha256=digest.hexdigest(),
                          vectors_used=len(chosen_pool),largest_chosen_negative_form=maxform))
    result = {'agent':'six-reviewer-4','role':'independent mathematical reviewer','target_height':8170,
              'author_modules_imported':False,'expected_records_select_domain':False,
              'five_edge_F_subsets':visits,'eligible_labeled_F':len(domain),
              'F_domain_sha256':hashlib.sha256(''.join(str(x)+'\n' for x in sorted(domain)).encode()).hexdigest(),
              'F_orbits':len(catalog),'column_tables_inspected':sum(r['column_tables'] for r in catalog),
              'normalized_profiles':sum(len(r['profiles']) for r in catalog),
              'labeled_local_cores':sum(r['orbit_size']*sum(p['ordered_low_multiplicity'] for p in r['profiles']) for r in catalog),
              'core_catalog':catalog,'admissible_six_rows':sum(row_counts.values()),
              'selected_rows_by_low_count':dict(sorted(row_counts.items())),
              'analytically_closed_rows':analytic,'zero_low_cases':cases,
              'finite_matrices':sum(r['states'] for r in cases),'negative_zero_sum_forms':sum(r['states'] for r in cases),
              'selected_vectors':sum(len(p['vectors']) for p in selected),
              'vector_max_absolute_entry':max(abs(x) for p in selected for q in p['vectors'] for x in q),
              'state_matrix_sha256':all_hash.hexdigest(),'witness_stream_sha256':witness_hash.hexdigest(),
              'distinct_stub_domains':paired_stubs.cache_info().currsize,
              'stub_domains':[stub_domains[k] for k in sorted(stub_domains)],'Ramsey_endpoint_decided':False}
    if export:
        export.write_text(json.dumps({'dimension':10,'records':selected},separators=(',',':'),sort_keys=True)+'\n')
    if compare:
        original = json.loads(compare.read_text())
        need(original['F_domain_sha256'] == result['F_domain_sha256'] and original['labeled_local_cores'] == result['labeled_local_cores'], 'passive complete core-domain comparison')
        for own,author in zip(cases,original['cases'][:len(cases)]):
            for field in ('F_mask','stars','row','slack_degrees','states','state_matrix_sha256'):
                need(json.loads(json.dumps(own[field])) == author[field], 'passive zero-low state/matrix comparison: '+field)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--vectors',type=Path,required=True)
    parser.add_argument('--export-used',type=Path)
    parser.add_argument('--compare-author',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=run(args.vectors,args.export_used,args.compare_author)
    data=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
    if args.check:
        need(data == args.check.read_bytes(), 'complete expected output comparison')
    sys.stdout.buffer.write(data)

if __name__=='__main__':
    main()
