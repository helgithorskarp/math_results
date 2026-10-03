"""Exact coefficient comparisons in Z[t,z,w], characteristic zero."""
from fractions import Fraction as Q
from polynomials import P,dot
from frame import make
from schema import require

def factor_rows(document):
    require(set(document)=={'schema_version','variable_order','coefficient_domain','rows'},'factor document grammar')
    require(document['schema_version']==1 and document['variable_order']==['t','z','w'] and document['coefficient_domain']=='Z','factor ring')
    require(set(document['rows'])=={'L5','M6','H10','H12'},'all four new factors')
    answer={}
    for name,rows in document['rows'].items():
        require(type(rows)is list and bool(rows),'nonempty literal polynomial')
        terms={};keys=[]
        for row in rows:
            require(type(row)is list and len(row)==4,'integral factor row')
            i,j,k,co=row
            require(all(type(e)is int and e>=0 for e in (i,j,k)) and k==0,'bivariate exponent slots')
            require(type(co)is str and str(int(co))==co and int(co)!=0,'nonzero canonical integer coefficient')
            key=(i,j,k);require(key not in terms,'no repeated coefficient');keys.append(key);terms[key]=int(co)
        require(keys==sorted(keys),'canonical coefficient order');answer[name]=P(terms)
    return answer

def exact_divide(f,d):
    # Lexicographic polynomial division, never numerical division. An
    # answer is accepted only after whole integer coefficient comparison.
    g={k:Q(v) for k,v in f.c.items()};q={};ld=max(d.c)
    while g:
        lm=max(g)
        require(all(x>=y for x,y in zip(lm,ld)),'nonzero polynomial remainder')
        mon=tuple(x-y for x,y in zip(lm,ld));co=g[lm]/d.c[ld];q[mon]=q.get(mon,Q(0))+co
        for key,v in d.c.items():
            kk=tuple(x+y for x,y in zip(key,mon));g[kk]=g.get(kk,Q(0))-co*v
            if not g[kk]:del g[kk]
    require(all(v.denominator==1 for v in q.values()),'integral quotient')
    a=P({k:int(v) for k,v in q.items()});require(a*d==f,'whole division identity');return a

def affine(f):
    require(all(k[2]<=1 for k in f.c),'affine in the positive radical')
    return P({k:v for k,v in f.c.items() if k[2]==0}),P({(a,b,0):v for (a,b,c),v in f.c.items() if c==1})

def degree(f):return [max((k[i] for k in f.c),default=0) for i in range(3)]

def derive(document):
    f=factor_rows(document);t,z,w=[P.var(i) for i in range(3)];m=make(t,z,w)
    a,b,c,D,C,J=m['a'],m['b'],m['c'],m['D'],m['C'],m['J'];R=m['root_squared']
    F5=t*a**10*b*c*(3*t-1);F6=a**5*b*c*(3*t-1)*(3*t+1)
    raw={};parts={}
    for name,i,j,F in (('5-12',5,12,F5),('6-8',6,8,F6)):
        raw[name]=dot(m['points'][i],m['B_num'][j],t)-t*a*a*m['Omega']
        parts[name]=affine(exact_divide(raw[name],F))
    A5,B5=parts['5-12'];A6,B6=parts['6-8']
    Z=t*(3*t+1)*z-(1+2*t)
    M5=1+2*t-t*t-2*t*b*c*z
    Qp=a*D*z*z-2*D*z+2*t*t-t+1
    H5=32*(b*z+1)**2*(1-b*z)*(b*c*z+t)*Z*Qp
    H6=4*(b*z+1)**2*Qp*f['H10']*f['H12']
    identities=[
        ('5-12 A',A5,2*D*(b*z+1)*C*f['L5']),
        ('5-12 B',B5,-2*(b*z+1)*C*M5),
        ('6-8 B',B6,2*(b*z+1)*f['M6']),
        ('5-12 square',A5*A5-B5*B5*R,a*b**5*c**3*J*C**2*H5),
        ('6-8 square',A6*A6-B6*B6*R,a**2*b**4*c**3*J*H6),
        ('quadratic square',a*Qp,D*(a*z-1)**2+4*t*t),
        ('chart boundary M5',b*(1+2*t-t*t)-2*t*b*c,b*(1-5*t*t))]
    for name,left,right in identities:require(left==right,'generic identity: '+name)
    return f|{'Z':Z,'M5':M5,'Q':Qp},parts,{
        'generic_whole_polynomial_identities':len(identities),
        'integer_factor_divisions':2,
        'raw_excess_degree_bounds':{name:degree(p) for name,p in raw.items()},
        'raw_excess_terms':{name:len(p.c) for name,p in raw.items()},
        'no_cancelled_chart_boundary_or_Z_factor':True}
