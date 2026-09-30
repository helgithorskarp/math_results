"""Exact conditional adjacent-five exclusion; no floats, CAS or solver.
Author: six-tammes-1, researcher. CPython >=3.11 standard library.
The original-vertex/contact/face interpretation is in PROOF.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import copy, hashlib, json

from fans import need, run, build, edges_of, boundary_cycle, star_path
from polynomial import T, ONE, bernstein, pgcd, trim
from rational import Rat

C=Rat(T); U=Rat(ONE); Z=Rat(); REF=2*C/(U+C)
CLASSES=(((8,12),(9,13)),((10,12),(11,13)))
EXTRA_CONTACTS=((10,11,12,13),(8,9,12,13))
GCDS=((0,0,1,0,-3,2),(0,1,4,-6,-34,7,86,-18,-80,40))

def dot(x,y):
    return (U-C)*sum((a*b for a,b in zip(x,y)),Z)+C*sum(x,Z)*sum(y,Z)

def sign_open(r):
    def sign(p):
        b=bernstein(p)
        if b and all(x>=0 for x in b) and any(x>0 for x in b):return 1
        if b and all(x<=0 for x in b) and any(x<0 for x in b):return -1
        return 0
    return sign(r.n)*sign(r.d)

def determinant(rows):
    a,b,c=rows
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def normal(a):return tuple((U-C)*a[k]+C*sum(a,Z) for k in range(3))

def cramer(points):
    ns=[normal(a) for a in points]; d=determinant(ns)
    y=tuple(determinant([tuple(C if j==k else x for j,x in enumerate(row)) for row in ns]) for k in range(3))
    need(all(not (sum((a*b for a,b in zip(row,y)),Z)-C*d).n for row in ns),'N Y=d c1')
    for col in range(3):
        rhs=[row[col] for row in ns]
        for k in range(3):
            image=determinant([tuple(rhs[i] if j==k else x for j,x in enumerate(row)) for i,row in enumerate(ns)])
            need(not (image-(d if k==col else Z)).n,'adj(N) N=d I')
    return d,y,dot(y,y)-d*d

def generic_coordinates(triangles):
    original=set(edges_of(triangles));edges=set(original)
    active={v for e in edges for v in e};removed=[]
    while len(active)>3:
        nb={v:{w for e in edges if v in e for w in e if w!=v} for v in active}
        ears=sorted(v for v in active if len(nb[v])==2);need(ears,'missing ear')
        new=ears[0];a,b=sorted(nb[new]);old=(nb[a]&nb[b])-{new}
        need(len(old)==1,'unique old third')
        removed.append((new,a,b,next(iter(old))))
        active.remove(new);edges={e for e in edges if new not in e}
    anchors=tuple(sorted(active));need(edges==set(combinations(anchors,2)),'anchor triangle')
    co={v:tuple(U if j==k else Z for k in range(3)) for j,v in enumerate(anchors)}
    for new,a,b,old in reversed(removed):co[new]=tuple(REF*(x+y)-z for x,y,z in zip(co[a],co[b],co[old]))
    return co

def direct_coordinates():
    co={1:(U,Z,Z),6:(Z,U,Z),7:(Z,Z,U)}
    for new,a,b,old in ((2,1,6,7),(0,1,2,6),(3,0,1,2),(4,0,3,1),(5,0,4,3)):
        co[new]=tuple(REF*(x+y)-z for x,y,z in zip(co[a],co[b],co[old]))
    return co

def correspondence(row,rep):
    cycle=boundary_cycle(row['faces']);target=boundary_cycle(rep['faces']);n=len(cycle)
    for shift in range(n):
        for sign in (-1,1):
            m={v:target[(shift+sign*k)%n] for k,v in enumerate(cycle)}
            if {tuple(sorted(m[v] for v in t)) for t in row['faces']}==set(map(tuple,rep['faces'])) and {m[0],m[1]}=={0,1}:return m
    raise ValueError('missing full face/F correspondence')

def paired_fan_cover():
    rows=run();need(len(rows)==9,'nine rotations')
    good=[r for r in rows if max(r['triangle_counts'][v] for v in (2,3))<=2]
    need([(r['i'],r['j']) for r in good]==[(1,1),(3,3)],'two five ceiling')
    rep=good[0];target=generic_coordinates(rep['faces'])
    for row in good:
        need(row['canonical_mask']==172253945,'A8 mask')
        m=correspondence(row,rep);co=generic_coordinates(row['faces'])
        need(all(not (dot(co[a],co[b])-dot(target[m[a]],target[m[b]])).n for a,b in combinations(sorted(co),2)),'Gram correspondence')
    direct=direct_coordinates()
    need(all(direct[v]==target[v] for v in direct),'direct/ear coordinate audit')
    return rows,rep

def complete_core(rep):
    triangles=rep['faces'];co=direct_coordinates();qs=[]
    seeds=((0,2,5,8),(1,3,7,9),(2,6,8,10),(3,4,9,11),(4,5,11,12),(6,7,10,13))
    for f,a,b,new in seeds:
        if f in (0,1):
            path=star_path(f,triangles);need({path[0],path[-1]}=={a,b},'sole F Q endpoints')
        den=U+dot(co[a],co[b]);need(sign_open(den)==1,'positive Q denominator')
        q=tuple(2*C/den*(x+y)-z for x,y,z in zip(co[a],co[b],co[f]))
        need(not (dot(q,q)-U).n,'Q unit norm')
        need(not (dot(q,co[a])-C).n and not (dot(q,co[b])-C).n,'Q contact identity')
        co[new]=q;qs.append((f,a,new,b))
    need(all(not (dot(a,a)-U).n for a in co.values()),'all unit identities')
    need(all(sign_open(Rat(x.d)) for a in co.values() for x in a),'core coordinate poles')
    contacts=[];gaps=[];exceptions={p for row in CLASSES for p in row}
    for a,b in combinations(sorted(co),2):
        g=C-dot(co[a],co[b])
        if not g.n:contacts.append((a,b))
        elif (a,b) in exceptions:
            need(sign_open(U-dot(co[a],co[b]))==1,'distinct exceptional positions')
        else:need(sign_open(g)==1,'strict packing gap');gaps.append((a,b))
    prescribed=set(edges_of(triangles))
    for f,a,new,b in qs:prescribed.update((tuple(sorted((f,a))),tuple(sorted((a,new))),tuple(sorted((new,b))),tuple(sorted((b,f)))))
    need(set(contacts)==prescribed and len(contacts)==25 and len(gaps)==62,'core graph/four exceptions')
    for row in CLASSES:
        a,b=row[0];x,y=row[1]
        need(C-dot(co[a],co[b])==C-dot(co[x],co[y]),'paired exceptional gap identity')
    degrees=dict(sorted(Counter(v for e in contacts for v in e).items()))
    need(degrees=={0:5,1:5,2:4,3:4,4:4,5:4,6:4,7:4,8:3,9:3,10:3,11:3,12:2,13:2},'base core degrees')
    need(2*5+12*4-2*len(contacts)==8,'eight unfilled base endpoints')
    need((2*5+13*4)//2-4==27,'27 actual core contacts required')
    return co,contacts,qs,degrees

# Independent rational polynomial operations for the Bezout identity audit.
# This shares the computed polynomials, not the integer pseudoremainder algorithm.
def ftrim(p):
    q=list(map(Fraction,p))
    while q and not q[-1]:q.pop()
    return tuple(q)
def fadd(a,b):return ftrim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def fscale(a,k):return ftrim([x*k for x in a])
def fmul(a,b):
    if not a or not b:return ()
    p=[Fraction(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):p[i+j]+=x*y
    return ftrim(p)
def fdiv(a,b):
    need(b,'zero Fraction polynomial divisor');r=ftrim(a);q=[Fraction(0)]*max(0,len(a)-len(b)+1)
    while r and len(r)>=len(b):
        k=len(r)-len(b);u=r[-1]/b[-1];q[k]=u
        r=fadd(r,fscale((Fraction(0),)*k+b,-u))
    return ftrim(q),r

def gcd_audit(a,b,wanted):
    need(pgcd(a,b)==wanted,'integer polynomial gcd')
    r0,r1=ftrim(a),ftrim(b);s0,s1=(Fraction(1),),();t0,t1=(),(Fraction(1),)
    while r1:
        q,r=fdiv(r0,r1);r0,r1=r1,r
        s0,s1=s1,fadd(s0,fscale(fmul(q,s1),-1))
        t0,t1=t1,fadd(t0,fscale(fmul(q,t1),-1))
    need(len(r0)==len(wanted),'Fraction gcd degree')
    scale=Fraction(wanted[-1])/r0[-1];s=fscale(s0,scale);t=fscale(t0,scale)
    need(fadd(fmul(s,ftrim(a)),fmul(t,ftrim(b)))==ftrim(wanted),'Bezout identity')
    need(sign_open(Rat(wanted)) in (-1,1),'nonvanishing common-root polynomial')
    text=json.dumps([[str(x) for x in s],[str(x) for x in t]],separators=(',',':'))
    return {'gcd':wanted,'gcd_sign':sign_open(Rat(wanted)),
            'bernstein_coefficients':[str(x) for x in bernstein(wanted)],
            'bezout_coefficient_counts':(len(s),len(t)),
            'bezout_sha256':hashlib.sha256(text.encode()).hexdigest()}

def extension_obstruction(co,contacts,degrees):
    rows=[]
    for k in range(2):
        actual=set(contacts)|set(CLASSES[k]);deg=Counter(v for e in actual for v in e)
        needed={i:(5 if i in (0,1) else 4)-deg[i] for i in sorted(co)}
        extra=tuple(i for i,n in needed.items() if n)
        need(len(actual)==27 and all(n in (0,1) for n in needed.values()),'actual core degree completion')
        need(extra==EXTRA_CONTACTS[k],'forced fifteenth-point contacts')
        a,b=CLASSES[k][0];gap=C-dot(co[a],co[b])
        triple=extra[:3];d,y,g=cramer([co[i] for i in triple])
        need(sign_open(Rat(g.d)) in (-1,1),'residual denominator poles')
        audit=gcd_audit(gap.n,g.n,GCDS[k])
        rows.append({'case':k,'exceptional_contacts':CLASSES[k],'fifteenth_point_contacts':extra,
                     'necessary_contact_triple':triple,'gap_numerator':gap.n,
                     'undivided_residual_degree':len(g.n)-1,**audit})
    return rows

def validate_seed(seed):
    need(seed=={'exceptional_classes':[[list(p) for p in row] for row in CLASSES],
               'fifteenth_point_contacts':[list(t) for t in EXTRA_CONTACTS]},'certificate seed/complete class mismatch')

def controls(seed,co):
    count=0
    def reject(action):
        nonlocal count
        try:action()
        except (ValueError,TypeError,KeyError):count+=1;return
        raise ValueError('false control accepted')
    bad=copy.deepcopy(seed);bad['exceptional_classes'].pop();reject(lambda:validate_seed(bad))
    bad=copy.deepcopy(seed);bad['fifteenth_point_contacts'][0][0]=5;reject(lambda:validate_seed(bad))
    bad=copy.deepcopy(seed);bad['exceptional_classes'][0][0]=[0,1];reject(lambda:validate_seed(bad))
    reject(lambda:Rat((1,),()))
    reject(lambda:Rat((1,)).__truediv__(Rat()))
    reject(lambda:Rat((1,))**-1)
    reject(lambda:gcd_audit((1,1),(2,1),(1,1)))
    need(sign_open(Rat((0,-1,1)))==-1,'negative interval polynomial')
    need(sign_open(Rat((1,-4,4)))==1,'open zero-endpoint sign')
    need(sign_open(Rat((-11,20)))==0,'changing sign unresolved')
    need(not determinant([(U,Z,Z),(U,Z,Z),(Z,Z,U)]).n,'singular determinant')
    need(pgcd((0,1,1),(0,1,2))==(0,1),'nontrivial rational gcd')
    need(fadd(fmul((Fraction(1,2),),(Fraction(2),)),())==(Fraction(1),),'Fraction polynomial control')
    return count+6

def main():
    seed=json.loads((Path(__file__).parent/'certificate.json').read_text());validate_seed(seed)
    cover,rep=paired_fan_cover();co,contacts,qs,degrees=complete_core(rep)
    obstruction=extension_obstruction(co,contacts,degrees)
    component_caps={}
    for p in (0,1):
        s=[s for s in range(10+p) if (15+p-s)%2==0 and 5-p+s<=8]
        need(s==([1,3] if p==0 else [0,2,4]),'remaining separated-four cap')
        component_caps[str(p)]=s
    output={'agent':'six-tammes-1','role':'researcher',
            'scope':'Conditional contacting ordinary fives excluded; global Tammes bound unchanged.',
            'algebra_interval':'1/2<c<3/5','inherited_profile_interval':'1/2<c<beta',
            'paired_fan_cover':cover,'quadrilaterals':qs,'core_contacts':contacts,'core_degrees':degrees,
            'core_strict_noncontacts':62,'exceptional_contact_pairs':4,
            'required_actual_core_contacts':27,'extension_cases':obstruction,
            'remaining_profiles':[[4,0,0,0],[2,1,0,0]],'separated_four_counts':component_caps,
            'controls':controls(seed,co)}
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__':main()
