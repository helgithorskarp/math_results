"""Exact three-addition completion of twelve fixed incumbent points.

Python3.11+, standard library. Fixed-root signs are rational enclosures;
no solver tolerance or floating selector runs in this verifier.
Actual author six-tammes-2, researcher. Ordinary proof remains unformalized.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
from fractions import Fraction as Q
import argparse
import hashlib
import json
import resource
import signal
import time
import field as f

HERE=Path(__file__).resolve().parent
CORE=(0,1,2,4,5,6,7,8,9,10,11,12)
INDEX='abcdefghijklmn'
FROZEN=('INPUT.json','PLAN.json','field.py','check.py')
def require(ok,message):
    if not ok:raise ValueError(message)
def norm(v,H):return f.dot(v,f.matvec(H,v))
def cramer(rows,rhs):
    D=f.det(rows)
    U=tuple(f.det([[rhs[i] if j==k else rows[i][j] for j in range(3)] for i in range(3)])
            for k in range(3))
    return U,D
def divide(U,D):
    inverse=f.inverse(D)
    return tuple(f.mul(x,inverse) for x in U)
def layout(data,plan):
    require(data['format']=='fixed-twelve-three-completion-v1','exact input schema')
    require(data['core_labels']==list(CORE),'exact twelve fixed labels')
    require(data['root_bracket']==[str(f.LO),str(f.HI)] or data['root_bracket']==[
        '0.59260590292507377809642492233275','0.59260590292507377809642492233276'],
        'exact distinguished real-root bracket')
    require(data['cap_bound']=='667/250' and data['cap_code_parameter_upper']=='593/1000',
            'exact selected cap constants')
    require(data['cut_short_squared_norm_upper']=='99/100' and data['fourteen_short_squared_norm_upper']=='3/4',
            'exact short-vertex bounds')
    require(data['q_active_labels']==[8,9,11] and data['other_active_labels']==[3,4,6],
            'exact alternative intersection names')
    require(plan['format']=='fixed-twelve-three-completion-plan-v1' and len(plan['cases'])==3,
            'all three original target cases')
    names=('cut','original-fourteen','other-fourteen')
    labels=(list(CORE)+['cut'],list(CORE)+[3,13],list(CORE)+[3,'q'])
    work=[]
    for k,(case,name,ls) in enumerate(zip(plan['cases'],names,labels)):
        require(case['name']==name and case['labels']==ls,'exact target order and active-plane labels')
        triples=list(combinations(range(len(ls)),3))
        require(len(case['tokens'])==len(triples),'complete fixed triple enumeration')
        for triple,token in zip(triples,case['tokens']):
            allowed=token in ('S','N') or (type(token)is str and len(token)==2 and
                ((token[0]=='I' and token[1] in INDEX[:len(ls)]) or
                 (token[0]=='U' and token[1] in INDEX[:3 if k==0 else 2])))
            require(allowed,'typed literal in the proper target')
            work.append((k,triple,token))
    require(len(work)==1014,'all286+364+364possible independent active triples')
    return work

def geometry(data):
    require(f.F==tuple(map(Q,(-1,-3,2,6,-1,13))),'exact quintic')
    require(f.evaluate(f.F,f.LO)<0<f.evaluate(f.F,f.HI),'opposite exact root-bracket signs')
    require(f.interval(tuple(i*f.F[i] for i in range(1,6)))[0]>0,'unique root in bracket')
    require(Q(1,2)<f.LO<f.HI<Q(593,1000)<Q(3,5),'metric and cap domain')
    H=tuple(tuple(f.ONE if i==j else f.T for j in range(3)) for i in range(3))
    V=[tuple(f.readpoly(p) for p in row) for row in data['vectors']]
    require(len(V)==15 and all(len(v)==3 for v in V),'fifteen reference vectors')
    for k,i in enumerate((0,5,11)):
        require(V[i]==tuple(f.ONE if j==k else f.ZERO for j in range(3)),'exact spanning anchor basis')
    require(all(norm(v,H)==f.ONE for v in V),'all reference unit identities')
    contacts=[]
    for i,j in combinations(range(15),2):
        product=f.dot(V[i],f.matvec(H,V[j]))
        if product==f.T:contacts.append([i,j])
        else:require(f.interval(product)[1]<Q(17,40),'strict reference noncontacts')
    require(len(contacts)==30,'reference thirty-contact incumbent')
    center=tuple(f.readpoly(p) for p in data['cap_center']);bound=Q(data['cap_bound'])
    n2=norm(center,H);upper=Q(data['cap_code_parameter_upper'])
    require(f.sign(f.sub(n2,f.scalar(bound*bound)))>0,'nonzero proper cap normal')
    gap=f.sub(f.scalar(2*bound*bound),f.scale(n2,1+upper))
    require(f.sign(f.sub(gap,f.scalar(Q(9,1000))))>0,'strict cap capacity above593/1000')
    Qrows=[f.matvec(H,V[i]) for i in (8,9,11)]
    numerator,determinant=cramer(Qrows,[f.T]*3)
    require(f.sign(determinant)!=0,'independent alternative common-contact planes')
    q=divide(numerator,determinant)
    other=tuple(f.readpoly(p) for p in data['alternate_last'])
    require(norm(q,H)==f.ONE and norm(other,H)==f.ONE,'both alternative unit identities')
    require(all(f.dot(Qrows[i],q)==f.T for i in range(3)),'q contacts8,9,11')
    require(all(f.dot(f.matvec(H,V[i]),other)==f.T for i in (3,4,6)),
            'other last point contacts3,4,6')
    require(f.sign(f.sub(f.dot(V[13],f.matvec(H,q)),f.T))>0,'p13andq cannot coexist')
    cut_units=[V[3],V[13],q];last_units=[V[14],other]
    constraints=[[(i,f.matvec(H,V[i]),f.T) for i in CORE]+[('cut',f.matvec(H,center),f.scalar(bound))],
                 [(i,f.matvec(H,V[i]),f.T) for i in CORE+(3,13)],
                 [(i,f.matvec(H,V[i]),f.T) for i in CORE+(3,)]+[('q',f.matvec(H,q),f.T)]]
    for candidate in cut_units:
        require(all(f.sign(f.sub(f.dot(row,candidate),rhs))<=0 for _,row,rhs in constraints[0]),
                'all three advertised cut unit vertices are feasible')
    require(len(set(cut_units))==3 and len(set(last_units))==2,'distinct exact completion choices')
    for target in constraints[1:]:
        for candidate in last_units:
            require(all(f.sign(f.sub(f.dot(row,candidate),rhs))<=0 for _,row,rhs in target),
                    'both advertised final completions pack in both forced branches')
    # Positive dependence among four retained points proves boundedness.
    tetra=(0,1,2,5)
    matrix=[[V[tetra[j]][i] for j in range(3)] for i in range(3)]
    U,D=cramer(matrix,[f.scale(x,-1) for x in V[5]])
    sign=f.sign(D)
    require(sign!=0 and all(f.sign(x)*sign>0 for x in U),'strict positive origin-spanning tetrahedron')
    require(all(f.add(f.dot(matrix[i],U),f.mul(D,V[5][i]))==f.ZERO for i in range(3)),
            'positive dependence exact Cramer identity')
    return H,V,constraints,[cut_units,last_units,last_units],contacts,q,other

def predicate(entry,H,constraints,units):
    k,triple,token=entry;target=constraints[k]
    rows=[target[i][1] for i in triple];rhs=[target[i][2] for i in triple]
    D=f.det(rows)
    if token=='S':
        require(D==f.ZERO,'certified singular active triple');return {'kind':'singular'}
    sign=f.sign(D);require(sign!=0,'independent active basis for this literal')
    U,_=cramer(rows,rhs)
    require(all(f.dot(rows[i],U)==f.mul(rhs[i],D) for i in range(3)),
            'all homogeneous Cramer equations')
    if token[0]=='I':
        j=INDEX.index(token[1]);_,row,bound=target[j]
        require(f.sign(f.sub(f.dot(row,U),f.mul(bound,D)))*sign>0,'strict selected violated inequality')
        return {'kind':'infeasible','witness':target[j][0]}
    require(all(f.sign(f.sub(f.dot(row,U),f.mul(bound,D)))*sign<=0 for _,row,bound in target),
            'exact feasibility of every advertised short or unit vertex')
    if token=='N':
        bound=Q(99,100) if k==0 else Q(3,4)
        require(f.sign(f.sub(norm(U,H),f.scale(f.mul(D,D),bound)))<0,
                'strict exact short-vertex squared norm')
        return {'kind':'short','point':divide(U,D)}
    require(token[0]=='U','unit literal')
    point=units[k][INDEX.index(token[1])]
    require(all(U[i]==f.mul(D,point[i]) for i in range(3)),'exact prescribed unit vertex')
    return {'kind':'unit','point':point,'unit_index':INDEX.index(token[1])}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--count',type=int,default=2500)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second exact-replay guard')))
    signal.alarm(50);started=time.monotonic()
    data=json.loads((HERE/'INPUT.json').read_text());plan=json.loads((HERE/'PLAN.json').read_text())
    work=layout(data,plan)
    require(0<=args.start<len(work) and 0<args.count<=2500,'bounded explicit actual replay range')
    stop=min(len(work),args.start+args.count)
    H,V,constraints,units,contacts,q,other=geometry(data)
    records=[];vertices=[[],[],[]]
    for ordinal in range(args.start,stop):
        if time.monotonic()-started>50:raise TimeoutError('logical replay guard; incomplete proof')
        entry=work[ordinal];result=predicate(entry,H,constraints,units)
        point=result.pop('point',None)
        if point is not None:
            require(point not in vertices[entry[0]],'no repeated feasible vertex in this replay slice')
            vertices[entry[0]].append(point)
        records.append([ordinal,entry[0],list(entry[1]),result])
    result={'actual_agent':'six-tammes-2','role':'researcher','status':'CHECKED_EXACT_LITERAL_RANGE',
            'checked_range':[args.start,stop],'actual_predicates_executed':len(records),
            'total_predicates':len(work),'all_requested_predicates_executed':len(records)==stop-args.start,
            'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in FROZEN},
            'kind_counts':dict(Counter(r[3]['kind'] for r in records)),
            'case_counts':dict(Counter(plan['cases'][r[1]]['name'] for r in records)),
            'actual_records':records,'exact_q':[[str(x) for x in poly] for poly in q],
            'geometry_and_boundedness_checked':True,'cap_capacity_checked':True,
            'known_reference_contacts':contacts,
            'wall_seconds':time.monotonic()-started,
            'cpu_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'threads':1,
            'full_certificate_executed_this_invocation':args.start==0 and stop==len(work),
            'independent_researcher_review':'pending','new_global_bound':False}
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('actual_records','known_reference_contacts','exact_q')},sort_keys=True))

if __name__=='__main__':main()
