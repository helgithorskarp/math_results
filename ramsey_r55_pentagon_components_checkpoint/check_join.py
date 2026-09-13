"""Definition-level control for the missing global component join.
No target search, solver, catalog or imported target theorem is used.
"""
from itertools import combinations
from collections import Counter
import json

def require(ok, message):
    if not ok:
        raise ValueError(message)

def edge(u, v):
    a, x = divmod(u, 5)
    b, y = divmod(v, 5)
    return (x-y) % 5 in (1, 4) if a == b else (a-b) % 5 in (1, 4)

def partition_profiles():
    # Independent dynamic recursion for unordered component sizes >= 5.
    def rec(total, minimum, remaining):
        if remaining == 0:
            return [()] if total == 0 else []
        result = []
        for first in range(minimum, total // remaining + 1):
            result.extend((first,) + tail for tail in rec(total-first, first, remaining-1))
        return result
    profiles = [(s, sizes) for k in range(1, 6) for s in range(21-4*k)
                for sizes in rec(43-s, 5, k)]
    require(len(profiles) == len(set(profiles)), 'duplicate profile')
    require(all(s+sum(p) == 43 and s+4*len(p) <= 20 for s,p in profiles), 'bad profile')
    return profiles

def main():
    cycles = []
    defects = [0, 0]
    for S in combinations(range(25), 5):
        degrees = [sum(edge(u,v) for v in S if u != v) for u in S]
        defects[0] += all(d == 0 for d in degrees)
        defects[1] += all(d == 4 for d in degrees)
        if all(d == 2 for d in degrees):
            cycles.append(S)
    internal = [S for S in cycles if len({v//5 for v in S}) == 1]
    transversal = [S for S in cycles if len({v//5 for v in S}) == 5]
    require(defects == [0, 0], 'control is not good25')
    require(len(internal) == 5 and len(transversal) == 3125, 'wrong cycle classes')
    require(len(cycles) == len(internal) + len(transversal), 'extra cycle class')
    proper = []
    for k in range(1,5):
        for B in combinations(range(5),k):
            found = [S for S in cycles if {v//5 for v in S} <= set(B)]
            require(len(found) == k and all(S in internal for S in found), 'proper block join')
            proper.append((B, len(found)))
    # C5 is prime: no proper subset of size 2,3,4 is a module.
    module_checks = 0
    for k in range(2,5):
        for M in combinations(range(5),k):
            outside = set(range(5))-set(M)
            require(any(len({edge(v,u) for u in M}) == 2 for v in outside), 'C5 module')
            module_checks += 1
    # Every cross-block pair occurs in a transversal cycle; every same-block
    # pair occurs in its internal cycle. Hence the full incidence 2-section
    # of this control is the complete graph on 25 vertices.
    pair_union = {pair for S in cycles for pair in combinations(S,2)}
    require(len(pair_union) == 300, 'full incidence support is not complete')
    profiles = partition_profiles()
    counts = dict(sorted(Counter(len(p) for _,p in profiles).items()))
    require(counts == {1:17,2:185,3:551,4:608,5:141}, 'profile cover mismatch')
    return {'status':'CHECKED_COMPONENT_JOIN_GAP', 'control_order':25,
            'control_monochromatic_fives':defects, 'all_five_sets_checked':53130,
            'internal_pentagons':5, 'five_component_pentagons':3125,
            'proper_block_subsets_checked':len(proper), 'C5_module_checks':module_checks,
            'full_incidence_pairs':len(pair_union), 'necessary_order43_profiles':len(profiles),
            'profile_counts_by_nontrivial_components':counts,
            'excluded_order43_profiles':0, 'global_terminal_decisions':0,
            'external_N5_used_only_for_profile_cover':True}

if __name__ == '__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
