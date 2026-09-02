#!/usr/bin/env python3
"""Canonical, order-independent digest of a one-anchor configuration list.

A configuration is keyed by (type, sorted Q-point references, sorted one-anchor vertex-neighbour lists, internal
edge pattern); the key does not depend on the enumeration order, on the multiprocessing completion order, or on
which of the two one-anchor points of a symmetric type II set is called x.  The digest is the SHA-256 of the
sorted key list (one key per line) and the multiset is reported as counts, so a regenerated enumeration
(configs_f.json, produced by enumerate_one_anchor.py + filter_configs.py, references = universe indices) and the
committed certificate (certificate.json.gz, references = compact labels) can be compared exactly.
usage: config_digest.py FILE [--universe DIR]     (FILE = configs*.json or certificate.json.gz)
       config_digest.py --compare A B [--universe DIR]
"""
import argparse, gzip, hashlib, json, os, sys
from collections import Counter
from pathlib import Path
NQ3, NQ2K = 1158, 2705
PAIRS = [(1, 2), (1, 3), (2, 3)]


def ref_from_index(q, labels):
    if q < NQ3:
        return f'q3:{q}'
    if q < NQ3 + NQ2K:
        return f'k2:{q - NQ3}'
    i, j, s = labels[q - NQ3 - NQ2K]
    return f'n:{i}:{j}:{s}'


def keys_from_configs(confs, labels):
    out = []
    for c in confs:
        qrefs, anchors = [], []
        for p in c['points']:
            if 'q' in p:
                qrefs.append(ref_from_index(p['q'], labels))
            else:
                anchors.append(','.join(map(str, sorted(p['nbrs']))))
        # edge pattern among the Q points / second one-anchor point, expressed on sorted references
        names = []
        for p in c['points']:
            names.append(ref_from_index(p['q'], labels) if 'q' in p else 'x' + ','.join(map(str, sorted(p['nbrs']))))
        edges = sorted(tuple(sorted((names[a], names[b]))) for a, b in c['edges'])
        out.append(f"{c['type']}|{';'.join(sorted(qrefs))}|{';'.join(sorted(anchors))}|{';'.join('-'.join(e) for e in edges)}")
    return out


def keys_from_certificate(cert):
    out = []
    for g in cert['groups']:
        xn = ','.join(map(str, sorted(g['xn'])))
        for t in ('I', 'II'):
            for rec in g[t]:
                refs = rec[:3]; e = rec[3]
                names = ['x' + xn]
                qrefs, anchors = [], [xn]
                for r in refs:
                    if r.startswith('x:'):
                        yn = ','.join(map(str, sorted(int(z) for z in r.split(':')[3].split(','))))
                        anchors.append(yn); names.append('x' + yn)
                    else:
                        qrefs.append(r); names.append(r)
                edges = [(names[0], names[k]) for k in (1, 2, 3)]
                for b, (i, j) in enumerate(PAIRS):
                    if e >> b & 1:
                        edges.append((names[i], names[j]))
                edges = sorted(tuple(sorted(ed)) for ed in edges)
                out.append(f"{t}|{';'.join(sorted(qrefs))}|{';'.join(sorted(anchors))}|{';'.join('-'.join(ed) for ed in edges)}")
    return out


def load_keys(path, labels):
    path = Path(path)
    if path.name.endswith('.gz'):
        cert = json.loads(gzip.open(path, 'rt').read())
        return keys_from_certificate(cert)
    confs = json.loads(path.read_text())
    return keys_from_configs(confs, labels)


def digest(keys):
    return hashlib.sha256('\n'.join(sorted(keys)).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+'); ap.add_argument('--compare', action='store_true')
    ap.add_argument('--universe', default=os.environ.get('ONE_ANCHOR_UNIVERSE', str(Path(__file__).resolve().parent / 'universe')))
    args = ap.parse_args()
    labels = None
    if any(not f.endswith('.gz') for f in args.files):
        labels = [tuple(l) for l in json.loads((Path(args.universe) / 'universe_meta.json').read_text())['nonk_labels']]
    allkeys = []
    for f in args.files:
        ks = load_keys(f, labels); allkeys.append(ks)
        cnt = Counter(ks)
        print(f'{f}: {len(ks)} configurations, {len(cnt)} distinct keys, digest {digest(ks)}')
    if args.compare or len(args.files) == 2:
        a, b = Counter(allkeys[0]), Counter(allkeys[1])
        only_a = a - b; only_b = b - a
        print(f'multiset difference: {sum(only_a.values())} only in first, {sum(only_b.values())} only in second -> {"IDENTICAL" if not only_a and not only_b else "DIFFERENT"}')
        for k in list(only_a)[:5]: print('  first only:', k)
        for k in list(only_b)[:5]: print('  second only:', k)


if __name__ == '__main__':
    main()
