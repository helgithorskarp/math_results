"""Exact conditional eight-Q exclusion. six-tammes-1, researcher.
CPython>=3.11 standard library. Original-face bridges are in PROOF.md.
No numerical root, floating value, solver, CAS or parameter sample.
"""
from pathlib import Path
import copy,json
import atlas
from polynomial import T,ONE,need,bernstein
from rational import Rat

C=Rat(T);U=Rat(ONE);Z=Rat();REF=2*C/(U+C)

def dot(a,b):
    return (U-C)*sum((x*y for x,y in zip(a,b)),Z)+C*sum(a,Z)*sum(b,Z)

def signp(p):
    b=bernstein(p)
    for s in (-1,1):
        if b and all(s*x>=0 for x in b) and any(s*x>0 for x in b):return s
    return 0

def sign(r):return signp(r.n)*signp(r.d)

def record(r):
    need(sign(r) in (-1,1),'strict sign certificate')
    n=bernstein(r.n);d=bernstein(r.d)
    return {'n':r.n,'d':r.d,'interval':('1/2','3/5'),'open':True,'sign':sign(r),
            'numerator_Bernstein_coefficients':list(map(str,n)),
            'denominator_Bernstein_coefficients':list(map(str,d))}

def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def unit(a):need(not (dot(a,a)-U).n,'unit coefficient identity')

def audit(co):
    for a in co.values():
        unit(a)
        for x in a:need(signp(x.d) in (-1,1),'coordinate denominator nonzero')

def third(a,b,s):
    need(s in (-1,1),'equilateral seed sign');unit(a);unit(b)
    need(not (dot(a,b)-C).n,'equilateral seed contact edge')
    u=cross(a,b);total=sum(u,Z)
    v=tuple(C/(U+C)*(x+y)+s*((U+2*C)*z-C*total)/(U+C) for x,y,z in zip(a,b,u))
    unit(v);need(not (dot(v,a)-C).n and not (dot(v,b)-C).n,'equilateral seed contact identities')
    return v

def reflect(a,b,old):
    unit(a);unit(b);unit(old)
    need(not (dot(a,b)-C).n and not (dot(a,old)-C).n and not (dot(b,old)-C).n,'old equilateral triangle')
    v=tuple(REF*(x+y)-z for x,y,z in zip(a,b,old));unit(v)
    need(not (dot(v,a)-C).n and not (dot(v,b)-C).n,'reflected contact identities')
    return v

def qopp(f,a,b):
    for x in (f,a,b):unit(x)
    need(not (dot(f,a)-C).n and not (dot(f,b)-C).n,'old Q contact corner')
    den=U+dot(a,b);need(sign(den)==1,'positive original Q divisor before division')
    v=tuple(2*C/den*(x+y)-z for x,y,z in zip(a,b,f));unit(v)
    need(not (dot(v,a)-C).n and not (dot(v,b)-C).n,'Q reflection contact identities')
    return v

def representative(cert):
    promoted=set(cert['promoted_endpoints']);types=['R']*15
    for f in (0,7):types[f]='F'
    for e in atlas.EARS:types[e]='R' if e in promoted else 'D'
    for v in atlas.OUT:types[v]='R' if v==cert['outside_R'] else 'D'
    return {'p':cert['p'],'k':len(promoted),'types':types,'QA':cert['QA'],'QB':cert['QB'],
            'free_Ts':tuple(tuple(t) for t in cert['free_Ts'])}

def image(case,m):
    types=['']*15
    for i,t in enumerate(case['types']):types[m[i]]=t
    q={m[0]:m[case['QA']],m[7]:m[case['QB']]}
    return (case['p'],tuple(types),(q[0],q[7]),
            tuple(sorted(tuple(sorted(m[i] for i in t)) for t in case['free_Ts'])))

def cover(cert):
    out=atlas.run();rep=representative(cert)
    need(cert['p']==0 and cert['promoted_endpoints']==[1,6] and cert['QA']==12 and cert['QB']==13 and cert['outside_R']==14,'named residual representative')
    need({tuple(sorted(t)) for t in cert['free_Ts']}=={(1,12,14),(6,13,14)},'both original free Ts')
    need(all(atlas.reject(rep,k) is None for k in range(1,4)),'representative obeys all necessary filters')
    target=image(rep,{i:i for i in range(15)});maps=[]
    for c in out['survivors']:
        choices=[m for m in atlas.GROUP if image(c,m)==target]
        need(choices,'full role/Q/free-face relabeling to representative')
        m=choices[0]
        need({tuple(sorted(m[i] for i in t)) for t in atlas.TS}=={tuple(sorted(t)) for t in atlas.TS},'all eight fixed fan faces mapped')
        maps.append(tuple(m[i] for i in range(15)))
    # No canonical edge mask is used to infer a coordinate identity.
    return {k:v for k,v in out.items() if k not in ('survivors','seconds')},maps

def metric(cert):
    need(cert['R_seeds']==[-1,1] and cert['B_seeds']==[-1,1],'both signs in both finite seed covers')
    base={0:(U,Z,Z),1:(Z,U,Z),2:(Z,Z,U)}
    for new,a,b,old in ((3,0,2,1),(4,0,3,2),(5,0,4,3)):
        base[new]=reflect(base[a],base[b],base[old])
    base[12]=qopp(base[0],base[1],base[5]);audit(base)
    rows=[]
    for rs in cert['R_seeds']:
        co=dict(base);co[14]=third(co[1],co[12],rs);audit(co)
        if rs==-1:
            pair=cert['forbidden_pairs']['R_negative'];gap=C-dot(co[pair[0]],co[pair[1]])
            need(sign(gap)==-1,'negative R seed forbidden original pair')
            rows.append({'R_seed':rs,'constructed_original_labels':sorted(co),
                         'forbidden_pair':pair,'gap':record(gap)})
            continue
        co[6]=tuple(2*C*x-y for x,y in zip(co[14],co[1]))
        co[13]=tuple(2*C*x-y for x,y in zip(co[14],co[12]))
        for i in (6,13):unit(co[i]);need(not (dot(co[i],co[14])-C).n,'half-turn common contact')
        need(not (dot(co[6],co[13])-C).n,'other free-T edge')
        co[8]=qopp(co[14],co[12],co[6]);audit(co)
        for bs in cert['B_seeds']:
            work=dict(co);work[7]=third(work[6],work[8],bs)
            if bs==1:
                work[9]=reflect(work[7],work[8],work[6]);work[10]=reflect(work[7],work[9],work[8])
            audit(work)
            key='B_negative' if bs==-1 else 'B_positive';pair=cert['forbidden_pairs'][key]
            gap=C-dot(work[pair[0]],work[pair[1]])
            need(sign(gap)==-1,'B seed forbidden original pair')
            rows.append({'R_seed':rs,'B_seed':bs,'constructed_original_labels':sorted(work),
                         'forbidden_pair':pair,'gap':record(gap)})
    need(len(rows)==3,'three terminal leaves cover R minus and both R plus B seeds')
    return rows

def verify(cert):
    a,maps=cover(cert);leaves=metric(cert)
    return {'agent':'six-tammes-1','role':'researcher','proof_interval':('1/2','3/5'),
            'original_label_cover':a,'full_face_relabeling_witnesses':maps,
            'metric_leaves':leaves,'all_constructed_positions_unit':True,
            'all_coordinate_and_original_Q_divisors_nonzero':True,
            'largest_constructed_original_patch':14,
            'every_computed_Gram_gap_asserted_nonnegative':False,
            'conclusion':'No complete convex simple cellular T/Q graph with degree pattern(5^2,4^13) and two ordinary fives; therefore the inherited q8/beta branch is excluded.'}

def controls(cert):
    changes=(('wrong_profile',lambda c:c.update(p=1)),
             ('same_fan_promoted_endpoints',lambda c:c.update(promoted_endpoints=[1,5])),
             ('opposite_alias',lambda c:c.update(QB=12)),
             ('wrong_free_triangle',lambda c:c['free_Ts'][0].__setitem__(1,13)),
             ('omitted_free_triangle',lambda c:c['free_Ts'].pop()),
             ('omitted_R_seed',lambda c:c.update(R_seeds=[1])),
             ('omitted_B_seed',lambda c:c.update(B_seeds=[1])),
             ('wrong_R_forbidden_pair',lambda c:c['forbidden_pairs'].update(R_negative=[0,1])),
             ('wrong_B_negative_forbidden_pair',lambda c:c['forbidden_pairs'].update(B_negative=[6,7])),
             ('wrong_B_positive_forbidden_pair',lambda c:c['forbidden_pairs'].update(B_positive=[0,7])))
    result=[]
    for name,mutate in changes:
        c=copy.deepcopy(cert);mutate(c)
        try:verify(c)
        except (ValueError,KeyError) as err:result.append({'name':name,'rejected':True,'reason':str(err)})
        else:raise ValueError('Invalid certificate accepted: '+name)
    return result

def main():
    cert=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text());r=verify(cert)
    r['controls']=controls(cert);print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
