"""Independent scalar/port, route-cover and unbounded-closure checks.

Author/executing agent: six-sorting-2, researcher. No generator or solver
is imported. Marker-port checking continues the cited7436 scalar checker.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent
PAIRS=tuple(itertools.combinations(range(9),2))
LOWER=[0,0,1,3,5,9,12,16,19,25,29,35]
INITIAL=(5,7,1,288,40,0,0,0,0)
FIELDS=['max5','max7','min1','high288','test40','q5','q8','union288_510','q0_capped2']


def scalar(values,word):
    values=list(values)
    for a,b in word:
        if values[a]>values[b]: values[a],values[b]=values[b],values[a]
    return values


def mask(row): return sum(v<<i for i,v in enumerate(row))


def rows(f):
    selected=f['critical_single_bounds']+f['selected_mixed_bounds']+f['designated_bounds']
    return list({(r['x'],r['y']):r for r in selected}.values())


def witnesses(f):
    checks=rank_controls=0
    for w in rows(f):
        high,low=set(w['fixed_high']),set(w['fixed_low'])
        assert not high & low
        free=[i for i in range(11) if i not in high|low]
        assert len(free)==w['middle_count']
        assert w['cap']==35-LOWER[len(free)]-w['deleted']
        assignments=list(itertools.product((0,1),repeat=len(free)))
        assignments += [tuple(range(len(free))),tuple(reversed(range(len(free))))]
        for assignment in assignments:
            values=[100 if i in high else -100 if i in low else assignment[free.index(i)] for i in range(11)]
            colors=[2 if i in high else 0 if i in low else 1 for i in range(11)]
            ports=[None if i in high|low else free.index(i) for i in range(11)]
            retained=[];deleted=0
            for section_index,section in enumerate((f['prefix'],f['after'])):
                for a,b in section:
                    outside=colors[a]!=1 or colors[b]!=1
                    deleted+=outside
                    if not outside: retained.append((ports[a],ports[b]))
                    if colors[a]>colors[b]:
                        colors[a],colors[b]=colors[b],colors[a]
                        ports[a],ports[b]=ports[b],ports[a]
                    if values[a]>values[b]: values[a],values[b]=values[b],values[a]
                if section_index==0:
                    order=f['prefix_output_order']
                    values=[values[i] for i in order]
                    colors=[colors[i] for i in order]
                    ports=[ports[i] for i in order]
            assert deleted==w['deleted']
            assert mask([int(v==2) for v in colors[1:10]])==w['x']
            assert mask([int(v!=0) for v in colors[1:10]])==w['y']
            replay=scalar(assignment,retained)
            assert [replay[p] for p in ports if p is not None]==[v for v in values if -100<v<100]
            checks+=1
        rank_controls+=2
    return dict(witnesses=len(rows(f)),assignments=checks,distinct_rank_controls=rank_controls)


def transition(s,pair):
    p5,p7,pmin,high,test,q5,q8,union,q0=s
    values=[[int(i==p5) for i in range(9)],[int(i==p7) for i in range(9)],
            [int(i!=pmin) for i in range(9)],[(high>>i)&1 for i in range(9)],
            [(test>>i)&1 for i in range(9)]]
    low=[int(i!=0) for i in range(9)];a,b=pair
    q5+=bool(values[0][a] or values[0][b]);q8+=8 in pair
    union+=bool(values[3][a] or values[3][b] or not(low[a] and low[b]))
    q0=min(2,q0+int(not(low[a] and low[b])))
    if q5>2 or q8>1 or union>4: return None
    assert scalar(low,[pair])==low
    out=[scalar(v,[pair]) for v in values]
    return(out[0].index(1),out[1].index(1),out[2].index(0),mask(out[3]),mask(out[4]),q5,q8,union,q0)


def closure(cert):
    assert cert['fields']==FIELDS and cert['wires']==9 and tuple(cert['initial'])==INITIAL
    assert cert['bounds']==dict(q5=2,q8=1,union288_510=4)
    assert cert['excluded']==dict(max5=8,max7=8,min1=0,high288=384,test40=384,q0_capped2=2)
    states={tuple(s) for s in cert['states']}
    assert len(states)==len(cert['states']) and INITIAL in states
    allowed=0
    for s in states:
        assert len(s)==9 and all(type(v) is int for v in s)
        p5,p7,pmin,high,test,q5,q8,union,q0=s
        assert 5<=p5<=8 and p7 in (7,8) and pmin in (0,1)
        assert high in (288,320,384) and 0<=test<512 and test.bit_count()==2
        assert 0<=q5<=2 and 0<=q8<=1 and 0<=union<=4 and q0 in (0,1,2)
        assert (p5,p7,pmin,high,test,q0)!=(8,8,0,384,384,2)
        for pair in PAIRS:
            nxt=transition(s,pair)
            if nxt is not None:
                allowed+=1;assert nxt in states,('Missing successor',s,pair,nxt)
    return dict(states=len(states),transitions=36*len(states),allowed=allowed)


def kernel_cover(expected):
    # Written route-cost summation proves at most three pre-root events.
    # The checker independently tests every pair word of lengths two/three,
    # using scalar rows rather than the generator's memoized positions.
    wires=(1,2,3,4,6,7);pairs=tuple(itertools.combinations(wires,2))
    accepted=[];attempted=0
    for length in (2,3):
        for word in itertools.product(pairs,repeat=length):
            attempted+=1
            tracks=[[int(i==p) for i in range(9)] for p in (3,4,7)]
            costs=[0,0,0];valid=True
            for a,b in word:
                occupied={v.index(1) for v in tracks}
                if not occupied & {a,b}: valid=False;break
                for i,row in enumerate(tracks):
                    costs[i]+=bool(row[a] or row[b]);tracks[i]=scalar(row,[(a,b)])
                if max(costs)>2:valid=False;break
            if valid and all(row.index(1)==7 for row in tracks):accepted.append(word)
    assert Counter(map(len,accepted))=={2:3,3:21}
    full=[w+((5,7),(7,8)) for w in accepted if len(w)==3]
    assert len(full)==len(set(full))==21
    assert set(full)=={tuple(map(tuple,w)) for w in expected}
    for word in full:
        tracks=[[int(i==p) for i in range(9)] for p in (3,4,5,7,8)]
        costs=[0]*5;unary=binary=0
        for a,b in word:
            occupied={v.index(1) for v in tracks}
            binary+=a in occupied and b in occupied
            unary+=(a in occupied)!=(b in occupied)
            for i,row in enumerate(tracks):
                costs[i]+=bool(row[a] or row[b]);tracks[i]=scalar(row,[(a,b)])
        assert binary==4 and unary==1 and costs==[4,4,2,4,1]
        assert all(row.index(1)==8 for row in tracks)
    return dict(all_pair_words_tested=attempted,binary_candidates=3,unary_candidates=21,
                exact_full_passages=[4,4,2,4,1])


def main():
    if not __debug__:raise RuntimeError('Run without -O')
    start=time.monotonic();f=json.loads((HERE/'fixture.json').read_text())
    assert f['lower_sizes']==LOWER and f['full_budget']==35
    assert f['full_prefix_size']==19 and f['reference_suffix_budget']==16
    assert len(f['prefix'])==14 and f['after']==f['K_after']+f['pure_minimum']
    assert f['pure_minimum']==[[0,5],[0,1]]
    caps={(w['x'],w['y']):w['cap'] for w in rows(f)}
    assert [caps[1<<i,511] for i in (3,4,5,7,8)]==[4,4,2,4,1]
    assert caps[288,510]==4
    K=set();L=set()
    for state in range(2048):
        values=[(state>>i)&1 for i in range(11)]
        out=scalar(values,f['prefix']);out=[out[i] for i in f['prefix_output_order']]
        k=scalar(out,f['K_after']);K.add(mask(k[:10]));assert k[10]==max(values)
        assert scalar(k[:10],f['K_control20'])+[k[10]]==sorted(values)
        ell=scalar(out,f['after']);L.add(mask(ell[1:10]))
        assert ell[0]==min(values) and ell[10]==max(values)
        assert [ell[0]]+scalar(ell[1:10],f['control18'])+[ell[10]]==sorted(values)
    assert K==set(f['K_states']) and len(K)==127
    assert L==set(f['states']) and len(L)==109
    assert {i for i in range(9) if 1<<i in L}=={3,4,5,7,8}
    assert all(x==0 or any((x>>i)&1 for i in (3,4,5,7,8)) for x in L)
    assert {288,510,509,40}<=L
    certpath=HERE/'min0-closure.json'
    assert hashlib.sha256(certpath.read_bytes()).hexdigest()==f['min0_certificate']['sha256']
    cert=json.loads(certpath.read_text());closed=closure(cert)
    assert closed=={k:f['min0_certificate'][k] for k in ('states','transitions','allowed')}
    bad=dict(cert);bad['states']=cert['states'][:-1]
    negative=0
    for trial in (bad,dict(cert,states=cert['states']+[[8,8,0,384,384,2,1,4,2]])):
        try:closure(trial)
        except AssertionError:negative+=1
        else:raise AssertionError('Corrupt closure accepted')
    coverage=kernel_cover(f['maximum_kernel_words'])
    images=[]
    for word in f['maximum_kernel_words']:
        target=set()
        for state in L:
            row=scalar([(state>>i)&1 for i in range(9)],word)
            assert row[8]==int(state!=0)
            target.add(mask(row[:8]))
        images.append(len(target))
    result=dict(agent='six-sorting-2',role='researcher',status='INDEPENDENT_STRUCTURE_VERIFIED',
                original_inputs=2048,checked_original_controls=4096,K_states=127,L_states=109,
                marker_audit=witnesses(f),sole0_closure=closed,closure_negative_controls=negative,
                maximum_cover=coverage,literal_front_images=images,
                literal_front_row_executions=21*109,seconds=time.monotonic()-start,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                scope='Written pruning/commutation and imported small-size bounds remain dependencies; not external review')
    print(json.dumps(result))


if __name__=='__main__':main()
