"""Independent census and literal integer certificate checker.

Actual author: six-books-3, researcher. Imports no generator code.
F is enumerated by binary adjacency; all three ordered low-neighbor
sets are enumerated by degree backtracking. Slack uses edge-weight
backtracking. No PSD algorithm or floating-point arithmetic is used.
"""
from collections import Counter
from itertools import permutations, product
from pathlib import Path
import argparse
import copy
import hashlib
import json

HERE = Path(__file__).resolve().parent
EDGES = [(i, j) for i in range(6) for j in range(i + 1, 6)]
INDEX = {p: k for k, p in enumerate(EDGES)}


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def decode(mask):
    a = [[0] * 6 for _ in range(6)]
    for k, (i, j) in enumerate(EDGES):
        if mask & (1 << k):
            a[i][j] = a[j][i] = 1
    return a


def labeled_stars(adjacency):
    remaining = [3 - sum(row) for row in adjacency]
    allowed = [(k, i, j) for k, (i, j) in enumerate(EDGES) if not adjacency[i][j]]
    def attach(sequence):
        if len(sequence) == 3:
            if not any(remaining):
                yield tuple(sequence)
            return
        for k, i, j in allowed:
            if remaining[i] and remaining[j]:
                remaining[i] -= 1
                remaining[j] -= 1
                yield from attach(sequence + [k])
                remaining[i] += 1
                remaining[j] += 1
    yield from attach([])


def slack_graphs(degrees):
    remaining = list(degrees)
    out = []
    def assign(k, sequence):
        if k == 15:
            if not any(remaining):
                out.append(tuple(sequence))
            return
        i, j = EDGES[k]
        for weight in range(min(remaining[i], remaining[j]) + 1):
            remaining[i] -= weight
            remaining[j] -= weight
            assign(k + 1, sequence + [k] * weight)
            remaining[i] += weight
            remaining[j] += weight
    assign(0, [])
    return sorted(out)


def matrices(f, stars, slack, triple):
    """Construct pair intersections by degree classes, not adjacency products."""
    low_neighbors = [set(EDGES[k]) for k in stars]
    slack_weights = Counter(slack)
    same_block = lambda i, j: (i in triple) == (j in triple)
    s = [[0] * 10 for _ in range(10)]
    s[0][0] = 2
    for low in range(1, 4):
        s[low][low] = 4
    for high in range(4, 10):
        s[high][high] = 5
        s[0][high] = s[high][0] = 1
    for i in range(3):
        for j in range(i + 1, 3):
            s[1+i][1+j] = s[1+j][1+i] = 2 - len(low_neighbors[i] & low_neighbors[j])
        for high in range(6):
            value = (0 if high in low_neighbors[i] else
                     3 - sum(f[high][x] for x in low_neighbors[i]))
            s[1+i][4+high] = s[4+high][1+i] = value
    for k, (i, j) in enumerate(EDGES):
        high_common = sum(f[i][x] and f[j][x] for x in range(6))
        low_common = sum(i in row and j in row for row in low_neighbors)
        value = (1 if f[i][j] else 4) - high_common - low_common - slack_weights[k]
        s[4+i][4+j] = s[4+j][4+i] = value
    r = [[s[i][j] for j in range(1, 10)] for i in range(1, 10)]
    for i in range(6):
        for j in range(6):
            r[3+i][3+j] -= int(same_block(i, j))
    check([sum(row) for row in s] == [8,16,16,16,20,20,20,20,20,20],
          'full row-sum bridge failed')
    check(all(r[i][i] == 4 and sum(r[i]) == 16 for i in range(9)),
          'residual row bridge failed')
    return s, r


def certificate_check(expected, certificates):
    records = expected['records']
    check(len(records) == 12, 'incomplete F catalogue')
    reps = [r['F_mask'] for r in records]
    check(reps == sorted(set(reps)), 'duplicate or unordered F representative')
    domain = {}
    for mask in range(1 << 15):
        if mask.bit_count() != 6:
            continue
        a = decode(mask)
        if any(sum(row) > 3 for row in a):
            continue
        if any(a[i][j] and sum(a[i][x] and a[j][x] for x in range(6)) > 1
               for i, j in EDGES):
            continue
        domain[mask] = a
    # Exact entry-level orbit cover, with a fixed inverse relabeling per F.
    relabel = {}
    orbit_sizes = {}
    for representative in reps:
        original = decode(representative)
        images = {}
        for p in permutations(range(6)):
            image = 0
            inverse = [0] * 6
            for v in range(6):
                inverse[p[v]] = v
            for k, (i, j) in enumerate(EDGES):
                if original[i][j]:
                    image |= 1 << INDEX[tuple(sorted((p[i], p[j])))]
            images.setdefault(image, tuple(inverse))
        check(min(images) == representative, 'F representative not minimum')
        check(not (set(images) & set(relabel)), 'overlapping F orbits')
        check(set(images) <= set(domain), 'F orbit outside binary domain')
        orbit_sizes[representative] = len(images)
        for mask, inverse in images.items():
            relabel[mask] = (representative, inverse)
    check(set(relabel) == set(domain), 'binary F domain not covered entrywise')
    actual_core_weights = Counter()
    for mask, adjacency in domain.items():
        representative, inverse = relabel[mask]
        for sequence in labeled_stars(adjacency):
            normalized = tuple(sorted(INDEX[tuple(sorted((inverse[i], inverse[j])))]
                                      for k in sequence for i, j in [EDGES[k]]))
            actual_core_weights[representative, normalized] += 1
    pool = {}
    check(certificates.get('dimension') == 9, 'wrong certificate dimension')
    for record in certificates['records']:
        key = record['F_mask'], tuple(record['stars'])
        check(key not in pool, 'duplicate certificate core')
        for vector in record['vectors']:
            check(len(vector) == 9 and all(type(x) is int for x in vector) and any(vector),
                  'malformed integer certificate vector')
        pool[key] = record['vectors']
    # Generate both blocks of each partition independently; no assumption
    # that vertex zero belongs to a prescribed block before normalization.
    partitions = set()
    for bits in range(1 << 6):
        if bits.bit_count() == 3:
            left = tuple(i for i in range(6) if bits >> i & 1)
            right = tuple(i for i in range(6) if not bits >> i & 1)
            partitions.add(min(left, right))
    partitions = sorted(partitions)
    check(len(partitions) == 10, 'incomplete triple partitions')
    counts, weighted = Counter(), Counter()
    actual_records = []
    expected_core_weights = {}
    digest = hashlib.sha256()
    for rep in reps:
        f = decode(rep)
        deficits = [3 - sum(row) for row in f]
        stars_census = Counter(tuple(sorted(x)) for x in labeled_stars(f))
        slacks = slack_graphs(deficits)
        cores = []
        for stars in sorted(stars_census):
            key = rep, stars
            check(key in pool, 'missing certificate core')
            multiplicity = stars_census[stars]
            weight = orbit_sizes[rep] * multiplicity
            expected_core_weights[key] = weight
            cores.append({'stars': list(stars), 'low_label_multiplicity': multiplicity})
            counts['local_cores_after_F_and_S3_normalization'] += 1
            weighted['labeled_local_cores'] += weight
            for slack in slacks:
                check(len(slack) == 3, 'slack edge total failed')
                for triple in partitions:
                    s, r = matrices(f, stars, slack, triple)
                    digest.update(encode([rep, stars, slack, triple, r]))
                    counts['states'] += 1
                    weighted['states'] += weight
                    if any(x < 0 for row in s for x in row):
                        status = 'full_negative_entry'
                    elif any(x < 0 for row in r for x in row):
                        status = 'residual_negative_entry'
                    else:
                        status = 'negative_quadratic_form'
                    # Required for every state, including both negative-entry
                    # categories. No PSD solver or entry cut is trusted.
                    check(any(sum(vector[i] * sum(r[i][j] * vector[j] for j in range(9))
                                  for i in range(9)) < 0 for vector in pool[key]),
                          'state lacks a negative integer form')
                    counts['negative_forms_checked'] += 1
                    weighted['negative_forms_checked'] += weight
                    counts[status] += 1
                    weighted[status] += weight
        actual_records.append({'F_mask': rep, 'orbit_size': orbit_sizes[rep],
                               'deficits': deficits, 'slack_multigraphs': len(slacks),
                               'cores': cores})
    check(actual_records == records, 'core catalogue differs entrywise')
    check(actual_core_weights == expected_core_weights, 'labeled core cover differs entrywise')
    check(set(pool) == set(expected_core_weights), 'extra certificate core')
    vectors = [v for rec in certificates['records'] for v in rec['vectors']]
    actual = {'F_six_edge_labeled': sum(mask.bit_count() == 6 for mask in range(1 << 15)),
              'F_after_necessary_cuts': len(domain), 'F_orbits': len(reps),
              'F_domain_sha256': hashlib.sha256(''.join(str(x)+'\n' for x in sorted(domain)).encode()).hexdigest(),
              'records': actual_records, 'normalized_state_counts': dict(sorted(counts.items())),
              'labeled_state_counts': dict(sorted(weighted.items())),
              'state_matrix_sha256': digest.hexdigest(), 'negative_vector_count': len(vectors),
              'negative_vector_max_abs_entry': max(abs(x) for v in vectors for x in v),
              'negative_vectors_sha256': hashlib.sha256(encode(certificates)).hexdigest(), 'survivors': 0}
    for key, value in actual.items():
        check(expected[key] == value, 'summary mismatch at ' + key)
    return actual


def control_check():
    counts = Counter()
    for bits in range(1 << 10):
        if bits.bit_count() != 5:
            continue
        steps = [s for s in range(1, 11) if bits >> (s - 1) & 1]
        r = [[int(i != j and any((j - i) % 22 in (s, 22 - s) for s in steps))
              for j in range(22)] for i in range(22)]
        check(all(sum(row) == 10 for row in r), 'control not regular')
        a = [j for j in range(22) if r[0][j]]
        b = [j for j in range(1, 22) if not r[0][j]]
        h = [sum(r[i][j] for j in a) for i in a]
        m = [[1-r[v][i] for i in a] for v in b]
        t = [sum(row[i] for row in m) for i in range(10)]
        check(t == [x+2 for x in h], 'column identity failure')
        counts['column_identities'] += 10
        for v, row in zip(b, m):
            check(sum(r[v][w] for w in b) == sum(row), 'outside identity failure')
            counts['outside_degree_identities'] += 1
        eps = [[0] * 10 for _ in range(10)]
        for i in range(10):
            for j in range(i+1, 10):
                x, y = a[i], a[j]
                if r[x][y]:
                    pages = sum(r[x][z] and r[y][z] for z in range(22))
                    slack = 3-pages
                    forced = t[i]+t[j]-9-sum(r[x][z] and r[y][z] for z in a)-slack
                else:
                    pages = sum(z not in (x,y) and not r[x][z] and not r[y][z]
                                for z in range(22))
                    slack = 6-pages
                    local_blue_pages = sum(z not in (x,y) and not r[x][z] and not r[y][z]
                                           for z in a)
                    forced = 6-slack-local_blue_pages
                check(forced == sum(row[i]*row[j] for row in m), 'pair identity failure')
                eps[i][j] = eps[j][i] = slack
                counts['pair_identities'] += 1
        u = sum(eps[i][j] for i in range(10) for j in range(i+1, 10))
        psi = sum((sum(row)-4)*(sum(row)-5)//2 for row in m)
        check(2*(u+psi) == -120+8*sum(h)-sum(x*x for x in h), 'scalar identity failure')
        counts['scalar_budgets'] += 1
        for i in range(10):
            incident_excess = sum((sum(row)-4)*row[i] for row in m)
            neighbor_h = sum(h[j] for j in range(10) if r[a[i]][a[j]])
            check(sum(eps[i]) == 3*h[i]+sum(h)-24-neighbor_h-incident_excess,
                  'incident identity failure')
            counts['incident_slack_identities'] += 1
        counts['controls'] += 1
    # All ordered assignments of the six degree-two neighbor pairs, then
    # normalize only their permutation. This reconstructs the ten profiles.
    pairs4 = [(i,j) for i in range(4) for j in range(i+1,4)]
    profiles = set()
    for assignment in product(range(6), repeat=6):
        d = [0]*4
        for k in assignment:
            i,j = pairs4[k]; d[i] += 1; d[j] += 1
        if d == [3]*4:
            profiles.add(tuple(sorted(assignment)))
    counts['bipartite_profiles'] = len(profiles)
    for assignment in sorted(profiles):
        neighbor = [set(pairs4[k]) for k in assignment]
        demand = sum(3 for i in range(6) for j in range(4) if j not in neighbor[i])
        check(demand == 36, 'wrong mixed demand')
        for bits in range(1 << 10):
            if bits.bit_count() != 4:
                continue
            lows = [i for i in range(6) if bits >> i & 1]
            highs = [j for j in range(4) if bits >> (6+j) & 1]
            if any(j in neighbor[i] for i in lows for j in highs):
                continue
            if any(neighbor[i] == neighbor[j] for i in lows for j in lows if i<j):
                continue
            check(len(highs) in [0,1,4] and len(lows)*len(highs)<=3, 'bad four-set')
            counts['bipartite_admissible_four_sets'] += 1
    data = (HERE/'baseline21.rows').read_bytes()
    lines = data.decode().splitlines()
    check(len(lines)==21 and all(len(x)==21 and set(x)<={'0','1'} for x in lines), 'bad baseline')
    edge_count = 0; red_max = 0; blue_max = 0
    for i in range(21):
        check(lines[i][i]=='0', 'baseline loop')
        for j in range(i+1,21):
            check(lines[i][j]==lines[j][i], 'baseline asymmetric')
            if lines[i][j]=='1':
                edge_count += 1
                red_max = max(red_max,sum(lines[i][k]==lines[j][k]=='1' for k in range(21)))
            else:
                blue_max = max(blue_max,sum(k not in [i,j] and lines[i][k]==lines[j][k]=='0'
                                           for k in range(21)))
    check((edge_count,red_max,blue_max)==(93,3,6), 'baseline caps mismatch')
    return dict(sorted(counts.items())),hashlib.sha256(data).hexdigest()


def negative_controls(expected, certificates):
    rejected = 0
    examples = []
    d = copy.deepcopy(expected); d['records'].pop(); examples.append((d,certificates))
    d = copy.deepcopy(expected); d['records'][1]=copy.deepcopy(d['records'][0]); examples.append((d,certificates))
    d = copy.deepcopy(expected); d['records'][0]['cores'].pop(); examples.append((d,certificates))
    d = copy.deepcopy(expected); d['records'][0]['orbit_size'] += 1; examples.append((d,certificates))
    d = copy.deepcopy(expected); d['state_matrix_sha256']='0'*64; examples.append((d,certificates))
    c = copy.deepcopy(certificates); c['records'][0]['vectors']=[[0]*9]; examples.append((expected,c))
    c = copy.deepcopy(certificates)
    for record in c['records']:
        record['vectors'] = [[1,0,0,0,0,0,0,0,0]] if record['vectors'] else []
    d = copy.deepcopy(expected); d['negative_vectors_sha256']=hashlib.sha256(encode(c)).hexdigest()
    examples.append((d,c))
    for d,c in examples:
        try:
            certificate_check(d,c)
        except (RuntimeError,KeyError,ValueError,IndexError):
            rejected += 1
        else:
            raise RuntimeError('forged certificate accepted')
    check(rejected==7, 'negative-control accounting failed')
    return rejected


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--negative-controls',action='store_true')
    args=parser.parse_args()
    expected=json.loads((HERE/'expected.json').read_text())
    certificates=json.loads((HERE/'negative_vectors.json').read_text())
    actual=certificate_check(expected,certificates)
    control_counts, baseline_sha=control_check()
    check(control_counts==expected['control_counts'], 'control counts differ')
    check(baseline_sha==expected['baseline21_rows_sha256'], 'baseline hash differs')
    hist=[]
    for n0 in range(2):
        for n2 in range(11-n0):
            n3=10-n0-n2
            if 2*n2+3*n3>=26 and (2*n2+3*n3)%2==0:
                hist.append([n0,n2,n3])
    check(hist==expected['remaining_local_histograms_n0_n2_n3'], 'histogram list differs')
    check(expected['regular_red_triangle_interval']==[96,110], 'triangle interval differs')
    if args.negative_controls:
        rejected=negative_controls(expected,certificates)
        print(json.dumps({'negative_controls_rejected':rejected},sort_keys=True))
    else:
        print(encode(expected).decode(),end='')


if __name__=='__main__':
    main()
