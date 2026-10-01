"""Check one exact fifteen-point extension. Standard-library Python only.

Coordinates are rational in a basis with Gram matrix (1-c)I+cJ.
Positive eigenvalues establish its faithful Euclidean realization in R3.
No search, optimizer, tolerance or external data enters this checker.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import hashlib,json

HERE=Path(__file__).resolve().parent
CONTACTS=((0,1),(0,7),(1,2),(1,7),(2,3),(2,6),(2,7),
          (3,4),(3,5),(3,6),(4,5),(5,6),(6,7))

def need(condition,message):
    if not condition:raise ValueError(message)

def pair(x):return [x.numerator,x.denominator]
def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def check():
    path=HERE/'certificate.json';data=json.loads(path.read_text())
    need(data['schema']=='tammes15-octagon2-extension-v1','fixed schema')
    need(data['cosine']==[59479,100000],'fixed rational cosine')
    need(data['core_labels']==list(range(8)) and data['extra_labels']==list(range(8,15)),'fifteen distinct labels')
    need(data['required_core_contacts']==[list(p) for p in CONTACTS],'fixed thirteen-contact pattern')
    c=Q(*data['cosine']);r=2*c/(1+c)
    need(1-c>0 and 1+2*c>0,'positive definite rank-three Gram matrix')
    points=[[r*r-1,-r,r+r*r],[r,-1,r],[Q(1),Q(0),Q(0)],[r,r,-1],
            [r**3+r*r-r,r**3+2*r*r-1,-r-r*r],
            [r*r-1,r+r*r,-r],[Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(1)]]
    points=[[Q(x) for x in a] for a in points]
    def dot(a,b):return (1-c)*sum(x*y for x,y in zip(a,b))+c*sum(a)*sum(b)
    denominator=data['extra_chart_denominator'];numerators=data['extra_chart_numerators']
    need(type(denominator) is int and denominator==100000,'fixed chart grid')
    need(len(numerators)==7 and all(len(row)==2 and all(type(n) is int for n in row) for row in numerators),
         'seven rational chart pairs')
    for a,b in numerators:
        u,v=Q(a,denominator),Q(b,denominator)
        need(-4<=u<=4 and -4<=v<=4,'chart bounds')
        R=1+(1-c*c)*(u*u+v*v)+2*c*(1-c)*u*v
        need(R>0,'positive chart denominator')
        points.append([(R-2-2*c*(u+v))/R,2*u/R,2*v/R])
    need(all(dot(a,a)==1 for a in points),'all fifteen exact unit identities')
    gaps=[(i,j,c-dot(points[i],points[j])) for i,j in combinations(range(15),2)]
    need(len(gaps)==105 and all(g>=0 for _,_,g in gaps),'all105 exact pair inequalities')
    actual=[(i,j) for i,j,g in gaps if g==0]
    need(actual==list(CONTACTS),'exact contacts are precisely the thirteen fixed core edges')
    strict=[g for _,_,g in gaps if g>0]
    return {'agent':'six-tammes-2','role':'researcher',
            'status':'EXACT_FIFTEEN_POINT_EIGHT_CORE_EXTENSION',
            'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'cosine':pair(c),'core_points':8,'extension_points':7,'unit_identities':15,
            'pair_inequalities':105,'exact_contacts':13,'strict_pairs':len(strict),
            'minimum_strict_gap':pair(min(strict)),
            'coefficient_coordinates_sha256':digest([[pair(x) for x in a] for a in points]),
            'pair_gaps_sha256':digest([[i,j,pair(g)] for i,j,g in gaps]),
            'scope':'Exact construction with minimum separation arccos(59479/100000). Positive Gram eigenvalues give a realization in R3. No global or conditional optimality claimed.'}

if __name__=='__main__':print(json.dumps(check(),indent=2,sort_keys=True))
