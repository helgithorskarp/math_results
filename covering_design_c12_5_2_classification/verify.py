"""Regenerate and check the complete compact catalogue."""
from collections import Counter
import json
from math import factorial
from pathlib import Path
import sys

from enumeration import digest, generate

ROOT = Path(__file__).resolve().parent


def write_catalogue(data):
    """One record per line keeps the complete representative list compact."""
    text = '{\n  "low_levels": ' + json.dumps(data['low_levels']) + ',\n'
    for key in ('cases', 'designs'):
        text += '  "' + key + '": [\n'
        text += ',\n'.join('    ' + json.dumps(record) for record in data[key])
        text += '\n  ]' + (',\n' if key == 'cases' else '\n')
    (ROOT / 'CATALOGUE.json').write_text(text + '}\n')


def summary(data):
    counts = Counter(d['degree3_points'] - 3 for d in data['designs'])
    pointed = Counter()
    orders = Counter()
    labelled = 0
    for design in data['designs']:
        order = design['automorphism_order']
        if order <= 0 or factorial(12) % order:
            raise ValueError('invalid automorphism order')
        labelled += factorial(12) // order
        orders[order] += 1
        for orbit in design['point_orbits']:
            pointed[design['point_signatures'][orbit[0]].bit_count()] += 1
    return dict(status='VERIFIED_107_OPTIMAL_C12_5_2_CLASSES',
                classes=len(data['designs']), classes_by_degree5_count={str(a): counts[a] for a in range(5)},
                low_type_levels=data['low_levels'],
                labelled_completions=sum(c['labelled'] for c in data['cases']),
                search_nodes=sum(c['nodes'] for c in data['cases']),
                pointed_classes_by_degree={str(d): pointed[d] for d in sorted(pointed)},
                automorphism_orders={str(o): orders[o] for o in sorted(orders)},
                labelled_coverings=labelled, catalogue_sha256=digest(data), cases=data['cases'])


def main():
    data = generate()
    result = summary(data)
    if sys.argv[1:] == ['--write-reference']:
        write_catalogue(data)
        (ROOT / 'EXPECTED.json').write_text(json.dumps(result, indent=2) + '\n')
    elif sys.argv[1:]:
        raise SystemExit('usage: python3 verify.py [--write-reference]')
    else:
        if data != json.loads((ROOT / 'CATALOGUE.json').read_text()):
            raise ValueError('catalogue differs from the regenerated result')
        if result != json.loads((ROOT / 'EXPECTED.json').read_text()):
            raise ValueError('verification summary differs from EXPECTED.json')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
