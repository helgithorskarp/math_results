"""Independent physical check, without producer/solver imports."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def has_clique(vertices, edges, color=True):
    return all((tuple(sorted(e)) in edges) == color for e in it.combinations(vertices, 2))


def pentagon(vertices, edges):
    return all(sum(tuple(sorted((u, v))) in edges for v in vertices if v != u) == 2 for u in vertices)


def check(cert):
    if cert['cycle_order'] != 7 or cert['vertex_labels'] != list(range(7)):
        raise ValueError('cycle labels')
    cycle = {tuple(sorted((i, (i+1) % 7))) for i in range(7)}
    # All7-bit contacts, classified by physical triangles and pentagons on8 vertices.
    physical_contacts = []
    for s in range(128):
        e = cycle | {(i, 7) for i in range(7) if s >> i & 1}
        if any(has_clique(q, e) for q in it.combinations(range(8), 3)):
            continue
        if any(pentagon(q, e) for q in it.combinations(range(8), 5)):
            continue
        physical_contacts.append(s)
    if cert['allowed_contacts'] != physical_contacts:
        raise ValueError('contact coverage')
    rows = {}
    for row in cert['contact_pairs']:
        if set(row) != {'s', 't', 'independent'}:
            raise ValueError('row fields')
        key = row['s'], row['t']
        if any(type(x) is not int or not 0 <= x < 128 for x in key) or key in rows:
            raise ValueError('row key')
        q = row['independent']
        if len(q) != 3 or len(set(q)) != 3 or any(type(v) is not int or not 0 <= v < 7 for v in q):
            raise ValueError('stable labels')
        if any((key[0] | key[1]) >> v & 1 for v in q) or not has_clique(q, cycle, False):
            raise ValueError('stable witness')
        rows[key] = q
    found = set()
    rejection_counts = {'triangle': 0, 'pentagon': 0, 'independent5': 0}
    witness_stream = hashlib.sha256()
    for s in range(128):
        for t in range(128):
            # C7 on0..6; root7; its nonadjacent neighbors8,9.
            e = cycle | {(7, 8), (7, 9)}
            e |= {(i, 8) for i in range(7) if s >> i & 1}
            e |= {(i, 9) for i in range(7) if t >> i & 1}
            if any(has_clique(q, e) for q in it.combinations(range(10), 3)):
                rejection_counts['triangle'] += 1
                continue
            if any(pentagon(q, e) for q in it.combinations(range(10), 5)):
                rejection_counts['pentagon'] += 1
                continue
            found.add((s, t))
            if (s, t) not in rows or not has_clique(rows[s, t] + [8, 9], e, False):
                raise ValueError(('physical independent5', s, t))
            q = next((q for q in it.combinations(range(10), 5) if has_clique(q, e, False)), None)
            if q is None:
                raise ValueError(('missing physical obstruction', s, t))
            witness_stream.update(f'{s},{t}:{q}\n'.encode())
            rejection_counts['independent5'] += 1
    if found != set(rows):
        raise ValueError('pair coverage')
    # C9 demonstrates sharpness of the order10 lemma.
    c9 = {tuple(sorted((i, (i+1) % 9))) for i in range(9)}
    if any(has_clique(q, c9) for q in it.combinations(range(9), 3)):
        raise ValueError('C9 triangle')
    if any(pentagon(q, c9) or has_clique(q, c9, False) for q in it.combinations(range(9), 5)):
        raise ValueError('C9 forbidden set')
    if not any(has_clique(q, c9, False) for q in it.combinations(range(9), 4)):
        raise ValueError('C9 independence')
    # In the cubic case, all possible partition sizes are checked separately.
    candidates = [(a, b) for a in range(7) for b in range(7)
                  if a+b == 6 and a <= 4 and b <= 2]
    if candidates != [(4, 2)] or 3*4 <= 3*2 + 2*2:
        raise ValueError('cubic contradiction')
    # Integer version of the global lower bound:8*(3M)>=n(n-1)(n-5).
    gaps = {str(n): n*(n-1)*(n-5) - 36*n*(n-1) for n in (42, 43)}
    if any(v <= 0 for v in gaps.values()):
        raise ValueError('global triangle gap')
    return {'status': 'VERIFIED_INDUCED_PENTAGON_FORCING_KERNEL',
            'physical_contacts': len(physical_contacts), 'physical_pairs': 16384,
            'compatible_pairs': len(found), 'physical_cases': rejection_counts,
            'witness_stream_sha256': witness_stream.hexdigest(),
            'cubic_incidence_demand': 12, 'cubic_incidence_supply': 10,
            'scaled_global_gaps': gaps, 'sharp_small_witness': 'C9',
            'trust': 'unformalized universal proof in PROOF.md plus exact finite checks'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('certificate', type=Path)
    a = p.parse_args()
    print(json.dumps(check(json.loads(a.certificate.read_text())), sort_keys=True, indent=2))
