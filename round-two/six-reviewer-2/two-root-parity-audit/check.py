"""Independent original-adjacency and parity audit of LEMMA9199.

Only credited mathematical adjacency data and the primary21 text are inputs.
No researcher executable, graph package, solver or numerical arithmetic.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()


def adjacency(masks):
    n = len(masks)
    need(all(type(v) is int and 0 <= v < 1 << n for v in masks), 'integer adjacency domain')
    rows = [{j for j in range(n) if v >> j & 1} for v in masks]
    need(all(i not in row for i, row in enumerate(rows)), 'no self loops')
    need(all((j in rows[i]) == (i in rows[j]) for i in range(n) for j in range(n)), 'undirected adjacency')
    return rows


def pair_data(rows, u, v):
    universe = set(range(len(rows))) - {u, v}
    # Direct witness enumeration retains both actual endpoints and signs.
    red = int(v in rows[u])
    cr = sum(w in rows[u] and w in rows[v] for w in universe)
    cb = sum(w not in rows[u] and w not in rows[v] for w in universe)
    need(cb == len(rows)-2-len(rows[u])-len(rows[v])+cr+2*red,
         'signed endpoint inclusion-exclusion')
    return red, cr, cb


def original(rows, require_rootless=True):
    need(len(rows) == 22, 'original order22')
    degree = [len(v) for v in rows]
    need(sorted(degree) == [9]*4+[10]*18, 'entire original degree multiset')
    lows = [i for i, d in enumerate(degree) if d == 9]
    highs = [i for i, d in enumerate(degree) if d == 10]
    q = sum(v in rows[u] for u, v in combinations(lows, 2))
    a = [sum(v in rows[u] for v in lows) for u in lows]
    types = [len(rows[v] & set(lows)) for v in highs]
    counts = [types.count(t) for t in range(5)]
    need(sum(counts) == 18 and sum(t*counts[t] for t in range(5)) == 36-2*q,
         'whole high-type and low-degree count')
    need(counts[1] == 2*q-2*counts[0]+counts[3]+2*counts[4],
         'rootless hypothesis kept in exact general count')
    if require_rootless:
        need(counts[0] == 0, 'rootlessness')
    raw = [[pair_data(rows, i, x)[1] for x in highs] for i in lows]
    slacks = [[(3 if x in rows[i] else 5)-raw[k][l]
        for l, x in enumerate(highs)] for k, i in enumerate(lows)]
    D = sum(map(sum, slacks))
    # This second count walks through every ORIGINAL center, not a type formula.
    wedges = 0
    for center in range(22):
        left = rows[center] & set(lows)
        right = rows[center] & set(highs)
        wedges += sum(1 for i in left for x in right)
    typed = sum(t*(10-t)*counts[t] for t in range(5)) + sum(v*(9-v) for v in a)
    need(sum(map(sum, raw)) == wedges == typed, 'all original mixed two-edge walks')
    need(D == 2*counts[0]+2*counts[3]+6*counts[4]+sum(v*v for v in a),
         'exact general mixed slack including empty high types')
    alpha = []
    for i in lows:
        neighbors = sorted(rows[i])
        edges = sum(v in rows[u] for u, v in combinations(neighbors, 2))
        value = 27-2*edges
        need(value % 2 == 1, 'all four odd nine-neighborhood parities')
        need(value == sum(3-pair_data(rows, i, x)[1] for x in neighbors),
             'literal whole incident red slack')
        alpha.append(value)
    mixed_blue = sum(slacks[k][l] for k, i in enumerate(lows)
                     for l, x in enumerate(highs) if x not in rows[i])
    mixed_red_by_low = [sum(slacks[k][l] for l, x in enumerate(highs) if x in rows[i])
                        for k, i in enumerate(lows)]
    need(D == sum(mixed_red_by_low)+mixed_blue, 'whole mixed slack partition')
    if q == 0:
        need(alpha == mixed_red_by_low, 'independent lows exact parity partition')
    all_slacks = [(3-cr if red else 6-cb) for u, v in combinations(range(22), 2)
                  for red, cr, cb in [pair_data(rows, u, v)]]
    return {'q':q, 'counts_n0_to_n4':counts, 'low_vertices':lows,
        'high_vertices':highs, 'low_degrees_inside_L':a, 'mixed_walks':wedges,
        'mixed_slack':D, 'mixed_slack_matrix':slacks, 'mixed_blue_slack':mixed_blue,
        'mixed_red_slack_by_low':mixed_red_by_low, 'neighborhood_odd_slacks':alpha,
        'minimum_mixed_slack':min(map(min, slacks)), 'minimum_global_page_slack':min(all_slacks),
        'Ramsey_valid':all(v >= 0 for v in all_slacks),
        'one_nine_roots':counts[1], 'adjacency_sha256':digest([sorted(v) for v in rows])}


def small_graphs():
    stream = hashlib.sha256(); graphs = pairs = 0
    for n in range(1, 7):
        edges = list(combinations(range(n), 2))
        for code in range(1 << len(edges)):
            rows = [set() for _ in range(n)]
            for k, (u, v) in enumerate(edges):
                if code >> k & 1:
                    rows[u].add(v); rows[v].add(u)
            records = []
            for u, v in edges:
                red, cr, cb = pair_data(rows, u, v)
                records.append([u,v,red,len(rows[u]),len(rows[v]),cr,cb])
                pairs += 1
            stream.update(json.dumps([n,code,records], separators=(',', ':')).encode()+b'\n')
            graphs += 1
    need((graphs,pairs) == (33867,502170), 'entire small graph and pair census')
    return {'graphs':graphs,'pairs':pairs,'orders':[1,2,3,4,5,6],
            'all_direct_endpoint_records_sha256':stream.hexdigest(),
            'role':'Complete convention check, not a22-host exclusion or theorem bridge.'}


def profiles():
    # Build the relaxation by partitions of the eighteen HIGH slots. No
    # closed n1 formula is used to generate the full profile list.
    rows = []
    for n1 in range(19):
        for n2 in range(19-n1):
            for n3 in range(19-n1-n2):
                n4 = 18-n1-n2-n3
                degree = n1+2*n2+3*n3+4*n4
                if degree > 36 or (36-degree) % 2:
                    continue
                q = (36-degree)//2
                if q <= 6:
                    rows.append([q,n1,n2,n3,n4])
    rows.sort()
    need(len(rows) == 141 and len({tuple(v) for v in rows}) == 141, 'complete relaxed profile census')
    need(all(n1 == 2*q+n3+2*n4 for q,n1,n2,n3,n4 in rows), 'all count identities')
    excluded = [v for v in rows if v[1] < 2]
    boundary = [v for v in rows if v[1] == 2]
    need(excluded == [[0,0,18,0,0],[0,1,16,1,0]], 'whole zero/one-root exceptional list')
    need(boundary == [[0,2,14,2,0],[0,2,15,0,1],[1,2,16,0,0]], 'whole exact-two boundary')
    return {'all_relaxed_profiles':rows,'zero_one_exceptional_profiles':excluded,
            'exact_two_profiles':boundary,'sha256':digest(rows),
            'role':'Necessary counts only; no graph occurrence is claimed.'}


def primary():
    raw = (ROOT/'PRIMARY21.txt').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
         'entire fresh primary raw source')
    matrix, end = json.JSONDecoder().raw_decode(raw.decode())
    need(len(matrix) == 21 and all(len(v) == 21 for v in matrix), 'primary matrix order')
    need(all(type(v) is int and v in [0,1] for row in matrix for v in row), 'binary original matrix')
    need(all(matrix[i][i] == 0 for i in range(21)) and
         all(matrix[i][j] == matrix[j][i] for i in range(21) for j in range(21)),
         'primary symmetry and original diagonal')
    rows = [{j for j in range(21) if i != j and matrix[i][j] == 0} for i in range(21)]
    maxima = [0,0]; edges = 0
    for u,v in combinations(range(21),2):
        red, cr, cb = pair_data(rows,u,v);edges += red
        maxima[0 if red else 1] = max(maxima[0 if red else 1], cr if red else cb)
    need(edges == 93 and maxima == [3,6], 'actual known primary21 witness')
    return {'order':21,'red_edges':edges,'blue_edges':210-edges,'page_maxima':maxima,
            'degree_histogram':[[k,v] for k,v in sorted(Counter(map(len, rows)).items())],
            'matrix_sha256':digest(matrix),'raw_sha256':hashlib.sha256(raw).hexdigest(),
            'trailing_metadata_bytes':len(raw[end:]),'role':'Prior-art witness validation.'}


def boundary_tables(profile_rows):
    tables=[]
    for q,n1,n2,n3,n4 in profile_rows:
        if n1 != 2:continue
        D=2*n3+6*n4+(2 if q == 1 else 0)
        if q == 0:
            allocations=set()
            from itertools import product
            for alpha in product(range(1,D+1,2),repeat=4):
                blue=D-sum(alpha)
                if blue >= 0:
                    allocations.add((tuple(sorted((27-v)//2 for v in alpha)),blue))
            allocations=sorted(allocations)
            need(allocations == ([((13,13,13,13),0)] if n3 == 2 else
                                 [((12,13,13,13),0),((13,13,13,13),2)]),
                 'all nonnegative odd neighborhood slack allocations')
            tables.append({'profile':[q,n1,n2,n3,n4],'D':D,
                'all_low_neighborhood_edge_multisets_and_total_blue_slack':
                [[list(edges),blue] for edges,blue in allocations]})
        else:
            need(q == 1 and n3 == n4 == 0 and D == 2, 'only remaining exact-two sector')
            # Two isolated low vertices force positive odd mixed-red slacks.
            options=[(p,r,D-p-r) for p in range(1,D+1,2) for r in range(1,D+1,2)
                     if D-p-r >= 0]
            need(options == [(1,1,0)], 'all isolated parity budgets consume D2')
            allowed=[c for c in range(4) if (3-c)%2 == 1]
            need(allowed == [0,2], 'low-edge common-neighbor parity plus red cap')
            tables.append({'profile':[q,n1,n2,n3,n4],'D':D,
                'isolated_low_red_neighborhood_edges':[13,13],
                'every_mixed_blue_slack':0,'all_mixed_red_slacks_at_nonisolated_lows':0,
                'valid_graph_common_neighbors_of_only_low_edge':allowed,
                'nonisolated_low_neighborhood_degree_profiles':
                [{'low_edge_common_neighbors':c,'degrees':[c]+[3]*8,
                  'edges':(c+24)//2} for c in allowed],
                'mixed_caps_only_low_edge_common_neighbors':'even; global red cap adds0 or2'})
    need(len(tables) == 3, 'complete exact-two boundary table')
    degree_profiles=[]
    for d0 in range(10):
        for d1 in range(10-d0):
            for d2 in range(10-d0-d1):
                d3=9-d0-d1-d2
                if 3*d0+2*d1+d2 == 1:
                    degree_profiles.append([0]*d0+[1]*d1+[2]*d2+[3]*d3)
    need(degree_profiles == [[2]+[3]*8], '13-edge max-three nine-neighborhood degree profile')
    return {'all_exact_two_cases':tables,'13_edge_low_neighborhood_degree_profiles':degree_profiles,
            'weaker_hypotheses_two_root_theorem':'Degrees9^4,10^18 and no empty high type; only mixed red cap3 and mixed blue cap5 are needed. No L-L or H-H cap enters the two-root theorem. The low-edge0/2 refinement separately retains its red cap3.'}


def exact_record(actual, expected):
    need(type(actual) is type(expected), 'record exact type')
    if isinstance(actual, dict):
        need(actual.keys() == expected.keys(), 'entire record field set')
        for k in actual:exact_record(actual[k],expected[k])
    elif isinstance(actual, list):
        need(len(actual) == len(expected), 'entire record list')
        for a,b in zip(actual,expected):exact_record(a,b)
    else:
        need(actual == expected, 'entire record value')


def reject(action):
    try:action()
    except ValueError:return
    raise ValueError('intentional damage accepted')


def damaged_rootlessness(rows):
    # Two low incidences move from x to y; two high incidences move back.
    # Entire original degrees are preserved, while type2/type2 becomes0/4.
    lows = {i for i,v in enumerate(rows) if len(v) == 9}
    highs = set(range(22))-lows
    for x,y in combinations(sorted(highs),2):
        tx=rows[x]&lows;ty=rows[y]&lows
        if len(tx) != 2 or len(ty) != 2 or tx&ty:continue
        possible=(rows[y]&highs)-rows[x]-{x,y}
        if len(possible) < 2:continue
        changed=[set(v) for v in rows]
        for a in tx:
            changed[x].remove(a);changed[a].remove(x)
            changed[y].add(a);changed[a].add(y)
        for z in sorted(possible)[:2]:
            changed[y].remove(z);changed[z].remove(y)
            changed[x].add(z);changed[z].add(x)
        need(list(map(len,changed)) == list(map(len,rows)), 'degree-preserving quantifier damage')
        original(changed,require_rootless=False)
        reject(lambda:original(changed))
        return {'all_degrees_preserved':True,'general_empty_type_identity_checked':True,
                'rootless_model_rejected':True,'counts':original(changed,False)['counts_n0_to_n4']}
    raise ValueError('missing explicit degree-preserving rootlessness damage')


def record():
    doc=json.loads((ROOT/'INPUT-controls.json').read_text())
    need(doc['schema'] == 1 and len(doc['controls']) == 6, 'all six credited original controls')
    outputs=[]; originals=[]
    for fixture in doc['controls']:
        rows=adjacency(fixture['red_masks']);out=original(rows)
        need(out['q'] == fixture['expected_q'] and out['counts_n0_to_n4'][1:] == fixture['expected_n'], 'credited fixture actual type data')
        need(not out['Ramsey_valid'], 'invalid signed controls never witnesses')
        outputs.append({'name':fixture['name'],**out});originals.append(rows)
    cases=[]
    baseline=doc['controls'][0]['red_masks']
    bad=list(baseline);bad[0] |= 1
    reject(lambda:adjacency(bad));cases.append('self loop')
    bad=list(baseline);bad[0] ^= 1 << 1
    reject(lambda:adjacency(bad));cases.append('asymmetric adjacency')
    bad=list(baseline);bad[0]=float(bad[0])
    reject(lambda:adjacency(bad));cases.append('floated integer mask')
    bad=[set(v) for v in originals[0]];u=0;v=next(iter(bad[u]));bad[u].remove(v);bad[v].remove(u)
    reject(lambda:original(bad));cases.append('symmetric wrong original degree')
    quantifier=damaged_rootlessness(originals[0]);cases.append('degree-preserving empty high type')
    prof=profiles()
    value={'agent':'six-reviewer-2','role':'independent mathematical reviewer','target':9199,
        'small_graph_endpoint_census':small_graphs(),'profiles':prof,'original_controls':outputs,
        'primary21':primary(),'quantifier_control':quantifier,'rejected_adjacency_damages':cases,
        'proved_exact_two_boundary':boundary_tables(prof['all_relaxed_profiles']),
        'ordinary_bridges':'Written in REVIEW: all-original double counting, odd neighborhood parity, zero nonnegative slacks and explicit imported rootlessness. Finite controls do not prove a22-host exclusion.'}
    # Damage checks use genuine mathematical fields; no assert is disabled by -O.
    for name in ['omitted boundary profile','false mixed slack','floated root count','omitted full profile']:
        changed=json.loads(json.dumps(value))
        if name=='omitted boundary profile':changed['proved_exact_two_boundary']['all_exact_two_cases'].pop()
        elif name=='false mixed slack':changed['original_controls'][0]['mixed_slack'] += 1
        elif name=='floated root count':changed['original_controls'][0]['one_nine_roots']=0.0
        else:changed['profiles']['all_relaxed_profiles'].pop()
        reject(lambda:exact_record(value,changed))
    value['rejected_record_damages']=['omitted boundary profile','false mixed slack','floated root count','omitted full profile']
    return value


if __name__ == '__main__':
    result=record()
    if '--record' in sys.argv:
        print(json.dumps(result,indent=2,sort_keys=True))
    else:
        exact_record(result,json.loads((ROOT/'expected.json').read_text()))
        print(json.dumps({'status':'PASS','canonical_record_sha256':digest(result),
            'original_signed_controls':6,'whole_profiles':141,'whole_small_graphs':33867,
            'whole_endpoint_pairs':502170,'exact_two_boundary_cases':3},sort_keys=True))
