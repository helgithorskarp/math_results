"""Independent scalar-marker replay and exhaustive Boolean-trajectory DFS.

No generator, solver, or graph imports. See README.md for the analytic
reduction and the imported sorting-size theorem boundary.
"""
import functools
import hashlib
import itertools
import json
import resource
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def execute(values,network):
    values=list(values);deleted=[]
    for step,(a,b) in enumerate(network):
        if values[a] not in (0,1) or values[b] not in (0,1):
            deleted.append(step)
        if values[a]>values[b]:
            values[a],values[b]=values[b],values[a]
    return values,deleted


def verify_cut(prefix,order,row):
    high,low=row['fixed_maxima'],row['fixed_minima']
    assert not set(high)&set(low)
    assert len(set(high))==len(high) and len(set(low))==len(low)
    assert all(0<=i<11 for i in high+low)
    free=[i for i in range(11) if i not in high+low]
    assert sorted(row['output_order'])==list(range(len(free)))
    assert len(row['retained_network'])+len(row['deleted_steps'])==14
    assert all(0<=a<len(free) and 0<=b<len(free) and a!=b for a,b in row['retained_network'])
    for bits in range(1<<len(free)):
        values=[2 if i in high else -2 if i in low else 0 for i in range(11)]
        data=[bits>>i&1 for i in range(len(free))]
        for i,v in zip(free,data):values[i]=v
        direct,deleted=execute(values,prefix);logical=[direct[p] for p in order]
        assert deleted==row['deleted_steps']
        assert [i for i,v in enumerate(logical) if v==2]==row['maximum_holes']
        assert [i for i,v in enumerate(logical) if v==-2]==row['minimum_holes']
        replay,_=execute(data,row['retained_network'])
        assert [replay[p] for p in row['output_order']]==[v for v in logical if v in (0,1)]
    return 1<<len(free)


def all_kernel_words(side,positions,caps,opposite_wire,ordered_candidates):
    rows=tuple(tuple(int(i==p) if side=='maximum' else int(i!=p) for i in range(11)) for p in positions)
    target=(0,)*10+(1,) if side=='maximum' else (0,)+(1,)*10
    pairs=tuple(itertools.combinations(range(11),2))

    @functools.lru_cache(None)
    def walk(current,costs):
        if all(row==target for row in current):return frozenset({()})
        words=set()
        for a,b in pairs:
            if side=='maximum' and a==opposite_wire and any(current[positions.index(i)][b] for i in ordered_candidates):continue
            if side=='minimum' and b==opposite_wire and any(not current[positions.index(i)][a] for i in ordered_candidates):continue
            touched=[bool(row[a] or row[b]) if side=='maximum' else not(row[a] and row[b]) for row in current]
            if not any(touched):continue
            after_costs=tuple(q+t for q,t in zip(costs,touched))
            if any(q>cap for q,cap in zip(after_costs,caps)):continue
            after=[list(row) for row in current]
            for row in after:
                if row[a]>row[b]:row[a],row[b]=row[b],row[a]
            words.update(((a,b),)+tail for tail in walk(tuple(map(tuple,after)),after_costs))
        return frozenset(words)
    return walk(rows,(0,0,0))


def route_count(network,side,wire):
    values=[int(i==wire) if side=='maximum' else int(i!=wire) for i in range(11)]
    count=0
    for a,b in network:
        count+=bool(values[a] or values[b]) if side=='maximum' else not(values[a] and values[b])
        if values[a]>values[b]:values[a],values[b]=values[b],values[a]
    return count


def main():
    start=time.monotonic()
    f=json.loads((ROOT/'fixture.json').read_text())
    c=json.loads((ROOT/'certificate.json').read_text())
    assert c['schema']==1 and c['agent']=='six-sorting-2' and c['role']=='researcher'
    assert c['target']=='X/10' and c['known_lower_sizes']=={'9':25,'10':29,'11':35}
    assert (c['prefix_size'],c['completion_budget'],c['full_budget'])==(14,21,35)
    P,order,R=f['prefix'],f['prefix_output_order'],f['known_22_suffix']
    assert len(P)==14 and sorted(order)==list(range(11)) and len(R)==22
    assert all(0<=a<11 and 0<=b<11 and a!=b for a,b in P)
    assert all(0<=a<b<11 for a,b in R)
    assert len(f['original_prefix'])==21
    assert f['original_fixed_maxima']==[1,5] and f['original_output_holes']==[10,12]
    image=set()
    for bits in range(2048):
        values=[bits>>i&1 for i in range(11)]
        out,_=execute(values,P);logical=[out[p] for p in order]
        image.add(sum(v<<i for i,v in enumerate(logical)))
        complete,_=execute(logical,R)
        assert complete==sorted(values)
        original=[];next_free=iter(values)
        for i in range(13):original.append(2 if i in f['original_fixed_maxima'] else next(next_free))
        direct,deleted=execute(original,f['original_prefix'])
        assert len(deleted)==7 and [i for i,v in enumerate(direct) if v==2]==[10,12]
        assert logical==[v for v in direct if v!=2]
    assert sorted(image)==c['states'] and len(image)==136
    assert all(((1<<w)-1)<<(11-w) in image for w in range(12))
    maxima=sorted(x.bit_length()-1 for x in image if x.bit_count()==1)
    minima=sorted((2047^x).bit_length()-1 for x in image if x.bit_count()==10)
    assert maxima==[6,9,10] and minima==[0,1,5]
    assert all(x==0 or any(x>>i&1 for i in maxima) for x in image)
    assert all(x==2047 or any(not(x>>j&1) for j in minima) for x in image)
    ordered=[(i,j) for i,j in itertools.product(maxima,minima) if all((x>>j&1)<=(x>>i&1) for x in image)]
    assert ordered==[(6,0),(6,1),(9,1),(9,5),(10,0),(10,1)]
    assert list(map(list,ordered))==c['initially_ordered_max_min_pairs']
    marker_checks=0;singles=set()
    for row in c['single_extremum_bounds']:
        side,wire=row['polarity'],row['wire']
        assert (side,wire) not in singles;singles.add((side,wire))
        assert len(row['fixed_maxima'])==int(side=='maximum')
        assert len(row['fixed_minima'])==int(side=='minimum')
        assert row['maximum_holes']==([wire] if side=='maximum' else [])
        assert row['minimum_holes']==([wire] if side=='minimum' else [])
        cap=35-29-len(row['deleted_steps'])
        assert row['suffix_touch_cap']==cap==({6:3,9:3,10:3}[wire] if side=='maximum' else {0:4,1:3,5:5}[wire])
        marker_checks+=verify_cut(P,order,row)
        assert route_count(R,side,wire)<=cap+1
    assert singles=={('maximum',i) for i in maxima}|{('minimum',j) for j in minima}
    assert [(r['maximum_wire'],r['minimum_wire']) for r in c['mixed_bounds']]==list(itertools.product(maxima,minima))
    assert [r['suffix_union_cap'] for r in c['mixed_bounds']]==[5,4,6,5,4,7,5,4,6]
    bounds={}
    for row in c['mixed_bounds']:
        i,j=row['maximum_wire'],row['minimum_wire']
        assert len(row['fixed_maxima'])==len(row['fixed_minima'])==1
        assert row['maximum_holes']==[i] and row['minimum_holes']==[j]
        assert row['suffix_union_cap']==35-25-len(row['deleted_steps'])
        bounds[i,j]=row['suffix_union_cap']
        marker_checks+=verify_cut(P,order,row)
        _,deleted=execute([2 if k==i else -2 if k==j else 0 for k in range(11)],R)
        assert len(deleted)<=row['suffix_union_cap']+1
    assert c['derived_minimum_caps']=={'0':3,'1':2,'5':4}
    # Shared max/min gates are unary for each side. Replay a finite superset
    # of possible binary depths, costs and intersections independently.
    depths=((1,2,2),(2,1,2),(2,2,1));binary_cases=ordered_cases=0
    for d,e in itertools.product(depths,repeat=2):
        for q in itertools.product(*(range(x,4) for x in d)):
            for r in itertools.product(range(e[0],5),range(e[1],4),range(e[2],6)):
                possible=True
                for a,b in itertools.product(range(3),repeat=2):
                    intersection_cap=min(q[a]-d[a],r[b]-e[b])
                    if q[a]+r[b]-intersection_cap>bounds[maxima[a],minima[b]]:
                        possible=False;break
                if not possible:continue
                binary_cases+=1
                assert all(x<=y for x,y in zip(r,(3,2,4)))
                if any(q[maxima.index(i)]+r[minima.index(j)]>bounds[i,j] for i,j in ordered):continue
                ordered_cases+=1
                assert r[1]==1 or (r[1]==2 and max(q)<=2)
                if r[1]==1:assert e==(2,1,2)
    assert binary_cases and ordered_cases
    expected={'minimum_1608':('minimum',[0,5,1],[3,4,1],{'2':1,'3':23,'4':240,'5':1344},
                              {'polarity':'maximum','wire':10,'ordered_candidates':[0,1]}),
              'maximum_50':('maximum',[6,9,10],[2,2,2],{'2':3,'3':47,'4':0,'5':0},
                            {'polarity':'minimum','wire':0,'ordered_candidates':[6,10]})}
    cover_counts=[];seen=set()
    for cover in c['kernel_cover']:
        identifier=cover['id'];assert identifier in expected and identifier not in seen;seen.add(identifier)
        side,positions,caps,lengths,opposite=expected[identifier]
        assert (cover['polarity'],cover['initial_candidates'],cover['candidate_touch_caps'])==(side,positions,caps)
        assert cover['opposite_fixed_trajectory']==opposite
        words=all_kernel_words(side,positions,caps,opposite['wire'],opposite['ordered_candidates'])
        counts={str(k):sum(len(w)==k for w in words) for k in range(2,6)}
        assert counts==lengths==cover['counts_by_length']
        assert sum(counts.values())==len(words)==cover['words']
        data=(json.dumps(sorted(words),separators=(',',':'))+'\n').encode()
        assert hashlib.sha256(data).hexdigest()==cover['canonical_word_sha256']
        cover_counts.append(len(words))
    assert seen==set(expected) and c['tagged_cover_count']==sum(cover_counts)==1658
    print(json.dumps({'status':'verified','states':136,'original_alignment_inputs':2048,
                      'individual_bounds':6,'mixed_bounds':9,'marker_assignments':marker_checks,
                      'derived_minimum_caps':[3,2,4],'binary_cost_cases':binary_cases,
                      'ordered_cost_cases':ordered_cases,'kernel_words':cover_counts,
                      'tagged_cover_count':1658,'known_22_controls':1,
                      'seconds':time.monotonic()-start,
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__=='__main__':main()
