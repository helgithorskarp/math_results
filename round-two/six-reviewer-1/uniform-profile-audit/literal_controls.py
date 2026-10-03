"""Fresh four balanced profiles, direct eight-factor product and residual root
recursion in E[beta]/(beta^2-H/N). Real beta is the positive square root.

No claim of finite-parameter feasibility follows from a fourth jet alone.
"""
from fractions import Fraction as Q
from math import comb
from field import E,I,W,need
import poly as P
import jets as J


class X:
    __slots__=('a','b')
    radicand=E(1)
    def __init__(self,a=0,b=0):
        if isinstance(a,X):self.a,self.b=a.a,a.b
        else:self.a,self.b=E(a),E(b)
    def __bool__(self):return bool(self.a)or bool(self.b)
    def __eq__(self,other):
        other=X(other)
        return self.a==other.a and self.b==other.b
    def __add__(self,other):
        other=X(other);return X(self.a+other.a,self.b+other.b)
    __radd__=__add__
    def __neg__(self):return X(-self.a,-self.b)
    def __sub__(self,other):return self+-X(other)
    def __rsub__(self,other):return X(other)+-self
    def __mul__(self,other):
        other=X(other)
        if not self or not other:return X(0)
        return X(self.a*other.a+X.radicand*self.b*other.b,
                 self.a*other.b+self.b*other.a)
    __rmul__=__mul__
    def __pow__(self,n):
        out=X(1)
        for _ in range(n):out=out*self
        return out
    def conjugate(self):return X(self.a.conjugate(),self.b.conjugate())
    def record(self):return [self.a.record(),self.b.record()]


def peval(p,values):
    out=X(0)
    for e,c in p.items():
        term=X(c)
        for j,n in enumerate(e):term=term*values[j]**n
        out=out+term
    return out


def smul(a,b):
    out=[X(0)for _ in range(5)]
    for j,c in enumerate(a):
        if not c:continue
        for k,d in enumerate(b):
            if j+k<=4 and d:out[j+k]=out[j+k]+c*d
    return out


def sadd(a,b):return [a[j]+b[j]for j in range(5)]


def sscale(a,c):return [v*c for v in a]


def spower(a,n):
    out=[X(1),X(0),X(0),X(0),X(0)]
    for _ in range(n):out=smul(out,a)
    return out


PROFILES=[(1,-1,0,0,0,0,0,0),(7,-1,-1,-1,-1,-1,-1,-1),
          (1,1,1,1,-1,-1,-1,-1),(3,2,1,0,-1,-1,-2,-2)]


def run(primary,indices=(0,1,2,3)):
    record=[];comparisons=0
    for index in indices:
        w=PROFILES[index]
        norm=sum(v*v for v in w);X.radicand=J.H/norm
        beta=X(0,1);v=[beta*a for a in w]
        need(sum(v,X())==0 and sum((a*a for a in v),X())==X(J.H),'literal balance and norm')
        cubic=sum((a**3 for a in v),X());quartic=sum((a**4 for a in v),X())
        values=[cubic,quartic,X(0),X(0),X(0),X(0)]
        base={int(key):{tuple(e):E(c)for e,c in p}for key,p in primary['base_controls'].items()}
        for key,p in base.items():values[key]=peval(p,values)
        critical=[]
        for a in v:
            u=X(J.A0)+cubic*a*X(J.ell/J.H)-X(J.rho)*a*a
            critical.append([X(0),X(I)*a,u,X(I)*(values[2]+values[5]*a),values[4]])
        # Polynomial in z whose coefficients are independently truncated t-series.
        product=[[X(1),X(0),X(0),X(0),X(0)]]
        for zeta in critical:
            out=[[X(0)for _ in range(5)]for _ in range(len(product)+1)]
            for h,a in enumerate(product):
                out[h]=sadd(out[h],smul(a,sscale(zeta,-1)))
                out[h+1]=sadd(out[h+1],a)
            product=out
        derivative=[sscale(a,9)for a in product]
        primitive=[[X(0)for _ in range(5)]for _ in range(10)]
        for h,a in enumerate(derivative):
            primitive[h+1]=sscale(a,Q(1,h+1))
        anchor=[X(1),X(0),X(-1),X(0),X(0)]
        for h,a in enumerate(primitive[1:],1):
            primitive[0]=sadd(primitive[0],sscale(smul(a,spower(anchor,h)),-1))
        for t in range(5):
            formal={h:peval({tuple(e):E(c)for e,c in p},values)
                    for h,p in primary['whole_primitive_maps'][t]}
            formal={h:a for h,a in formal.items()if a}
            actual={h:a[t]for h,a in enumerate(primitive)if a[t]}
            need(actual==formal,'literal whole anchored primitive '+str(w)+'/'+str(t));comparisons+=1
        def residual(root):
            out=[X(0)for _ in range(5)]
            for h,a in enumerate(primitive):out=sadd(out,smul(a,spower(root,h)))
            return out
        need(not any(residual(anchor)),'literal marked anchor identity');comparisons+=1
        roots=[];normals=[]
        for j in range(9):
            z=W**j;root=[X(z),X(0),X(0),X(0),X(0)]
            for t in range(1,5):
                value=residual(root)[t];root[t]=root[t]-value*X(1/(9*z**8))
            need(not any(residual(root)),'literal all-nine root residual');comparisons+=1
            expected=[peval({tuple(e):E(c)for e,c in p},values)
                      for p in primary['whole_root_jets'][j]]
            need(root[1]==0 and root[2:]==expected,'literal residual jets vs formal jets');comparisons+=1
            squared=smul(root,[a.conjugate()for a in root])
            normal=sscale(sadd(squared,[X(-1),X(0),X(0),X(0),X(0)]),Q(1,2))
            expected=[peval({tuple(e):E(c)for e,c in p},values)
                      for p in primary['whole_individual_normals'][j]]
            need(normal[2:]==expected,'literal all-nine normals vs formal normals');comparisons+=1
            roots.append([a.record()for a in root]);normals.append([a.record()for a in normal])
        cost=[X(0)for _ in range(5)]
        for zeta in critical:
            distance=sadd(anchor,sscale(zeta,-1))
            squared=smul(distance,[a.conjugate()for a in distance])
            deviation=sadd(squared,[X(-1),X(0),X(0),X(0),X(0)])
            inverse=[X(1),X(0),X(0),X(0),X(0)]
            for n,c in [(1,Q(-1,2)),(2,Q(3,8)),(3,Q(-5,16)),(4,Q(35,128))]:
                inverse=sadd(inverse,sscale(spower(deviation,n),c))
            cost=sadd(cost,inverse)
        expected=[peval({tuple(e):E(c)for e,c in p},values)for p in primary['whole_objective']]
        need(cost==expected,'literal full objective vs moment objective');comparisons+=1
        record.append({'balanced_integer_direction':list(w),'positive_radical_squared':X.radicand.record(),
                       'full_primitive':[[a.record()for a in row]for row in primitive],
                       'all_nine_residual_roots':roots,'all_nine_individual_normals':normals,
                       'full_objective':[a.record()for a in cost]})
    return {'literal_profiles':record,'literal_comparisons':comparisons}


if __name__=='__main__':
    import json,hashlib,argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--profile',type=int,choices=range(4),required=True)
    args=parser.parse_args()
    out=run(J.run(),(args.profile,));data=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'record_sha256':hashlib.sha256(data).hexdigest(),'record_bytes':len(data),
                      'literal_comparisons':out['literal_comparisons']}))
