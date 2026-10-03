"""Exact compressed BASE record producer; the separate checker is required."""
from itertools import combinations
from math import lcm
import json
import struct
from hashlib import sha256
from pathlib import Path
import time

started = time.monotonic()
P = ((8,0),(9,0),(10,1),(14,1),(12,10))
B = [n for n in range(8,2521) if 2520 % n == 0 and n not in (8,9,10,12,14)]
D = [d for d in range(1,316) if 315 % d == 0]
edges = [(a,b) for a,b in combinations(D,2)]
matching = [(a,b) for a in edges for b in edges if set(a).isdisjoint(b)]
maximum_four_tail_capacity = max(315 // lcm(*a)+315 // lcm(*b) for a,b in matching)
points = [x for x in range(2520) if all(x % n != a for n,a in P)]
actions = {n:[0]*n for n in B}
for i,x in enumerate(points):
    for n in B:actions[n][x%n] |= 1<<i
remaining = [n for n in B if n not in (15,18)]
low,high = 65536,-1
rows = []
digest = sha256()
for a15 in range(15):
    for a18 in range(18):
        U = actions[15][a15] | actions[18][a18]
        caps = [max((v & ~U).bit_count() for v in actions[n]) for n in remaining]
        K = U.bit_count()+sum(caps)
        row=[a15,a18,U.bit_count(),*caps,K]
        raw=struct.pack('<38H',*row);digest.update(raw);rows.append(raw)
        low,high=min(low,K),max(high,K)
Path('scratch/four-tail-global-base-pilot.bin').write_bytes(b''.join(rows))
result={'agent':'six-covering-3','role':'researcher','phase':'PRODUCER_ONLY_SEPARATE_CHECKER_REQUIRED',
        'required_fullP_points':len(points),'complete_raw_pairs':270,
        'capacity_range':[low,high],'global_BASE_holes_lower_candidate':len(points)-high,
        'maximum_four_tail_hole_capacity':maximum_four_tail_capacity,
        'all_ordered_disjoint16d_edge_matchings':len(matching),
        'uniform_five_productive_TAIL_claimed':False,'stream_sha256':digest.hexdigest(),
        'seconds':time.monotonic()-started}
Path('scratch/four-tail-global-base-pilot.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
