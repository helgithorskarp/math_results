"""Check a compact assignment recipe against every archived edge; standard library only.

This does not import the producer, FLINT, a SAT solver, or the earlier proof checker.
The geometry and non-four-colourability are explicit dependencies, not re-proved here.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, itertools, json

S = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def valid_word(word, edges, omit_origin=False):
    require(len(word) == 64513, 'word length')
    require(all(0 <= c < (4 if omit_origin else 5) for v, c in enumerate(word) if not (omit_origin and v == 0)), 'colour range')
    for u, v in edges:
        if omit_origin and u == 0:
            continue
        require(word[u] != word[v], 'monochromatic edge ' + str((u, v)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--producer-word', type=Path)
    ap.add_argument('--check-expected', action='store_true')
    args = ap.parse_args()
    cert = json.loads((S / 'CERTIFICATE.json').read_text())
    raw = (args.work / 'exact_points.json').read_bytes()
    require(digest(raw) == cert['inputs']['exact_points.json']['sha256'], 'pinned points')
    data = json.loads(raw)
    require(data['denominator'] == 96 and data['basis_radicands'] == [1, 2, 3, 6, 5, 10, 15, 30], 'basis and denominator')
    points = data['points']
    require(len(points) == 64513 and points[0] == [0] * 16, 'origin and order')
    raw = (args.work / 'source_graph.dimacs').read_bytes()
    require(digest(raw) == cert['inputs']['source_graph.dimacs']['sha256'], 'pinned author edges')
    lines = raw.decode('ascii').splitlines()
    require(lines[0].split() == ['p', 'edge', '64513', '542472'], 'DIMACS header')
    edges = []
    for line in lines[1:]:
        fields = line.split()
        require(len(fields) == 3 and fields[0] == 'e', 'edge syntax')
        u, v = sorted(int(x) - 1 for x in fields[1:])
        require(0 <= u < v < 64513, 'edge labels')
        edges.append((u, v))
    require(len(edges) == len(set(edges)) == 542472, 'edge multiplicity')

    # Integer linear forms in the archived radical coefficients.
    # The resulting word is checked directly, regardless of the recipe's derivation.
    weights = cert['colour_bit_numerators']
    base = []
    for v, row in enumerate(points):
        divisor = 32 if v <= 32256 else 4
        values = [sum(a * b for a, b in zip(w, row)) for w in weights]
        require(all(x % divisor == 0 for x in values), 'integer colour recipe')
        base.append(sum(((x // divisor) % 2) << j for j, x in enumerate(values)))
    require(base[0] == 0, 'root residue')
    cross = [(u, v) for u, v in edges if 0 < u <= 32256 < v]
    boundary_left = sorted({u for u, v in cross})
    boundary_right = sorted({v for u, v in cross})
    require(len(cross) == len(boundary_left) == len(boundary_right) == 120, '120-edge matching')
    require(all(base[u] == base[v] == 0 for u, v in cross), 'all joining ports have residue zero')
    internal = [(u, v) for u, v in edges if not (0 < u <= 32256 < v)]
    require(all(base[u] != base[v] for u, v in internal), 'two proper half-colourings with common root')
    palette = cert['second_half_palette']
    require(sorted(palette) == list(range(4)) and palette[0] != 0, 'palette swap')
    word = bytes([4] + base[1:32257] + [palette[c] for c in base[32257:]])
    valid_word(word, edges)
    valid_word(word, edges, omit_origin=True)
    if args.producer_word:
        require(args.producer_word.read_bytes() == word, 'independent recipe agrees with polynomial producer')

    permutations = [p for p in itertools.permutations(range(4)) if all(base[u] != p[base[v]] for u, v in cross)]
    require(len(permutations) == 18 and all(p[0] != 0 for p in permutations), 'complete 24-palette classification')
    controls = {}
    def reject(name, bad):
        try:
            valid_word(bad, edges)
        except ValueError:
            controls[name] = True
        else:
            raise ValueError('negative control accepted: ' + name)
    bad = bytearray(word); bad[0] = 0
    reject('reuse_origin_colour_zero', bad)
    bad = bytearray(word); u, v = edges[0]; bad[v] = bad[u]
    reject('monochromatic_edge', bad)
    reject('identity_second_palette', bytes([4] + base[1:]))
    reject('truncated_word', word[:-1])
    bad = bytearray(word); bad[1] = 5
    reject('sixth_colour', bad)
    result = {
        'status': 'VERIFIED_VND_RESIDUE_FIVE_COLOURING_AND_ORIGIN_DELETION',
        'vertices': 64513, 'strict_edges_from_accepted_source': 542472,
        'five_colour_counts': {str(k): v for k, v in sorted(Counter(word).items())},
        'origin_deletion_vertices': 64512,
        'origin_deletion_edges': sum(u != 0 for u, v in edges),
        'origin_degree': sum(u == 0 for u, v in edges),
        'cross_edges': 120, 'boundary_vertices_per_half': 120,
        'all_cross_port_colours': [0, 0],
        'compatible_relative_palette_permutations': len(permutations),
        'five_colour_word_sha256': digest(word),
        'first_half_residue_word_sha256': digest(bytes(base[:32257])),
        'second_half_residue_word_with_root_sha256': digest(bytes([0] + base[32257:])),
        'boundary_left_labels': boundary_left,
        'boundary_right_labels': boundary_right,
        'negative_controls': controls, 'new_solver_calls': 0,
        'non_four_colourability_dependency': 'h3927, accepted h3941; not re-run',
        'target_improvement': False,
    }
    if args.check_expected:
        require(result == json.loads((S / 'EXPECTED.json').read_text()), 'expected receipt')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
