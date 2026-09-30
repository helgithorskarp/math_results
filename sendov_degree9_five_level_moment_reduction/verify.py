#!/usr/bin/env python3
"""Degree-nine five-level active-moment reduction, exact author certificate.

Actual author six-sendov-2, researcher. Standard library, exact Q[x,y,z]
and Fraction arithmetic. The rational/commutant kernel openly adapts the
author's four-level source. No campaign import, floating proof input or
external solver. Written projection and exhaustive-chart bridges remain
ordinary mathematics; independent review of this extension is pending.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import argparse, hashlib, json

CHECKS=0
def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)

class P:
    """Sparse exact Q[x0,x1,x2]; exponent order is explicit and fixed."""
    def __init__(self, value=0):
        if isinstance(value, P):
            value = value.t
        if isinstance(value, (int, F)):
            value = {(0, 0, 0): F(value)}
        self.t = {tuple(e): F(c) for e, c in value.items() if c}
        if any(len(e) != 3 or any(k < 0 for k in e) for e in self.t):
            raise ValueError('invalid polynomial exponent')

    def __add__(self, other):
        out = dict(self.t)
        for e, c in P(other).t.items():
            out[e] = out.get(e, F(0)) + c
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        out = {}
        for e, c in self.t.items():
            for h, b in P(other).t.items():
                k = tuple(x+y for x, y in zip(e, h))
                out[k] = out.get(k, F(0)) + c*b
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/F(scalar))

    def __pow__(self, n):
        if n < 0:
            raise ValueError('negative polynomial power')
        out, a = P(1), self
        while n:
            if n & 1:
                out *= a
            a *= a
            n //= 2
        return out

    def __eq__(self, other):
        return self.t == P(other).t

    def dump(self):
        return [[*e, str(c)] for e, c in sorted(self.t.items())]

def subst(poly, variables):
    powers = []
    for axis, v in enumerate(variables):
        degree = max((e[axis] for e in poly.t), default=0)
        row = [P(1)]
        for _ in range(degree):
            row.append(row[-1]*P(v))
        powers.append(row)
    out = P(0)
    for e, c in poly.t.items():
        term = P(c)
        for axis, k in enumerate(e):
            term *= powers[axis][k]
        out += term
    return out

def scalar(poly, values):
    out = subst(poly, values)
    require(not any(any(e) for e in out.t), 'evaluation is scalar')
    return out.t.get((0, 0, 0), F(0))

def derivative(poly, axis):
    return P({tuple(k-1 if i == axis else k for i, k in enumerate(e)):
              e[axis]*c for e, c in poly.t.items() if e[axis]})

def remove_monomial(poly, axis, power, name):
    require(all(e[axis] >= power for e in poly.t), name+' divisibility')
    reduced = P({tuple(k-power if i == axis else k for i, k in enumerate(e)):
                 c for e, c in poly.t.items()})
    variable = (X, H, U)[axis]
    require(reduced*variable**power == poly, name+' reconstruction')
    return reduced

def prod(values):
    out = P(1)
    for v in values:
        out *= v
    return out

def affine_power(poly, box):
    """Binomial affine substitution performed one axis at a time."""
    data = dict(poly.t)
    for axis, (a, b) in enumerate(box):
        out = {}
        for e, c in data.items():
            for k in range(e[axis]+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(e[axis], k)*a**(e[axis]-k)*(b-a)**k
        data = {e: c for e, c in out.items() if c}
    return data

def bernstein(poly, box):
    degrees = tuple(max((e[i] for e in poly.t), default=0) for i in range(3))
    normalized = affine_power(poly, box)
    data = dict(normalized)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in data.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*F(comb(k, e[axis]), comb(degree, e[axis]))
        data = {e: c for e, c in out.items() if c}
    indices = list(product(*(range(n+1) for n in degrees)))
    coefficients = [data.get(e, F(0)) for e in indices]
    # Independent inverse basis identity in the normalized power coordinates.
    inverse = dict(data)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in inverse.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(degree, k)*comb(k, e[axis])*(-1)**(k-e[axis])
        inverse = {e: c for e, c in out.items() if c}
    require(inverse == normalized, 'complete inverse Bernstein reconstruction')
    return coefficients, degrees

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def certificate(name, poly, box, strict=False):
    require(len(box) == 3 and all(a < b for a, b in box), name+' genuine box')
    coefficients, degrees = bernstein(poly, box)
    for value in coefficients:
        require(value > 0 if strict else value >= 0, name+' Bernstein sign')
    return {'name': name, 'box': [[str(a), str(b)] for a, b in box],
            'degrees': list(degrees), 'entries': len(coefficients),
            'zero': sum(c == 0 for c in coefficients), 'minimum': str(min(coefficients)),
            'polynomial_sha256': digest(poly.dump()),
            'coefficient_sha256': digest(list(map(str, coefficients)))}

def solve(a, b):
    n = len(b)
    a = [list(r)+[v] for r, v in zip(a, b)]
    for j in range(n):
        pivots = [i for i in range(j, n) if a[i][j]]
        require(bool(pivots), 'nonzero Gaussian pivot')
        i = pivots[0]
        a[j], a[i] = a[i], a[j]
        t = a[j][j]
        a[j] = [v/t for v in a[j]]
        for i in range(j+1, n):
            t = a[i][j]
            if t:
                a[i] = [u-t*v for u, v in zip(a[i], a[j])]
    out = [F(0)]*n
    for j in range(n-1, -1, -1):
        out[j] = a[j][-1]-sum(a[j][k]*out[k] for k in range(j+1, n))
    return out

def independent_rows(rows):
    pivots, selected = {}, []
    for original in rows:
        r = list(original)
        for j, b in sorted(pivots.items()):
            t = r[j]
            if t:
                r = [u-t*v for u, v in zip(r, b)]
        if any(r):
            j = next(j for j, v in enumerate(r) if v)
            t = r[j]
            pivots[j] = [v/t for v in r]
            selected.append(original)
    return selected

def pinching(theta):
    """Rational Frobenius projection of ww* to the symmetric commutant."""
    n = 8
    require(len(theta) == n and sum(theta) == 0, 'balanced definition control')
    a = [[(theta[i] if i == j else 0)-(theta[i]+theta[j])/n
          for j in range(n)] for i in range(n)]
    pairs = list(combinations_with_replacement(range(n), 2))
    weights = [F(1 if i == j else 2) for i, j in pairs]
    w = [theta[i]*theta[j]/n for i, j in pairs]
    all_rows = []
    for i in range(n):
        for j in range(i+1, n):
            row = []
            for h, k in pairs:
                v = (a[i][h] if k == j else 0)-(a[k][j] if i == h else 0)
                if h != k:
                    v += (a[i][k] if h == j else 0)-(a[h][j] if i == k else 0)
                row.append(v)
            all_rows.append(row)
    rows = independent_rows(all_rows)
    rhs = [sum(c*v for c, v in zip(row, w)) for row in rows]
    gram = [[sum(c*d/g for c, d, g in zip(row, other, weights))
             for other in rows] for row in rows]
    lam = solve(gram, rhs)
    projected = [v-sum(row[k]*b for row, b in zip(rows, lam))/weights[k]
                 for k, v in enumerate(w)]
    for row in all_rows:
        require(sum(c*v for c, v in zip(row, projected)) == 0,
                'original commutation constraint')
    residual = [u-v for u, v in zip(w, projected)]
    require(sum(g*u*v for g, u, v in zip(weights, projected, residual)) == 0,
            'Frobenius orthogonality')
    return sum(g*v*v for g, v in zip(weights, projected)), len(rows)


X,Y,Z=[P({tuple(int(i==j) for j in range(3)):1}) for i in range(3)]

def mm(a,b):
    n=len(a)
    return [[sum((a[i][h]*b[h][j] for h in range(n)),P(0))
             for j in range(n)] for i in range(n)]

def ms(a,c):return [[v*c for v in row] for row in a]
def ma(a,b):return [[u+v for u,v in zip(row,other)] for row,other in zip(a,b)]
def mt(a):return sum((a[i][i] for i in range(len(a))),P(0))

def trace_word_coefficients(degree):
    result={}
    for mask in range(1<<degree):
        positions=[i for i in range(degree) if mask>>i&1]
        if not positions:key=(degree,);coefficient=F(1)
        else:
            gaps=[(positions[(i+1)%len(positions)]-p)%degree or degree
                  for i,p in enumerate(positions)]
            key=tuple(sorted(gaps));coefficient=F((-1)**len(positions),8**len(positions))
        result[key]=result.get(key,F(0))+coefficient
    return result

def moment_oracle(masses,levels,target):
    mu2=sum((m*t**2 for m,t in zip(masses,levels)),P(0))
    mu4=sum((m*t**4 for m,t in zip(masses,levels)),P(0))
    aa=mu2**2+8*mu2-8*mu4
    bb=mu2**2-48*mu2+16*mu4+224-32*sum(
        ((m-1)*(1-t**2)**2 for m,t in zip(masses,levels)),P(0))
    bound=(target*mu2-122*mu2**2-224*mu4)*bb+45*aa**2
    return aa,bb,bound,mu2,mu4

def raw_cases():
    return {
      'double':([2,2,2,1,1],[P(-1),X,Y,Z,2-2*X-2*Y-Z],750),
      'singleton':([1,2,2,2,1],[P(-1),X,Y,Z,1-2*X-2*Y-2*Z],750),
      'heavy4':([1,1,1,1,4],[P(-1),X,Y,Z,(1-X-Y-Z)/4],650)}

def symbolic_compression(masses,levels,target):
    require(len(masses)==5 and sum(masses)==8,'five positive labels')
    theta=[t for m,t in zip(masses,levels) for _ in range(m)]
    require(sum(theta,P(0))==0,'polynomial balance')
    groups=[i for i,m in enumerate(masses) for _ in range(m)]
    eye=[[P(int(i==j)) for j in range(8)] for i in range(8)]
    ee=[[P(F(1,8)) for j in range(8)] for i in range(8)]
    pp=ma(eye,ms(ee,-1))
    diagonal=[[theta[i] if i==j else P(0) for j in range(8)] for i in range(8)]
    cc=[[diagonal[i][j]-(theta[i]+theta[j])/8 for j in range(8)] for i in range(8)]
    block=[[P(F(int(groups[i]==groups[j]),masses[groups[i]]))
            for j in range(8)] for i in range(8)]
    uu=ma(block,ms(ee,-1))
    ww=[[theta[i]*theta[j]/8 for j in range(8)] for i in range(8)]
    cc2=mm(cc,cc)
    zz=ma(uu,ms(mm(cc2,uu),-1))
    aa,bb,bound,mu2,mu4=moment_oracle(masses,levels,target)
    require(mm(pp,pp)==pp,'balanced projection idempotent')
    require(mm(uu,uu)==uu and mt(uu)==4,'block-balanced projector rank4')
    require(mm(mm(pp,diagonal),pp)==cc,'defining full8x8 compression')
    require(mm(uu,cc)==mm(cc,uu),'block invariance / commutation')
    require(mm(uu,ww)==ww and mm(ww,uu)==ww,'w lies in balanced block space')
    require(mt(ww)==mu2/8,'defining displacement norm')
    require(mt(cc2)==3*mu2/4,'full second compression trace')
    require(mt(mm(cc2,cc2))==mu4/2+mu2**2/32,'full fourth compression trace')
    require(all(zz[i][j]==zz[j][i] for i in range(8) for j in range(8)),
            'symmetric active test matrix')
    require(mm(zz,cc)==mm(cc,zz),'test matrix commutes with compression')
    require(mt(mm(ww,zz))==aa/64,'active test numerator')
    require(mt(mm(zz,zz))==bb/32,'subtract all known zero-weight modes')
    return {'masses':masses,'target':target,'levels':[p.dump() for p in levels],
            'polynomial_sha256':{name:digest(poly.dump()) for name,poly in
              zip(('A','B','bound','mu2','mu4'),(aa,bb,bound,mu2,mu4))}}

def charts():
    for half in (0,1):
        total=X+half
        difference=(2-total)*Y
        delta=(total if half==0 else 2-total)*Z
        a=(total+difference)/2;b=(total-difference)/2
        center=1-total
        yield 'double'+str(half),'double',[P(-1),a,b,center+delta,center-delta]
    for half in (0,1):
        a=X/3+(X+3)*Y/6 if half==0 else (X+1)/2+(1-X)*Y/2
        low=(X-a)/2
        width=(3*a-X)/2 if half==0 else (X-a+2)/2
        b=low+width*Z;c=X-a-b
        yield 'singleton'+str(half),'singleton',[P(-1),a,b,c,1-2*X]
    free=[2*X-1,2*Y-1,2*Z-1]
    yield 'heavy4','heavy4',[P(-1),*free,(1-sum(free,P(0)))/4]

def cover_tree(tree,box,poly,label,depth=0):
    require(depth<=24,label+' bounded cover depth')
    if tree=='active_bound':
        row=certificate(label+' active bound',poly,box)
        volume=prod_fraction(b-a for a,b in box)
        return [row],volume,1
    require(isinstance(tree,list) and len(tree)==3,label+' both closed children required')
    axis,left,right=tree
    require(type(axis) is int and axis in (0,1,2),label+' cube split axis')
    lo,hi=box[axis];mid=(lo+hi)/2
    records=[];volume=F(0);leaves=0
    for child,pair in ((left,(lo,mid)),(right,(mid,hi))):
        childbox=list(box);childbox[axis]=pair
        rows,size,count=cover_tree(child,childbox,poly,label,depth+1)
        records.extend(rows);volume+=size;leaves+=count
    require(volume==prod_fraction(b-a for a,b in box),label+' full closed cube cover')
    return records,volume,leaves

def prod_fraction(values):
    out=F(1)
    for v in values:out*=v
    return out

def reverse_chart(kind,levels):
    require(levels[0]==-1,'saturated negative label')
    if kind=='double':
        a,b=sorted(levels[1:3],reverse=True)
        c,d=sorted(levels[3:],reverse=True)
        total=a+b;delta=(c-d)/2
        require(0<=total<=2,'double sum covers[0,2]')
        half=int(total>1)
        u=(a-b)/(2-total) if total!=2 else F(0)
        width=min(total,2-total)
        v=delta/width if width else F(0)
        return 'double'+str(half),(total-half,u,v)
    if kind=='singleton':
        a,b,c=sorted(levels[1:4],reverse=True)
        total=a+b+c;threshold=(total+1)/2
        require(0<=total<=1,'singleton sum covers[0,1]')
        half=int(a>threshold)
        if half==0:
            u=(a-total/3)/((total+3)/6)
            width=(3*a-total)/2
        else:
            u=(a-threshold)/((1-total)/2) if total!=1 else F(0)
            width=(total-a+2)/2
        v=(b-(total-a)/2)/width if width else F(0)
        return 'singleton'+str(half),(total,u,v)
    require(kind=='heavy4','known inverse chart kind')
    return 'heavy4',tuple((t+1)/2 for t in levels[1:4])

def build(data):
    initial_checks=CHECKS
    require(set(data)=={'format','cases'} and
            data['format']=='closed-unit-cube-bisection-trees-v1',
            'exact cover schema')
    require(isinstance(data['cases'],list),'cover case list')
    lookup={}
    for row in data['cases']:
        require(set(row)=={'chart','tree'} and isinstance(row['chart'],str),
                'only chart names and bisection trees supplied')
        require(row['chart'] not in lookup,'no duplicated cube chart')
        lookup[row['chart']]=row['tree']
    chart_map={name:(kind,levels) for name,kind,levels in charts()}
    require(set(lookup)==set(chart_map) and len(chart_map)==5,
            'every required saturation/order cube and no extra cube')
    partitions={tuple(sorted(p,reverse=True)) for p in
                combinations_with_replacement(range(1,9),5) if sum(p)==8}
    require(partitions=={(4,1,1,1,1),(3,2,1,1,1),(2,2,2,1,1)},
            'all positive five-part partitions of8')
    words={}
    for degree,expected in [(2,{(2,):F(3,4),(1,1):F(1,64)}),
             (4,{(4,):F(1,2),(1,3):F(1,16),(2,2):F(1,32),
                 (1,1,2):F(-1,128),(1,1,1,1):F(1,4096)})]:
        derived=trace_word_coefficients(degree)
        require(derived==expected,'complete cyclic trace word expansion')
        words[str(degree)]=[[list(key),str(value)] for key,value in sorted(derived.items())]
    cases=raw_cases()
    symbolic={name:symbolic_compression(*row) for name,row in cases.items()}
    primitives={name:moment_oracle(*row) for name,row in cases.items()}
    unit=[(F(0),F(1))]*3
    entries=0;domain_entries=0;leaf_count=0
    output=[];controls=[];cache={};profile_refs=[];round_trips=0
    def definition_control(theta,label):
        key=tuple(sorted(theta))
        if key not in cache:
            require(sum(key)==0 and max(map(abs,key))==1,label+' definition normalization')
            psi,rank=pinching(key)
            mu2=sum(t*t for t in key);mu4=sum(t**4 for t in key)
            jj=(122*mu2**2+224*mu4-5760*psi)/mu2
            cache[key]=len(controls)
            controls.append({'label':label,'theta':list(map(str,key)),
                'mu2':str(mu2),'mu4':str(mu4),'Psi':str(psi),'J':str(jj),
                'commutant_rank':rank})
        return cache[key],F(controls[cache[key]]['Psi'])
    for name,kind,levels in charts():
        masses,raw_levels,target=cases[kind]
        aa,bb,bound,mu2,mu4=primitives[kind]
        variables=levels[1:4]
        require([subst(t,variables) for t in raw_levels]==levels,name+' exact chart substitution')
        require(sum((m*t for m,t in zip(masses,levels)),P(0))==0,name+' symbolic balance')
        physical=[]
        for i,t in enumerate(levels):
            for sign in (-1,1):
                physical.append(certificate(name+' |level'+str(i)+'|<=1 sign'+str(sign),1+sign*t,unit))
        if kind=='double':
            orders=[levels[1]-levels[2],levels[3]-levels[4]]
        elif kind=='singleton':
            orders=[levels[1]-levels[2],levels[2]-levels[3]]
        else:orders=[]
        physical.extend(certificate(name+' ordered equal-mass labels'+str(i),p,unit)
                        for i,p in enumerate(orders))
        domain_entries+=sum(row['entries'] for row in physical)
        pulled=subst(bound,variables)
        records,volume,leaves=cover_tree(lookup[name],unit,pulled,name)
        require(volume==1,name+' complete closed parameter cube')
        entries+=sum(row['entries'] for row in records);leaf_count+=leaves
        output.append({'chart':name,'kind':kind,'target':target,'masses':masses,
            'levels':[t.dump() for t in levels],'domain_certificates':physical,
            'bound_certificates':records,'leaves':leaves})
        points=list(product((F(0),F(1)),repeat=3))+[(F(1,2),)*3,
               (F(1,3),F(2,5),F(3,7)),(F(4,5),F(1,4),F(2,3))]
        for index,point in enumerate(points):
            actual=[scalar(t,point) for t in levels]
            theta=[t for m,t in zip(masses,actual) for _ in range(m)]
            control_index,psi=definition_control(theta,name+' profile'+str(index))
            t2=sum(m*t*t for m,t in zip(masses,actual))
            t4=sum(m*t**4 for m,t in zip(masses,actual))
            a=t2*t2+8*t2-8*t4
            b=t2*t2-48*t2+16*t4+224-32*sum((m-1)*(1-t*t)**2
                                                          for m,t in zip(masses,actual))
            require(a>0 and b>0,name+' positive test numerator/denominator')
            require(psi>=a*a/(128*b),name+' defining pinching versus active minorant')
            upper=122*t2+224*t4/t2-45*a*a/(t2*b)
            require(upper<=target,name+' exact profile majorant control')
            inverse_name,inverse_point=reverse_chart(kind,actual)
            require(all(0<=v<=1 for v in inverse_point),name+' closed inverse coordinates')
            inverse_kind,inverse_levels=chart_map[inverse_name]
            require(inverse_kind==kind,'inverse preserves multiplicity class')
            inverse_actual=[scalar(t,inverse_point) for t in inverse_levels]
            inverse_theta=sorted(t for m,t in zip(masses,inverse_actual) for _ in range(m))
            require(inverse_theta==sorted(theta),name+' inverse chart including collisions')
            round_trips+=1
            profile_refs.append({'chart':name,'point':list(map(str,point)),
                'definition_control':control_index,'A':str(a),'B':str(b),'upper':str(upper),
                'inverse_chart':inverse_name,'inverse_point':list(map(str,inverse_point))})
    require(entries==8019 and leaf_count==11,'all complete bound coefficient/leaf totals')
    theta=[F(1)]*3+[F(-1)]*3+[F(1,3),F(-1,3)]
    comparison,psi=definition_control(theta,'credited3+3+1+1 comparison')
    require(psi==F(17,81) and F(controls[comparison]['J'])==F(5472,7)>750,
            'credited comparison excludes the two cohorts from the five-level maximum')
    comparison_labels=[F(1),F(-1),F(-1),F(1,3),F(-1,3)]
    comparison_masses=[3,2,1,1,1]
    require(sorted(t for m,t in zip(comparison_masses,comparison_labels) for _ in range(m))==sorted(theta),
            'comparison admits3+2+1+1+1 labels')
    require(F(13,8)**4/F(10985,33554432)==F(106496,5),'credited displacement normalization')
    basin={'2+2+2+1+1':F(106496,5*750),'4+1+1+1+1':F(106496,5*650)}
    require(basin['4+1+1+1+1']==F(4096,125),'heavy-cohort leading radius lower bound')
    return {'author':'six-sendov-2','role':'researcher',
      'scope':'all balanced max-normalized2+2+2+1+1 and4+1+1+1+1 labels, including collisions',
      'proof_status':'ordinary author proof and exact certificates; independent review pending',
      'new_bounds':{'2+2+2+1+1':'750','4+1+1+1+1':'650'},
      'cyclic_trace_words':words,'raw_symbolic_controls':symbolic,
      'cubes':output,'bound_sign_coefficients':entries,
      'physical_chart_sign_coefficients':domain_entries,'closed_leaves':leaf_count,
      'full_compression_controls':controls,'profile_references':profile_refs,
      'inverse_chart_round_trips':round_trips,
      'comparison_definition_control':comparison,
      'cohort_basin_liminf_lower_bounds':{k:str(v) for k,v in basin.items()},
      'five_level_remaining_class':'3+2+1+1+1; its maximum is not proved here',
      'checks':CHECKS-initial_checks}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover',type=Path,default=Path(__file__).with_name('cover.json'))
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-manifest',action='store_true',help='author regeneration only')
    args=parser.parse_args()
    require(args.cover.is_file(),'required complete cube cover absent')
    if not args.write_manifest:require(args.manifest.is_file(),'required regression manifest absent')
    result=build(json.loads(args.cover.read_text()))
    if args.write_manifest:args.manifest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:require(result==json.loads(args.manifest.read_text()),'complete exact record equality')
    print(json.dumps({'status':'PASS','checks':CHECKS,
      'bound_sign_coefficients':result['bound_sign_coefficients'],
      'physical_chart_sign_coefficients':result['physical_chart_sign_coefficients'],
      'cubes':len(result['cubes']),'closed_leaves':result['closed_leaves'],
      'full_compression_controls':len(result['full_compression_controls']),
      'inverse_chart_round_trips':result['inverse_chart_round_trips'],
      'canonical_record_sha256':digest(result)},sort_keys=True))
if __name__=='__main__':main()
