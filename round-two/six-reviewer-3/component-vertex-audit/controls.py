"""Fresh exact quadratic-field matrices, Gaussian vertices and semantic controls.

Uses the credited literal frame DAG; no integer-image identity arithmetic,
primitive factors, author's inputs or frozen outputs are used by this engine.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
from itertools import combinations
from geometry import model, LABELS, CONTACTS

ROLES = [((0,6,7), 0, 99), ((1,4,12), 1, 99), ((2,8,10), 2, 98),
         ((5,7,9), 5, 10), ((6,9,11), 11, 98)]
CAPS = {98: ((-8,12,-5), 9), 99: ((-5,-14,20), 15)}


class Field:
    def __init__(self, square):
        self.square = F(square)
        if self.square <= 0:
            raise ValueError('strict positive signed-root square required')
        n, d = isqrt(self.square.numerator), isqrt(self.square.denominator)
        self.rational_root = F(n,d) if n*n==self.square.numerator and d*d==self.square.denominator else None

    def value(self, a=0, b=0):
        a, b = F(a), F(b)
        if self.rational_root is not None:
            a, b = a+b*self.rational_root, F(0)
        return Number(a,b,self)


class Number:
    def __init__(self, a, b, field): self.a, self.b, self.field = a,b,field
    def coerce(self, v):
        if isinstance(v, Number):
            if v.field is not self.field: raise ValueError('different real fields')
            return v
        return self.field.value(v)
    def __add__(self, v):
        v=self.coerce(v);return self.field.value(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return self.field.value(-self.a,-self.b)
    def __sub__(self,v):return self+-self.coerce(v)
    def __rsub__(self,v):return self.coerce(v)+-self
    def __mul__(self,v):
        v=self.coerce(v)
        return self.field.value(self.a*v.a+self.b*v.b*self.field.square,self.a*v.b+self.b*v.a)
    __rmul__=__mul__
    def __truediv__(self,v):
        v=self.coerce(v);n=v.a*v.a-v.b*v.b*self.field.square
        if n==0:raise ValueError('zero field divisor')
        return self*self.field.value(v.a/n,-v.b/n)
    def __rtruediv__(self,v):return self.coerce(v)/self
    def sign(self):
        if self.b==0:return (self.a>0)-(self.a<0)
        if self.a==0:return (self.b>0)-(self.b<0)
        if (self.a>0)==(self.b>0):return (self.a>0)-(self.a<0)
        comparison=self.a*self.a-self.b*self.b*self.field.square
        if comparison==0:return 0
        return ((comparison>0)-(comparison<0))*((self.a>0)-(self.a<0))
    def same(self,v):return (self-self.coerce(v)).sign()==0
    def record(self):return [str(self.a),str(self.b)]


def gram(u,v,t):
    # A separate full nine-term physical matrix multiplication.
    return sum(u[i]*v[j]*(1 if i==j else t) for i in range(3) for j in range(3))


def solve(matrix,rhs):
    a=[list(row)+[rhs[i]] for i,row in enumerate(matrix)]
    for j in range(3):
        pivot=next((i for i in range(j,3) if a[i][j].sign()!=0),None)
        if pivot is None:raise ValueError('singular physical active basis')
        a[j],a[pivot]=a[pivot],a[j]
        divisor=a[j][j];a[j]=[v/divisor for v in a[j]]
        for i in range(3):
            if i==j:continue
            multiplier=a[i][j];a[i]=[a[i][k]-multiplier*a[j][k] for k in range(4)]
    return [a[i][3] for i in range(3)]


def vertices_at(t,z,known_root=None,require_packing=False):
    t,z=F(t),F(z);m=model()
    @lru_cache(None)
    def scalar(n):
        if n.op=='c':return F(n.args[0])
        if n.op=='t':return t
        if n.op=='z':return z
        if n.op=='+':return scalar(n.args[0])+scalar(n.args[1])
        if n.op=='-':return -scalar(n.args[0])
        if n.op=='*':return scalar(n.args[0])*scalar(n.args[1])
        raise ValueError('unknown literal frame operation')
    R,O=scalar(m['R']),scalar(m['Omega']);field=Field(R)
    if O<=0:raise ValueError('positive physical clearing denominator required')
    if known_root is not None and (F(known_root)<=0 or F(known_root)**2!=R):
        raise ValueError('wrong original positive radical')
    p={i:[field.value(scalar(q.p),scalar(q.q))/O for q in m['Y'][i]] for i in LABELS}
    for i in LABELS:
        if not gram(p[i],p[i],t).same(1):raise ValueError('actual original unit fails')
    for i,j in CONTACTS:
        if not gram(p[i],p[j],t).same(t):raise ValueError('actual original contact fails')
    packing=[[i,j,gram(p[i],p[j],t).record(),(t-gram(p[i],p[j],t)).sign()]
             for i,j in combinations(LABELS,2)]
    if require_packing and any(row[-1]<0 for row in packing):
        raise ValueError('credited control is not an original packing')
    normals={**p,**{i:[field.value(v) for v in n] for i,(n,rhs) in CAPS.items()}}
    values=[];semantic_rejections=[]
    for triple,central,violated in ROLES:
        matrix=[[sum(normals[i][j]*(1 if j==k else t) for j in range(3)) for k in range(3)] for i in triple]
        x=solve(matrix,[field.value(t)]*3)
        a,b,c,L=1+t,1-t,1+2*t,7*t*t+2*t-1
        ends=[i for i in triple if i!=central]
        intrinsic=[t*(a*a*(p[ends[0]][k]+p[ends[1]][k])-L*p[central][k])/(b*b*c) for k in range(3)]
        if not all(x[k].same(intrinsic[k]) for k in range(3)):
            raise ValueError('whole Gaussian/intrinsic vertex differs')
        if not all(gram(p[i],x,t).same(t) for i in triple):
            raise ValueError('actual active equations fail')
        norm=t*t*(5*t+3)/(b*c)
        if not gram(x,x,t).same(norm) or norm<=1:
            raise ValueError('actual long vertex/norm fails')
        comparisons={i:gram(n,x,t)-(CAPS[i][1] if i in CAPS else t) for i,n in normals.items()}
        if comparisons[violated].sign()<=0:
            raise ValueError('physical original inequality not violated')
        # Real changes of physical coordinates or actual cap direction must fail.
        damage_x=list(x);damage_x[0]=damage_x[0]+1
        if all(gram(p[i],damage_x,t).same(t) for i in triple):
            raise ValueError('damaged physical vertex accepted')
        semantic_rejections.append({'triple':list(triple),'actual_coordinate_plus1_rejected':True})
        wrong=[v+1 if k==0 else v for k,v in enumerate(normals[violated])]
        if gram(wrong,x,t).same(gram(normals[violated],x,t)):
            raise ValueError('damaged actual normal undetected')
        semantic_rejections.append({'triple':list(triple),'actual_normal_plus1_changes_whole_product':True})
        values.append({'triple':list(triple),'central':central,'whole_original_vertex':[v.record() for v in x],
                       'norm':str(norm),'all14_physical_excesses':[[i,v.record(),v.sign()] for i,v in comparisons.items()],
                       'required_violated_original_plane':violated})
    return {'t':str(t),'z':str(z),'positive_square':str(R),'rational_root':str(field.rational_root) if field.rational_root is not None else None,
            'Omega':str(O),'all66_actual_core_pair_products':packing,
            'packing_required_for_credited_control_only':require_packing,
            'all5_original_vertices':values,'actual_semantic_rejections':semantic_rejections}


def signed_implication(A,B,w):
    A,B,w=F(A),F(B),F(w)
    if B<=0 or w<=0 or B*B*w*w-A*A<=0:
        raise ValueError('strict signed-square hypotheses absent')
    if A+B*w<=0:raise ValueError('claimed positive actual excess fails')
    return [str(A),str(B),str(w),str(A+B*w)]


def check():
    controls=[vertices_at('29/50','5400/3973','454484658996081/225033203125000',True)]
    for t in ['14/25','3/5']:
        for z in ['6/5','7/5']:controls.append(vertices_at(t,z))
    positive=[signed_implication(A,1,3) for A in [-2,0,2]]
    negative=[]
    for A,B,w in [(-2,1,-3),(0,1,0),(2,1,2),(0,0,3),(0,-1,3)]:
        try:signed_implication(A,B,w)
        except ValueError:negative.append([A,B,w])
        else:raise ValueError('missing signed-square premise accepted')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'independent_Fraction_quadratic_field_Gaussian_controls':controls,
            'all25_physical_vertices_with_every14_original_plane':True,
            'all5_cores_full_units_contacts_and66_pair_lists':True,
            'core_packing_claim_only_at_credited10012_control':True,
            'signed_square_positive_controls':positive,'missing_premises_rejected':negative,
            'negative_root_false_converse_witness':{'A':-2,'B':1,'w':-3,'square_excess':5,'actual_excess':-5},
            'new_target_factor_program_or_expected_input':False,
            'no_integer_image_or_interval_sign_engine_in_this_program':True}


if __name__=='__main__':
    import json
    print(json.dumps(check(),sort_keys=True,separators=(',',':')))
