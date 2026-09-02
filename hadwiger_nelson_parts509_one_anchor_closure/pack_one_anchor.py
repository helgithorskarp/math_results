#!/usr/bin/env python3
"""Compact certificate of the one-anchor closure (verification needs neighbour lists and internal edges only).

Configurations are grouped by their one-anchor point x:
  group = {'v': anchor vertex, 'xn': over-inclusive vertex-neighbour list of x, 'I': [[r1, r2, r3, e], ...],
           'II': [[ry, rb, rd, e], ...]}   (x is a common unit neighbour of v and of the referenced points; its
           binary64 coordinates are kept in the scratch enumeration output only)
  r = point reference: 'q3:I' (index into completion_points.json of the swap closure; neighbours from that list),
      'k2:I' (index into q2k_points of triple_certificate.json), 'n:I:J:S' (non-K intersection point of vertices
      I, J, sign S; neighbours {I, J}), or 'x:X:Y:N1,N2,..' (type II second one-anchor point y: coordinates and
      its over-inclusive vertex neighbours).
  e = bitmask of the internal unit edges among the three points other than x, bits (1,2), (1,3), (2,3);
      x is adjacent to all three points.  Configuration index ci = position in the flattened order
      (groups in file order, within a group first the 'I' then the 'II' list).
Declared pairs: 'ci:u' -> status; fresh rows: proper 4-colourings of G − u.
usage: pack_one_anchor.py CONFIGS_F.json COVER.json OUT.json.gz [--universe DIR]
       (DIR = output directory of build_universe.py, whose universe_meta.json maps universe indices to non-K labels;
        default: env ONE_ANCHOR_UNIVERSE or ./universe.  The label list is checked against q2k_extra.json of the
        triple-closure directory, the committed source of the non-K labels, before use.)
"""
import json, sys, gzip, hashlib, argparse, os
from pathlib import Path
from paths import Q2K_EXTRA
NQ3, NQ2K = 1158, 2705
ap = argparse.ArgumentParser(); ap.add_argument('configs'); ap.add_argument('cover'); ap.add_argument('out')
ap.add_argument('--universe', default=os.environ.get('ONE_ANCHOR_UNIVERSE', str(Path(__file__).resolve().parent / 'universe')))
args = ap.parse_args()
meta = json.loads((Path(args.universe) / 'universe_meta.json').read_text())
labels = meta['nonk_labels']
committed_labels = json.loads(Q2K_EXTRA.read_text())['nonk_labels']
assert sorted(map(tuple, labels)) == sorted(map(tuple, committed_labels)) and labels == sorted(labels), 'universe labels differ from the committed non-K label list'
sys.argv = [sys.argv[0], args.configs, args.cover, args.out]
confs = json.loads(Path(sys.argv[1]).read_text()); cov = json.loads(Path(sys.argv[2]).read_text())
assert cov['n_configs'] == len(confs)


def ref(p):
    if 'q' in p:
        q = p['q']
        if q < NQ3:
            return f'q3:{q}'
        if q < NQ3 + NQ2K:
            return f'k2:{q - NQ3}'
        i, j, s = labels[q - NQ3 - NQ2K]
        assert p['nbrs'] == [i, j]
        return f'n:{i}:{j}:{s}'
    return 'x:%.17g:%.17g:%s' % (p['x'][0], p['x'][1], ','.join(map(str, p['nbrs'])))


def ecode(edges):
    e = set(tuple(sorted(x)) for x in edges)
    assert {(0, 1), (0, 2), (0, 3)} <= e
    rest = e - {(0, 1), (0, 2), (0, 3)}
    code = 0
    for b, pr in enumerate([(1, 2), (1, 3), (2, 3)]):
        if pr in rest:
            code |= 1 << b; rest.discard(pr)
    assert not rest
    return code


groups = []; index = {}; members = {}
for ci, c in enumerate(confs):
    v = int(c['id'].split(':')[1]); x = c['points'][0]
    key = (v, round(x['x'][0], 9), round(x['x'][1], 9), tuple(x['nbrs']))
    if key not in index:
        index[key] = len(groups); groups.append({'v': v, 'xn': x['nbrs'], 'I': [], 'II': []})
    groups[index[key]][c['type']].append([ref(p) for p in c['points'][1:]] + [ecode(c['edges'])])
    members.setdefault(index[key], []).append((c['type'], ci))
compact_ci = {}; counter = 0
for gi in range(len(groups)):
    for t in ('I', 'II'):
        for tt, ci in members[gi]:
            if tt == t:
                compact_ci[ci] = counter; counter += 1
assert counter == len(confs)
declared = {f"{compact_ci[int(k.split(':')[0])]}:{k.split(':')[1]}": v for k, v in cov['status'].items()}
cert = {'description': 'One-anchor family of the delete-5-add-4 closure of the Parts-509 graph: configurations grouped by one-anchor point (compact references), declared pairs Û(A), fresh witness colourings',
        'n_configs': len(confs), 'n_groups': len(groups), 'groups': groups, 'declared': declared, 'fresh_rows': cov['new_rows'],
        'histogram': cov['histogram'], 'candidates': cov['candidates'], 'direct_tests': cov['direct'],
        'row_convention': 'fresh rows are proper 4-colourings of G − u as digit strings over vertex indices 0..508 with - at u',
        'configs_f_sha256': hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()}
raw = json.dumps(cert, separators=(',', ':')).encode()
with gzip.open(sys.argv[3], 'wb', compresslevel=9) as f:
    f.write(raw)
print(f'{len(confs)} configurations in {len(groups)} groups; json {len(raw)/1e6:.1f} MB, gz {Path(sys.argv[3]).stat().st_size/1e6:.2f} MB; sha256(gz) {hashlib.sha256(Path(sys.argv[3]).read_bytes()).hexdigest()[:16]}')
