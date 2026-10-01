"""Literal whole-spine calibrations, independent scalar checks and damages."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import audit


def run():
    data = json.loads((audit.ROOT/'CERTIFICATE.json').read_text())
    key,G,columns,capacities,cycles,zeros = audit.geometry()
    patterns = audit.literal_patterns()
    page_checks = 0
    for position,(i,j) in enumerate(audit.PAIRS):
        wi,wj = columns[i],columns[j]
        for s in range(max(0,wi+wj-11),min(wi,wj)+1):
            R = [set() for _ in range(22)]
            for a in range(10):
                R[0].add(a+1);R[a+1].add(0)
                for b in range(10):
                    if G[a][b]:R[a+1].add(b+1)
            miss_i = set(range(wi))
            miss_j = set(range(s)) | set(range(wi,wi+wj-s))
            for a,miss in ((i,miss_i),(j,miss_j)):
                for b in set(range(11))-miss:
                    R[a+1].add(b+11);R[b+11].add(a+1)
            red = G[i][j]
            actual = sum((p in R[i+1]) == bool(red) and (p in R[j+1]) == bool(red) for p in range(22) if p not in (i+1,j+1))
            audit.need((actual <= (3 if red else 6)) == (s <= capacities[position]), 'literal whole-spine capacity calibration')
            page_checks += 1

    scalar_checks = 0
    vectors = [(r['tags'],r['weights']) for r in data['direct']]+[([0,1],v) for v in data['split']['weights']]
    for tags,weights in vectors:
        for tag in tags:
            for word,bits in patterns.items():
                direct = weights[tags.index(tag)]+sum(weights[len(tags)+i] for i in range(10) if word & (1 << i))
                for i in range(10):
                    for j in range(i+1,10):
                        # Closed-form triangular pair index, no feature vector.
                        if word & (1 << i) and word & (1 << j):
                            at = i*(19-i)//2+j-i-1
                            direct += weights[len(tags)+10+at]
                dot = sum(a*b for a,b in zip(weights,audit.features(tag,bits,tags)))
                audit.need(direct == dot, 'independent full binary-row scalar identity')
                scalar_checks += 1

    rejected = []
    def reject(label,bad):
        try:audit.run_data(bad)
        except ValueError as exc:rejected.append({'label':label,'reason':str(exc)})
        else:raise ValueError('bad certificate accepted: '+label)

    bad = deepcopy(data);bad['graph_key'] += 1;reject('wrong marked graph',bad)
    bad = deepcopy(data);bad['extraneous'] = 0;reject('unknown schema field',bad)
    bad = deepcopy(data);bad['direct'].pop();reject('missing direct case',bad)
    bad = deepcopy(data);bad['direct'][0]['outside_deficits'] = [2,1];reject('wrong row-excess partition',bad)
    bad = deepcopy(data);bad['direct'][0]['tags'] = [0,1];reject('incorrect tag order',bad)
    bad = deepcopy(data);bad['direct'][0]['weights'].pop();reject('truncated vector',bad)
    bad = deepcopy(data);bad['direct'][0]['weights'][0] = True;reject('boolean coefficient',bad)
    bad = deepcopy(data);bad['direct'][0]['weights'][12] = -1;reject('negative pair multiplier',bad)
    bad = deepcopy(data);bad['direct'][0]['weights'] = [0]*57;reject('zero direct contradiction',bad)
    bad = deepcopy(data);bad['split']['weights'].pop();reject('missing reusable vector',bad)
    bad = deepcopy(data);bad['split']['weights'][0] = [0]*57;reject('erased main branch cover',bad)
    bad = deepcopy(data);bad['split']['outside_deficits'] = [2,1];reject('incorrect split inventory',bad)

    raw = (audit.ROOT/'PRIMARY21.txt').read_bytes()
    matrix,end = json.JSONDecoder().raw_decode(raw.decode())
    audit.need(len(matrix) == 21 and all(len(row) == 21 for row in matrix), 'primary dimensions')
    audit.need(all(type(matrix[i][j]) is int and matrix[i][j] in (0,1) and matrix[i][j] == matrix[j][i] for i in range(21) for j in range(21)), 'primary literal colors')
    red_edges = red_pages = blue_pages = 0
    for i,j in combinations(range(21),2):
        color = matrix[i][j]
        pages = sum(matrix[i][p] == color and matrix[j][p] == color for p in range(21) if p not in (i,j))
        if color == 0:red_edges += 1;red_pages = max(red_pages,pages)
        else:blue_pages = max(blue_pages,pages)
    audit.need((red_edges,red_pages,blue_pages) == (93,3,6), 'known primary positive whole-page control')
    audit.need(raw.decode()[end:].strip().startswith('search_function_used ='), 'metadata tail separated')
    return {'literal_whole_spine_capacity_checks':page_checks,'independent_all_binary_row_scores':scalar_checks,
            'semantic_damage_rejections':len(rejected),'rejections':rejected,
            'primary21':{'sha256':sha256(raw).hexdigest(),'red_edges':red_edges,'red_pages':red_pages,'blue_pages':blue_pages}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result))
