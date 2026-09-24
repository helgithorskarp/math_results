"""Positive fixtures and size-preserving negative witness mutations."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

from audit import direct_check, graph, isomorphic
from enumeration import check_cover

ROOT = Path(__file__).resolve().parent


def signatures(blocks):
    return [sum(1 << j for j, block in enumerate(blocks) if p in block) for p in range(12)]


def main():
    catalogue = json.loads((ROOT / 'CATALOGUE.json').read_text())['designs']
    matches = []
    for fixture in json.loads((ROOT / 'FIXTURES.json').read_text()):
        rows = signatures(fixture['blocks'])
        check_cover(rows)
        found = [d['id'] for d in catalogue if isomorphic(graph(rows), graph(d['point_signatures']))]
        if len(found) != 1:
            raise ValueError('historical fixture lacks a unique catalogue class')
        matches.append(dict(fixture=fixture['name'], catalogue_id=found[0]))
    sample = catalogue[0]
    blocks = [set(p for p in range(12) if b >> p & 1) for b in sample['blocks']]
    changed = None
    for i in range(9):
        for old in sorted(blocks[i]):
            for new in sorted(set(range(12)) - blocks[i]):
                trial = [set(b) for b in blocks]
                trial[i] = trial[i] - {old} | {new}
                if len({tuple(sorted(b)) for b in trial}) != 9:
                    continue
                if any(not any(p in b and q in b for b in trial) for p, q in combinations(range(12), 2)):
                    changed = trial
                    break
            if changed is not None:
                break
        if changed is not None:
            break
    if changed is None:
        raise ValueError('failed to construct an invalid size-preserving mutation')
    bad = deepcopy(sample)
    bad['blocks'] = [sum(1 << p for p in b) for b in changed]
    bad['point_signatures'] = signatures(changed)
    rejected = []
    for name, function in [('primary_uncovered_pair', lambda: check_cover(bad['point_signatures'])),
                           ('audit_uncovered_pair', lambda: direct_check(bad)),
                           ('primary_missing_point', lambda: check_cover(sample['point_signatures'][:-1]))]:
        try:
            function()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative witness was accepted: ' + name)
    print(json.dumps(dict(status='FIXTURES_AND_MUTATIONS_PASSED', fixtures=matches, rejected=rejected), indent=2))


if __name__ == '__main__':
    main()
