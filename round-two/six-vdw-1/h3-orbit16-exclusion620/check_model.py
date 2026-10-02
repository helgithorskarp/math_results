"""Separate ratio-coset/CRT/raw-row audit and whole first/second AP definition."""
import argparse
import json
from math import gcd
from pathlib import Path

SCOPE='Chosen multiplicative subgroup field invariance; arbitrary antipodal phase rows; all actual cyclic regular APs; poles absent.'


def require(ok,message):
    if not ok:raise ValueError(message)


def audit(d,target=False):
    keys={'author','role','model_kind','field_prime','row_half','AP_length','period','subgroup','cosets',
          'fixed_first_coset_row','palette','variables','free_point_inputs_before_AP','point_literals',
          'membership_clauses','fixed_row_clauses','palette_clauses','distinct_AP_clauses','clauses','scope'}
    require(type(d) is dict and set(d)==keys,'exact schema; no hidden constraints or old decoder')
    require((d['author'],d['role'],d['model_kind'])==('six-vdw-1','researcher','arbitrary_subgroup_antipodal_regular'),'actual attribution/domain')
    for key in ['field_prime','row_half','AP_length','period','variables','free_point_inputs_before_AP','distinct_AP_clauses']:
        require(type(d[key]) is int,'exact integer '+key)
    q,m,k=d['field_prime'],d['row_half'],d['AP_length'];H=d['subgroup'];fixed=d['fixed_first_coset_row']
    require(3<=q<=31 and 1<=m<=10 and 2<=k<=7 and all(q%i for i in range(2,q)) and gcd(q,2*m)==1,'prime/CRT/AP domains')
    require(type(H) is list and H and all(type(h) is int and 1<=h<q for h in H) and H==sorted(set(H)) and 1 in H and all(a*b%q in H for a in H for b in H),'actual multiplicative group')
    require(type(d['palette']) is bool and(fixed is None or(type(fixed) is int and 0<=fixed<2**m and not d['palette'])),'fixed-row/palette domains')
    classes=sorted({tuple(s for s in range(1,q) if s*pow(r,-1,q)%q in H) for r in range(1,q)},key=lambda c:c[0])
    require(sum(map(len,classes))==q-1 and all(len(c)==len(H) for c in classes),'complete disjoint ratio-class inventory')
    require(type(d['cosets']) is list and all(type(c) is list and all(type(r) is int for r in c) for c in d['cosets']) and d['cosets']==[list(c) for c in classes],'entire actual coset identities/order')
    n,nv=2*q*m,m*len(classes)
    require((d['period'],d['variables'],d['free_point_inputs_before_AP'])==(n,nv,nv-(m if fixed is not None else int(d['palette']))),'full original input freedom')
    if target:require((q,m,k,H,fixed,d['palette'],nv)==(31,10,7,[1,5,25],16,False,100),'production firstcoset16 H3 target')
    require(d['scope']==SCOPE and d['membership_clauses']==[],'declared arbitrary-coset regular-only domain')
    literal=[None]*n;identities=0
    for r in range(1,q):
        g=next(i for i,c in enumerate(classes) if r in c)
        for s in range(2*m):
            x=next(x for x in range(r,n,q) if x%(2*m)==s)
            var=m*g+s%m+1;literal[x]=var if s<m else -var
            for raw in range(2**m):
                original=((raw//2**(s%m))%2+s//m)%2
                encoded=((raw//2**((abs(literal[x])-1)%m))%2+int(literal[x]<0))%2
                require(original==encoded,'ALL original absolute row/actual point truths')
                identities+=1
    require(type(d['point_literals']) is list and len(d['point_literals'])==n and all(v is None or(type(v) is int and 0<abs(v)<=nv) for v in d['point_literals']) and d['point_literals']==literal,'whole independent physical point table')
    appearance={v:[0,0] for v in range(1,nv+1)};anti=group=0
    for x,v in enumerate(literal):
        if v is None:continue
        appearance[abs(v)][int(v<0)]+=1
        require(literal[(x+n//2)%n]==-v,'actual antipodal literal identity');anti+=1
        for h in H:
            y=next(y for y in range(n) if y%q==(x%q)*h%q and y%(2*m)==x%(2*m))
            require(literal[y]==v,'actual subgroup field/phase literal identity');group+=1
    require(all(c==[len(H),len(H)] for c in appearance.values()),'all independent inputs have only chosen H identification')
    fixed_units=[] if fixed is None else [[j+1 if (fixed//2**j)%2 else -(j+1)] for j in range(m)]
    palette_units=[[-1]] if d['palette'] else []
    for key,expected in [('fixed_row_clauses',fixed_units),('palette_clauses',palette_units)]:
        require(type(d[key]) is list and all(type(c) is list and all(type(v) is int for v in c) for c in d[key]) and d[key]==expected,'complete '+key)
    accepted=0
    if fixed is not None:
        for raw in range(2**m):
            holds=all(((raw//2**(abs(c[0])-1))%2)==int(c[0]>0) for c in fixed_units)
            require(holds==(raw==fixed),'full original first-coset row cylinder');accepted+=holds
    AP=set();visited=regular=poles=taut=0
    for a in range(n):
        for b in range(n):
            if a==b:continue
            pos=[(a+j*(b-a))%n for j in range(k)];visited+=1
            if any(x%q==0 for x in pos):poles+=1;continue
            regular+=1;support={literal[x] for x in pos}
            if any(-v in support for v in support):taut+=1;continue
            AP.add(tuple(sorted(support,key=lambda v:(abs(v),v))))
            AP.add(tuple(sorted((-v for v in support),key=lambda v:(abs(v),v))))
    require(d['distinct_AP_clauses']==len(AP),'complete physical AP clause dimension')
    expected=AP|{tuple(c) for c in fixed_units+palette_units}
    actual=d['clauses']
    require(type(actual) is list and all(type(c) is list and c and all(type(v) is int and 0<abs(v)<=nv for v in c) for c in actual),'exact clause types/domains')
    require(actual==[list(c) for c in sorted(expected)] and len(actual)==len({tuple(c) for c in actual}),'entire ordered canonical actual AP/unit clause set')
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_ARBITRARY_H3_ROW16_MODEL_AUDIT' if target else 'COMPLETE_GENERIC_SUBGROUP_MODEL_AUDIT',
            'variables':nv,'free_point_inputs_before_AP':d['free_point_inputs_before_AP'],'cosets':len(classes),'subgroup_order':len(H),
            'clauses':len(actual),'distinct_AP_clauses':len(AP),'fixed_row_units':len(fixed_units),'palette_units':len(palette_units),'membership_clauses':0,
            'all_cyclic_pairs':visited,'regular_pairs':regular,'pole_touching_pairs':poles,'tautological_regular_pairs':taut,
            'all_raw_row_inputs':2**m,'raw_row_point_truths':identities,'actual_antipodal_literal_identities':anti,'actual_subgroup_literal_identities':group,
            'independent_coset_point_inputs':nv,'input_positive_negative_occurrences':[len(H),len(H)],
            'first_row_truth_inputs':2**m if fixed is not None else 0,'first_row_accepted_masks':accepted,
            'scope':'Exact full chosen-subgroup definition equivalence only; no coloring/refutation/W bound.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);a=p.parse_args();d=json.loads(a.model.read_text())
    result=audit(d,True)
    expected=(f"p cnf {d['variables']} {len(d['clauses'])}\n"+''.join(' '.join(map(str,c))+' 0\n' for c in d['clauses'])).encode()
    require(a.model.with_suffix('.cnf').read_bytes()==expected,'entire production DIMACS bytes')
    print(json.dumps(result,sort_keys=True),flush=True)
