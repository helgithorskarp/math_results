"""Small characteristic-zero arithmetic over Q(omega), omega^2=omega-1."""
from fractions import Fraction
import hashlib
import json

ZERO=(Fraction(0),Fraction(0))
ONE=(Fraction(1),Fraction(0))
UNITS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def need(condition,message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def add(a,b):
    return (a[0]+b[0],a[1]+b[1])


def mul(a,b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]+a[1]*b[1])


def conj(a):
    return (a[0]+a[1],-a[1])


def canonical(row):
    return min(tuple(mul(u,a) for a in row) for u in UNITS)


def padd(a,b,scale=1):
    result=dict(a)
    for ij,v in b.items():
        result[ij]=add(result.get(ij,ZERO),(scale*v[0],scale*v[1]))
        if result[ij]==ZERO:
            del result[ij]
    return result


def pmul(a,b):
    result={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            ij=i+k,j+l
            result[ij]=add(result.get(ij,ZERO),mul(x,y))
    return {ij:v for ij,v in result.items() if v!=ZERO}


def pconj(a):
    return {ij:conj(v) for ij,v in a.items()}


def decode(terms):
    need(terms==sorted(terms),'sorted coefficient terms')
    result={}
    for i,j,a,b,d in terms:
        need(all(type(v) is int for v in (i,j,a,b,d)) and i>=0 and j>=0 and d>0,'exact coefficient domain')
        need((i,j) not in result and (a or b),'distinct nonzero terms')
        result[i,j]=(Fraction(a,d),Fraction(b,d))
    return result


PONE={(0,0):ONE}
U={(1,0):ONE}
V={(0,1):ONE}
UP=padd(PONE,U)
VP=padd(PONE,V)
D=pmul(UP,VP)
D2=pmul(D,D)


def equations(rows):
    result=[]
    for a,b,c in rows:
        linear={(0,0):a,(1,0):b,(0,1):c}
        ac,bc,cc=map(conj,(a,b,c))
        opposite=padd(padd(pmul({(0,0):ac},D),pmul({(1,0):bc},VP),-1),pmul({(0,1):cc},UP),-1)
        g=padd(pmul(linear,opposite),D,-1)
        if g:
            result.append(g)
    need(len(result)==3,'two anchor equations eliminate and three remain')
    return result


def targets(exceptional):
    if not exceptional:
        return [('contradiction',D2)]
    return [('difference',pmul(D2,padd(U,V,-1))),
            ('norm',pmul(D2,{(0,0):ONE,(0,1):ONE,(0,2):(Fraction(4),Fraction(0))}))]


def check_identities(certificate,keys):
    need(certificate['schema']=='hn-radix-two-coordinate-identities-v1','identity schema')
    forms=certificate['normal_forms']
    need(len(forms)==len(keys)==32,'32 complete normal forms')
    checked=0
    for index,(entry,key) in enumerate(zip(forms,keys)):
        need(entry['normalized_rows']==[[list(d) for d in row] for row in key],'exact normalized input rows')
        generators=equations(key)
        goals=targets(index==0)
        need(len(entry['identities'])==len(goals),'complete identity list')
        for identity,(name,target) in zip(entry['identities'],goals):
            need(identity['claim']==name and len(identity['multipliers'])==3,'identity target and arity')
            total={}
            for raw,g in zip(identity['multipliers'],generators):
                m=decode(raw)
                need(all(i+j<=identity['multiplier_degree_bound'] for i,j in m),'multiplier degree bound')
                total=padd(total,pmul(m,g))
            need(total==target,'exact polynomial identity over Q(omega)')
            checked+=1
    return checked
