"""Exact literal certificate checker; standard library, no producer/LP import."""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from math import gcd,lcm
from pathlib import Path

HERE=Path(__file__).resolve().parent
GROUPS=((10,12,15,16,18,20),(24,30),(36,40),(45,48),(60,72),(80,90),(120,144),(180,240),(360,720))
CAPS=(34,34,34,34,27)

def need(ok,message):
    if not ok:raise RuntimeError(message)

def hit(rows,x):return any(x%m==a for a,m in rows)

def compulsory(x):return x%8!=5 and x%9!=6 and x%18!=3 and x%4!=0

def targets():
    S={4*t for t in range(180) if t%9!=6}
    B=[{4*t for t in range(180) if t%9!=6 and t%2!=p and t%3!=b} for p in range(2) for b in (1,2)]
    B.append({4*t for t in range(180) if t%9!=6 and t%3==0})
    return S,B

def physical_map(u,v,permutation):
    # CRT inverse: y mod144 and f mod5; 144^-1 mod5=4.
    out=[]
    for x in range(720):
        y=(u*(x%144)+v)%144;f=permutation[x%5]
        out.append(y+144*((4*(f-y))%5))
    return out

def generators():
    identity=list(range(5));out=[physical_map(13,36,identity),physical_map(1,72,identity)]
    for f in range(4):
        p=identity.copy();p[f],p[f+1]=p[f+1],p[f]
        out.append(physical_map(1,0,p))
    return out

def orbit_partition(F):
    gs=generators();unseen=set(F);orbits=[]
    while unseen:
        todo=[min(unseen)];orb=set(todo)
        for x in todo:
            for g in gs:
                y=g[x]
                if y not in orb:orb.add(y);todo.append(y)
        need(orb<=F,'orbit exits compulsory domain')
        unseen-=orb;orbits.append(sorted(orb))
    return orbits

def verify(c):
    need(c['schema']==1 and c['period']==720 and c['fixed']==[[5,8],[6,9]] and c['allowed_holes']==[[3,18],[0,4]],'domain metadata')
    need(c['groups']==[list(g) for g in GROUPS] and c['target_caps']==list(CAPS),'original blocks/caps')
    need(c['core_twelve_present_nonzero'] is True and c['core_compulsory_gain_at_least']==204,'core restrictions')
    need(c['group_average_size']==2880 and c['supply_ratio']==[377,370] and c['whole_first_stage_or_full_cover'] is False,'claim scope')
    F={x for x in range(720) if compulsory(x)};S,B=targets();gs=generators()
    need(len(F)==370 and len(S)==160 and [len(b) for b in B]==[50,50,50,50,40],'literal demand domains')
    y_orbits=c['compulsory_y_orbits']
    need(len(y_orbits)==13 and sum(len(o) for o in y_orbits)==74,'orbit dimensions')
    recorded=[sorted(x for x in F if x%144 in o) for o in y_orbits]
    actual=orbit_partition(F)
    need(sorted(recorded)==sorted(actual),'generator BFS orbits differ from certificate')
    class_points=0
    all_labels=[m for g in GROUPS for m in g]+[8,9]
    for g in gs:
        need(sorted(g)==list(range(720)) and {g[x] for x in F}==F and {g[x] for x in S}==S,'not a target bijection')
        images=[{g[x] for x in b} for b in B]
        need(sorted(map(sorted,images[:4]))==sorted(map(sorted,B[:4])) and images[4]==B[4],'five caps not preserved')
        for m in all_labels:
            for a in range(m):
                original=set(range(a,720,m));image={g[x] for x in original};new_a=g[a]%m
                need(image==set(range(new_a,720,m)),'generator changes original modulus/class')
                class_points+=len(original)
        need(g[5]%8==5 and g[6]%9==6 and all(g[a]%12==a for a in range(12)),'fixed classes/12 phases changed')
    masses=[Fraction(0) for _ in GROUPS];moments=[Fraction(0) for _ in y_orbits];denominators=[];uniform_gains=[]
    for t in c['terms']:
        g=t['group'];num,den=t['probability'];rows=t['classes']
        need(type(g) is int and 0<=g<9 and type(num) is int and type(den) is int and 0<num<=den and gcd(num,den)==1,'rational term syntax')
        need(len({m for a,m in rows})==len(rows) and all(m in GROUPS[g] and type(a) is int and 0<=a<m for a,m in rows),'original phase inventory')
        if g==0:need(any(m==12 and a!=0 for a,m in rows),'original12 absent or phase0')
        selected={x for x in range(720) if hit(rows,x)}
        need(all(len(selected&b)<=cap for b,cap in zip(B,CAPS)),'term violates block coverage cap')
        counts=[len(selected&set(o)) for o in recorded]
        need(counts==t['compulsory_orbit_counts'],'literal original-phase orbit incidence differs')
        if g==0:need(sum(counts)>=204,'core compulsory gain below204')
        p=Fraction(num,den);masses[g]+=p;denominators.append(den);uniform_gains.append(sum(counts))
        for j,value in enumerate(counts):moments[j]+=p*value
    ratio=Fraction(377,370)
    need(len(c['terms'])==18 and all(m==1 for m in masses),'group masses not one')
    need(moments==[ratio*len(o) for o in recorded],'exact orbit supply is not377/370')
    D=lcm(*denominators);need(D==c['probability_common_denominator']==129870,'probability denominator')
    return {'terms':18,'original_class_occurrences':sum(len(t['classes']) for t in c['terms']),
            'compulsory_points':370,'orbits':13,'symmetry_generators':6,'original_phase_points_audited':class_points,
            'group_average_size':2880,'common_denominator':D,'supply_ratio':[377,370],
            'exact_group_masses_one':True,'exact_orbit_supply_verified':True,
            'scaled_point_mass':D*2880*377//370,'full_cover_found':False}

def text_encoding(c):
    D=c['probability_common_denominator'];lines=[f"720 {D} 2880 377 370 {len(c['terms'])}"]
    for t in c['terms']:
        n,d=t['probability'];lines.append(' '.join(map(str,[t['group'],n*(D//d),len(t['classes'])]+[x for r in t['classes'] for x in r])))
    return '\n'.join(lines)+'\n'

def damages(c):
    tests=[]
    q=deepcopy(c);q['terms'][0]['classes'][0][0]+=1;tests.append(('original-phase',q))
    q=deepcopy(c);q['terms'][0]['probability'][0]+=1;tests.append(('probability',q))
    q=deepcopy(c);q['terms'][0]['compulsory_orbit_counts'][0]+=1;tests.append(('orbit-incidence',q))
    q=deepcopy(c);q['terms'][0]['classes'][1][0]=0;tests.append(('forbidden-twelve',q))
    q=deepcopy(c);q['terms'].pop();tests.append(('missing-term',q))
    q=deepcopy(c);q['target_caps'][4]=28;tests.append(('cap',q))
    q=deepcopy(c);q['compulsory_y_orbits'][0][0]+=1;tests.append(('orbit',q))
    q=deepcopy(c);q['supply_ratio'][0]=378;tests.append(('stronger-ratio',q))
    rejected=[]
    for name,q in tests:
        try:verify(q)
        except RuntimeError:rejected.append(name)
        else:raise RuntimeError('semantic damage escaped: '+name)
    return rejected

if __name__=='__main__':
    c=json.loads((HERE/'certificate.json').read_text());result=verify(c)
    need(text_encoding(c)==(HERE/'certificate.txt').read_text(),'JSON/text certificates differ')
    result['damages_rejected']=damages(c)
    result['certificate_sha256']=hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest()
    expected=HERE/'expected.json'
    if expected.exists():need(result==json.loads(expected.read_text()),'frozen expected checker values differ')
    print(json.dumps(result))
