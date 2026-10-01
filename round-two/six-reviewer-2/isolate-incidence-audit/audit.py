"""Independent six-vector audit, six-reviewer-2, mathematical reviewer.

No researcher module. Third split generator uses ternary partial partitions.
Tags mean row-size excess, not outside degree deficit.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT_HASH = '63ba27d0ef4fa100a14f09f902850842aa03e5b3e6ade5ba34ecac6d71bbf839'
ADJACENCY = ((7,8,9), (), (5,6), (6,8,9), (5,7,9),
             (2,4,8), (2,3,7), (0,4,6), (0,3,5), (0,3,4))
PAIRS = tuple(combinations(range(10), 2))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def geometry():
    G = [[int(j in ADJACENCY[i]) for j in range(10)] for i in range(10)]
    need(all(G[i][i] == 0 for i in range(10)) and all(G[i][j] == G[j][i] for i,j in PAIRS), 'literal graph simple')
    key = sum(1 << k for k,(i,j) in enumerate(PAIRS) if G[i][j])
    need(key == 710617334208, 'literal graph key')
    degrees = [sum(row) for row in G]
    columns = [d+2+int(i == 0) for i,d in enumerate(degrees)]
    # Actual prefix: root0 and local vertices1..10. Count every known page.
    prefix = [[0]*11 for _ in range(11)]
    for i in range(10):
        prefix[0][i+1] = prefix[i+1][0] = 1
        for j in range(10):
            prefix[i+1][j+1] = G[i][j]
    capacities = []
    for i,j in PAIRS:
        red = bool(G[i][j])
        known = sum(prefix[i+1][k] == red and prefix[j+1][k] == red for k in range(11) if k not in (i+1,j+1))
        cap = (3-known-(11-columns[i]-columns[j])) if red else (6-known)
        need(cap >= 0, 'nonnegative literal pair capacity')
        capacities.append(cap)
    cycles = []
    for S in combinations(range(10),4):
        if all(sum(G[i][j] for j in S) == 2 for i in S):
            need(sum(columns[i] for i in S) == 21 and sum(capacities[PAIRS.index((i,j))] for i,j in combinations(S,2)) == 10, 'four-column equality')
            cycles.append(S)
    need(len(cycles) == 2, 'two induced cycles')
    zeros = tuple(pair for pair,cap in zip(PAIRS,capacities) if cap == 0)
    need(columns[1] == 2 and all(capacities[k] <= 1 for k,pair in enumerate(PAIRS) if 1 in pair), 'isolated-column split bridge')
    return key, G, columns, capacities, cycles, zeros


def literal_patterns():
    """Coefficients of product_i (1+x_i): enumerate every binary row."""
    words = [0]
    for i in range(10):
        words += [word | (1 << i) for word in words]
    need(words == list(range(1024)), 'complete binary expansion')
    return {word:tuple(int(bool(word & (1 << i))) for i in range(10)) for word in words}


def row_allowed(bits, columns, capacities, cycles, equalities):
    if any(bits[i] and columns[i] == 0 for i in range(10)):
        return False
    if any(bits[i] and bits[j] and capacities[k] == 0 for k,(i,j) in enumerate(PAIRS)):
        return False
    return not equalities or all(sum(bits[i] for i in S) in (1,2) for S in cycles)


def domains(tags, columns, capacities, cycles, equalities, all_patterns):
    return {tag:[word for word,bits in all_patterns.items() if sum(bits) == 4+tag and row_allowed(bits,columns,capacities,cycles,equalities)] for tag in tags}


def features(tag, bits, tags):
    return tuple(int(tag == t) for t in tags)+bits+tuple(bits[i]*bits[j] for i,j in PAIRS)


def vector_check(weights, tags, counts, columns, capacities, domain, patterns):
    need(type(weights) is list and len(weights) == len(tags)+55 and all(type(x) is int for x in weights), 'integer vector dimension')
    need(all(x >= 0 for x in weights[len(tags)+10:]), 'nonnegative pair multipliers')
    minima = {}
    rows_checked = 0
    for tag in tags:
        values = [sum(a*b for a,b in zip(weights,features(tag,patterns[word],tags))) for word in domain[tag]]
        minima[str(tag)] = min(values) if values else None
        rows_checked += len(values)
    rhs = tuple(counts[tag] for tag in tags)+tuple(columns)+tuple(capacities)
    total = sum(a*b for a,b in zip(weights,rhs))
    valid = total < 0 and all(x is None or x >= 0 for x in minima.values())
    return {'valid':valid,'upper_total':total,'minimum_row_scores':minima,'rows_checked':rows_checked}


def partial_partitions(columns, capacities, cycles, patterns):
    """Color eight eligible columns as unused/left/right; quotient exchange.

    Two rows containing isolated1 avoid2 and otherwise are disjoint.
    Neither rows nor supplied candidate pairs are enumerated as a product.
    """
    U = (0,3,4,5,6,7,8,9)
    pairs = []
    states = 0
    for coloring in product(range(3), repeat=8):
        states += 1
        S = [U[k] for k,x in enumerate(coloring) if x == 1]
        T = [U[k] for k,x in enumerate(coloring) if x == 2]
        if len(S) not in (3,4) or len(T) not in (3,4):
            continue
        left = (len(S)-3, 2+sum(1 << i for i in S))
        right = (len(T)-3, 2+sum(1 << i for i in T))
        if left >= right:
            continue
        if not all(row_allowed(patterns[word],columns,capacities,cycles,True) for _,word in (left,right)):
            continue
        need((left[1] & right[1]) == 2, 'literal isolated-only intersection')
        pairs.append((left,right))
    pairs.sort()
    need(len(set(pairs)) == len(pairs), 'unique ternary branches')
    return pairs, states


def run_data(certificate):
    need(type(certificate) is dict and set(certificate) == {'graph_key','direct','split'}, 'certificate schema')
    key,G,columns,capacities,cycles,zeros = geometry()
    need(certificate['graph_key'] == key and type(certificate['graph_key']) is int, 'certificate graph key')
    patterns = literal_patterns()
    need(type(certificate['direct']) is list and len(certificate['direct']) == 2, 'two direct vectors')
    direct_results = []
    for record,partition in zip(certificate['direct'],([3],[2,1])):
        need(set(record) == {'outside_deficits','tags','weights'} and record['outside_deficits'] == partition, 'direct partition coverage')
        tags = [0]+sorted(set(partition))
        need(record['tags'] == tags, 'direct tag order')
        counts = Counter(partition);counts[0] = 11-len(partition)
        domain = domains(tags,columns,capacities,cycles,False,patterns)
        verdict = vector_check(record['weights'],tags,counts,columns,capacities,domain,patterns)
        need(verdict['valid'], 'direct weighted contradiction')
        direct_results.append({'row_excess_partition':partition,'domains':{str(t):len(domain[t]) for t in tags},**verdict})
    split = certificate['split']
    need(type(split) is dict and set(split) == {'outside_deficits','tags','weights'} and split['outside_deficits'] == [1,1,1] and split['tags'] == [0,1], 'split excess partition coverage')
    need(type(split['weights']) is list and len(split['weights']) == 4, 'four reusable vectors')
    initial = domains([0,1],columns,capacities,cycles,True,patterns)
    branches,states = partial_partitions(columns,capacities,cycles,patterns)
    coverage = [0]*4
    first_usage = [0]*4
    records = []
    for left,right in branches:
        removed = [patterns[left[1]],patterns[right[1]]]
        counts = {0:8-int(left[0] == 0)-int(right[0] == 0),1:3-int(left[0] == 1)-int(right[0] == 1)}
        residual_columns = [columns[i]-sum(bits[i] for bits in removed) for i in range(10)]
        residual_caps = [cap-sum(bits[i]*bits[j] for bits in removed) for cap,(i,j) in zip(capacities,PAIRS)]
        need(min(residual_columns+residual_caps) >= 0 and sum(counts.values()) == 9, 'residual inventory')
        domain = domains([0,1],residual_columns,residual_caps,cycles,True,patterns)
        judgments = [vector_check(weights,[0,1],counts,residual_columns,residual_caps,domain,patterns) for weights in split['weights']]
        hits = [i for i,v in enumerate(judgments) if v['valid']]
        need(hits, 'uncovered actual two-row branch')
        for i in hits:
            coverage[i] += 1
        first_usage[hits[0]] += 1
        records.append({'rows':[list(left),list(right)],'residual_domain_sizes':{str(t):len(domain[t]) for t in (0,1)},'vectors':judgments})
    compact = json.dumps(branches,separators=(',',':')).encode()
    return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','graph_key':key,'local_degrees':[sum(row) for row in G],
            'columns':columns,'pair_capacities':capacities,'pair_capacity_sum':sum(capacities),'zero_pairs':[list(p) for p in zeros],
            'cycles':[list(S) for S in cycles],'direct':direct_results,'split':{'ternary_states':states,'branches':len(branches),
            'initial_domains':{str(t):len(initial[t]) for t in (0,1)},'branch_sha256':sha256(compact).hexdigest(),
            'coverage':coverage,'first_usage':first_usage,'tag_pair_counts':{str(k):v for k,v in sorted(Counter((l[0],r[0]) for l,r in branches).items())},
            'checked_row_scores':sum(v['rows_checked'] for r in records for v in r['vectors']),
            'verification_transcript_sha256':sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()},
            'refinement':{'row_count_forced':11,'row_excess_sum':3,'edge_count_premise_used':False,'actual_outside_deficit_tags_used':False}}


def run(path=ROOT/'CERTIFICATE.json'):
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == INPUT_HASH, 'frozen certificate hash')
    result = run_data(json.loads(raw))
    result['certificate_sha256'] = INPUT_HASH
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=ROOT/'CERTIFICATE.json')
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    result = run(args.certificate)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'complete':True,'branches':result['split']['branches'],'coverage':result['split']['coverage'],'branch_sha256':result['split']['branch_sha256']}))
