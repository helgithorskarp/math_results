"""Independent finite-degree interpolation, not a target polynomial import."""
import hashlib,json,math,pathlib,sys,time
from fractions import Fraction as F
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'pass34/libs'))
from sympy.polys.fields import field
from sympy.polys.domains import QQ
from frame import build,forms

K,q=field('q',QQ)
def fraction(x):return F(int(x.numerator),int(x.denominator))
def poly(p):return [fraction(p.get((i,),QQ.zero)) for i in range(max(0,p.degree())+1)]
def evaluate(coeff,x):
    y=0
    for a in reversed(coeff):y=y*x+a
    return y
def shifted(coeff):
    return [sum(coeff[j]*math.comb(j,i)*4**(j-i) for j in range(i,len(coeff))) for i in range(len(coeff))]
def trim(a):
    while len(a)>1 and not a[-1]:a.pop()
    return a
def det_prefixes(a):
    a=[row[:] for row in a];previous=1;values=[]
    for k in range(len(a)):
        pivot=a[k][k];values.append(pivot)
        if not pivot:raise ValueError('zero prefix determinant at reconstruction node')
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                n=pivot*a[i][j]-a[i][k]*a[k][j]
                quotient,remainder=divmod(n,previous)
                if remainder:raise ValueError('nonexact Bareiss quotient')
                a[i][j]=quotient
            a[i][k]=0
        previous=pivot
    return values
def interpolate(values):
    delta=list(values);out=[F(0)]*len(values);fall=[1];fac=1
    for degree in range(len(values)):
        if degree:
            new=[0]*(len(fall)+1)
            for i,a in enumerate(fall):new[i]-=(degree-1)*a;new[i+1]+=a
            fall=new;fac*=degree
        for i,a in enumerate(fall):out[i]+=F(delta[0]*a,fac)
        delta=[delta[i+1]-delta[i] for i in range(len(delta)-1)]
    return trim(out)
def encode(coeff):return [str(x) for x in coeff]
def clear(matrix):
    rows=[];domains=[];bounds=[]
    for row in matrix:
        d=K.ring.one
        for x in row:
            if x:d=d.lcm(x.denom)
        dom=poly(d);shift=shifted(dom)
        if any(x<0 for x in shift) or shift[0]<=0:raise ValueError('unproved row domain')
        cleared=[x.numer*(d//x.denom) if x else K.ring.zero for x in row]
        rational=[poly(x) for x in cleared];factor=math.lcm(*(a.denominator for v in rational for a in v))
        integer=[[int(a*factor) for a in v] for v in rational]
        domains.append(dict(coefficients=encode(dom),positive_scale=factor))
        rows.append(integer);bounds.append(max(len(v)-1 for v in integer))
    return rows,domains,bounds
def audit(extra):
    start=time.monotonic();model=build(q);blocks,off=forms(model,extra)
    tables=[]
    # Include six residual scalar signs as one-by-one rational forms.
    for label,matrix in list(zip(['alphaH','betaH','alphaL','betaL','nu','muL'],[[[x]] for x in model['scalars']]))+list(zip(['heavy anti','light anti','heavy standard','fixed'],blocks)):
        rows,domains,row_bounds=clear(matrix)
        degree_bounds=[sum(row_bounds[:i+1]) for i in range(len(rows))]
        stream=[]
        for v in range(max(degree_bounds)+1):
            a=[[evaluate(p,4+v) for p in row] for row in rows];stream.append(det_prefixes(a))
        coefficients=[]
        for i,bound in enumerate(degree_bounds):
            coeff=interpolate([x[i] for x in stream[:bound+1]])
            if coeff[0]<=0 or any(x<0 for x in coeff):raise ValueError('shifted positivity failed '+label+' '+str(i))
            # Extra value is only an arithmetic control, not the degree proof.
            node=bound+5;actual=det_prefixes([[evaluate(p,4+node) for p in row] for row in rows])[i]
            if evaluate(coeff,node)!=actual:raise ValueError('independent extra-node mismatch')
            coefficients.append(dict(degree_bound=bound,degree=len(coeff)-1,shifted_coefficients=encode(coeff),extra_node=node,extra_value=str(actual)))
        tables.append(dict(label=label,row_domains=domains,row_degree_bounds=row_bounds,
            original_cleared_entries=[[encode(p) for p in row] for row in rows],minors=coefficients))
    record=dict(extra_margin=str(extra),dimension=20,multiplicities=[2,1,1,1],
        residual_basis='D=M1-M2,P=M1+M2,WA1,WF1,WA2,WF2,WA3,WF3',
        original_field_identities=model['identities'],off_sector_positions=off,
        untouched_dimensions=['q-2','q-3'],untouched_margins=[str(17-extra),str(2*q+5-extra)],tables=tables)
    raw=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
    return record,dict(seconds=time.monotonic()-start,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),obligations=sum(len(t['minors']) for t in tables),positive_coefficients=sum(sum(x>0 for x in map(F,m['shifted_coefficients'])) for t in tables for m in t['minors']))
if __name__=='__main__':
    extra=F(sys.argv[1]) if len(sys.argv)>1 else F(0)
    record,summary=audit(extra)
    path=pathlib.Path(__file__).resolve().parent/('UNIFORM-'+str(extra).replace('/','_')+'.json')
    path.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
