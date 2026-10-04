"""THREE-mark all-q whole reader. Adapted from own7fa whole reader; no producer, field-engine or sector imports.

An identity with coordinate degree bounds D and coefficient l1 bound C
is evaluated at (B,B^(D0+1),B^((D0+1)(D1+1))), B>2C. Every monomial
has a different base-B position. Zero integer encoding therefore forces
every coefficient to vanish, by successive reduction modulo B. This
is an exact complete coefficient identity, not sampled positivity.
"""
from pathlib import Path
from math import prod
import json,time,signal,resource,hashlib

def require(ok,msg):
    if not ok:raise ValueError(msg)

class E:
    def __init__(self,op,args=(),value=0,degree=None,bound=None):
        self.op,self.args,self.val=op,args,value
        self.degree=degree if degree is not None else (0,0,0)
        self.bound=abs(value) if bound is None else bound
    def __add__(self,b):
        b=expr(b)
        if not self.bound:return b
        if not b.bound:return self
        return E('+',(self,b),degree=tuple(max(a,c) for a,c in zip(self.degree,b.degree)),bound=self.bound+b.bound)
    __radd__=__add__
    def __neg__(self):return E('neg',(self,),degree=self.degree,bound=self.bound)
    def __sub__(self,b):return self+-expr(b)
    def __rsub__(self,b):return expr(b)+-self
    def __mul__(self,b):
        b=expr(b)
        if not self.bound or not b.bound:return E('const')
        return E('*',(self,b),degree=tuple(a+c for a,c in zip(self.degree,b.degree)),bound=self.bound*b.bound)
    __rmul__=__mul__
    def __pow__(self,n):
        require(type(n) is int and n>=0,'exact nonnegative expression power')
        out=expr(1)
        for _ in range(n):out=out*self
        return out
    def evaluate(self,point,cache):
        if self in cache:return cache[self]
        if self.op=='const':v=self.val
        elif self.op=='poly':v=sum(c*prod(point[j]**k[j] for j in range(3)) for k,c in self.val)
        elif self.op=='+':v=self.args[0].evaluate(point,cache)+self.args[1].evaluate(point,cache)
        elif self.op=='*':v=self.args[0].evaluate(point,cache)*self.args[1].evaluate(point,cache)
        elif self.op=='neg':v=-self.args[0].evaluate(point,cache)
        else:raise ValueError('closed expression operation')
        cache[self]=v;return v

def expr(x):return x if isinstance(x,E) else E('const',value=x)

def polynomial(data):
    require(set(data)=={'denominator','terms'},'entire encoded polynomial schema')
    den=data['denominator'];terms=data['terms']
    require(type(den) is int and den>0 and len(terms)<=512,'polynomial input guards')
    out=[]
    for k,c in terms:
        require(type(k) is list and len(k)==3 and all(type(z) is int and z>=0 for z in k),'three exponents')
        require(type(c) is str and str(int(c))==c and int(c)!=0,'canonical integer coefficient')
        out.append((tuple(k),int(c)))
    require(out==sorted(out) and len(set(k for k,c in out))==len(out),'every coefficient once in order')
    deg=tuple(max((k[j] for k,c in out),default=0) for j in range(3))
    return E('poly',value=tuple(out),degree=deg,bound=sum(abs(c) for k,c in out)),den,out

def positive(terms):
    return dict(terms).get((0,0,0),0)>0 and all(c>=0 for k,c in terms)

def exact_identities(identities,label):
    nonzero=[z for z in identities if z.bound]
    D=tuple(max((z.degree[j] for z in nonzero),default=0) for j in range(3))
    C=max((z.bound for z in nonzero),default=0)
    bits=(2*C).bit_length()+1
    strides=(1,D[0]+1,(D[0]+1)*(D[1]+1))
    slots=prod(z+1 for z in D)
    require((slots*bits+7)//8<=32*1024*1024,'unchanged32MiB whole identity encoding guard')
    B=1<<bits;point=tuple(B**z for z in strides);cache={}
    for i,z in enumerate(identities):
        require(z.evaluate(point,cache)==0,label+' full coefficient identity '+str(i))
    return dict(identities=len(identities),coordinate_degree=D,coefficient_bound_bits=C.bit_length(),
                radix_bits=bits,encoding_bytes_bound=(slots*bits+7)//8,
                method='exact injective bounded-coefficient base encoding')

def original_forms():
    variables=[]
    for j in range(3):
        k=tuple(int(i==j) for i in range(3));variables.append(E('poly',value=((k,1),),degree=k,bound=1))
    u,v,w=variables;d=1+u;l=2+v;h=l+d;q=4+w;s=q+3*h;D=3*h
    ell=3*(h+2*l)+1;N=2*q+6*(h+2*l);t=3*h*l
    # NEW three-mark even-five metric and complete original images,
    # cleared independently of the producer with one t factor.
    G=[4*t*(q-1),4*D*t,3*D*(q-3)*t,6*q*D*t,2*s*d]
    jx=[0,-2*t,(q-3)*t,2*q*t,0]
    jl=[0,-2*t,(q-3)*t,-q*t,s*d]
    z=[-2*t*(q-1),12*l*t,-3*t*(q-3)*(h+2*l),-6*t*q*d,-6*l*s*d]
    old=[[expr(0) for j in range(5)] for i in range(5)]
    old[0][0]=4*(q*q-1);old[0][1]=old[1][0]=-4*D*(q-1)
    old[1][1]=4*D*D;old[2][2]=6*D*D*(q-3);old[3][3]=12*q*D*D
    forms=[]
    for i in range(5):
        row=[]
        for j in range(5):
            den=t*ell*G[i]
            ss=ell*t*t*old[i][j]+3*h*ell*jx[i]*jx[j]+6*l*ell*jl[i]*jl[j]+z[i]*z[j]
            num=((N-1)*den if i==j else expr(0))-ss
            row.append((num,den))
        forms.append(row)
    return forms

def check(data):
    require(set(data)=={'version','agent','role','domain','guards','forms','rows','updates','polynomials','fields'},'complete compact schema')
    require(data['version']==1 and data['agent']=='six-downset-1' and data['role']=='researcher','version and actual author')
    require(data['domain']=='u,v,w>=0; d=1+u,l=2+v,h=l+d,q=4+w','exact ALL-q three-mark domain')
    require(data['guards']==dict(child_seconds=60,polynomial_terms=512,packing_bytes=33554432,native_threads=1),'unchanged guards')
    polys=data['polynomials'];fields=data['fields'];poly=[polynomial(z) for z in polys]
    require(len({json.dumps(z,sort_keys=True) for z in polys})==len(polys),'unique polynomial intern')
    require(len({json.dumps(z,sort_keys=True) for z in fields})==len(fields),'unique field intern')
    usedp=set();usedf=set();fs=[]
    def pp(i):
        require(type(i) is int and 0<=i<len(poly),'polynomial ID');usedp.add(i);return poly[i]
    for f in fields:
        require(set(f)=={'numerator','denominator_factors'},'complete rational field')
        n,nd,nt=pp(f['numerator']);num=n;den=expr(nd);seen=set()
        for i,e in f['denominator_factors']:
            require(type(e) is int and e>0 and i not in seen,'distinct positive denominator power');seen.add(i)
            b,bd,bt=pp(i);require(positive(bt),'whole denominator coefficient positivity')
            num=num*(bd**e);den=den*b**e
        fs.append((num,den))
    def field(i):
        require(type(i) is int and 0<=i<len(fields),'field ID');usedf.add(i);return fs[i]
    def same(i,j,msg):
        require(i==j,msg)  # Producer interning is lossless, verified as a strict link.
        field(i)
    require(set(data['forms'])=={'three-even-five-allq'},'only and entire five-block')
    A=data['forms']['three-even-five-allq']
    require(len(A)==5 and all(len(row)==5 for row in A),'ALL25 original form positions')
    originals=original_forms();identities=[]
    for i in range(5):
        for j in range(5):
            n,d=field(A[i][j]);nn,dd=originals[i][j];identities.append(n*dd-nn*d)
    initial=exact_identities(identities,'original normalized cap')
    require(len(data['rows'])==5 and len(data['updates'])==30,'ALL5 pivots and30 updates')
    working=[row[:] for row in A];local=[];index=0;coefficient_count=0
    for k,r in enumerate(data['rows']):
        require(set(r)=={'group','order','pivot','shifted_numerator','positive','denominator_positive','degree','terms','shifted_terms'},'whole pivot record')
        require(r['group']=='three-even-five-allq' and r['order']==k+1,'pivot order')
        same(r['pivot'],working[k][k],'pivot linked to actual working diagonal')
        f=fields[r['pivot']];p,den,terms=pp(f['numerator'])
        require(positive(terms),'complete shifted numerator positivity')
        require(r['shifted_numerator']==f['numerator'],'no omitted/altered shifted coefficients')
        pp(r['shifted_numerator'])
        require(r['positive'] is True and r['denominator_positive'] is True and r['terms']==len(terms)
                and r['shifted_terms']==len(terms) and r['degree']==max(sum(e) for e,c in terms),'all pivot metadata')
        coefficient_count+=len(terms)
        for i in range(k+1,5):
            for j in range(k+1,5):
                z=data['updates'][index];index+=1
                require(set(z)=={'group','k','i','j','before','left','right','pivot','after'},'whole local update')
                require(z['group']=='three-even-five-allq' and (z['k'],z['i'],z['j'])==(k,i,j),'every ordered local location')
                for key,target in (('before',working[i][j]),('left',working[i][k]),('right',working[k][j]),('pivot',working[k][k])):
                    same(z[key],target,'full working-matrix link '+key)
                pn,pd=field(z['pivot']);bn,bd=field(z['before']);an,ad=field(z['after'])
                ln,ld=field(z['left']);rn,rd=field(z['right'])
                # Exact cleared polynomial of p*(b-a)-left*right.
                local.append(pn*(bn*ad-an*bd)*ld*rd-ln*rn*pd*bd*ad)
                working[i][j]=z['after']
    updates=exact_identities(local,'local Schur')
    require(usedf==set(range(len(fields))) and usedp==set(range(len(polys))),'all and only referenced fields/polynomials')
    return dict(agent='six-downset-1',role='researcher',complete=True,
        original_form_fields=25,pivots=5,local_updates=30,positive_pivot_coefficients=coefficient_count,
        original_identity=initial,local_identity=updates,field_count=len(fields),polynomial_count=len(polys),
        source_imports='standard library only; independent closed forms',
        original_generic_bridge_proved_by_this_reader=False,independent_review=False)

if __name__=='__main__':
    def alarm(a,b):raise TimeoutError('unchanged60s separate whole checker guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);started=time.monotonic()
    folder=Path(__file__).resolve().parent;f=folder/'THREE-EVEN-FIVE-ALLQ-CERTIFICATE.json'
    require(f.stat().st_size<=32*1024*1024,'unchanged32MiB input guard')
    raw=f.read_bytes();result=check(json.loads(raw))
    result.update(certificate_sha256=hashlib.sha256(raw).hexdigest(),seconds=time.monotonic()-started,
                  peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__)
    signal.alarm(0)
    (folder/'THREE-EVEN-FIVE-ALLQ-CHECKED.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
