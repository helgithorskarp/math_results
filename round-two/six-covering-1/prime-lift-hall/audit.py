"""Independent physical replay; imports no generator or production checker."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


core = json.loads((HERE / 'core.json').read_text())['congruences']
near = json.loads((HERE / 'near.json').read_text())['congruences']
cert = json.loads((HERE / 'certificate.json').read_text())
expected = json.loads((HERE / 'expected.json').read_text())
need(cert['prime'] == 3 and cert['core_period'] == 5040 and cert['period'] == 15120, 'periods')
need(len(core) == 53 and len({m for a, m in core}) == 53, 'core labels')
need({m for a, m in core} == {m for m in range(8, 5041) if 5040 % m == 0}, 'core divisor completion')
need(all(type(a) is int and type(m) is int and 0 <= a < m for a, m in core), 'core phases')
core_R = [x for x in range(5040) if all(x % m != a for a, m in core)]
full_R = [x for x in range(15120) if all(x % m != a for a, m in core)]
need(full_R == sorted(x + j * 5040 for x in core_R for j in range(3)), 'projection multiplicities')
parents = sorted({x % 9 for x in core_R})
need(parents == [r for r, n, g in expected['residual_fibers']], 'residual parents')


def lift(x, s):
    choices = [x + j * 5040 for j in range(3) if (x + j * 5040) % 27 == s]
    need(len(choices) == 1, 'unique compatible lift')
    return choices[0]


physical = {s: [lift(x, s) for x in core_R if x % 9 == s % 9]
            for s in range(27) if s % 9 in parents}
need(len(physical) == 18 and sum(map(len, physical.values())) == 885, 'physical fibers')
need(len({x for S in physical.values() for x in S}) == 885, 'disjoint physical fibers')
samples = {}
for r, points in cert['point_witnesses']:
    need(r in parents and r not in samples and points, 'sample parent')
    need(all(x in core_R and x % 9 == r for x in points), 'sample uncovered')
    samples[r] = points
need(set(samples) == set(parents), 'sample parents')
sample_physical = {s: [lift(x, s) for x in samples[s % 9]] for s in physical}
targets = [x for S in sample_physical.values() for x in S]
need(len(targets) == len(set(targets)) == 30, 'target separation')
E = [d for d in range(1, 561) if 560 % d == 0]
H = cert['hall_fibers']
need(H == [0, 2, 5, 8], 'Hall parents')
restricted = [s for s in physical if s % 9 in H]
need(len(restricted) == 12, 'restricted copies')
neighbor_union = set()
for s in restricted:
    S = sample_physical[s]
    for d in E:
        m = 27 * d
        a = S[0] % m
        if all(x % m == a for x in S):
            neighbor_union.add(d)
need(sorted(neighbor_union) == cert['neighbor_resources'] == [1, 2, 4, 5, 10, 20], 'literal singleton neighborhood')
lower = len(physical) + len(restricted) - len(neighbor_union)
need(lower == cert['resource_lower_bound'] == 24 and lower > len(E), 'literal strict budget')
# An explicit matching plus the Hall upper bound establishes the maximum.
matching = expected['matching']
need(len(matching) == 12 and len({d for d, r, j in matching}) == 12, 'matching resources')
need(len({r + 9 * j for d, r, j in matching}) == 12, 'matching fibers')
for d, r, j in matching:
    need(d in E and r in parents and 0 <= j < 3, 'matching domain')
    S = physical[r + 9 * j]
    a = S[0] % (27 * d)
    need(all(x % (27 * d) == a for x in S), 'matching physical progression')
need(len(matching) == len(physical) - (len(restricted) - len(neighbor_union)), 'matching upper equality')
# All phases, ordinary progressions, and physical residual membership.
Rset = set(full_R)
capacities = []
for d in E:
    m = 27 * d
    capacity = max(sum(x in Rset for x in range(a, 15120, m)) for a in range(m))
    capacities.append([m, capacity])
need(capacities == expected['capacities'], 'literal capacity table')
need(len(full_R) == expected['ordinary_uniform_demand'] == 885, 'uniform demand')
need(sum(c for m, c in capacities) == expected['ordinary_uniform_capacity'] == 896, 'uniform capacity')
need(len(near) == 73 and len({m for a, m in near}) == 73 and
     {m for a, m in near} == {m for m in range(8, 15121) if 15120 % m == 0}, 'near labels')
need(all(type(a) is int and type(m) is int and 0 <= a < m for a, m in near), 'near phases')
need({m: a for a, m in near if 5040 % m == 0} == {m: a for a, m in core}, 'near/core identity')
holes = [x for x in range(15120) if all(x % m != a for a, m in near)]
need(len(holes) == expected['near_cover_holes'] == 101, 'near holes')
hole_hash = hashlib.sha256(','.join(map(str, holes)).encode()).hexdigest()
need(hole_hash == expected['near_holes_sha256'], 'near hole hash')
print(json.dumps({'physical_core_residual': len(core_R), 'physical_lifted_residual': len(full_R),
                  'target_points': len(targets), 'lifted_fibers': len(physical),
                  'hall_copies': len(restricted), 'hall_neighbors': sorted(neighbor_union),
                  'maximum_singleton_matching': len(matching), 'required_resources': lower,
                  'available_resources': len(E), 'uniform_capacity': sum(c for m, c in capacities),
                  'near_cover_holes': len(holes)}, sort_keys=True))
