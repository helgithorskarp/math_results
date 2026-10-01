"""Complete exact single-switch neighbourhoods of three specified seeds.

Tuple link intersections and pair degrees independently check every output
and every point-defect entry. All 2002 distinct neighbours have unequal
point row invariants, excluding any thirteen-cycle automorphism. This is
not an isomorphism census or an enumeration of the full theorem's closure.
six-downset-2, researcher. Standard library; assertions enabled.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from cyclic13_gram import orbit_partition,blocks_from_mask
from pasch_defect import all_trades,switch_update


def literal_defect(v,lam,blocks):
    tuples=[tuple(x for x in range(v)if a>>x&1)for a in blocks]
    assert len(tuples)==len(set(tuples)) and all(len(a)==3 for a in tuples)
    pairs=Counter(p for a in tuples for p in combinations(a,2))
    assert len(pairs)==v*(v-1)//2 and set(pairs.values())=={lam}
    links=[{tuple(y for y in a if y!=x)for a in tuples if x in a}for x in range(v)]
    assert all(len(z)==lam*(v-1)//2 for z in links)
    u=lam*(lam-1)//2
    return [[0 if x==y else len(links[x]&links[y])-u for y in range(v)]for x in range(v)]


def run():
    v=13;trades=all_trades(v);orbit,_=orbit_partition()
    # Verify both sides' complete tuple pair degrees for every generated trade.
    for groups,even,odd in trades:
        counts=[]
        for side in (even,odd):
            tuples=[tuple(x for x in range(v)if a>>x&1)for a in side]
            degree=Counter(p for a in tuples for p in combinations(a,2))
            assert len(degree)==12 and set(degree.values())=={1};counts.append(degree)
        assert counts[0]==counts[1]
    out={'agent':'six-downset-2','role':'researcher','v':v,'all_underlying_trades':len(trades),
        'labelled_six_point_supports':1716,'matchings_per_support':15,
        'all_trade_pair_degrees_checked':2*12*len(trades),'inputs':[]}
    all_entries=0;all_pairs=0;all_neighbours=0
    for lam,mask,required in ((4,23768,572),(5,40920,650),(6,106488,780)):
        blocks=blocks_from_mask(mask,orbit);U=set(blocks);old=literal_defect(v,lam,blocks)
        row_hist=Counter();delta_hist=Counter();signature_hist=Counter();seen=set();transcript=sha256()
        for groups,even,odd in trades:
            if even<=U and odd.isdisjoint(U):reverse=False
            elif odd<=U and even.isdisjoint(U):reverse=True
            else:continue
            changed=sorted((U-(odd if reverse else even))|(even if reverse else odd))
            independent=literal_defect(v,lam,changed)
            new,Z,Delta,info=switch_update(v,lam,blocks,groups,reverse)
            assert new==changed and Z==independent
            assert all(Delta[x][y]==independent[x][y]-old[x][y]for x in range(v)for y in range(v))
            assert all(sum(row)==0 for row in independent)
            actual=max(sum(map(abs,row))for row in independent)
            delta=max(sum(map(abs,row))for row in Delta)
            signatures=len({tuple(sorted(row))for row in independent})
            assert signatures>1,'A claimed nontransitive witness had constant point invariants'
            assert info['new_absolute_row']==actual and info['Delta_absolute_row']==delta
            assert info['new_point_row_signature_count']==signatures
            key=tuple(changed);assert key not in seen;seen.add(key)
            row_hist[actual]+=1;delta_hist[delta]+=1;signature_hist[signatures]+=1
            transcript.update(json.dumps(changed,separators=(',',':')).encode()+b'\n')
            all_entries+=v*v;all_pairs+=v*(v-1)//2
        assert len(seen)==required
        all_neighbours+=len(seen)
        out['inputs'].append({'lambda':lam,'base_orbit_mask':mask,
            'distinct_labelled_single_switch_neighbours':len(seen),
            'all_neighbours_have_no_thirteen_cycle_automorphism':True,
            'absolute_row_histogram':{str(k):z for k,z in sorted(row_hist.items())},
            'Delta_absolute_row_histogram':{str(k):z for k,z in sorted(delta_hist.items())},
            'distinct_point_row_signature_count_histogram':{str(k):z for k,z in sorted(signature_hist.items())},
            'all_neighbour_transcript_sha256':transcript.hexdigest()})
    assert all_neighbours==2002
    out.update({'total_distinct_labelled_neighbours_in_specified_cohorts':all_neighbours,
        'direct_new_design_pair_degrees_checked':all_pairs,'direct_new_defect_entries_checked':all_entries,
        'direct_link_intersections_checked':all_neighbours*v*(v-1),'direct_full_Schur_forms':0,
        'noncyclicity_reason':'Sorted point-defect row entries are invariant under design automorphisms; unequal row multisets exclude point transitivity and hence a thirteen-cycle.'})
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    expected=Path(__file__).with_name('pasch_neighbourhood_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'Expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
