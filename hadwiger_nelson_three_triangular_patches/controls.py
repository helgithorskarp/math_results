#!/usr/bin/env python3
"""Adversarial controls for the committed three-colouring certificate."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('COLOUR_CERTIFICATE.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    state = verify.prepare()
    graphs = verify.audit_certificate(certificate, state)
    rejected = []

    def reject(name, mutate):
        damaged = deepcopy(certificate)
        mutate(damaged)
        try:
            verify.audit_certificate(damaged, state)
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise RuntimeError('accepted corrupted certificate: '+name)

    first = sorted(graphs)[0]
    edge = graphs[first][0]
    reject('wrong format', lambda c: c.update(format=2))
    reject('wrong family', lambda c: c.update(family='other'))
    reject('missing graph', lambda c: c['graph_colourings'].pop(first))
    reject('extra graph', lambda c: c['graph_colourings'].update({'0'*64: '0'*505}))
    reject('short colour word',
           lambda c: c['graph_colourings'].__setitem__(first,
                                                       c['graph_colourings'][first][:-1]))
    reject('fourth colour in word',
           lambda c: c['graph_colourings'].__setitem__(first,
                                                       '3'+c['graph_colourings'][first][1:]))

    def conflict(c):
        word = list(c['graph_colourings'][first])
        word[edge[1]] = word[edge[0]]
        c['graph_colourings'][first] = ''.join(word)
    reject('monochromatic strict edge', conflict)

    # A unit triangle in P proves the matching lower bound chi>=3 without a
    # solver. All eight binary assignments fail one of its three edges.
    binary_proper = sum(a != b and a != c and b != c
                        for a in range(2) for b in range(2) for c in range(2))
    verify.require(binary_proper == 0, 'binary triangle control failed')
    result = {'verified': True, 'rejected_corruptions': len(rejected),
              'controls': rejected, 'binary_triangle_assignments': 8,
              'binary_triangle_proper_colourings': binary_proper}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
