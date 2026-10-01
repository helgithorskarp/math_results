"""Complete cyclic13 middle cohort: independent counts and direct full Z checks.

The MITM generator supplies unique candidates. An independently built
tuple-orbit generating function counts the entire target set. Every
candidate is checked from actual triples, all pair degrees and all169
link intersections. Equal cardinality proves coverage. No large slack
matrices or full isomorphism census. Ordinary bridge in DEFECT_GRAM_CAP.md.
six-downset-2, researcher. Standard library; assertions enabled.
"""
import argparse
from collections import Counter,defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from cyclic13_gram import balanced_masks,blocks_from_mask
from defect_gram import scalar_data,compact_scalars,row_defect_data
from verify import rejects


def independent_signatures():
    remaining=set(combinations(range(13),3));groups=[]
    while remaining:
        a=min(remaining)
        orbit={tuple(sorted((x+j)%13 for x in a))for j in range(13)}
        assert len(orbit)==13 and orbit<=remaining
        remaining-=orbit;groups.append(orbit)
    assert len(groups)==22
    signatures=[]
    for o in groups:
        degree=Counter(p for a in o for p in combinations(a,2))
        sig=tuple(degree[0,j]for j in range(1,7));assert sum(sig)==3
        for p in combinations(range(13),2):
            d=p[1]-p[0];assert degree[p]==sig[min(d,13-d)-1]
        signatures.append(sig)
    return signatures


def independent_count(lam,signatures):
    coefficient={(0,)*6:1};largest=1
    for sig in signatures:
        new=coefficient.copy()
        for v,c in coefficient.items():
            target=tuple(v[i]+sig[i]for i in range(6))
            if max(target)<=lam:new[target]=new.get(target,0)+c
        coefficient=new;largest=max(largest,len(coefficient))
    return coefficient.get((lam,)*6,0),largest


def direct_defect(lam,blocks):
    assert len(blocks)==len(set(blocks))==26*lam
    links=[set()for _ in range(13)];degree=Counter()
    for a in blocks:
        assert type(a)is int and 0<a<1<<13 and a.bit_count()==3
        pts=[x for x in range(13)if a>>x&1]
        degree.update(combinations(pts,2))
        for x in pts:links[x].add(a^(1<<x))
    assert len(degree)==78 and set(degree.values())=={lam}
    assert all(len(link)==6*lam for link in links)
    u=lam*(lam-1)//2
    Z=[[0 if x==y else len(links[x]&links[y])-u for y in range(13)]for x in range(13)]
    assert all(sum(row)==0 for row in Z)
    rows=[sum(map(abs,row))for row in Z]
    assert len(set(rows))==1  # Verified literal cyclic regularity, not assumed for general designs.
    assert all(Z[x][y]==Z[(x+1)%13][(y+1)%13]for x in range(13)for y in range(13))
    return max(rows),Z


def run():
    orbit,sig,families=balanced_masks();independent=independent_signatures()
    out={'agent':'six-downset-2','role':'researcher','v':13,
        'triple_orbits':22,'triple_partition_size':286,'pair_orbits':6,
        'left_subsets':2048,'right_subsets':2048,'complete_simple_cyclic_subset_space':4194304,
        'cohorts':{},'direct_full_Schur_forms':0,
        'trust_boundary':'Exact full cohort counts and all point defects. Whole cap follows the complete ordinary Gram/mode criterion; no full isomorphism census or dense slack elimination.'}
    transcript=sha256();total=0
    for lam in (4,5,6):
        count,states=independent_count(lam,independent)
        assert len(families[lam])==len(set(families[lam]))==count
        histogram=Counter();maximum=-1;first_max=None
        for a in families[lam]:
            blocks=blocks_from_mask(a,orbit)
            actual,Z=direct_defect(lam,blocks)
            assert actual<=28
            histogram[actual]+=1
            if actual>maximum:maximum=actual;first_max=a
            transcript.update(f'{lam}:{a}:{actual}\n'.encode())
        assert maximum==28
        data=scalar_data(13,lam,28);assert data['whole_interval_sufficient']
        total+=count
        out['cohorts'][str(lam)]={'labelled_fixed_shift_designs':count,
            'independent_DP_max_states':states,'maximum_defect_absolute_row':maximum,
            'gamma_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'first_max_gamma_mask':first_max,'N':data['N'],'s':data['s'],
            'conditional_scalars':compact_scalars(data)}
    assert total==3372
    out['complete_designs_checked']=total
    out['direct_defect_entries_checked']=169*total
    out['direct_link_intersections_checked']=156*total
    out['all_design_pair_degrees_checked']=78*total
    out['cohort_transcript_sha256']=transcript.hexdigest()
    lam=4;a=out['cohorts']['4']['first_max_gamma_mask'];blocks=blocks_from_mask(a,orbit)
    row_defect_data(13,lam,blocks,28)
    rejects(lambda:row_defect_data(13,lam,blocks,27))
    rejects(lambda:row_defect_data(13,lam,blocks[:-1],28))
    rejects(lambda:row_defect_data(13,lam,blocks+[blocks[0]],28))
    rejects(lambda:direct_defect(lam,blocks[:-1]))
    rejects(lambda:scalar_data(6,2,28))
    rejects(lambda:scalar_data(13,1,28))
    rejects(lambda:scalar_data(13,4,-1))
    out['rejection_controls']=7
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    parser.add_argument('--write-expected',action='store_true');args=parser.parse_args()
    assert not(args.check and args.write_expected)
    out=run();expected=Path(__file__).with_name('defect_gram_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
