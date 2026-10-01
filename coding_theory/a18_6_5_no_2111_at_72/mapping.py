"""Regenerate every actual seven-point mapping fiber from literal stars."""
import hashlib
import json
from paths import WORK


def run():
    d = json.loads((WORK/'tail_carrier.json').read_text())
    if not d['status'].startswith('COMPLETE') or len(d['pairs']) != 64:
        raise RuntimeError('incomplete tail carrier')
    lines = ['PAIR2111_V1 '+str(d['total_orbits'])]
    specs = []
    for pair in d['pairs']:
        first = d['stars'][pair['first']]
        second = d['stars'][pair['second']]
        for orbit in pair['orbits']:
            fixed = [-1]*16
            for u, v in zip(second['tail'], orbit['representative']):
                fixed[u-1] = v-1
            a = sorted(w >> 1 for w in first['words'] if not w & 1)
            b = sorted(w >> 1 for w in second['words'] if not w & 1)
            if len(a) != 17 or len(b) != 17:
                raise RuntimeError('wrong residual star lengths')
            index = len(specs)
            lines.append(' '.join(map(str, [index]+a+b+fixed)))
            specs.append(dict(index=index, first=pair['first'], second=pair['second'],
                              tail_orbit=orbit['index'], orbit_size=orbit['orbit_size'], fixed=fixed))
    raw = ('\n'.join(lines)+'\n').encode()
    (WORK/'mapping_fibers.txt').write_bytes(raw)
    record = dict(agent='six-code-3', role='researcher', fibers=specs,
                  matrix_sha256=hashlib.sha256(raw).hexdigest())
    (WORK/'mapping_specs.json').write_text(json.dumps(record, indent=2)+'\n')
    print('COMPLETE mapping matrices', len(specs), record['matrix_sha256'])
    return record


if __name__ == '__main__':
    run()
