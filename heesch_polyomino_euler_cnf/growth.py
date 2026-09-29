"""Enumerate one exact cell-growth family; no Heesch decisions are made here."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from corona import normalize, orientations
from topology import FOUR, flood_counts, local_counts


def generate_family(seed, added=3):
    if type(added) is not int or added < 0:
        raise ValueError('added count must be a nonnegative integer')
    seed = normalize(seed)
    if flood_counts(seed) != (1, 0) or local_counts(seed)[3]:
        raise ValueError('seed must be a disc polyomino')
    layer = {seed}
    sizes = []
    for _ in range(added):
        enlarged = set()
        for tile in layer:
            cells = set(tile)
            boundary = {(x + dx, y + dy) for x, y in cells for dx, dy in FOUR} - cells
            for p in boundary:
                enlarged.add(normalize(cells | {p}))
        layer = enlarged
        sizes.append(len(layer))
    family = sorted({min(orientations(tile)) for tile in layer
                     if flood_counts(tile) == (1, 0) and local_counts(tile)[3] == 0})
    return family, sizes


def independent_family(seed, added=3):
    """All subsets of the bounded taxicab neighbourhood, rather than growth paths."""
    from validate_cover import independent_variants
    root = set(normalize(seed))
    potential = sorted({(x + dx, y + dy) for x, y in root
                        for dx in range(-added, added + 1)
                        for dy in range(-added, added + 1)
                        if abs(dx) + abs(dy) <= added} - root)
    adjacent = {(x + dx, y + dy) for x, y in root for dx, dy in FOUR} - root
    family = set()
    examined = 0
    connected = 0
    for raw in itertools.combinations(potential, added):
        examined += 1
        extra = set(raw)
        reached = extra & adjacent
        while True:
            larger = reached | {p for p in extra - reached
                                if any((p[0] + dx, p[1] + dy) in reached for dx, dy in FOUR)}
            if larger == reached:
                break
            reached = larger
        if reached != extra:
            continue
        connected += 1
        cells = root | extra
        if flood_counts(cells) == (1, 0) and local_counts(cells)[3] == 0:
            family.add(min(independent_variants(cells)))
    return sorted(family), {'potential_cells': len(potential),
                            'subsets_examined': examined, 'connected_subsets': connected}


def serialization(family):
    return json.dumps(family, separators=(',', ':')) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=Path, default=Path(__file__).parent / 'kaplan17.json')
    parser.add_argument('--added', type=int, default=3)
    parser.add_argument('--independent', action='store_true')
    parser.add_argument('--family', type=Path)
    args = parser.parse_args()
    seed = json.loads(args.seed.read_text())['cells']
    family, sizes = generate_family(seed, args.added)
    raw = serialization(family)
    stats = {'layer_counts': sizes, 'free_disc_shapes': len(family),
             'family_sha256': hashlib.sha256(raw.encode()).hexdigest()}
    if args.independent:
        independent, details = independent_family(seed, args.added)
        assert independent == family
        stats.update(details)
        stats['independent_family_exactly_matches'] = True
    if args.family:
        args.family.write_text(raw)
    print(json.dumps(stats, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
