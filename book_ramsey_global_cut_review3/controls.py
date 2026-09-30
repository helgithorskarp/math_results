#!/usr/bin/env python3
"""Targeted corruption controls; uses only this reviewer's checker."""
from copy import deepcopy
import json
from pathlib import Path
import audit


def rejects(action, label):
    try:
        action()
    except ValueError:
        return label
    raise ValueError('corruption accepted: ' + label)


def main():
    data = json.loads((Path(__file__).resolve().parent / 'INPUT.json').read_text())
    labels = []
    rows = data['local_fixtures'][0]['rows'].copy()
    rows[0] = ('1' if rows[0][1] == '0' else '0').join([rows[0][:1], rows[0][2:]])
    labels.append(rejects(lambda: audit.decode(rows), 'asymmetric adjacency'))
    case = next(t for t in data['uniform_templates'] if t['name'] == 'C7')
    Q = [tuple(e) for e in case['Q_edges']]
    missing = deepcopy(case)
    missing['book_records'] = missing['book_records'][1:]
    labels.append(rejects(lambda: audit.uniform_case(Q, missing), 'omitted survivor'))
    duplicate = deepcopy(case)
    duplicate['book_records'].append(duplicate['book_records'][0])
    labels.append(rejects(lambda: audit.uniform_case(Q, duplicate), 'duplicate survivor'))
    altered = deepcopy(case)
    altered['column_masks'][0] ^= 1
    labels.append(rejects(lambda: audit.uniform_case(Q, altered), 'altered binary column'))
    _, adj = audit.template(Q)
    r = case['book_records'][0]
    for bit, (a, b) in enumerate(audit.PAIRS7):
        if r[0] >> bit & 1:
            adj[15+a] |= 1 << (15+b)
            adj[15+b] |= 1 << (15+a)
    audit.verify_book(adj, r[3], r[4])
    bad_pages = r[4].copy()
    bad_pages[0] = r[3][0]
    labels.append(rejects(lambda: audit.verify_book(adj, r[3], bad_pages), 'book contains spine vertex'))
    local = audit.decode(data['local_fixtures'][0]['rows'])
    a = 0
    b = next(j for j in range(1, 11) if j not in local[a])
    audit.edge(local, a, b)
    labels.append(rejects(lambda: audit.literal_identities(local, 0), 'wrong neighborhood histogram'))
    # audit.literal_identities checks every omitted-+2 row mutation separately.
    print(json.dumps({'negative_controls': labels, 'rejected': len(labels)}, sort_keys=True))


if __name__ == '__main__':
    main()
