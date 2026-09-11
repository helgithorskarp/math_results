"""Standard-library exact checks. SAT proof checking is a separate step."""
from collections import Counter
from itertools import combinations_with_replacement
from pathlib import Path
import argparse, hashlib, json
from model import *

def verify():
    assert len(P)==156 and len(LINES)==806 and len(PLANES)==156
    assert all(len(h)==31 for h in PLANES)
    through = [set(i for i,h in enumerate(PLANES) if p in h) for p in range(156)]
    assert all(len(h)==31 for h in through)
    assert all(len(through[i]&through[j])==6 for i in range(156) for j in range(i))
    # Complete parameter-specific parallel profiles.
    profiles72 = [p for p in combinations_with_replacement(range(8,17),5) if sum(p)==72]
    pair = lambda p:sum(x*(x-1)//2 for x in p)
    assert len(profiles72)==18
    assert all(2*pair(p)<=972+11*p.count(16) for p in profiles72)
    assert 2*15336-31*972==540 and (540+10)//11==50
    ordinary = [p for p in profiles72 if 12 not in p]
    special = [p for p in combinations_with_replacement(range(13,17),5) if sum(p)==77]
    assert max(map(pair,special))==558
    assert max(pair(p) for p in ordinary if min(p)>=13)==487
    assert max(map(pair,ordinary))==508
    assert 15768-6*558-25*487==245 and (245+20)//21==12
    assert 218-5*12==158
    assert [m for m in range(16,32) if m%5==3]==[18,23,28]
    assert 72+5*4>6*15 and 73+5*4>6*15 and 1+31*2<72
    assert 72+5*4>16+5*15
    assert 73+5*4>12+5*16
    b = base23()
    assert len(b)==31 and Counter(b)=={0:18,1:6,2:4,3:3}
    assert all(sum(b[i] for i in l)%5==3 for l in lines(3))
    A = arcs(); details = {}
    expected = {'E128':(80,40,20,16),'E143':(65,65,0,26),
                'L23':(90,30,20,16),'L28':(75,50,0,31)}
    for name,K in A.items():
        assert tuple(Counter(K)[i] for i in range(4))==expected[name]
        assert all(sum(K[i] for i in l)%5==3 for l in LINES)
        assert not any(all(K[i]>0 for i in h) for h in PLANES)
        if name.startswith('E'):
            assert not any(all(len({K[j] for j in l if j!=v})==1
                               for l in LINES if v in l)
                           for v in range(156) if K[v]==3)
        L,C = parameters(K)
        details[name]={'size':sum(K),'low_planes':L,'selected_weight':C}
    # With no multiplicity-two points, C=3u+w <= 2u+L.
    for name,need,bound in [('E143',14,6),('L28',12,11)]:
        K=A[name];L,C=parameters(K)
        assert 2 not in K and (C-L+1)//2==need
        counts = [sum(tuple(sorted(K[j] for j in l))==(0,0,0,0,0,3)
                      for l in LINES if q in l) for q in range(156) if K[q]==0]
        assert set(counts)=={bound} and need>bound
        details[name].update(zero_points=len(counts),required_8_planes=need,
                             available_A1_lines=bound)
    # All E128 flags, without automorphism reduction.
    K=A['E128'];hm=[sum(1<<i for i in h) for h in PLANES];checked=[]
    for q,f in flags(K):
        ss=slots(K,q,f);mx=[max(K[i] for i in s) for s in ss]
        assert len(ss)==18 and sum(mx)-parameters(K)[1]==1
        rows=tuple(reconstruction_rows(K,q,f));counts=[0,0]
        def visit(j,left,mask):
            if j==len(ss):
                if left:return
                counts[0]+=1
                if all((mask&hm[r]).bit_count() in allowed for r,allowed in rows):
                    counts[1]+=1
                return
            for i in ss[j]:
                loss=mx[j]-K[i]
                if loss<=left:visit(j+1,left-loss,mask|(1<<i))
        visit(0,1,0)
        assert counts==[297,0]
        checked.append([q,f,*counts])
    assert len(checked)==320
    details['E128'].update(flags=len(checked),candidates=95040,survivors=0,
                          flag_results_sha256=hashlib.sha256(json.dumps(checked,separators=(',',':')).encode()).hexdigest())
    matrices,orbits=lift23_cover(A['L23'])
    cover=[{'representative':o['representative'],'size':len(o['flags'])} for o in orbits]
    assert cover==[{'representative':[16,16],'size':30},
                   {'representative':[16,66],'size':120},
                   {'representative':[61,51],'size':120},
                   {'representative':[61,71],'size':120},
                   {'representative':[61,91],'size':60}]
    assert sum(o['size'] for o in cover)==len(flags(A['L23']))==450
    details['L23'].update(verified_symmetries=len(matrices),flags=450,orbits=cover)
    return {'status':'FINITE_REDUCTION_CHECKS_PASSED_SAT_CERTIFICATES_STILL_REQUIRED',
            'profiles72':[list(p) for p in profiles72],'minimum_16_planes':50,'minimum_16_planes_through_each_projective_point':2,'sparse_low_planes_minimum':12,
            'sparse_dual_size_maximum':158,'arcs':details}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);p.add_argument('--compare',type=Path)
    a=p.parse_args();result=verify()
    if a.compare:assert result==json.loads(a.compare.read_text())
    text=json.dumps(result,indent=2)+'\n'
    if a.out:a.out.write_text(text)
    print(text,end='')
