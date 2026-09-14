"""Reject corrupted positive certificates through the full verifier."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from verify import HERE, verify


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    args = parser.parse_args()
    original = json.loads((HERE / 'certificate.json').read_text())
    graph = json.loads((args.graph_work / 'graph.json').read_text())
    mutations = []
    bad = deepcopy(original)
    a, b = graph['edges'][0]
    word = list(bad['words'][0])
    word[b] = word[a]
    bad['words'][0] = ''.join(word)
    mutations.append(('unit-edge violation', bad, 'proper colouring'))
    bad = deepcopy(original)
    bad['words'] = [bad['words'][0]] * 5
    mutations.append(('incomplete coverage by valid words', bad, 'complete two-pair coverage'))
    bad = deepcopy(original)
    bad['pairs'][0] = graph['edges'][0]
    mutations.append(('wrong pair domain', bad, 'selected 84 pairs'))
    with TemporaryDirectory() as tmp:
        for label, cert, expected in mutations:
            path = Path(tmp) / 'bad.json'
            path.write_text(json.dumps(cert))
            try:
                verify(args.graph_work, path)
            except ValueError as error:
                if str(error) != expected:
                    raise RuntimeError((label, str(error), expected))
                print('REJECTED:', label)
            else:
                raise RuntimeError('accepted corruption: ' + label)
    print('ALL THREE CORRUPTION CONTROLS REJECTED')
