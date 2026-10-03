"""Independent Gaussian enumeration of all three older completion polytopes."""
import json,itertools,hashlib,sys
from fractions import Fraction as F
from algebra import A,T,dot,solve,determinant,sign
from normals import references

def setup():
    d,root,p,alt,q=references();n=[A(v) for v in d['cap_center']];b=F(667,250)
    dep=solve([[p[j][i] for j in (0,1,2)] for i in range(3)],[-x for x in p[5]])
    if any(sign(x,root)!=1 for x in dep):raise ValueError('positive spanning dependence')
    if any(sum((dep[j]*p[k][i] for j,k in enumerate((0,1,2))),A())+p[5][i] for i in range(3)):raise ValueError('whole origin dependence')
    nn=dot(n,n)
    if not sign(nn-b*b,root)==1 or sign(2*b*b-(1+F(593,1000))*nn-F(9,1000),root)!=1:raise ValueError('strict open cap capacity')
    if sign(dot(p[13],q)-F(97,100),root)!=1:raise ValueError('incompatible two unit choices')
    for group in ([p[3],p[13],q],[p[14],alt]):
        for u,v in itertools.combinations(group,2):
            if sign(dot([a-b for a,b in zip(u,v)],[a-b for a,b in zip(u,v)])-F(1,25),root)!=1:raise ValueError('all squared separations')
    return d,root,p,alt,q,n,b,dep

def enumerate_poly(kind):
    d,root,p,alt,q,n,b,dep=setup();labels=d['core_labels']
    if labels!=[0,1,2,4,5,6,7,8,9,10,11,12]:raise ValueError('literal twelve core coverage')
    ns=[p[i] for i in labels];rhs=[T]*12
    if kind=='K':ns+=[n];rhs+=[A(b)];units=[('p3',p[3]),('p13',p[13]),('q',q)];short=F(99,100)
    elif kind in ('p13','q'):ns+=[p[3],p[13] if kind=='p13' else q];rhs+=[T,T];units=[('p14',p[14]),('c14',alt)];short=F(3,4)
    else:raise ValueError('literal target')
    rows=[[(1-T)*v[i]+T*sum(v,A()) for i in range(3)] for v in ns]
    records=[];counts={k:0 for k in ('singular','infeasible','short','unit')};found=set()
    for ordinal,triple in enumerate(itertools.combinations(range(len(ns)),3)):
        mat=[rows[i] for i in triple];det=determinant(mat);rec=dict(ordinal=ordinal,triple=list(triple))
        if not det:rec['kind']='singular'
        else:
            v=solve(mat,[rhs[i] for i in triple]);bad=next((i for i,(r,h) in enumerate(zip(rows,rhs)) if sign(sum((x*y for x,y in zip(r,v)),A())-h,root)>0),None)
            if bad is not None:rec.update(kind='infeasible',violated_plane=bad)
            else:
                norm=dot(v,v)
                if sign(short-norm,root)==1:rec.update(kind='short',norm_squared=norm.encode())
                else:
                    match=next((name for name,u in units if u==v),None)
                    if match is None or norm!=1:raise ValueError('unclassified feasible norm')
                    rec.update(kind='unit',name=match);found.add(match)
        counts[rec['kind']]+=1;records.append(rec)
    if found!={name for name,u in units}:raise ValueError('entire advertised unit section')
    return dict(kind=kind,triples=len(records),census=counts,all_ordinals=list(range(len(records))),records=records,positive_dependence=[x.encode() for x in dep])

def maps():
    d,root,p,alt,q,n,b,dep=setup();cyc=[v[:] for v in p]
    r=2*T/(1+T)
    for label,i,j,o in [(12,5,7,0),(13,11,9,5)]:cyc[label]=[r*(a+c)-e for a,c,e in zip(cyc[i],cyc[j],cyc[o])]
    common_cyclic=[v[:] for v in p];common_cyclic[14]=alt
    records=[];gram_count=pair_count=0
    for case in d['candidate_gram_permutations']:
        a,last=case['case'];actual=[v[:] for v in p];actual[13]=p[13] if a=='p13' else q;actual[14]=p[14] if last=='p14' else alt
        for i,j in itertools.combinations(range(15),2):
            if sign(dot(actual[i],actual[j])-T,root)>0:raise ValueError('all completion packing pairs')
            pair_count+=1
        match=case['heuristic_matches'][0];perm=match['permutation'];reference=p if match['reference']=='asymmetric' else common_cyclic
        if sorted(perm)!=list(range(15)):raise ValueError('whole Gram relabeling permutation')
        for i in range(15):
            for j in range(15):
                if dot(actual[i],actual[j])!=dot(reference[perm[i]],reference[perm[j]]):raise ValueError('entire completion Gram')
                gram_count+=1
        records.append(dict(case=[a,last],reference=match['reference'],permutation=perm))
    perm=d['known_cyclic_permutation']
    if sorted(perm)!=list(range(15)):raise ValueError('canonical cyclic permutation')
    for i in range(15):
        for j in range(15):
            if dot(common_cyclic[i],common_cyclic[j])!=dot(cyc[perm[i]],cyc[perm[j]]):raise ValueError('canonical cyclic full Gram')
            gram_count+=1
    if not F(2100000,10**8)==F(21,1000) or F(2003,10**7)>F(1,1000):raise ValueError('coarse input radius')
    return dict(completions=records,all_pair_bounds=pair_count,all_Gram_positions=gram_count,heuristic_float_fields_used=False)
if __name__=='__main__':print(json.dumps(maps() if sys.argv[1]=='maps' else enumerate_poly(sys.argv[1]),sort_keys=True))
