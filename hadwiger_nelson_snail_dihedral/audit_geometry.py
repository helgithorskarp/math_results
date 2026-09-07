"""Independent geometry in basis a^i b^j c^k e^l, a=i*sqrt(3).

The verifier never imports geometry.py. Optional --producer compares every
coordinate, coincidence class and edge with a regenerated producer directory.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import verify as v

from independent_field import ONE, D, bar, norm, minus, times, exact_seed, exact_addresses, double_change_basis

def audit(producer=None):
    ctx = v.context()
    seed = exact_seed()
    base_edges = [(i,j) for i,j in itertools.combinations(range(29),2)
                  if norm(minus(seed[i],seed[j]))==times(D*D,ONE)]
    count = 0
    pairs = 0
    norm_checks = 0
    positions = 0
    residue_basis = [1]*16
    for i in range(16):
        for bit,root in enumerate(v.ROOTS):
            if i&(1<<bit):
                residue_basis[i] = residue_basis[i]*root%v.P

    def residue(x):
        return sum(a*b for a,b in zip(x,residue_basis))%v.P

    census = []
    for c in range(29):
        for a in range(29):
            if c==a:
                continue
            formal,target = exact_addresses(seed,c,a)
            xs,bxs = v.addresses(ctx,c,a)
            denominator = 2*D*residue(norm(minus(seed[a],seed[c])))%v.P
            inverse = v.inv(denominator)
            v.require([residue(x)*inverse%v.P for x in formal]==xs,
                      'direct scalar versus exact coordinates')
            v.require([residue(bar(x))*inverse%v.P for x in formal]==bxs,
                      'direct scalar versus exact conjugates')
            first = {}
            for i,x in enumerate(formal):
                first.setdefault(x,i)
            representatives = sorted(first.values())
            edges = []
            for i,j in itertools.combinations(representatives,2):
                pairs += 1
                if (xs[i]-xs[j])*(bxs[i]-bxs[j])%v.P==1:
                    norm_checks += 1
                    if norm(minus(formal[i],formal[j]))==target:
                        edges.append((i,j))
            record = {'centre':c,'axis':a,'D3_vertices':len(representatives),
                      'D3_edges':len(edges),'D9_vertices':3*len(representatives)-2,
                      'D9_edges':3*len(edges)}
            if producer is not None:
                original = json.loads((producer/f'case_{c:02}_{a:02}.json').read_text())
                ids = original['address_ids']
                v.require(len(ids)==174,'producer address count')
                transformed = [times(8,double_change_basis(x)) for x in original['points']]
                v.require([transformed[j] for j in ids]==formal,'independent full coordinate comparison')
                v.require(len(set(transformed))==len(representatives)==len(transformed),
                          'independent coincidence comparison')
                expected_edges = sorted(tuple(sorted((ids[i],ids[j]))) for i,j in edges)
                v.require(expected_edges==[tuple(e) for e in original['edges']],
                          'independent complete edge comparison')
            census.append(record)
            positions += len(formal)
            count += 1
    payload = json.dumps(census,separators=(',',':')).encode()
    return {'verified':True,'cases':count,'formal_positions_checked':positions,
            'distinct_point_pairs_checked':pairs,'full_norm_checks_after_modular_filter':norm_checks,
            'seed_vertices':len(seed),'seed_edges':len(base_edges),
            'seed_p_q_neighbours':[[j if i==u else i for i,j in base_edges if u in (i,j)] for u in [0,1]],
            'D3_vertices_range':[min(r['D3_vertices'] for r in census),max(r['D3_vertices'] for r in census)],
            'D3_edges_range':[min(r['D3_edges'] for r in census),max(r['D3_edges'] for r in census)],
            'D9_vertices_range':[min(r['D9_vertices'] for r in census),max(r['D9_vertices'] for r in census)],
            'D9_edges_range':[min(r['D9_edges'] for r in census),max(r['D9_edges'] for r in census)],
            'census_sha256':hashlib.sha256(payload).hexdigest(),
            'producer_compared_entry_by_entry':producer is not None}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--producer',type=Path)
    args = p.parse_args()
    print(json.dumps(audit(args.producer),indent=2))


if __name__ == '__main__':
    main()
