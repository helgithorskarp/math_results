"""Late comparison: no original executable is imported."""
from itertools import combinations,product
from collections import Counter
from math import comb
from pathlib import Path
import json,hashlib

def require(ok,msg):
    if not ok:raise ValueError(msg)

def compare(D,original):
    domain=[];attempted=0
    pools={s:[sum(1<<x for x in c) for c in combinations(range(6),s)] for s in [3,4]}
    for d in D:
        if any(l not in [0,1] for l in d['lows']):continue
        for s0,s1 in product(pools[3]+pools[4],repeat=2):
            lows=d['lows']+[4-s0.bit_count(),4-s1.bit_count()]
            if sum(lows)>3:continue
            attempted+=1
            r=d['red_rows'][:]+[0,0]
            def edge(i,j):r[i]|=1<<j;r[j]|=1<<i
            for s,bits,ts in [(14,s0,[11,13]),(15,s1,[11,12])]:
                for j in [1,2]+ts:edge(s,j)
                for x in range(6):
                    if bits&(1<<x):edge(s,3+x)
            deg=d['degrees']+[10-lows[3],10-lows[4]]
            q=[dd-a.bit_count() for dd,a in zip(deg,r)]
            beta=[q[x]-3 for x in range(3,9)]
            if any(b<0 or b>2 for b in beta) or sum(beta)!=1+sum(lows):continue
            require(q[:3]==[0,6,0] and q[9:]==[4,4,2,3,3,2,2],'original physical outside ranks')
            okay=True;universe=(1<<16)-1
            for i,j in combinations(range(16),2):
                if r[i]&(1<<j):
                    lower=(r[i]&r[j]).bit_count()+max(0,q[i]+q[j]-6)
                    cap=3
                else:
                    lower=((universe^r[i]^(1<<i))&(universe^r[j]^(1<<j))).bit_count()+max(0,6-q[i]-q[j])
                    cap=6
                if lower>cap:okay=False;break
            if okay:domain.append([lows,d['columns']+[6,6],s0,s1,beta])
    domain.sort();require(domain==original['X_domain'],'all original208 entries')
    flags=[list(w) for w in product([0,1],repeat=5) if sum(w)<=3]
    counts=Counter(tuple(row[0]) for row in domain)
    coverage=[{'low_T0_T1_T2_SY0_SY1':l,'ordinary_Y_low_count':3-sum(l),
               'labeled_ordinary_Y_choices':comb(6,3-sum(l)),'X_interfaces':counts[tuple(l)]} for l in flags]
    require(coverage==original['tag_coverage'],'all26 coverage entries')
    require(sum(c['labeled_ordinary_Y_choices'] for c in coverage)==165,'all165 low placements')
    union=0
    for l,c,_,_,_ in domain:
        rows=[{x for x in range(6) if c[x]&(1<<t)} for t in [1,2]]
        p=[[len(W&s) for s in [{3,5},{2,4}]] for W in rows]
        union+=any(min(v)>0 for v in p)
    require(union==112 and len(domain)-union==96,'original ordinary finish partition')
    require(all(d[0][0]==1 for d in domain),'original T0 actual tag')
    require(original['flag_words']==26 and original['labeled_actual_low_placements']==165
            and original['X_interface_count']==208 and original['every_X_interface_has_T0_degree9'] is True,'original scope fields')
    require(original['finish']=={'union_obstruction':112,'two_T_three_sets_obstruction':96,
       'labeled_SX_Y_frames':18720,'compatible_T_Y_row_pairs':0},'original finish fields')
    sha=hashlib.sha256(json.dumps(domain,separators=(',',':')).encode()).hexdigest()
    require(sha==original['X_domain_sha256'],'complete original domain digest')
    return {'original_rows':len(domain),'all_original_rows_and_26_tag_records_equal':True,
        'original_domain_sha256':sha,'labeled_low_placements':165,'original_union_obstruction':union,
        'original_two_T_obstruction':len(domain)-union,'late_SY_candidates':attempted,
        'original_executable_imported':False}
