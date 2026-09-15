"""Exact finite relation check and four-point metric obstruction.

This checks an impossible proposed gluing, not coordinates of a plane graph.
"""
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canon(word):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in word)


def fails(word, clause):
    (a, b), (c, d) = clause
    return word[a] == word[b] and word[c] == word[d]


def determinant(matrix):
    n = len(matrix)
    total = Fraction(0)
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = Fraction((-1)**inversions)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        total += term
    return total


def source_distance(a, b, denominator):
    a, b, c, d = (x-y for x, y in zip(a, b))
    return (Fraction(a*a+33*b*b+3*c*c+11*d*d, denominator**2),
            Fraction(2*(a*b+c*d), denominator**2))


def verify(cert):
    n = cert['roles']
    require(n == 7, 'role count')
    clauses = cert['clauses']
    require(len(clauses) == 62, 'clause count')
    normalized = []
    for clause in clauses:
        require(len(clause) == 2 and all(len(e) == 2 for e in clause), 'clause shape')
        flat = [v for e in clause for v in e]
        require(all(type(v) is int and 0 <= v < n for v in flat), 'role domain')
        require(len(set(flat)) == 4, 'source terminals must be distinct')
        normalized.append(tuple(sorted(tuple(sorted(e)) for e in clause)))
    require(len(set(normalized)) == len(clauses), 'duplicate clause')
    require(cert['raw_points'] == n+7*len(clauses) <= 508, 'raw budget')
    rejected, canonical, stream = 0, set(), hashlib.sha256()
    for word in itertools.product(range(4), repeat=n):
        bad = [i for i, c in enumerate(clauses) if fails(word, c)]
        require(bad, 'four-colour assignment survives')
        rejected += 1
        canonical.add(canon(word))
        stream.update(bytes((bad[0],)))
    require(len(canonical) == 715, 'canonical pattern count')
    five = cert['five_colour_terminal_word']
    require(len(five) == n and all(type(c) is int and 0 <= c < 5 for c in five), 'five-word domain')
    require(not any(fails(five, c) for c in clauses), 'five-word fails')

    rows = cert['source_terminal_rows']
    require(rows == [[6, 0, -6, 0], [12, 0, 12, 0],
                     [20, 0, 0, 4], [-5, -1, 5, -1]], 'source rows')
    den = cert['source_coordinate_denominator']
    require(den == 12, 'source denominator')
    for a, b in ((0, 1), (2, 3)):
        require(source_distance(rows[a], rows[b], den) == (7, 0), 'marked distance')
    four = cert['equidistant_four_roles']
    require(len(four) == len(set(four)) == 4 and all(v in range(n) for v in four), 'four roles')
    wanted = set(itertools.combinations(sorted(four), 2))
    found = set()
    for w in cert['metric_witness']:
        edge = tuple(w['pair'])
        pos = w['selected_clause_position']
        require(edge in wanted and 0 <= pos < len(clauses), 'witness range')
        require(list(edge) in clauses[pos], 'metric pair not required by cited clause')
        found.add(edge)
    require(found == wanted, 'incomplete four-point metric witness')
    gram = [[Fraction(7) if i == j else Fraction(7, 2) for j in range(3)] for i in range(3)]
    det = determinant(gram)
    require(det == Fraction(*cert['declared_gram_determinant']) == Fraction(343, 2), 'Gram determinant')
    require(cert['physical_realization_exists'] is False, 'no physical realization may be asserted')
    mandatory = {tuple(sorted(e)) for clause in clauses for e in clause}
    return {'status': 'RELATION_INCONSISTENT_BUT_EXACT_GEOMETRY_IMPOSSIBLE',
            'roles': n, 'clauses': len(clauses), 'raw_label_budget': cert['raw_points'],
            'named_four_colour_words_rejected': rejected,
            'canonical_four_colour_patterns_rejected': len(canonical),
            'first_reject_stream_sha256': stream.hexdigest(),
            'five_colour_terminal_word_checked': five,
            'required_squared_pair_distance': 7, 'mandatory_long_pairs': len(mandatory),
            'equidistant_four_roles': four,
            'gram_determinant': [det.numerator, det.denominator],
            'actual_plane_graph_supplied': False, 'record_candidate': False,
            'selected_incidence_system_retired': True}


def main():
    cert = json.loads(Path(__file__).with_name('certificate.json').read_text())
    print(json.dumps(verify(cert), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
