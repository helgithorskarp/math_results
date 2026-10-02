"""Post-seal comparison of every author AP entry using the reviewer oracle.

No author executable is imported. The native transcript convention is explicit.
"""
import argparse
import csv
import hashlib
import itertools
import json
from collections import Counter
from math import gcd
from pathlib import Path
from independent import audit, check_pack, crt, orbits, relabel, require


def read_author(path):
    with path.open(newline='') as f:
        table = list(csv.reader(f))
    header = ['index', 't', 'd2', 'd3'] + [v for j in range(1, 10) for v in ('a' + str(j), 'step' + str(j))]
    require(table[0] == header and len(table) == 70, 'author full CSV census')
    representatives = [o[0] for o in orbits()]
    groups = {}
    for index, row in enumerate(table[1:]):
        require(len(row) == 22, 'author row length')
        values = list(map(int, row))
        require(all(str(n) == text for n, text in zip(values, row)), 'author canonical integers')
        require(values[0] == index and tuple(values[1:4]) == representatives[index], 'author entire state order')
        pairs = tuple(tuple(values[4 + 2 * j:6 + 2 * j]) for j in range(9))
        require(all(1 <= d <= 309 for _, d in pairs), 'author short-step domain')
        groups[representatives[index]] = pairs
    return groups


def literal_values(ap):
    return [ap['points'], ap['columns'], [ap['color']] * 7, ap['integer_lift']]


def compare(author):
    known = json.loads((Path(__file__).resolve().parent / 'AUTHOR_COMPARISON.json').read_text())
    for name, wanted in known['target_files'].items():
        require(hashlib.sha256((author / name).read_bytes()).hexdigest() == wanted, 'pinned target input ' + name)
    groups = read_author(author / 'certificate.csv')
    own_summary, own_record = audit(groups)
    expected = json.loads((author / 'expected.json').read_text())
    representatives = hashlib.sha256()
    transported = hashlib.sha256()
    records = {'representatives': [], 'transported': []}
    rep_hist, transport_hist, exchanges = Counter(), Counter(), Counter()
    encode = lambda x: (json.dumps(x, separators=(',', ':')) + '\n').encode('ascii')
    components = orbits()
    for index, component in enumerate(components):
        rep = component[0]
        for j, ((a, d), ap) in enumerate(zip(groups[rep], check_pack(rep, groups[rep]))):
            row = [index, j, rep, a, d, literal_values(ap)]
            representatives.update(encode(row))
            records['representatives'].append(row)
            rep_hist[gcd(d, 618)] += 1
        for target in component:
            # relabel's forward normalization gives coordinates in SOURCE.
            # Its inverse sends representative coordinates to TARGET, which
            # matches the native transcript's chosen ordered root-pair map.
            maps = [relabel(rep, order) for order in itertools.permutations(range(3))]
            _, slope, offset, exchange = next(m for m in maps if m[0] == target)
            alpha = pow(slope, -1, 103)
            beta = -alpha * offset % 103
            aa, bb = crt(alpha, 1), crt(beta, 0)
            pairs = []
            for a, d in groups[rep]:
                a, d = (aa * a + bb) % 618, aa * d % 618
                if d > 309:
                    a, d = (a + 6 * d) % 618, 618 - d
                pairs.append((a, d))
            literal = check_pack(target, pairs)
            for j, ((a, d), ap) in enumerate(zip(pairs, literal)):
                rep_color = check_pack(rep, groups[rep])[j]['color']
                require(ap['color'] == rep_color ^ exchange, 'author chosen-map exchange')
                row = [rep, target, exchange, j, a, d, literal_values(ap)]
                transported.update(encode(row))
                records['transported'].append(row)
                transport_hist[gcd(d, 618)] += 1
            exchanges[exchange] += 1
    require(representatives.hexdigest() == expected['representative_literal_transcript_sha256'], 'every representative transcript entry')
    require(transported.hexdigest() == expected['transported_literal_transcript_sha256'], 'every transported transcript entry')
    require({str(k): v for k, v in rep_hist.items()} == expected['representative_step_gcd_histogram'], 'representative steps')
    require({str(k): v for k, v in transport_hist.items()} == expected['transported_step_gcd_histogram'], 'transported steps')
    require({str(k): v for k, v in exchanges.items()} == expected['transport_color_flip_state_histogram'], 'all exchanges')
    cuts = []
    for holes in range(4):
        for roots in range(holes + 1):
            e = holes - roots
            m = 100 - e
            values = []
            for distance in range(m + 1):
                hit = distance + e >= 9 and m - distance + e >= 9
                require(hit == (9 - e <= distance <= 91), 'masked distance')
                require(hit == (abs(m - 2 * distance) <= 82 + e), 'masked correlation')
                values.append(int(hit))
            cuts.append({'holes': holes, 'root_holes': roots, 'valid_distance_flags': values})
    summary = {'status': 'EVERY_AUTHOR_AP_ENTRY_INDEPENDENTLY_MATCHED',
               'target': 9745, 'author_certificate_sha256': hashlib.sha256((author / 'certificate.csv').read_bytes()).hexdigest(),
               'representative_transcript_sha256': representatives.hexdigest(),
               'transported_transcript_sha256': transported.hexdigest(),
               'representative_entries': len(records['representatives']),
               'transported_entries': len(records['transported']),
               'literal_point_entries': 7 * (len(records['representatives']) + len(records['transported'])),
               'mask_classes': len(cuts), 'integer_distance_values': sum(len(c['valid_distance_flags']) for c in cuts),
               'independent_author_pack_summary': own_summary}
    records.update({'summary': summary, 'cuts': cuts, 'own_coordinate_transports': own_record})
    require(json.loads(json.dumps(summary)) == known['summary'], 'entire comparison summary')
    raw = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    require(hashlib.sha256(raw).hexdigest() == known['entire_record_sha256'], 'entire comparison record')
    return summary, records


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', type=Path, required=True)
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    summary, records = compare(args.author)
    if args.record:
        args.record.write_text(json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps(summary, sort_keys=True))
