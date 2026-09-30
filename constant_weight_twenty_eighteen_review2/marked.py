"""Alternative complete star cover for the imported degree20/19 multiplicity-one input.

Every split first star merges to P; its eighteen other second-star blocks
are P-four-arcs, with a P-collinear uncovered triple marking the shared word.
Thus the completed all-branch18-arc census covers these stars too.
"""
from itertools import combinations
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import json
import time

from exact import insist, encoded, mask, bits, packing
from domain import group, image_word, edge_mask, PAIRS, INDEX, pmask


def color(words, mode):
    adjacency = [0] * len(words)
    for i, j in combinations(range(len(words)), 2):
        if (words[i] & words[j]).bit_count() <= 2:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    assigned, classes, unseen = [0] * len(words), [], (1 << len(words)) - 1
    while unseen:
        def key(z):
            degree = (adjacency[z] & unseen).bit_count() if mode // 2 else adjacency[z].bit_count()
            return assigned[z].bit_count(), degree, words[z] if mode % 2 else -words[z]
        v = max(bits(unseen), key=key)
        c = 0
        while assigned[v] >> c & 1:
            c += 1
        if c == len(classes):
            classes.append([])
        classes[c].append(words[v])
        unseen ^= 1 << v
        for z in bits(adjacency[v] & unseen):
            assigned[z] |= 1 << c
    classes = [sorted(v) for v in classes]
    insist(sorted(w for c in classes for w in c) == sorted(words) and all(all((a & b).bit_count() >= 3 for a, b in combinations(c, 2)) for c in classes), 'false marked coloring')
    return classes


def run(work, output):
    started = time.monotonic()
    summary = json.loads((work / 'summary.json').read_text())
    insist(summary['status'] == 'COMPLETE', 'marked audit requires complete main census')
    domain = json.loads((work / 'domain.json').read_text())
    p = domain['plane']
    triangles = [(mask(t), line) for line in p for t in combinations(tuple(bits(line)), 3)]
    symmetries = group()
    standard = mask((1, 2, 3))
    transporters = {t: [g for g in symmetries if image_word(t, g) == standard] for t, _ in triangles}
    insist(all(len(v) == 72 for v in transporters.values()), 'marked flag transporter differs')
    cache, certificates, normalized = {}, [], set()
    for path in sorted(work.glob('batch_*.jsonl')):
        for line in path.read_text().splitlines():
            row = json.loads(line)
            leaf = domain['leaves'][row['index']]
            if leaf[5] != 0 or not row['covers']:
                continue
            leave = leaf[3]
            actual_triangles = [(t, line) for t, line in triangles if leave & pmask(t) == pmask(t)]
            for cover in row['covers']:
                for t, owner in actual_triangles:
                    if t not in cache:
                        first = [mask(q) for q in combinations(range(16), 5)
                                 if (mask(q) & t).bit_count() <= 2 and
                                 all((mask(q) & old).bit_count() <= 2 for old in p if old != owner)]
                        insist(len(first) == 378, 'marked old-word universe differs')
                        cache[t] = first
                    union = [w | 1 << 17 for w in p if w != owner] + [t | 1 << 16 | 1 << 17]
                    union += [w | 1 << 16 for w in cover]
                    packing(union, size=38)
                    insist(sum(w >> 17 & 1 for w in union) == 20 and sum(w >> 16 & 1 for w in union) == 19 and sum(bool(w >> 16 & 1) and bool(w >> 17 & 1) for w in union) == 1, 'marked star parameters differ')
                    q = [w for w in cache[t] if all((w & r).bit_count() <= 2 for r in cover)]
                    insist(all(all((w & r).bit_count() <= 2 for r in union) for w in q), 'false marked residual candidate')
                    choices = [color(q, mode) for mode in range(4)]
                    classes = min(choices, key=lambda c: (len(c), encoded(c)))
                    insist(len(classes) <= 19, 'marked branch lacks upper19 color certificate')
                    record = {'index': row['index'], 'cover': cover, 'triangle': t, 'residual_candidates': q, 'colors': classes}
                    certificates.append(record)
                    original = leave ^ pmask(t)
                    transported = []
                    for g in transporters[t]:
                        mapped = edge_mask((g[x], g[y]) for j in bits(original) for x, y in (PAIRS[j],))
                        blocks = tuple(sorted(image_word(w, g) for w in cover))
                        transported.append((mapped, blocks))
                    least = min(h for h, _ in transported)
                    normalized.update((h, blocks) for h, blocks in transported if h == least)
    insist(len(normalized) == 1093, 'independent complete marked star cover differs from source1093')
    result = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer', 'status': 'COMPLETE', 'marked_star_occurrences': len(certificates), 'normalized_star_pairs': len(normalized), 'max_residual_candidates': max(r['residual_candidates'].__len__() for r in certificates), 'max_colors': max(len(r['colors']) for r in certificates), 'color_counts': dict(Counter(len(r['colors']) for r in certificates)), 'certificate_sha256': sha256(encoded(certificates)).hexdigest(), 'normalized_star_sha256': sha256(encoded(sorted(normalized))).hexdigest(), 'seconds': time.monotonic() - started}
    (output / 'marked-certificates.json').write_bytes(encoded(certificates))
    (output / 'marked-summary.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    run(args.work, args.output)
