"""Literal candidate reconstruction and full pivot replay of one pilot interval."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import time

from bindings import Native, swap_points, v, verifier


def input_case(case, orientation):
    v.check(type(case) is int and 0 <= case < 46, 'literal case domain')
    v.check(type(orientation) is int and orientation in (0, 1), 'literal orientation domain')
    star, rows, cols, fixed = copy.deepcopy(verifier.inputs()[case])
    star['orientation'] = orientation
    if orientation:
        fixed = [swap_points(w) for w in fixed]
        rows, cols = cols, rows
        star['row'], star['col'] = star['col'], star['row']
        star['cells'] = [(c, r) for r, c in star['cells']]
        star['fixed'] = sorted(v.bits(w) for w in fixed)
    return star, rows, cols, fixed


def joint(words):
    v.packing(words, 44)
    v.check([sum(c in w for w in words) for c in (17, 15, 16)] == [19, 19, 20],
            'literal mixed center degrees')
    v.check([sum({a, b} <= w for w in words) for a, b in ((17, 15), (17, 16), (15, 16))] == [5, 5, 4],
            'literal mixed pair multiplicities')
    v.check(not any({15, 16, 17} <= w for w in words), 'literal covered center triple')


def replay(case, orientation, start, size, work, executable):
    begun = time.monotonic()
    star, rows, cols, fixed = input_case(case, orientation)
    ts, covers, nodes = verifier.covers(fixed)
    v.check(type(start) is int and 0 <= start < len(covers), 'literal interval start')
    v.check(type(size) is int and 0 < size <= 1000, 'bounded literal interval size')
    finish = min(start + size, len(covers)); tag = f'{case}-{orientation}-{start}-{finish}'
    yw, ya = v.base(rows, fixed, 15); zw, za = v.base(cols, fixed, 16)
    header = {'star': star, 'triples': [v.bits(t) for t in ts], 'covers': covers,
              'y_words': [v.bits(w) for w in yw], 'y_adjacent': [v.bits(a) for a in ya],
              'z_words': [v.bits(w) for w in zw], 'z_adjacent': [v.bits(a) for a in za]}
    primary_header_path = work / f'header-{case}-{orientation}.json'
    primary_header = json.loads(primary_header_path.read_text())
    v.compare(header, {k: a for k, a in primary_header.items() if k != 'cover_nodes'},
              'literal oriented full universe/header mismatch')
    primary = json.loads((work / f'primary-{tag}.json').read_text())
    v.check(primary['status'] == 'COMPLETE_PRIMARY_INTERVAL_ONLY' and primary['start'] == start
            and primary['finish'] == finish and primary['case'] == case and
            primary['orientation'] == orientation, 'primary interval completion binding')
    yt = [{i for i, w in enumerate(yw) if len(w & (t | {15, 16})) <= 2} for t in ts]
    zt = [{i for i, w in enumerate(zw) if len(w & (t | {15, 16})) <= 2} for t in ts]
    counts = Counter(); profiles = Counter(); joints = []; native_nodes = 0; max_nodes = 0
    carrier = work / f'carrier-{tag}.jsonl'
    with Native(executable, [ya, za]) as engine, carrier.open() as stream:
        for ci in range(start, finish):
            if time.monotonic() - begun > 60:
                raise RuntimeError('INCOMPLETE literal pilot guard; no exclusion')
            cover = covers[ci]; extra = [ts[i] | {15, 16} for i in cover]
            ys = sorted(set.intersection(*(yt[i] for i in cover)))
            yc, count = engine.query(0, ys, target=10)
            native_nodes += count; max_nodes = max(max_nodes, count)
            counts.update(covers=1, y_ten=len(yc))
            record = {'cover': ci, 'y_candidates': ys, 'y_ten': yc, 'z_cases': []}
            for q in yc:
                private_y = [yw[i] for i in q]
                prefix = fixed + extra + private_y
                v.packing(prefix, 33)
                m = v.stats(prefix, 15)['m']; profiles[m] += 1
                zs = sorted(i for i in set.intersection(*(zt[i] for i in cover))
                            if all(len(zw[i] & a) <= 2 for a in private_y))
                zc, count = engine.query(1, zs, target=11)
                native_nodes += count; max_nodes = max(max_nodes, count)
                counts.update(z_eleven=len(zc))
                record['z_cases'].append({'y': q, 'y_m': m, 'z_candidates': zs, 'z_eleven': zc})
                for r in zc:
                    words = prefix + [zw[i] for i in r]
                    joint(words)
                    blocks = sorted(v.bits(w) for w in words)
                    joints.append({'case': case, 'orientation': orientation, 'cover': ci,
                                   'y': q, 'z': r, 'y_m': m, 'blocks': blocks,
                                   'core_sha256': v.sha(blocks)})
            line = stream.readline(); v.check(bool(line), 'truncated primary interval')
            v.compare(record, json.loads(line), 'entrywise mixed candidate/clique-list mismatch')
        v.check(not stream.readline(), 'extra primary interval record')
    v.compare(joints, json.loads((work / f'joints-{tag}.json').read_text()), 'literal complete mixed cores')
    for key in ('covers', 'y_ten', 'z_eleven'):
        v.check(counts[key] == primary['counts'].get(key, 0), 'literal interval count mismatch')
    v.compare(dict(profiles), primary['y_m_census'], 'literal nineteen-star profile counts')
    v.check(len(joints) == primary['cores'], 'literal core count mismatch')
    for label, path in [('header_sha256', primary_header_path), ('carrier_sha256', carrier),
                        ('joints_sha256', work / f'joints-{tag}.json')]:
        v.check(hashlib.sha256(path.read_bytes()).hexdigest() == primary[label], 'pilot byte binding')
    result = {'status': 'COMPLETE_ENTRYWISE_INTERVAL_ONLY', 'case': case, 'orientation': orientation,
              'start': start, 'finish': finish, 'total_covers': len(covers), 'counts': dict(counts),
              'cores': len(joints), 'native_nodes': native_nodes, 'max_query_nodes': max_nodes,
              'literal_cover_nodes': nodes, 'seconds': time.monotonic() - begun,
              'header_sha256': primary['header_sha256'], 'carrier_sha256': primary['carrier_sha256'],
              'joints_sha256': primary['joints_sha256']}
    (work / f'verified-{tag}.json').write_bytes(v.encode(result))
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, required=True)
    parser.add_argument('--orientation', type=int, choices=(0, 1), required=True)
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--size', type=int, default=1000)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--executable', type=Path, required=True)
    args = parser.parse_args()
    replay(args.case, args.orientation, args.start, args.size, args.work, args.executable)
