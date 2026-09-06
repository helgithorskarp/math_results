"""Rebuild compact evidence and run the independent checker and controls."""
from hashlib import sha256
from pathlib import Path
import json

import build
import check
import controls
import novelty


def main():
    root = Path(__file__).parent
    entries = (root/'SHA256SUMS').read_text().splitlines()
    for line in entries:
        digest, name = line.split('  ', 1)
        check.need(sha256((root/name).read_bytes()).hexdigest() == digest, 'manifest: '+name)
    generated = (json.dumps(build.build(), separators=(',', ':'))+'\n').encode()
    check.need(generated == (root/'certificate.json').read_bytes(), 'byte-identical certificate regeneration')
    for name, result in [('expected.json', check.check(json.loads(generated))),
                         ('controls_expected.json', controls.controls()),
                         ('novelty_expected.json', novelty.compare())]:
        check.need(result == json.loads((root/name).read_text()), 'expected result: '+name)
    print(json.dumps({'status': 'REPRODUCED_CAYLEY40_OBSTRUCTION',
                      'manifest_entries': len(entries), 'certificate_regenerated': True,
                      'all_connection_sets_covered': 1 << 20,
                      'saved_graph_novelty_checks': 21,
                      'ramsey_bound_improved': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
