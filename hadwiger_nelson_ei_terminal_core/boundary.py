"""Verify a mandatory-vertex obstruction using only existing SAT witnesses.

No solver is imported. The optional extraction reads the bounded search's
saved colour words and restricts them to the published 502-point half.
"""
import argparse
import hashlib
import json
from pathlib import Path
import geometry as G


def verify(words):
    rows = G.rows()
    n = len(rows)
    cert = G.read('certificate.json')
    origin, terminal = cert['pins']
    local = G.read('boundary_certificate.json')['mandatory_half_nonterminals']
    G.require(local == sorted(set(local)) and len(local) == 416 and
              all(type(v) is int and 0 <= v < n and v not in (origin, terminal) for v in local), 'mandatory set')
    G.require(set(words) == set(map(str, local)), 'witness coverage')
    edges, labels, _ = G.spindle(rows)
    base = cert['half_four_colouring']
    G.require(base[origin] == base[terminal] == '0', 'base palette')
    def combine(left, right):
        return left+''.join(c for v, c in enumerate(right) if v != origin)
    checked = set()
    def deletion(word, omitted):
        G.require(type(word) is str and len(word) == 2*n-1 and set(word) <= set('0123'), 'deletion word format')
        G.require(all(word[u] != word[v] for u, v in edges if omitted not in (u, v)), 'global deletion witness')
        checked.add(omitted)
    for v in local:
        word = words[str(v)]
        G.require(type(word) is str and len(word) == n and set(word) <= set('0123'), 'local word format')
        G.require(word[origin] == '0' and word[terminal] == '1', 'local terminal colours')
        deletion(combine(word, base), v)
        deletion(combine(base, word), labels[v])
    deletion(combine(base, base), terminal)
    deletion(combine(base, base), labels[terminal])
    renamed = base.translate(str.maketrans('01', '10'))
    deletion(combine(base, renamed), origin)
    G.require(len(checked) == 835, 'mandatory global count')
    return {'verified': True, 'local_deletion_words': len(local),
            'global_vertex_deletion_colourings_checked': len(checked),
            'every_non_four_colourable_subgraph_contains_at_least_vertices': len(checked),
            'all_subgraphs_through_vertices_four_colourable': len(checked)-1,
            'target_508_excluded_inside_this_host': True,
            'scope_host_vertices': 2*n-1, 'lower_bound_attainment_claimed': False,
            'parent_4293_support_closed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--words', required=True, type=Path)
    parser.add_argument('--search', type=Path, help='optionally extract from a saved reduction.json')
    args = parser.parse_args()
    if args.search:
        G.require(not args.words.resolve().is_relative_to(G.ROOT.parent.resolve()), 'word output must be outside repository')
        search = json.loads(args.search.read_text())
        indices = G.read('source_certificate.json')['retained_source_indices']
        words = {str(v): ''.join(search['words'][str(indices[v])][i] for i in indices)
                 for v in G.read('boundary_certificate.json')['mandatory_half_nonterminals']}
        args.words.parent.mkdir(parents=True, exist_ok=True)
        args.words.write_text(json.dumps(words, sort_keys=True, indent=2)+'\n')
    else:
        words = json.loads(args.words.read_text())
    result = verify(words)
    result['word_file_sha256'] = hashlib.sha256(args.words.read_bytes()).hexdigest()
    result['word_file_bytes'] = args.words.stat().st_size
    if (G.ROOT/'boundary_expected.json').exists():
        G.require(result == G.read('boundary_expected.json'), 'boundary expected result differs')
    print(json.dumps(result, sort_keys=True, indent=2))
