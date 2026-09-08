"""Small complete encoding controls and independent geometry fixtures."""
from itertools import combinations, product
import argparse
import json
import geometry as G
import integer_audit as A
from verify import word_check


def main(boundary_words=None):
    assignments = 0
    for n in (2, 3):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [e for k, e in enumerate(possible) if mask >> k & 1]
            clauses = G.cnf(n, edges, [0, 1])
            for word in product(range(4), repeat=n):
                model = {4*v+c+1: word[v] == c for v in range(n) for c in range(4)}
                encoded = all(any(model[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses)
                direct = word[0] == 0 and word[1] == 1 and all(word[u] != word[v] for u, v in edges)
                G.require(encoded == direct, 'colour encoding control')
                assignments += 1
    boolean_assignments = 0
    for edges in ([], [(0, 1)]):
        clauses = G.cnf(2, edges, [0, 1])
        for mask in range(256):
            encoded = all(any(bool(mask >> (abs(lit)-1) & 1) == (lit > 0) for lit in clause) for clause in clauses)
            colours = [[c for c in range(4) if mask >> (4*v+c) & 1] for v in range(2)]
            direct = (all(len(cs) == 1 for cs in colours) and colours[0] == [0] and colours[1] == [1] and
                      all(colours[u] != colours[v] for u, v in edges))
            G.require(encoded == direct, 'arbitrary Boolean assignment control')
            boolean_assignments += 1
    # Both spindle endpoints, a unit neighbour of the origin, negative points,
    # and points with nonzero sqrt(11) and sqrt(33) coefficients.
    rows = sorted([(0, 0, 0, 0), (0, 0, 96, 0), (0, 0, -96, 0),
                   (0, 0, 36, 0), (18, 0, 18, 0), (0, 6, 0, 2), (6, -6, 12, 2)])
    edges, labels, _ = G.spindle(rows)
    points = A.points(rows)
    checked, _ = A.edges(points)
    G.require(edges == checked, 'spindle edge fixture')
    all_pairs = [(i, j) for i, j in combinations(range(len(points)), 2)
                 if A.distance(points[i], points[j]) == (A.SCALE*A.SCALE, 0, 0, 0, 0, 0, 0, 0)]
    G.require(checked == all_pairs, 'constant filter control')
    origin, terminal = rows.index((0, 0, 0, 0)), rows.index((0, 0, 96, 0))
    G.require((terminal, labels[terminal]) in edges and A.distance(points[origin], points[terminal])[0] ==
              9216*128*128, 'anchor fixture')
    rejected = 0
    for word, n, es, colours in [('0', 2, [], 4), ('04', 2, [], 4), ('00', 2, [(0, 1)], 4),
                                  ('05', 2, [], 5), ([0, 1], 2, [], 4)]:
        try:
            word_check(word, n, es, colours)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid colouring accepted')
    word_check('01', 2, [(0, 1)], 4)
    result = {'encoding_assignments': assignments, 'boolean_encoding_assignments': boolean_assignments,
                      'geometry_fixture_pairs': len(points)*(len(points)-1)//2,
                      'malformed_colourings_rejected': rejected}
    if boundary_words:
        import boundary
        words = json.loads(open(boundary_words).read())
        first = next(iter(words))
        bad_inputs = [dict(words), dict(words), dict(words)]
        del bad_inputs[0][first]
        bad_inputs[1][first] = '0'*len(words[first])
        bad_inputs[2]['extra'] = words[first]
        for bad in bad_inputs:
            try:
                boundary.verify(bad)
            except ValueError:
                continue
            raise ValueError('invalid boundary witness accepted')
        result['malformed_boundary_witnesses_rejected'] = len(bad_inputs)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--boundary-words')
    main(parser.parse_args().boundary_words)
