"""Complete block-tail matching, with explicit guards and per-product records."""
import argparse
import itertools
import json
import time
from pathlib import Path
import domain

def partials(c):
    su, sv, sx, sb = c['second_mark']
    u, v, y = c['first_mark']
    source_u = tuple(p for p in c['source_u_tail'] if p != su)
    target_u = tuple(p for p in c['target_u_tail'] if p != u)
    source_other = tuple(t for t in c['source_tails'] if t != c['source_u_tail'])
    target_other = tuple(t for t in c['target_tails'] if t != c['target_u_tail'])
    for u_images in itertools.permutations(target_u):
        for tail_images in itertools.permutations(target_other):
            for point_images in itertools.product(*(tuple(itertools.permutations(t)) for t in tail_images)):
                mapping = [-1] * 17
                mapping[su], mapping[sv], mapping[sx] = u, v, 17
                for p, image in zip(source_u, u_images):
                    mapping[p] = image
                for source, target in zip(source_other, point_images):
                    for p, image in zip(source, target):
                        mapping[p] = image
                domain.require(len({p for p in mapping if p >= 0}) == 14, 'partial map not injective')
                yield tuple(mapping)

def product(stars, first, second, seconds=10):
    c = domain.carrier(stars, first, second)
    start = time.monotonic()
    counts = dict(partial_maps=0, full_maps_tested=0)
    rejected = {}
    positives = []
    transcript = []
    all_partials = []
    for partial in partials(c):
        all_partials.append(list(partial))
        counts['partial_maps'] += 1
        if counts['partial_maps'] % 128 == 0 and time.monotonic() - start > seconds:
            raise RuntimeError('INCOMPLETE per-product guard')
        reason = domain.rejection(c, partial)
        if reason:
            rejected[reason] = rejected.get(reason, 0) + 6
            transcript.append([list(partial), reason])
            continue
        source_rest = [p for p in range(17) if partial[p] < 0]
        y = c['first_mark'][2]
        target_rest = sorted(set(range(18)) - {y} - set(partial))
        domain.require(len(source_rest) == len(target_rest) == 3, 'three residual points required')
        full_records = []
        for images in itertools.permutations(target_rest):
            counts['full_maps_tested'] += 1
            mapping = list(partial)
            for p, image in zip(source_rest, images):
                mapping[p] = image
            reason = domain.rejection(c, mapping)
            if reason:
                rejected[reason] = rejected.get(reason, 0) + 1
                full_records.append([list(images), reason])
            else:
                words = domain.core(c, mapping, stars)
                record = dict(point_map=mapping, word_masks=words, triangle_points=domain.triangle_points(c, mapping))
                positives.append(record)
                full_records.append([list(images), 'positive', domain.digest(words)])
        transcript.append([list(partial), full_records])
    domain.require(counts['partial_maps'] == 2592, 'gap in complete tail matches')
    domain.require(sum(rejected.values()) + len(positives) == 15552, 'gap in full-map accounting')
    return dict(status='COMPLETE_MARKED_PRODUCT', first=[first[0], list(first[1])],
                second=[second[0], list(second[1])], counts=counts, rejected_full_maps=rejected,
                positives=positives, transcript_sha256=domain.digest(transcript),
                partial_maps_sha256=domain.digest(sorted(all_partials)),
                positives_sha256=domain.digest(sorted(positives, key=lambda row: row['point_map'])),
                seconds=time.monotonic()-start)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixtures', required=True)
    parser.add_argument('--work', required=True)
    parser.add_argument('--first', type=int, default=0)
    parser.add_argument('--finish', type=int)
    args = parser.parse_args()
    stars = domain.load(args.fixtures)
    ds = domain.domains(stars)
    products = list(itertools.product(ds['first'], ds['second']))
    work = Path(args.work); work.mkdir(parents=True, exist_ok=True)
    finish = len(products) if args.finish is None else args.finish
    domain.require(0 <= args.first <= finish <= len(products), 'bad product interval')
    (work/'domains.json').write_text(json.dumps(ds, sort_keys=True, indent=2)+'\n')
    for index in range(args.first, finish):
        first, second = products[index]
        record = product(stars, first, second)
        record['product_index'] = index
        (work/f'product-{index:03d}.json').write_text(json.dumps(record, sort_keys=True, indent=2)+'\n')
        print(json.dumps(dict(index=index, positives=len(record['positives']), seconds=record['seconds'])), flush=True)

if __name__ == '__main__':
    main()
