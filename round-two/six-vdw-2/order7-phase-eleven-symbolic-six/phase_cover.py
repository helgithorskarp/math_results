"""Literal tail enumeration versus independently reconstructed gap compositions."""
from itertools import combinations,product
import hashlib
import json
from math import comb
from pathlib import Path
import sys


def require(condition,message):
    if not condition:raise ValueError(message)


def main(output):
    require(not output.exists(),'fresh complete phase receipt required')
    literal={};examined=windows=gates=0
    for selected in combinations(range(7,43),5):
        examined+=1
        if any(v-u==1 for u,v in zip(selected,selected[1:])):continue
        m=[int(i<6 or i in selected) for i in range(44)]
        if any(len({m[(i+j)%44] for j in range(8)})==1 for i in range(44)):continue
        g=(selected[0]-6,)+tuple(v-u-1 for u,v in zip(selected,selected[1:]))+(43-selected[-1],)
        require(sum(g)==33 and min(g)>=1 and max(g)<=7 and g not in literal,'literal gap map fails')
        require(m[:6]==[1]*6 and m[6]==m[43]==0 and sum(m)==11
                and all(not(m[i] and m[(i+1)%44]) for i in range(5,44)),'literal six-run class fails')
        previous=[False]*7;previous[0]=True
        for j in range(1,37):
            current=[True]+[previous[t] or (bool(m[j+6]) and previous[t-1]) for t in range(1,7)]
            require(current==[True]+[sum(m[7:j+7])>=t for t in range(1,7)],'complete threshold recurrence fails')
            previous=current;gates+=6
        require(previous[5] and not previous[6],'exact-five extension fails')
        literal[g]=m;windows+=44
    composition={}
    for prefix in product(range(7),repeat=5):
        last=9-sum(prefix)
        if not 0<=last<=6:continue
        g=tuple(7-a for a in (*prefix,last));m=[]
        for length,gap in zip((6,1,1,1,1,1),g):m.extend([1]*length+[0]*gap)
        require(len(m)==44 and g not in composition,'composition phase reconstruction fails')
        composition[g]=m
    require(literal==composition and examined==comb(36,5)==376992
            and len(literal)==comb(14,5)-6*comb(7,5)==1876,'ENTIRE independent phase cover differs')
    words=[''.join(str(v^b) for v in m) for g,m in sorted(literal.items()) for b in (0,1)]
    stream=''.join(word+'\n' for word in words).encode()
    require(len(set(words))==3752 and hashlib.sha256(stream).hexdigest()
            =='559ca52972badb98b3498f103d184b8550a6f481cc6109801e28a340bab9ec00','whole two-background phase stream differs')
    cosets={}
    H={pow(3,88*j,617) for j in range(7)}
    require(len(H)==7 and len({pow(3,j,617) for j in range(616)})==616,'actual field subgroup/root differs')
    for i in range(88):
        for h in H:
            point=pow(3,i,617)*h%617;require(point not in cosets,'overlapping actual cosets');cosets[point]=i
    require(set(cosets)==set(range(1,617)) and all(cosets[-p%617]==(i+44)%88 for p,i in cosets.items()),'actual antipodal interface fails')
    scalar=0
    for shift in range(44):
        for point,i in cosets.items():
            require(cosets[point*pow(3,shift,617)%617]==(i+shift)%88,'actual scalar orientation transport fails');scalar+=1
    result=dict(agent='six-vdw-2',role='researcher',status='EXACT_ENTIRE_PHASE_AND_FUNCTIONAL_COUNT_COVER',
                literal_tail_subsets=examined,gap_vectors_per_background=1876,total_phase_heads=3752,
                phase_windows=windows,functional_threshold_cells=gates,actual_field_points=616,actual_cosets=88,
                actual_scalar_checks=scalar,phase_stream_sha256=hashlib.sha256(stream).hexdigest(),
                necessary_phase_patterns_are_colorings=False,mathematical_exclusion=False,
                ordinary_threshold_induction_unformalized=True)
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    require(len(sys.argv)==2,'provide new output file');main(Path(sys.argv[1]))
