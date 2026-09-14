#!/usr/bin/env python3
"""Exact positive-parent fusion preflight, using only the standard library."""
import argparse
import base64
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 288
UNIT = (SCALE*SCALE,) + (0,)*7

def require(ok, detail):
    if not ok:
        raise ValueError(detail)

def digest(data):
    return sha256(data).hexdigest()

def read_json(relative):
    return json.loads((REPO/relative).read_text())

def point(axes):
    out = []
    for axis in axes:
        row = [SCALE*Fraction(x) for x in axis]
        require(len(row) == 8 and all(x.denominator == 1 for x in row), 'coordinate scale')
        out.append(tuple(map(int, row)))
    require(len(out) == 2, 'coordinate axes')
    return tuple(out)

def norm(p, q):
    result = [0]*8
    for axis in range(2):
        d = [a-b for a, b in zip(p[axis], q[axis], strict=True)]
        for i in range(8):
            result[0] += RAD[i]*d[i]*d[i]
            for j in range(i+1, 8):
                result[i ^ j] += 2*RAD[i & j]*d[i]*d[j]
    return tuple(result)

def proper(labels, edges, word, palette=range(4)):
    require(len(word) == len(labels), 'word length')
    colours = dict(zip(labels, map(int, word), strict=True))
    require(set(colours.values()) <= set(palette), 'word palette')
    checks = 0
    for a, b in edges:
        if a in colours and b in colours:
            require(colours[a] != colours[b], ('monochromatic edge', a, b))
            checks += 1
    return colours, checks

def unpack_g14(record):
    payload = record['deletion_colorings']
    raw = base64.b64decode(payload['base64'], validate=True)
    require(digest(raw) == payload['sha256'], 'G14 word hash')
    require(payload['rows'] == 510 and payload['values_per_row'] == 509, 'G14 word dimensions')
    require(len(raw) == 510*128, 'G14 payload size')
    rows = []
    for k in range(510):
        row = raw[128*k:128*(k+1)]
        require(row[-1] >> 2 == 0, 'G14 padding')
        rows.append([(row[i//4] >> (2*(i % 4))) & 3 for i in range(509)])
    return rows

def cnf(labels, edges):
    pos = {v: i for i, v in enumerate(labels)}
    clauses = [[4*i+c+1 for c in range(4)] for i in range(len(labels))]
    clauses.extend([-(4*pos[a]+c+1), -(4*pos[b]+c+1)] for a, b in edges for c in range(4))
    triangle = [0, 149, 152]
    require(all(e in edges for e in combinations(triangle, 2)), 'pin triangle')
    clauses.extend([[4*pos[v]+c+1] for c, v in enumerate(triangle)])
    return (f'p cnf {4*len(labels)} {len(clauses)}\n' +
            ''.join(' '.join(map(str, clause))+' 0\n' for clause in clauses)).encode()

def build():
    manifest = json.loads((HERE/'manifest.json').read_text())
    for path, expected in manifest['inputs'].items():
        require(digest((REPO/path).read_bytes()) == expected, ('input hash', path))
    pts = {}
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        row = tuple(3*int(x) for x in line.split())
        require(len(row) == 16, 'base coordinate width')
        pts[len(pts)] = (row[:8], row[8:])
    require(len(pts) == 509, 'base order')
    pairs = read_json('hadwiger_nelson_parts509_pair_replacement_classification/certificate.json')['records']
    additions = sorted({i for r in pairs for i in r['A']})
    require(len(additions) == 19 and len(pairs) == 63, 'replacement pool')
    q = read_json('hadwiger_nelson_parts509_swap_closure/completion_points.json')['points']
    for i in additions + [523, 619]:
        pts[509+i] = point([q[i]['x'], q[i]['y']])
    labels = sorted(pts)
    require(len(labels) == len(set(pts.values())) == 530, 'collision merging')
    edges = [e for e in combinations(labels, 2) if norm(pts[e[0]], pts[e[1]]) == UNIT]
    require(len(edges) == 2582 and sum(b < 509 for a, b in edges) == 2442, 'whole unit graph')
    adjacency = {v: set() for v in labels}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    for i in additions+[523, 619]:
        require(sorted(adjacency[509+i] & set(range(509))) == q[i]['neighbors'], 'completion neighbours')
    require([e for e in edges if e[0] >= 509] == [(1032, 1128)], 'new-point contacts')
    return pts, labels, edges, adjacency, additions, pairs

def compute(write_cnf=None, certificate=None):
    pts, labels, edges, adj, additions, pairs = build()
    old_labels = [v for v in labels if v not in (1032, 1128)]
    require(len(old_labels) == 528, 'tie host order')
    require(sum(a in old_labels and b in old_labels for a, b in edges) == 2573, 'tie host edges')
    containment = {}
    for tag in ('P25', 'P44', 'L2'):
        old = read_json('hadwiger_nelson_parts509_tie_union_minimum/certificate_'+tag+'.json')
        old_points = {point(p) for p in old['coordinates'].values()}
        outsiders = [v for v in labels if pts[v] not in old_points]
        require(outsiders == [1032, 1128], ('closed host containment', tag))
        containment[tag] = {'old_host_points': len(old_points), 'outside_labels': outsiders}
    # Distinguish the separate pure quadratic switching exclusion.
    base = [pts[v] for v in range(509)]
    switched = set(base + [tuple(tuple(-x if i & 2 else x for i, x in enumerate(axis))
                               for axis in p) for p in base[374:]])
    require(all(pts[v] not in switched for v in labels if v >= 509), 'switching host containment')
    certified_parents = [r for r in pairs if r['status'] == 'certified-not-4-colorable']
    require(len(certified_parents) == 60, 'imported parent records')
    common = set(range(509)) - {x for r in certified_parents for x in r['U']}
    require(len(common) == 495 and {97, 139} <= common, 'known parent destruction')

    # Reproduce the first deterministic, fixed-word-only ranking.
    original = read_json('hadwiger_nelson_parts509_criticality/certificate.json')
    raw = base64.b64decode(original['deletion_colorings_base64'], validate=True)
    require(digest(raw) == original['packed_deletion_colorings_sha256'], 'base word hash')
    require(len(raw) == 509*127, 'base word size')
    rank1 = []
    for v in sorted(common):
        vl = [x for x in range(509) if x != v]
        values = [(raw[127*v+i//4] >> (2*(i % 4))) & 3 for i in range(508)]
        col = dict(zip(vl, values, strict=True))
        blocked = [i for i in additions if {col[x] for x in adj[509+i] if x in col} == set(range(4))]
        degree = len(adj[v] - {1032, 1128})
        rank1.append((-len(blocked), -degree, v, blocked))
        if v == 97:
            proper(vl, edges, values)
    rank1.sort()
    require(rank1[0] == (-6, -11, 97, [2, 3, 43, 96, 211, 658]), 'first selected omission')

    # Reproduce the two-sided fixed-word preflight for the distinct fusion.
    old = read_json('hadwiger_nelson_parts509_tie_union_minimum/certificate_P25.json')
    g14 = read_json('hadwiger_nelson_parts509_g14_augmentation/certificate.json')['A_pair']
    gl = [i if kind == 'V' else 509+i for kind, i in g14['local_vertex_order']]
    require(gl == [v for v in range(509) if v != 350]+[1032, 1128], 'G14 parent labels')
    rows = unpack_g14(g14)
    rank2 = []
    for v in sorted(common & set(old['forced'])):
        oc = dict(zip([x for x in old['vertices'] if x != v], map(int, old['forced_witness'][str(v)]), strict=True))
        oc.pop(350, None)
        lists = {x: set(range(4)) - {oc[y] for y in adj[x] if y in oc} for x in (1032, 1128)}
        if any(a != b for a in lists[1032] for b in lists[1128]):
            continue
        gc = dict(zip([x for x in gl if x != v], rows[gl.index(v)], strict=True))
        blocked = [509+i for i in additions if {gc[y] for y in adj[509+i] if y in gc} == set(range(4))]
        if blocked:
            rank2.append((-len(blocked), -len(adj[v]), v, blocked))
    rank2.sort()
    require(len(rank2) == 11 and rank2[0] == (-4, -13, 139, [510, 512, 552, 640]), 'fusion selection')
    proper([x for x in gl if x != 139], edges, rows[gl.index(139)])
    # Only the selected P25 word is needed for the stated incompatibility.
    # Check its restriction against every edge of the original 528-point host.
    oc = dict(zip([x for x in old['vertices'] if x != 139], old['forced_witness']['139'], strict=True))
    ol = [x for x in old_labels if x not in (350, 139)]
    proper(ol, edges, ''.join(oc[x] for x in ol))

    cert = certificate or json.loads((HERE/'certificate.json').read_text())
    require(cert['format'] == 'hn-positive-parent-fusion-gate-v1' and len(cert['cases']) == 2, 'certificate format')
    cases = []
    for i, record in enumerate(cert['cases']):
        domain = old_labels if i == 0 else labels
        missing = [97] if i == 0 else [350, 139]
        require(record['omitted'] == missing, 'omission declaration')
        keep = [v for v in domain if v not in missing]
        chosen = set(keep)
        subedges = [e for e in edges if set(e) <= chosen]
        require((len(keep), len(subedges)) == ((527, 2562) if i == 0 else (528, 2563)), 'selected graph dimensions')
        require((record['vertices'], record['edges']) == (len(keep), len(subedges)), 'certificate dimensions')
        _, checked = proper(keep, subedges, record['four_colouring'])
        for parent in certified_parents:
            pl = (set(range(509))-set(parent['U'])) | {509+x for x in parent['A']}
            require(not pl <= chosen, 'known replacement parent remains')
        require(not set(range(509)) <= chosen and not set(gl) <= chosen, 'known base or G14 parent remains')
        data = cnf(keep, subedges)
        require(digest(data) == record['cnf_sha256'], 'discovery CNF identity')
        if write_cnf:
            Path(write_cnf).mkdir(parents=True, exist_ok=True)
            (Path(write_cnf)/(record['name']+'.cnf')).write_bytes(data)
        cases.append({'name': record['name'], 'vertices': len(keep), 'edges': len(subedges),
                      'four_colouring_checks': checked,
                      'edge_sha256': digest(''.join(f'{a} {b}\n' for a, b in subedges).encode())})
    return {'all_checks': True, 'whole_host_vertices': 530, 'whole_host_edges': 2582,
            'exact_pair_decisions': 530*529//2, 'cases': cases, 'closed_host_containment': containment,
            'two_sided_fixed_word_signals': 11, 'selected_fusion_omissions': [350, 139],
            'fresh_non_four_signal': False, 'record_certified': False,
            'full_fusion_host_minimum_order_decided': False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-cnf')
    args = parser.parse_args()
    print(json.dumps(compute(args.write_cnf), indent=2, sort_keys=True))
