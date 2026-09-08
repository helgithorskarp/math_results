"""Optional provenance audit; the final graph theorem needs no source theorem."""
import hashlib
import importlib.util
import json
from pathlib import Path
import geometry as G


def parent():
    repo = G.ROOT.parent
    for name, digest in G.read('source_dependencies.json').items():
        G.require(hashlib.sha256((repo/name).read_bytes()).hexdigest() == digest, 'changed source: '+name)
    def load(name):
        path = repo/'hadwiger_nelson_ei_global_interfaces'/(name+'.py')
        spec = importlib.util.spec_from_file_location('terminal_core_parent_'+name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    geometry, audit = load('geometry'), load('audit')
    cert = geometry.read(geometry.ROOT/'certificate.json')
    points, _, _ = geometry.half_layer()
    half, _ = geometry.completed_half(points, cert['selected_triangles'])
    rows = list(map(geometry.A.row, half))
    direct, _, _, _ = audit.half_layer()
    G.require(rows == audit.completed_half(direct, cert['selected_triangles']), 'source reconstructions differ')
    G.require(len(rows) == 4293 and geometry.digest(half) ==
              '42d27b5f427335eb0ccc1bec96a3142d79675ad83e385ab632c8159ce7a7af21', 'source graph identity')
    return rows


def verify():
    rows = parent()
    cert = G.read('source_certificate.json')
    indices = cert['retained_source_indices']
    G.require(type(indices) is list and indices == sorted(set(indices)) and
              all(type(v) is int and 0 <= v < len(rows) for v in indices), 'source index format')
    G.require([rows[v] for v in indices] == G.rows(), 'source subset differs')
    edges = G.half_edges(rows)
    word = cert['parent_four_colouring']
    G.require(len(edges) == 29934 and type(word) is str and len(word) == len(rows) and
              set(word) <= set('0123') and all(word[i] != word[j] for i, j in edges), 'parent four-colouring')
    G.require(''.join(word[v] for v in indices) == G.read('certificate.json')['half_four_colouring'], 'restricted word differs')
    return {'verified': True, 'parent_vertices': len(rows), 'parent_edges': len(edges),
            'parent_point_pairs_checked': len(rows)*(len(rows)-1)//2,
            'parent_four_colourable': True, 'retained_vertices': len(indices)}


if __name__ == '__main__':
    print(json.dumps(verify(), sort_keys=True))
