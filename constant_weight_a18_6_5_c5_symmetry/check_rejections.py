"""Five meaningful rejection controls for the actual no-ten-clique certificate."""
from pathlib import Path
import copy
import json
import verify


def main():
    folder = Path(__file__).resolve().parent
    certificate = json.loads((folder / 'certificate.json').read_text())
    full = verify.reconstruct()
    point_sets = [tuple(map(frozenset, orbit)) for orbit in full]
    adj = verify.adjacency([point_sets[i] for i in certificate['residual']])
    candidates = set(range(len(adj)))
    verify.check_tree(certificate['tree'], candidates, 10, adj)
    controls = {}
    bad = copy.deepcopy(certificate['tree'])
    bad['children'].pop()
    controls['missing_branch'] = bad
    bad = copy.deepcopy(certificate['tree'])
    bad['colors'][0].pop()
    controls['incomplete_partition'] = bad
    bad = copy.deepcopy(certificate['tree'])
    a, b = next((a, b) for a in range(len(adj)) for b in sorted(adj[a]) if b > a)
    for cls in bad['colors']:
        if b in cls:
            cls.remove(b)
    bad['colors'] = [cls for cls in bad['colors'] if cls]
    next(cls for cls in bad['colors'] if a in cls).append(b)
    controls['edge_in_color'] = bad
    controls['false_cardinality_leaf'] = {'small': True}
    bad = copy.deepcopy(certificate['tree'])
    bad['colors'][0].append(len(adj))
    controls['extra_vertex'] = bad
    rejected = {}
    for name, tree in controls.items():
        try:
            verify.check_tree(tree, candidates, 10, adj)
        except ValueError as error:
            rejected[name] = str(error)
        else:
            raise RuntimeError('invalid certificate accepted: ' + name)
    print(json.dumps({'controls_rejected': rejected}, indent=2))


if __name__ == '__main__':
    main()
