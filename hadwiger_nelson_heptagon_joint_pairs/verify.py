"""Exact geometry and positive two-pair coverage; no SAT dependency."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'hadwiger_nelson_heptagon_difference_lifts'))
import geometry as F


def require(value, message):
    if not value:
        raise ValueError(message)


def verify(graph_work, certificate):
    raw = (graph_work / 'graph.json').read_bytes()
    cert = json.loads(certificate.read_text())
    require(cert['schema'] == 'heptagon-joint-pairs-v1', 'schema')
    require(sha256(raw).hexdigest() == cert['graph_sha256'], 'graph identity')
    g = json.loads(raw)
    H, den = F.integerize(F.host())
    P = sorted({F.sub(a, b) for a in H for b in H})
    require(den == 7 and g['denominator'] == 7, 'denominator')
    require(H == list(map(tuple, g['host'])), 'motif')
    require(P == list(map(tuple, g['points'])) and len(P) == 421, 'strict support')
    E, S3 = [], []
    for a, b in combinations(range(421), 2):
        n = F.norm(F.sub(P[a], P[b]))
        if n == F.scale(F.ONE, 49):
            E.append((a, b))
        if n == F.scale(F.ONE, 147):
            S3.append((a, b))
    require(E == list(map(tuple, g['edges'])) and len(E) == 1848, 'all unit edges')
    require(S3 == list(map(tuple, g['sqrt3_pairs'])) and len(S3) == 126, 'sqrt3 pairs')
    pairs = list(map(tuple, cert['pairs']))
    prior = json.loads((HERE.parent / 'hadwiger_nelson_heptagon_kempe' / 'expected.json').read_text())
    require(pairs == list(map(tuple, prior['covered_pairs'])), 'selected 84 pairs')
    require(len(pairs) == len(set(pairs)) == 84 and set(pairs) <= set(S3), 'pair domain')
    where = {p: i for i, p in enumerate(P)}
    rot = [where[F.mul(F.POW[3], p)] for p in P]
    require(sorted(rot) == list(range(421)), 'rotation bijective')
    require({tuple(sorted((rot[a], rot[b]))) for a, b in E} == set(E), 'unit graph rotation')
    rp = [pairs.index(tuple(sorted((rot[a], rot[b])))) for a, b in pairs]
    q = list(range(421))
    for _ in range(14):
        q = [rot[v] for v in q]
    require(q == list(range(421)), 'rotation exponent')

    def canonical(key):
        z = tuple(sorted(key))
        orbit = []
        for _ in range(14):
            orbit.append(z)
            z = tuple(sorted(rp[i] for i in z))
        require(z == tuple(sorted(key)), 'pair orbit closure')
        return min(orbit)

    classes = Counter(canonical(k) for k in combinations(range(84), 2))
    covered = set()
    per_word = []
    words = cert['words']
    require(len(words) == 5, 'five base words')
    for text in words:
        require(len(text) == 421 and set(text) <= set('0123'), 'word format')
        word = list(map(int, text))
        require(all(word[a] != word[b] for a, b in E), 'proper colouring')
        mono = [i for i, (a, b) in enumerate(pairs) if word[a] == word[b]]
        hit = {canonical(k) for k in combinations(mono, 2)}
        per_word.append(len(hit))
        covered.update(hit)
    require(covered == set(classes), 'complete two-pair coverage')
    return {
        'status': 'ALL 3486 TWO-PAIR PRESCRIPTIONS EXTEND',
        'points': 421, 'unit_edges': len(E), 'physical_pair_checks': 88410,
        'selected_sqrt3_pairs': len(pairs), 'labelled_prescriptions': sum(classes.values()),
        'pair_set_rotation_classes': len(classes),
        'class_size_multiplicities': dict(sorted(Counter(classes.values()).items())),
        'base_words': len(words), 'base_edge_checks': len(words) * len(E),
        'class_coverage_per_word': per_word,
        'certificate_sha256': sha256(certificate.read_bytes()).hexdigest(),
        'graph_sha256': sha256(raw).hexdigest(),
        'record_improvement': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    started = time.perf_counter()
    result = verify(args.graph_work, args.certificate)
    result['seconds'] = time.perf_counter() - started
    print(json.dumps(result, indent=2))
