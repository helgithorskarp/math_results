"""Separate literal-field audit of the complete eight-minority packing cover."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import resource
import sys
import time

from common import pins, require, sha, endpoint_auditor
old = endpoint_auditor()
literal_field, expected_clauses = old.literal_field, old.expected_clauses


def main(work):
    start = time.monotonic()
    pins()
    # Independently place four indistinguishable extras and remove eight
    # tuples with a gap8, excluded by the imported phase-window lemma.
    rooted = []
    for units in itertools.combinations_with_replacement(range(8), 4):
        values = tuple(units.count(i) for i in range(8))
        if max(values) <= 3:
            rooted.append(values)
    canonical = sorted({min(t[j:]+t[:j] for j in range(8)) for t in rooted})
    require(len(rooted) == 322 and len(canonical) == 42, 'independent gap cover differs')
    orbit_sizes = Counter()
    labeled = set()
    for excess in canonical:
        gaps = tuple(4+t for t in excess)
        points = tuple(sum(gaps[:i])+i for i in range(8))
        orbit = {tuple(sorted((x+r) % 44 for x in points)) for r in range(44)}
        require(not orbit & labeled, 'overlapping phase orbits')
        labeled.update(orbit)
        orbit_sizes[len(orbit)] += 1
    require(len(labeled) == 1771 and dict(orbit_sizes) == {44:39, 22:2, 11:1},
            'incomplete labeled phase coverage')
    normalized = 0
    for positions in labeled:
        gaps = tuple((positions[(i+1) % 8]-positions[i]) % 44-1 for i in range(8))
        require(sum(gaps) == 36 and 4 <= min(gaps) and max(gaps) <= 7,
                'wrong actual phase gaps')
        excess = tuple(g-4 for g in gaps)
        anchors = [i for i in range(8) if excess[i:]+excess[:i] in canonical]
        require(anchors, 'labeled phase lacks canonical anchor')
        i = anchors[0]
        t = excess[i:]+excess[:i]
        target = tuple(sum(5+x for x in t[:j]) for j in range(8))
        require(tuple(sorted((x-positions[i]) % 44 for x in positions)) == target,
                'phase anchor loses a word')
        normalized += 2  # BOTH backgrounds, no phase-exchange quotient.
    data = json.loads((work / 'models.json').read_text())
    expected_stems = [f'case-{case:02d}-b-{b}' for case in range(1,43) for b in (0,1)]
    require([r['stem'] for r in data['records']] == expected_stems,
            'missing or duplicate eight-minority case')
    require({p.name for p in work.glob('*.cnf')} == {s+'.cnf' for s in expected_stems},
            'missing or unexpected model file')
    slots, supports = literal_field()
    records = []
    for index, record in enumerate(data['records']):
        case, background = index//2+1, index % 2
        require(record['case'] == case and record['background'] == background,
                'case metadata changes the complete cover')
        extras = canonical[case-1]
        gaps = tuple(4+t for t in extras)
        positions = [sum(5+x for x in extras[:j]) for j in range(8)]
        require(record['majority_gaps'] == list(gaps) and
                record['minority_positions'] == positions and
                record['phase_K'] == (36 if background else 8), 'wrong endpoint pattern')
        fixed = {i: background ^ int(i in positions) for i in range(44)}
        require(sum(fixed.values()) == record['phase_K'] and all(
            len({fixed[(i+j) % 44] for j in range(8)}) == 2 for i in range(44)),
            'model does not satisfy its published phase-window premise')
        semantic, free = expected_clauses(slots, supports, fixed)
        require(free == 0, 'packing model leaves a phase free')
        cnf = work / (record['stem']+'.cnf')
        lines = cnf.read_text().splitlines()
        require(lines[0].split() == ['p','cnf','44',str(record['clauses'])],
                'wrong model header or orientation reduction')
        rows = []
        for line in lines[1:]:
            values = list(map(int, line.split()))
            require(values and values[-1] == 0 and all(1 <= abs(v) <= 44
                    for v in values[:-1]), 'invalid literal')
            rows.append(tuple(sorted(values[:-1])))
        require(len(rows) == record['clauses'] and
                Counter(rows) == Counter(list(semantic)+[(-1,)]),
                'entire literal model differs')
        require(sha(cnf) == record['cnf_sha256'] and record['variables'] == 44,
                'model hash/dimension mismatch')
        records.append(dict(stem=record['stem'], clauses=len(rows), cnf_sha256=sha(cnf)))
    result = dict(agent='six-vdw-2', role='researcher', status='EXACT_ENDPOINT8_PACKING_AUDIT',
        rooted_profiles=322, cyclic_orbits_per_background=42,
        phase_orbit_sizes=dict(orbit_sizes), labeled_phase_words_per_endpoint=1771,
        normalized_phase_controls=normalized, records=records,
        literal_APs=375760, removed_zero_APs=4312, signed_supports=26488,
        seconds=time.monotonic()-start,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path = work / ('audit-optimized.json' if not __debug__ else 'audit-normal.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'records'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    main(parser.parse_args().work.absolute())
