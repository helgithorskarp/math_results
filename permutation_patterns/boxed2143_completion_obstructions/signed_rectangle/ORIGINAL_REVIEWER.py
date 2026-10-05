"""Lyra's independent length-difference and literal-box check of Theo522.

Expected graph edges come from recomputed inversion lengths of transposed
permutations, not the author's open-rectangle scan. No author executable is
imported. Uniform implications are checked in a separate written proof review.
"""

from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from definition_checker import occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def length(p):
    return sum(p[a] > p[b] for a in range(len(p)) for b in range(a + 1, len(p)))


def swap(p, a, b):
    return p[:a] + (p[b],) + p[a + 1:b] + (p[a],) + p[b + 1:]


@lru_cache(maxsize=6000)
def covers(p):
    baseline = length(p)
    edges, negative = [], []
    for a, b in itertools.combinations(range(len(p)), 2):
        delta = length(swap(p, a, b)) - baseline
        if abs(delta) == 1:
            edges.append((a, b))
        if delta == -1:
            negative.append((a, b))
    return tuple(edges), tuple(negative)


def normalized(data):
    return json.loads(json.dumps(data))


def graph_controls():
    patterns = tuple(p for p in itertools.permutations(range(1, 5))
                     if not any(p[i] < p[j] < p[k] or p[i] > p[j] > p[k]
                                for i, j, k in itertools.combinations(range(4), 3)))
    require(patterns == ((2, 1, 4, 3), (2, 4, 1, 3), (3, 1, 4, 2), (3, 4, 1, 2)),
            'Four-order classification differs')
    require(tuple(length(p) for p in patterns) == (2, 3, 3, 4), 'Sign counts differ')
    parents = swaps = quads = 0
    stream = hashlib.sha256()
    clique_types = Counter()
    for n in range(8):
        for p in itertools.permutations(range(1, n + 1)):
            edge_tuple, minus_tuple = covers(p)
            edges, minus = set(edge_tuple), set(minus_tuple)
            if n <= 6:
                baseline = length(p)
                for a, b in itertools.combinations(range(n), 2):
                    delta = length(swap(p, a, b)) - baseline
                    inside = sum(min(p[a], p[b]) < p[x] < max(p[a], p[b])
                                 for x in range(a + 1, b))
                    sign = 1 if p[a] < p[b] else -1
                    require(delta == sign * (1 + 2 * inside), 'Uniform swap formula control fails')
                    require(((a, b) in edges) == (inside == 0), 'Cover/rectangle control differs')
                    require(((a, b) in minus) == (inside == 0 and sign == -1), 'Negative cover differs')
                    swaps += 1
            selected = []
            for indices in itertools.combinations(range(n), 4):
                pairs = tuple(itertools.combinations(indices, 2))
                if all(pair in edges for pair in pairs):
                    values = tuple(p[x] for x in indices)
                    pattern = tuple(sorted(values).index(x) + 1 for x in values)
                    require(pattern in patterns, 'Clique has an excluded relative order')
                    clique_types[pattern] += 1
                    if sum(pair in minus for pair in pairs) == 2:
                        selected.append(indices)
                quads += 1
            actual = tuple(occurrences(p))
            require(tuple(selected) == actual, 'COMPLETE selected signed-K4/box sets differ')
            stream.update((json.dumps([p, sorted(edges), sorted(minus), actual],
                                     separators=(',', ':')) + '\n').encode())
            parents += 1
    require(len(covers((2, 1, 4, 3))[0]) == len(covers((2, 4, 1, 3))[0]) == 6,
            'Unsigned K4 examples differ')
    require(tuple(occurrences((2, 1, 4, 3))) and not tuple(occurrences((2, 4, 1, 3))),
            'Unsigned avoidance information-loss example fails')
    return {'complete_permutations_through7': parents, 'transpositions_through6': swaps,
            'quadruples_checked': quads, 'signed_graph_stream_sha256': stream.hexdigest(),
            'all_K4_relative_patterns': {''.join(map(str, k)): v for k, v in sorted(clique_types.items())}}


def interleave(p, rho):
    out = []
    for i, x in enumerate(p):
        out.append(2 * x - 1)
        if i < len(rho):
            out.append(2 * rho[i])
    return tuple(out)


def ascent_control():
    rows = []
    tested = forbidden = 0
    for m in range(2, 6):
        complete = 0
        for p in itertools.permutations(range(1, m + 1)):
            for rho in itertools.permutations(range(1, m)):
                word = interleave(p, rho)
                actual = tuple(occurrences(word))
                complete += 1
                tested += 1
                if not actual:
                    continue
                forbidden += 1
                degree = len(covers(word)[1])
                neighbors = []
                for a, b in itertools.combinations(range(m - 1), 2):
                    child_rho = swap(rho, a, b)
                    child = interleave(p, child_rho)
                    neighbors.append({'scaffold_positions_swapped': (a, b), 'rho': child_rho,
                                      'word': child, 'down_degree': len(covers(child)[1]),
                                      'occurrences': tuple(occurrences(child))})
                if all(x['down_degree'] <= degree for x in neighbors):
                    all_scores = [{'rho': r, 'down_degree': len(covers(interleave(p, r))[1]),
                                   'avoids': not tuple(occurrences(interleave(p, r)))}
                                  for r in itertools.permutations(range(1, m))]
                    rows.append({'m': m, 'complete_input_scaffold_pairs': complete, 'complete_length': False})
                    return normalized({'scope_rows': rows, 'input_scaffold_pairs_tested': tested,
                        'nonavoiding_pairs_tested': forbidden, 'strict_ascent_failure': {
                        'm': m, 'pi': p, 'rho': rho, 'word': word, 'down_degree': degree,
                        'negative_edges_zero_based_positions': covers(word)[1],
                        'boxed_occurrences': actual, 'all_even_transposition_neighbors': neighbors,
                        'all_scaffold_scores_for_this_input': all_scores,
                        'is_global_down_degree_maximizer_for_input':
                        degree == max(x['down_degree'] for x in all_scores)}})
        rows.append({'m': m, 'complete_input_scaffold_pairs': complete, 'complete_length': True})
    raise RuntimeError('Expected ascent failure not reached')


def run():
    began = time.monotonic()
    base = Path(__file__).parent
    packet = base / 'received/theo_bruhat_v1'
    manifest_bytes = (packet / 'MANIFEST.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    for filename, record in manifest['files'].items():
        source = (packet / filename).read_bytes()
        require(len(source) == record['bytes'] and hashlib.sha256(source).hexdigest() == record['sha256'],
                'Author frozen bytes changed: ' + filename)
    expected = json.loads((packet / 'bruhat-completion-probe-v1.json').read_text())
    graph = graph_controls()
    ascent = ascent_control()
    require(graph == expected['graph_controls'], 'Author graph control fields differ')
    require(ascent == expected['ascent_probe'], 'Author entire ascent-control fields differ')
    return {'author': 'literature-researcher-4', 'checker': 'literature-researcher-2',
            'decision_message_id': 410, 'full_target_solved': False,
            'checked_scope': 'complete finite signed-K4/literal-box sets, inversion-length cover criterion and strict-ascent failure; uniform geometric and conditional growth bridges reviewed separately',
            'author_manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
            'proof_sha256': manifest['files']['BRUHAT_RECTANGLE_REDUCTION_V1.md']['sha256'],
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'independence': 'expected covers from full inversion-length differences, literal target from own direct strict-rectangle generator; no author executable',
            'graph_controls': graph, 'ascent_probe': ascent, 'all_deterministic_fields_match': True,
            'python': platform.python_version(), 'elapsed_seconds': time.monotonic() - began,
            'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
