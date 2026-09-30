"""Exact double-five-Q exclusion. Author: six-tammes-1, researcher.
CPython >=3.11 standard library; no floats, solver or CAS.
The original-vertex and complete face-cover bridges are in PROOF.md.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import copy, json
from polynomial import T, ONE, bernstein, mul, need
from rational import Rat

C=Rat(T); U=Rat(ONE); Z=Rat(); REF=2*C/(U+C)
LO=F(1,2); HI=F(3,5)
TS=((0,2,4),(0,4,5),(0,5,6),(0,6,3),
    (1,3,7),(1,7,8),(1,8,9),(1,9,2))
SHARED_Q=(0,2,1,3)

def dot(a,b):
    return (U-C)*sum((x*y for x,y in zip(a,b)),Z)+C*sum(a,Z)*sum(b,Z)

def bsign(p,lo=LO,hi=HI,closed=False):
    bs=bernstein(p,lo,hi)
    for s in (-1,1):
        if bs and all(s*x>=0 for x in bs) and any(s*x>0 for x in bs):
            if not closed or (s*bs[0]>0 and s*bs[-1]>0):return s
    return 0

def sign(r,lo=LO,hi=HI,closed=False):
    return bsign(r.n,lo,hi,closed)*bsign(r.d,lo,hi,closed)

def sign_record(r,lo=LO,hi=HI,closed=False):
    need(sign(r,lo,hi,closed) in (-1,1),'strict rational sign required')
    n=bernstein(r.n,lo,hi);d=bernstein(r.d,lo,hi)
    return {'n':r.n,'d':r.d,'interval':(str(lo),str(hi)),
            'closed':closed,'sign':sign(r,lo,hi,closed),
            'numerator_Bernstein_range':(str(min(n)),str(max(n))),
            'denominator_Bernstein_range':(str(min(d)),str(max(d)))}

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def reflect(a,b,o):return tuple(REF*(x+y)-z for x,y,z in zip(a,b,o))

def third(a,b,s):
    need(s in (-1,1),'third-point sign')
    u=cross(a,b);total=sum(u,Z)
    v=tuple(C/(U+C)*(x+y)+s*((U+2*C)*z-C*total)/(U+C)
            for x,y,z in zip(a,b,u))
    need(not (dot(v,v)-U).n,'third-point unit identity')
    need(not (dot(v,a)-C).n and not (dot(v,b)-C).n,'third-point contact identities')
    return v

def qopp(f,a,b):
    den=U+dot(a,b);need(sign(den)==1,'positive Q reflection divisor')
    q=tuple(2*C/den*(x+y)-z for x,y,z in zip(a,b,f))
    need(not (dot(q,q)-U).n,'Q unit identity')
    need(not (dot(q,a)-C).n and not (dot(q,b)-C).n,'Q contact identities')
    return q

def poles(co):
    for a in co.values():
        need(not (dot(a,a)-U).n,'unit identity')
        for x in a:need(bsign(x.d) in (-1,1),'coordinate denominator pole')

def edges(faces):
    return {tuple(sorted((face[k],face[(k+1)%len(face)])))
            for face in faces for k in range(len(face))}

def core_audit(co,faces,contact_count):
    poles(co);contacts=[];strict=[]
    for a,b in combinations(sorted(co),2):
        gap=C-dot(co[a],co[b])
        if not gap.n:contacts.append((a,b))
        else:
            need(sign(gap)==1,'strict original core packing gap')
            strict.append((a,b))
    need(set(contacts)==edges(faces),'complete original core contacts')
    need(len(contacts)==contact_count,'core contact count')
    # Contact inner product c<1; other inner products <c. Thus all original
    # core positions are distinct, without relying on a floating sample.
    return {'vertices':sorted(co),'pairs':len(contacts)+len(strict),
            'contacts':contacts,'strict_noncontacts':strict,
            'all_unit':True,'all_distinct':True,'coordinate_poles_excluded':True}

def sector(co,faces,f,a,b):
    local=[];counts=Counter()
    for face in faces:
        if f in face:
            k=face.index(f);local.append(tuple(sorted((face[k-1],face[(k+1)%len(face)]))))
            counts[len(face)]+=1
    need(counts=={3:2,4:1},'two known Ts and one known Q at the saturated four')
    need(len(set(local))==3,'distinct known link sectors')
    degrees=Counter(v for e in local for v in e)
    need(len(degrees)==4 and sorted(degrees.values())==[1,1,2,2],'four-neighbor link path')
    active={next(iter(degrees))}
    while True:
        more=active|{v for e in local if active.intersection(e) for v in e}
        if more==active:break
        active=more
    need(active==set(degrees),'connected link path')
    need({v for v,n in degrees.items() if n==1}=={a,b},'forced missing-sector endpoints')
    need(sign(C-dot(co[a],co[b]))==1,'missing-sector endpoints are noncontacting')
    need(all(not (dot(co[f],co[v])-C).n for v in degrees),'four prescribed contact neighbors')
    return {'vertex':f,'known_link_edges':sorted(local),'missing_sector':(a,b)}

def seed_cover():
    base={0:(U,Z,Z),2:(Z,U,Z),4:(Z,Z,U)}
    for new,a,b,old in ((5,0,4,2),(6,0,5,4),(3,0,6,5)):
        base[new]=reflect(base[a],base[b],base[old])
    base[1]=qopp(base[0],base[2],base[3]);branches=[];good={}
    for s in (-1,1):
        co=dict(base);co[7]=third(co[1],co[3],s)
        co[8]=reflect(co[1],co[7],co[3]);co[9]=reflect(co[1],co[8],co[7])
        endpoint=reflect(co[1],co[9],co[8]);poles(co);poles({16:endpoint})
        gap=U-dot(co[2],endpoint)
        if not gap.n:
            need(endpoint==co[2],'endpoint coefficient identity')
            good[s]=co;branches.append({'sign':s,'endpoint_identity':True})
        else:
            need(sign(gap)==1,'discarded seed fails endpoint uniformly')
            branches.append({'sign':s,'endpoint_identity':False,'endpoint_gap':sign_record(gap)})
    need(set(good)=={1},'one admissible seed among BOTH signs')
    return branches,good

def verify(cert):
    branches,good=seed_cover()
    need(cert['B_seed_sign'] in good,'chosen seed satisfies endpoint condition')
    co=dict(good[cert['B_seed_sign']]);faces=list(TS)+[SHARED_Q]
    core10=core_audit(co,faces,18);sectors=[]
    need(len(cert['base_Qs'])==2,'two shared-four Q completions')
    for row in cert['base_Qs']:
        f,a,new,b=row
        need(new not in co,'preserve original core labels')
        sectors.append(sector(co,faces,f,a,b));co[new]=qopp(co[f],co[a],co[b]);faces.append(tuple(row))
    need(set(co)==set(range(12)),'twelve original core labels')
    core12=core_audit(co,faces,22)
    need(len(cert['last_Qs'])==3,'three last Q completions')
    for row in cert['last_Qs']:
        f,a,new,b=row
        need(new not in co,'new formal label, potential original alias retained')
        sectors.append(sector(co,faces,f,a,b));co[new]=qopp(co[f],co[a],co[b]);faces.append(tuple(row))
    need(set(co)==set(range(15)),'fifteen formal positions, NOT asserted all distinct')
    poles(co)
    i,j=cert['alias_pair'];bad=C-dot(co[i],co[j])
    need(sign(bad)==-1,'uniform forbidden gap forces original alias')
    p=tuple(cert['alias_polynomial']);delta=co[i][1]-co[j][1]
    need(delta.n==mul((0,-2),p),'second coordinate difference numerator is -2cP')
    need(bsign(delta.d) in (-1,1),'alias coordinate denominator nonzero')
    left,right=map(lambda q:F(*q),cert['root_strip'])
    need(LO<left<right<HI,'strict internal root strip')
    need(bsign(p,LO,left,True)==1,'no alias-polynomial root below strip, endpoints included')
    need(bsign(p,right,HI,True)==-1,'no alias-polynomial root above strip, endpoints included')
    a,b=cert['distinct_pair'];distance=U-dot(co[a],co[b]);gap=C-dot(co[a],co[b])
    need(sign(distance)==1,'critical other positions are always distinct')
    need(sign(gap,left,right,True)==-1,'distinct other points violate packing throughout root strip')
    return {'agent':'six-tammes-1','role':'researcher',
            'interval':('1/2','3/5'),'branches':branches,
            'core10':core10,'core12':core12,'forced_missing_sectors':sectors,
            'last_Qs':cert['last_Qs'],'all_fifteen_formal_positions_unit':True,
            'all_fifteen_formal_positions_distinct_asserted':False,
            'forbidden_alias_gap':sign_record(bad),
            'alias_coordinate_difference':{'n':delta.n,'d':delta.d,'factor':(0,-2),'P':p},
            'P_positive_below_strip':sign_record(Rat(p),LO,left,True),
            'P_negative_above_strip':sign_record(Rat(p),right,HI,True),
            'distinct_critical_pair':{'pair':(a,b),'distance':sign_record(distance)},
            'forbidden_strip_gap':{'pair':(a,b),'gap':sign_record(gap,left,right,True)},
            'conclusion':'No double-five Q; aliases and strip endpoints included.'}

def controls(cert):
    changes=(('wrong_B_seed',lambda c:c.update(B_seed_sign=-1)),
             ('wrong_base_Q_endpoint',lambda c:c['base_Qs'][0].__setitem__(1,5)),
             ('reused_original_core_label',lambda c:c['base_Qs'][0].__setitem__(2,8)),
             ('omitted_base_Q',lambda c:c['base_Qs'].pop()),
             ('wrong_last_Q_endpoint',lambda c:c['last_Qs'][0].__setitem__(1,6)),
             ('omitted_last_Q',lambda c:c['last_Qs'].pop()),
             ('wrong_alias_pair',lambda c:c.update(alias_pair=[12,13])),
             ('alias_pair_claimed_distinct',lambda c:c.update(distinct_pair=[12,14])),
             ('wrong_alias_polynomial',lambda c:c['alias_polynomial'].__setitem__(0,2)),
             ('root_strip_misses_root',lambda c:c.update(root_strip=[[14,25],[57,100]])))
    rows=[]
    for name,mutate in changes:
        c=copy.deepcopy(cert);mutate(c)
        try:verify(c)
        except (ValueError,KeyError) as err:rows.append({'name':name,'rejected':True,'reason':str(err)})
        else:raise ValueError('negative control accepted: '+name)
    return rows

def main():
    cert=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    result=verify(cert);result['controls']=controls(cert)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
