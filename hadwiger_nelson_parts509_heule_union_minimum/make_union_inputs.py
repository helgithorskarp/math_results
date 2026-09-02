#!/usr/bin/env python3
"""union_XXX.json (from union_graph.py) -> ambient_XXX.json ({'edges': ...}) + tu_XXX.json ({'start', 'added_points', 'deleted_vertices', 'ties'})
in the format of ties/forced_vertices.py and ties/ihs_thin2.py (Parts vertices 0..508, other points >= 509)."""
import json, sys
u = json.load(open(sys.argv[1])); tag = sys.argv[2]
n = len(u['points'])
assert all('P' in u['provenance'][i] for i in range(509)) and all('P' not in u['provenance'][i] for i in range(509, n))
json.dump({'vertices': n, 'parts_vertices': 509, 'edges_total': len(u['edges']), 'edges': [list(e) for e in u['edges']],
           'source': sys.argv[1]}, open(f'ambient_{tag}.json', 'w'))
json.dump({'start': list(range(n)), 'added_points': list(range(509, n)), 'deleted_vertices': [], 'ties': [],
           'provenance': u['provenance']}, open(f'tu_{tag}.json', 'w'))
print(tag, n, 'vertices', len(u['edges']), 'edges; points', n - 509)
