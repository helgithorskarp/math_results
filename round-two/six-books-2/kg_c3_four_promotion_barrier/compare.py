"""Compare every completed native labeled case with the complete pair census.

No totals or saved pass flags substitute for entry-level comparisons.  The
native search does not read the quotient, compatibility graph, or this checker.
This script transports each complete native terminal list to its representative.
"""
from array import array
from collections import Counter, defaultdict
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def integer(x, low=0, high=(1 << 63)-1):
    m.need(type(x) is int and low <= x <= high, 'integer domain')
    return x


def subset(xs, size=None):
    m.need(type(xs) is list and (size is None or len(xs) == size), 'subset length')
    ys = tuple(integer(x, 0, 34) for x in xs)
    m.need(tuple(sorted(set(ys))) == ys, 'ordered unique subset')
    return ys


def main(args):
    started = time.monotonic()
    for name in ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json'):
        m.need(not (Path('/scratch/research-team-sol61-six-20260929/state')/name).exists(),
               'pause/handover barrier')
    producer, native = args.producer, args.native
    metadata = json.loads((producer/'cases.json').read_text())
    manifest_hash = digest(producer/'cases.txt')
    m.need(metadata['status'] == 'COMPLETE_EXPLICIT_CASE_QUOTIENT' and
           metadata['manifest_sha256'] == manifest_hash, 'manifest identity')
    geometry = m.geometry()
    effective = sorted(set(tuple(tuple(x) for x in entry) for entry in m.centralizer(geometry)))
    m.need(len(effective) == 6, 'checked effective action')
    joins = list(combinations(range(7), 3))
    promotions = list(combinations(range(35), 4))
    join_rank = {J:i for i,J in enumerate(joins)}
    promotion_rank = {P:i for i,P in enumerate(promotions)}
    m.need(len(joins) == 35 and len(promotions) == 52360, 'complete product domain')
    join_images = [tuple(join_rank[tuple(sorted(v[j] for j in J))]
                         for v,r,b in effective) for J in joins]
    promotion_images = [array('I', (promotion_rank[tuple(sorted(b[p] for p in P))]
                                   for P in promotions)) for v,r,b in effective]
    by_labeled = {}
    weights, join_indices, promotion_indices = array('B'), array('B'), array('I')
    with (producer/'cases.txt').open() as stream:
        for index, line in enumerate(stream):
            fields = tuple(map(int, line.split()))
            m.need(len(fields) == 9 and fields[0] == index, 'manifest row/index')
            ji, pi = join_rank[fields[1:4]], promotion_rank[fields[4:8]]
            label = ji*52360+pi
            images = {join_images[ji][k]*52360+promotion_images[k][pi] for k in range(6)}
            m.need(min(images) == label and fields[8] == len(images), 'explicit canonical orbit/weight')
            m.need(label not in by_labeled, 'duplicate representative')
            by_labeled[label] = index
            weights.append(fields[8]);join_indices.append(ji);promotion_indices.append(pi)
    total = len(weights)
    m.need(total == metadata['representatives'] == 305874 and sum(weights) == 1832600,
           'complete representative inventory')
    bases, pools = bytearray(total), array('Q', [0])*total
    terminal_counts = {q:array('I', [0])*total for q in (8,9)}
    degree_counts = {q:array('I', [0])*total for q in (8,9)}
    two_color_counts = {q:array('I', [0])*total for q in (8,9)}
    inventory = defaultdict(list)
    producer_inputs = []
    next_index = 0
    for path in sorted(producer.glob('producer-*.jsonl')):
        summary = json.loads(path.with_suffix('.summary.json').read_text())
        m.need(digest(path) == summary['output_sha256'], 'producer bytes')
        phase_first = next_index
        footer = None
        with path.open() as stream:
            for line in stream:
                item = json.loads(line)
                if item.get('segment') is True:
                    m.need(footer is None, 'duplicate footer')
                    footer = item
                    continue
                m.need(footer is None and item['index'] == next_index and next_index < total,
                       'producer consecutive case')
                integer(item['index'], 0, total-1)
                m.need(set(item) == {'index','weight','base_blue_valid','pool','compatibility','targets'},
                       'producer schema')
                m.need(type(item['base_blue_valid']) is bool and item['weight'] == weights[next_index],
                       'producer base/weight')
                pool = subset(item['pool'])
                co = item['compatibility']
                m.need(type(co) is list and len(co) == len(pool), 'pair table size')
                for i,x in enumerate(co):
                    integer(x, 0, (1 << len(pool))-1)
                    m.need(not x >> i & 1, 'pair table self edge')
                m.need(set(item['targets']) == {'8','9'}, 'producer target schema')
                bases[next_index] = item['base_blue_valid']
                pools[next_index] = sum(1 << d for d in pool)
                m.need(item['base_blue_valid'] or not pool, 'invalid base has empty pool')
                for q in (8,9):
                    target = item['targets'][str(q)]
                    terminal_counts[q][next_index] = integer(target['blue_valid'], 0, 1 << 31)
                    degree_counts[q][next_index] = integer(target['degree_valid'], 0, 1 << 31)
                    two_color_counts[q][next_index] = integer(target['two_color_valid'], 0, 1 << 31)
                next_index += 1
        m.need(footer is not None and footer['first'] == phase_first and
               footer['next'] == next_index and footer['total'] == total and
               footer['complete'] is (next_index == total), 'producer actual phase footer')
        positive = producer/f'positive-{phase_first:06d}.jsonl'
        m.need(digest(positive) == summary['positive_sha256'], 'positive inventory bytes')
        with positive.open() as stream:
            for line in stream:
                item = json.loads(line)
                index = integer(item['index'], phase_first, next_index-1)
                q = len(item['D'])
                m.need(q in (8,9), 'positive target')
                D = subset(item['D'], q)
                m.need(tuple(item['J']) == joins[join_indices[index]] and
                       tuple(item['P']) == promotions[promotion_indices[index]] and
                       item['weight'] == weights[index] and
                       all(pools[index] >> d & 1 for d in D), 'positive case/domain')
                m.need(type(item['degrees']) is bool, 'degree predicate Boolean')
                inventory[index,q].append((D,integer(item['red_bad'],0,231),item['degrees']))
        producer_inputs.append(dict(file=path.name,sha256=summary['output_sha256'],
                                    positive_sha256=summary['positive_sha256']))
    m.need(next_index == total, 'producer census incomplete')
    expected_counts = Counter()
    expected_hist = {q:Counter() for q in (8,9)}
    for index in range(total):
        for q in (8,9):
            entries = inventory.get((index,q), [])
            entries.sort()
            m.need(len({x[0] for x in entries}) == len(entries), 'duplicate positive deletion')
            m.need(len(entries) == terminal_counts[q][index] and
                   sum(x[2] for x in entries) == degree_counts[q][index] and
                   sum(x[1] == 0 for x in entries) == two_color_counts[q][index],
                   'actual positive lists vs every producer count')
            expected_counts[q] += weights[index]*len(entries)
            for D,bad,degrees in entries:
                expected_hist[q][bad] += weights[index]
    observed = bytearray(total)
    counts = Counter()
    hist = {q:Counter() for q in (8,9)}
    native_inputs = []
    semantic = hashlib.sha256()
    next_index = 0
    for path in sorted(native.glob('native-*.jsonl')):
        summary = json.loads(path.with_suffix('.summary.json').read_text())
        m.need(digest(path) == summary['output_sha256'], 'native phase bytes')
        phase_first = next_index
        footer = None
        with path.open() as stream:
            for line in stream:
                item = json.loads(line)
                if item.get('segment') is True:
                    m.need(footer is None, 'duplicate native footer')
                    footer = item
                    continue
                m.need(footer is None and item['index'] == next_index and next_index < 1832600,
                       'native actual consecutive case')
                integer(item['index'], 0, 1832599)
                m.need(set(item) == {'index','joins','promotions','base_blue_valid','pool',
                                     'attempted','good','targets'}, 'native schema')
                for name in ('attempted','good'):
                    m.need(type(item[name]) is list and len(item[name]) == 10, 'native depth vector')
                    for x in item[name]:
                        integer(x)
                m.need(all(a >= b for a,b in zip(item['attempted'],item['good'])), 'native depth counts')
                m.need(set(item['targets']) == {'8','9'}, 'native target schema')
                ji,pi = divmod(next_index,52360)
                m.need(tuple(item['joins']) == joins[ji] and tuple(item['promotions']) == promotions[pi],
                       'native literal product coordinate')
                labels = [join_images[ji][k]*52360+promotion_images[k][pi] for k in range(6)]
                label = min(labels)
                k = labels.index(label)
                index = by_labeled[label]
                observed[index] += 1
                m.need(observed[index] <= weights[index], 'observed orbit excess')
                pool = subset(item['pool'])
                transported_pool = sum(1 << effective[k][1][d] for d in pool)
                m.need(type(item['base_blue_valid']) is bool and
                       item['base_blue_valid'] == bool(bases[index]) and
                       transported_pool == pools[index], 'every native base/pool transport')
                for q in (8,9):
                    m.need(type(item['targets'][str(q)]) is list and
                           len(item['targets'][str(q)]) == item['good'][q], 'native terminal counter')
                    entries = []
                    for target in item['targets'][str(q)]:
                        m.need(set(target) == {'D','red_bad','degrees'}, 'native terminal schema')
                        D = subset(target['D'], q)
                        m.need(all(d in pool for d in D) and type(target['degrees']) is bool,
                               'native terminal domain')
                        image = tuple(sorted(effective[k][1][d] for d in D))
                        bad = integer(target['red_bad'],0,231)
                        entries.append((image,bad,target['degrees']))
                        counts[q] += 1;hist[q][bad] += 1
                    entries.sort()
                    m.need(entries == inventory.get((index,q), []), 'COMPLETE terminal lists disagree')
                semantic.update(f'{next_index}:{index}:{transported_pool}\n'.encode())
                next_index += 1
        m.need(footer is not None and footer['first'] == phase_first and
               footer['next'] == next_index and footer['total'] == 1832600 and
               footer['complete'] is (next_index == 1832600), 'native actual phase footer')
        native_inputs.append(dict(file=path.name,sha256=summary['output_sha256'],
                                  first=phase_first,next=next_index))
    complete = next_index == 1832600
    if complete:
        m.need(observed == weights, 'FULL literal case orbit multiplicities')
        m.need(counts == expected_counts and hist == expected_hist, 'full transported histograms')
    result = dict(status='COMPLETE_ENTRYWISE_TWO_ALGORITHM_AGREEMENT' if complete
                      else 'ENTRYWISE_AGREEMENT_ON_EXACT_NATIVE_PREFIX_ONLY',
        first=0,next=next_index,total=1832600,producer_representatives=total,
        terminal_counts=dict(counts),terminal_red_hist={q:dict(sorted(v.items())) for q,v in hist.items()},
        expected_complete_counts=dict(expected_counts),
        expected_complete_red_hist={q:dict(sorted(v.items())) for q,v in expected_hist.items()},
        observed_orbit_counts=dict(Counter(observed)),manifest_sha256=manifest_hash,
        native_inputs=native_inputs,producer_inputs=producer_inputs,
        checked_bases_and_full_pools=next_index,checked_complete_terminal_lists=2*next_index,
        transport_sha256=semantic.hexdigest(),seconds=time.monotonic()-started,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        sources={p.name:digest(p) for p in
                 (Path(__file__),HERE/'model.py')},
        scope='Same-author distinct algorithms; ordinary completeness bridge unformalized; partial coverage is not a global exclusion.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('native_inputs','producer_inputs')},indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,required=True)
    ap.add_argument('--producer',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    main(ap.parse_args())
