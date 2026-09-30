"""Exact noncoincidence of the exceptional bridge, with B anchors8,9,10."""
from fractions import Fraction
from field import Field
from family import one,zero,t,REF,KAPPA,HI,DH,dot,cross,matvec,branch_field
from polynomial import need,root_count,value,mul
from itertools import combinations

EDGES=frozenset(((0,1),(0,4),(0,5),(0,6),(0,7),(1,2),(1,3),(1,4),(2,3),(3,4),(4,5),(5,6),(6,7)))

def real_field(p,bracket):
    lo,hi=(Fraction(*q) for q in bracket)
    need(Fraction(1,2)<lo<hi<Fraction(3,5),'exception root domain')
    need(root_count(p)==root_count(p,lo,hi)==1,'exception root counts')
    sl,sh=value(p,lo),value(p,hi);need(sl*sh<0,'exception root endpoints')
    for _ in range(160):
        mid=(lo+hi)/2;sm=value(p,mid);need(sm!=0,'unexpected rational exception root')
        if sm*sl>0:lo,sl=mid,sm
        else:hi,sh=mid,sm
    return Field(p,((lo.numerator,lo.denominator),(hi.numerator,hi.denominator)))

def recipe():
    from family import sign_open
    a={0:[one,zero,zero],6:[zero,one,zero],7:[zero,zero,one]}
    for v,i,j,old in ((5,0,6,7),(4,0,5,6),(1,0,4,5),(3,1,4,0),(2,1,3,4)):
        a[v]=[REF*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
    need(all(not (dot(x,x)-one).n for x in a.values()),'exception A norms')
    need(all(not (dot(a[i],a[j])-t).n for i,j in EDGES),'exception A contacts')
    w=dot(a[2],a[7]);c=[t/(one+w)*(x+y) for x,y in zip(a[2],a[7])]
    n=matvec(HI,cross(a[2],a[7]));D=DH*(one+w-2*t*t)/((one+w)**2*(one-w))
    v=[REF*(x+y)-z for x,y,z in zip(a[5],a[6],a[0])]
    alpha=dot(c,v)-KAPPA;beta=dot(n,v);R=alpha*alpha-D*beta*beta
    need(sign_open(alpha)==-1 and sign_open(beta)==sign_open(D)==1,'physical exceptional ear')
    u=[x-alpha/beta*y for x,y in zip(c,n)]
    return {'a':a},{'u':u,'v':v},R

def verify(entry):
    p=tuple(entry['root_polynomial']);f=real_field(p,entry['root_bracket']);model,case,R=recipe()
    need(len(p)==16 and R.n==mul(mul((-1,1),(-1,1)),p),'exception polynomial identity')
    results=[]
    for orientation in (-1,1):
        points=branch_field(model,case,orientation,f)
        need(all(f.dot(x,x)==f.one for x in points.values()),'exception13norms')
        need(all(f.sign(f.sub(f.one,f.dot(points[i],points[j])))==1 for i,j in combinations(range(13),2)),'exception actual noncoincidence')
        results.append({'orientation':orientation,'strictly_distinct_pairs':78,'A_B_cross_pairs':40})
    return {'root_degree':15,'branches':results,'A_B_coincidences':0,'local_scope':'With only B ears outside A, any packing realization is forced to have all13 original positions distinct; prior saturation theorem then applies.'}
