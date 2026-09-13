"""Solver-free verification of the three-rotation theorem's finite leaves."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import geometry as G

HERE = Path(__file__).resolve().parent

def word_ok(word, edges):
    return (len(word) == 159 and word[0] == 0
            and all(type(c) is int and 0 <= c < 4 for c in word)
            and all(word[a] != word[b] for a, b in edges))

def bridge_ok(a, b, edges, same=()):
    return all(a[i] != b[j] for i, j in edges) and all(a[i] == b[j] for i, j in same)

def load_certificate(path, internal):
    cert = json.loads(path.read_text())
    G.require(set(cert) == {'words', 'extensions', 'cycles'}, 'certificate schema')
    words = [tuple(map(int, s)) for s in cert['words']]
    G.require(len(set(words)) == len(words), 'duplicate certificate word')
    G.require(all(word_ok(w, internal) for w in words), 'invalid component coloring')
    extensions = {i: j for i, j in cert['extensions']}
    cycles = {(i, j): (a, b, c) for i, j, a, b, c in cert['cycles']}
    G.require(len(extensions) == len(cert['extensions']) and len(cycles) == len(cert['cycles']),
              'duplicate certificate index')
    G.require(all(0 <= k < len(words) for k in extensions.values()), 'word index')
    G.require(all(0 <= k < len(words) for row in cycles.values() for k in row), 'cycle word index')
    return cert, words, extensions, cycles

def verify(certificate=None):
    data = G.build()
    data['group_map'] = dict(data['groups'])
    lib, words = G.library()
    edges = data['internal']
    G.require(all(word_ok(w, edges) for w in words), 'library coloring')
    fixed = tuple(G.K.color(a) for a in data['A'])
    G.require(fixed == lib[0] and word_ok(fixed, edges), 'field-coloring interface')
    cert, extra, extensions, cycles = load_certificate(certificate or HERE/'certificate.json', edges)
    used_extensions = set()
    extension_words = []
    masks = []
    for i, (_, es) in enumerate(data['groups']):
        w = next((w for w in words if bridge_ok(fixed, w, es)), None)
        if w is None:
            G.require(i in extensions, 'missing fixed-field extension')
            w = extra[extensions[i]]
            used_extensions.add(i)
        G.require(bridge_ok(fixed, w, es), 'invalid fixed-field extension')
        extension_words.append(w)
        masks.append([sum(1 << j for j, b in enumerate(words) if bridge_ok(a, b, es))
                      for a in lib])
    G.require(used_extensions == set(extensions), 'unused extension row')
    # The two-copy in-E gluing formula is checked on every E contact phase.
    for u, (es, same) in data['e_data'].items():
        w = tuple(G.K.color(G.mul(u, a)) for a in data['A'])
        G.require(word_ok(w, edges) and bridge_ok(fixed, w, es, same), 'E gluing')
    root_by_field = defaultdict(list)
    for i, (g, f, z) in enumerate(data['roots']):
        root_by_field[f].append(i)
    comp_cache = {}
    hist = Counter()
    used_cycles = set()
    coverage = sha256()
    for f, ids in sorted(root_by_field.items()):
        d = data['fields'][f]
        for i, j in combinations(ids, 2):
            gi, _, u = data['roots'][i]
            gj, _, v = data['roots'][j]
            es, same, kind = G.relative_contacts(data, u, v, d)
            hist[kind] += 1
            if not es:
                G.require(not same, 'unhandled coincidence without contact')
                hist['no_outer_edges'] += 1
                continue
            key = tuple(es), tuple(same)
            if key not in comp_cache:
                comp_cache[key] = [sum(1 << k for k, b in enumerate(words)
                                      if bridge_ok(a, b, es, same)) for a in words]
            comp = comp_cache[key]
            witness = None
            for a in range(4):
                for b in range(24):
                    mm = comp[b] & masks[gj][a] if masks[gi][a] >> b & 1 else 0
                    if mm:
                        witness = a, b, (mm & -mm).bit_length()-1
                        break
                if witness is not None:
                    break
            if witness is not None:
                a, b, c = witness
                ca, cb, cc = lib[a], words[b], words[c]
                hist['library'] += 1
                tag = ['library', *witness]
            else:
                G.require((i, j) in cycles, 'missing cycle witness')
                indices = cycles[i, j]
                ca, cb, cc = [extra[k] for k in indices]
                used_cycles.add((i, j))
                hist['certificate'] += 1
                tag = ['certificate', *indices]
            G.require(bridge_ok(ca, cb, data['groups'][gi][1])
                      and bridge_ok(ca, cc, data['groups'][gj][1])
                      and bridge_ok(cb, cc, es, same), 'cycle coloring')
            coverage.update((json.dumps([i, j, tag], separators=(',', ':'))+'\n').encode())
    G.require(used_cycles == set(cycles), 'unused cycle witness')
    n = len(data['roots'])
    same_count = sum(len(ids)*(len(ids)-1)//2 for ids in root_by_field.values())
    result = {
        'vertices_per_copy': len(data['A']), 'internal_edges': len(edges),
        'three_copy_vertex_bound': 475, 'rotation_classes_outside_E': len(data['groups']),
        'outside_E_rotations': n, 'E_contact_rotations': len(data['e_roots']),
        'positive_radicands': data['radicands'], 'quadratic_extensions': len(data['fields']),
        'trace_zero_classes': 0, 'same_field_rotation_pairs': same_count,
        'different_field_rotation_pairs': n*(n-1)//2-same_count,
        'same_field_outcomes': dict(sorted(hist.items())),
        'fixed_field_extensions_in_library': len(data['groups'])-len(used_extensions),
        'fixed_field_extension_certificate_rows': len(used_extensions),
        'cycle_certificate_rows': len(used_cycles), 'certificate_component_words': len(extra),
        'certificate_sha256': sha256((certificate or HERE/'certificate.json').read_bytes()).hexdigest(),
        'coverage_sha256': coverage.hexdigest(), 'all_three_rotation_unions_four_colorable': True,
    }
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-expected', action='store_true')
    parser.add_argument('--certificate', type=Path)
    args = parser.parse_args()
    result = verify(args.certificate)
    if args.check_expected:
        G.require(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected result mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
