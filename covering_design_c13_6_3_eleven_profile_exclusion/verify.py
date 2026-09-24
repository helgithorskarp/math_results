"""Complete exact exclusion of the (11,10,9^11) degree profile."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

from catalogue import validate
from joins import prepare, join
from residual import Space, solve

ROOT = Path(__file__).resolve().parent
SCHEMA = ['design', 'h', 'q', 'r', 'shared_blocks', 'compatible_joins', 'joins_sha256',
          'residual_nodes', 'largest_residual_search', 'raw_embeddings', 'distinct_joins', 'degree_compatible']


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def generate():
    inputs = validate()
    roots, templates = prepare()
    if len(roots) != 442:
        raise ValueError('unexpected root census')
    rows = []
    totals = Counter()
    cutoffs = Counter()
    spaces = {}
    for root in roots:
        joined = join(root, templates)
        configurations = joined['configurations']
        if root['r'] not in spaces:
            spaces[root['r']] = Space(12, root['r'])
        node_sum = node_max = 0
        for fixed in configurations:
            answer = solve(spaces[root['r']], fixed, root['h'], root['q'])
            if answer['status'] != 'UNSAT':
                raise ValueError(('unexpected global completion', root, answer))
            node_sum += answer['nodes']
            node_max = max(node_max, answer['nodes'])
            cutoffs.update(answer['cutoffs'])
        rows.append([root['design'], root['h'], root['q'], root['r'], root['k'],
                     len(configurations), digest(configurations), node_sum, node_max,
                     joined['raw'], joined['unique'], joined['degree_ok']])
        totals.update(raw_embeddings=joined['raw'], distinct_joins=joined['unique'],
                      degree_compatible=joined['degree_ok'], compatible_joins=len(configurations),
                      residual_nodes=node_sum, roots_without_compatible_joins=int(not configurations))
    root_data = dict(schema=SCHEMA, rows=rows)
    summary = dict(status='VERIFIED_NO_11_10_9_PROFILE', inputs=inputs, roots=len(roots),
                   second_link_pointed_templates=sum(map(len, templates.values())),
                   largest_residual_search=max(row[8] for row in rows),
                   **dict(totals), cutoffs=dict(sorted(cutoffs.items())),
                   roots_sha256=digest(root_data),
                   links_file_sha256=sha256((ROOT / 'LINKS.json').read_bytes()).hexdigest())
    return summary, root_data


def main():
    summary, roots = generate()
    if sys.argv[1:] == ['--write-reference']:
        (ROOT / 'EXPECTED.json').write_text(json.dumps(summary, indent=2) + '\n')
        text = '{\n  "schema": ' + json.dumps(SCHEMA) + ',\n  "rows": [\n'
        text += ',\n'.join('    ' + json.dumps(row) for row in roots['rows'])
        (ROOT / 'ROOTS.json').write_text(text + '\n  ]\n}\n')
    elif sys.argv[1:]:
        raise SystemExit('usage: python3 verify.py [--write-reference]')
    else:
        if summary != json.loads((ROOT / 'EXPECTED.json').read_text()):
            raise ValueError('primary summary mismatch')
        if roots != json.loads((ROOT / 'ROOTS.json').read_text()):
            raise ValueError('primary root records mismatch')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
