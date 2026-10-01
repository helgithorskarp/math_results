"""Separate exact QQ geometry check; no import of check.py or discovery code.

Core coordinates come from ordered common-neighbor reflections. Extras
come from tangent vectors orthogonal to anchor2 and their metric norm.
Inner products use all nine explicit Gram-matrix entries. This audit is
same-author algorithmic validation, not independent peer review.
"""
from pathlib import Path
from itertools import combinations
import hashlib,json
from sympy.polys.domains import QQ

HERE=Path(__file__).resolve().parent
FOLDS=((1,2,7,6),(3,2,6,7),(0,1,7,2),(5,3,6,2),(4,3,5,6))
CONTACTS=((0,1),(0,7),(1,2),(1,7),(2,3),(2,6),(2,7),
          (3,4),(3,5),(3,6),(4,5),(5,6),(6,7))
def need(condition,message):
    if not condition:raise ValueError(message)
def pair(x):return [int(x.numerator),int(x.denominator)]
def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def audit():
    path=HERE/'certificate.json';data=json.loads(path.read_text())
    need(data['schema']=='tammes15-octagon2-extension-v1','native fixed schema')
    need(data['cosine']==[59479,100000],'native fixed cosine')
    need(data['core_labels']==list(range(8)) and data['extra_labels']==list(range(8,15)),'native exact labels')
    need(data['required_core_contacts']==[list(p) for p in CONTACTS],'native prescribed pattern')
    c=QQ(*data['cosine']);one=QQ.one;zero=QQ.zero
    need(one-c>0 and one+2*c>0,'native positive Gram eigenvalues')
    H=[[one if i==j else c for j in range(3)] for i in range(3)]
    def dot(a,b):return sum((a[i]*H[i][j]*b[j] for i in range(3) for j in range(3)),zero)
    points={2:[one,zero,zero],6:[zero,one,zero],7:[zero,zero,one]}
    r=2*c/(one+c)
    for new,i,j,old in FOLDS:
        need(new not in points and all(k in points for k in (i,j,old)),'native ordered fold')
        need(dot(points[i],points[j])==c and dot(points[i],points[old])==c
             and dot(points[j],points[old])==c,'native fold is a contact triangle')
        points[new]=[r*(points[i][k]+points[j][k])-points[old][k] for k in range(3)]
    denominator=data['extra_chart_denominator'];numerators=data['extra_chart_numerators']
    need(type(denominator) is int and denominator==100000,'native fixed chart grid')
    need(len(numerators)==7 and all(len(row)==2 and all(type(n) is int for n in row) for row in numerators),
         'native seven integer pairs')
    anchor=points[2]
    for label,(a,b) in zip(range(8,15),numerators):
        u,v=QQ(a,denominator),QQ(b,denominator)
        need(-4<=u<=4 and -4<=v<=4,'native chart bounds')
        tangent=[-c*(u+v),u,v]
        need(dot(tangent,anchor)==0,'native tangent orthogonality')
        N=dot(tangent,tangent)
        need(N>=0,'native nonnegative tangent norm')
        points[label]=[((N-one)*anchor[k]+2*tangent[k])/(N+one) for k in range(3)]
    need(set(points)==set(range(15)),'native fifteen labels')
    need(all(dot(points[i],points[i])==one for i in range(15)),'native every exact unit identity')
    gaps=[(i,j,c-dot(points[i],points[j])) for i,j in combinations(range(15),2)]
    need(all(g>=0 for _,_,g in gaps),'native all105 nonnegative gaps')
    need([(i,j) for i,j,g in gaps if g==0]==list(CONTACTS),'native exact contact set')
    strict=[g for _,_,g in gaps if g>0]
    return {'agent':'six-tammes-2','role':'researcher',
            'status':'SEPARATE_NATIVE_QQ_CONSTRUCTION_AUDIT_COMPLETED',
            'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'cosine':pair(c),'core_points':8,'extension_points':7,'unit_identities':15,
            'pair_inequalities':105,'exact_contacts':13,'strict_pairs':len(strict),
            'minimum_strict_gap':pair(min(strict)),
            'coefficient_coordinates_sha256':digest([[pair(x) for x in points[i]] for i in range(15)]),
            'pair_gaps_sha256':digest([[i,j,pair(g)] for i,j,g in gaps]),
            'scope':'Separate same-author QQ audit using reflected core, tangent stereographic construction and explicit matrix metric. No independent peer review or formalization, no optimization inference.'}

if __name__=='__main__':print(json.dumps(audit(),indent=2,sort_keys=True))
