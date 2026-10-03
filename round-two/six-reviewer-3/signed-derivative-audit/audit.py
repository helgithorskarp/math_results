"""Independent exact definition/interpolation audit of LEMMA9868.

CPython 3.11+, standard library. No researcher modules or frozen corpus.
All claims involving compactness, extrema and actual polynomials remain
ordinary proofs in PROOF.md. Fractions encode exact rational values.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, factorial
import hashlib, json, sys

M = [Q(0), Q(9,16), Q(3,5), Q(3,4), Q(1), Q(7,5), Q(17,8), Q(7,2), Q(1)]
E = Q(1,16000)

def need(condition, message):
    if not condition: raise ValueError(message)

def add(x,y):
    z=dict(x)
    for k,v in y.items(): z[k]=z.get(k,Q(0))+v
    return {k:v for k,v in z.items() if v}

def mul(x,y):
    z={}
    for k,v in x.items():
        for l,w in y.items():
            t=tuple(i+j for i,j in zip(k,l));z[t]=z.get(t,Q(0))+v*w
    return {k:v for k,v in z.items() if v}

def upmul(x,y):
    z=[Q(0)]*(len(x)+len(y)-1)
    for i,a in enumerate(x):
        for j,b in enumerate(y):z[i+j]+=a*b
    return z

def upadd(x,y):
    z=[Q(0)]*max(len(x),len(y))
    for i,c in enumerate(x):z[i]+=c
    for i,c in enumerate(y):z[i]+=c
    while len(z)>1 and not z[-1]:z.pop()
    return z
def ups(x,c):return [v*c for v in x]
def uppow(x,n):
    z=[Q(1)]
    for _ in range(n):z=upmul(z,x)
    return z
def upsum(*xs):
    z=[Q(0)]
    for x in xs:z=upadd(z,x)
    return z

def seed_penalty():
    """Rebuild ONLY the credited entry seed and radial penalty coefficients."""
    a=[Q(1),Q(-1)];b=upadd([Q(1)],ups(uppow(a,2),-1));L=[Q(8),Q(3)]
    d=ups(upmul(uppow(a,7),b),Q(1,2));T=[Q(0)]
    for k in range(2,9):
        term=upmul(upmul(uppow(a,8-k),uppow(b,k)),uppow(ups(L,Q(1,8)),k))
        T=upadd(T,ups(term,Q(comb(8,k),k+1)))
    A=uppow(a,8);B=upsum(A,upmul(d,L),T)
    Nm=upsum([Q(1)],ups(uppow(a,16),-1),ups(upmul(uppow(d,2),uppow(L,2)),-1),
       ups(upmul(upadd(A,upmul(d,L)),T),-2),ups(uppow(T,2),-1),
       ups(upmul(upmul([Q(8),Q(-6)],uppow(a,15)),b),-1))
    Nb=upadd([Q(1),Q(0),Q(9)],ups(B,-1))
    Nv=upadd(ups(upmul(uppow(a,6),uppow(b,2)),13),ups(upadd(B,[Q(-1)]),-6))
    seeds=[]
    for x,threshold in zip((Nm,Nb,Nv),(Q(1),Q(1,2),Q(1))):
        need(x[0]==x[1]==0,'full seed order')
        budget=x[2]-sum(abs(v)*E**(i-2) for i,v in enumerate(x) if i>2)
        need(budget>threshold,'whole seed coefficient tail')
        seeds.append({'coefficients':x,'budget':budget,'threshold':threshold})
    one={(0,0,0):Q(1)};aa={(0,0,0):Q(1),(0,1,0):Q(-1)}
    base=add(add(one,aa),{k:-c for k,c in mul(aa,{(1,0,0):Q(1)}).items()})
    penalties=[]
    for m in range(1,9):
        free=add(base,{k:-Q(8,m)*c for k,c in mul(mul(aa,aa),{(1,0,0):Q(1)}).items()})
        f=one
        for _ in range(8-m):f=mul(f,base)
        for _ in range(m):f=mul(f,free)
        integ={}
        for (t,e,u),c in f.items():
            need(u==0,'radial penalty variables')
            integ[e]=integ.get(e,Q(0))+9*c/Q(t+1)
        poly=[integ.get(j,Q(0)) for j in range(max(integ)+1)]
        dm=Q(64*(m-1),m)-Q(256*(m-1)*(m-2),3*m*m)
        poly=upsum(poly,ups(uppow(upadd([Q(1)],ups(a,Q(8,m))),m),-1),
                    [Q(-8)],ups(uppow(a,9),8),ups(uppow(a,3),-Q(39,5)*dm))
        j=next(j for j,c in enumerate(poly) if c)
        budget=poly[j]-sum(abs(c)*E**(i-j) for i,c in enumerate(poly) if i>j)
        need(j==(1 if m in (1,8) else 0) and budget>0,'complete radial penalty face')
        penalties.append({'m':m,'coefficients':poly,'leading_order':j,'budget':budget})
    return {'polar_seeds':seeds,'radial_penalties':penalties}

def lagrange(nodes):
    basis=[]
    for i,x in enumerate(nodes):
        row=[Q(1)];den=Q(1)
        for j,y in enumerate(nodes):
            if i!=j:row=upmul(row,[-y,Q(1)]);den*=x-y
        basis.append([t/den for t in row])
    return basis

def integral_value(p,k,a,u):
    """Numerically evaluate the defining integral, with EXACT rationals."""
    m=8-p;rs=[Q(1,2)]*(m-k)
    if k:rs += [Q(1,2)+Q(403,100)*u/k]*k
    ts=[Q(1)]
    for r in rs:ts=upmul(ts,[Q(1),-a*r])
    return 9*(-a)**p*sum(t/Q(i+p+1) for i,t in enumerate(ts))

def definition_power(p,k):
    """Multiply t,v,u factors first; a=.99+.01v. Integrate LAST."""
    a={(0,0,0):Q(99,100),(0,1,0):Q(1,100)}
    tr={(1,0,0):Q(1,2)}
    if k:tr[(1,0,1)]=Q(403,100*k)
    one={(0,0,0):Q(1)}
    flo=add(one,{key:-v for key,v in mul(a,{(1,0,0):Q(1,2)}).items()})
    free=add(one,{key:-v for key,v in mul(a,tr).items()})
    f={(p,0,0):Q(9)*(-1)**p}
    for _ in range(p):f=mul(f,a)
    for _ in range(8-p-k):f=mul(f,flo)
    for _ in range(k):f=mul(f,free)
    out={}
    for (t,v,u),c in f.items():out[v,u]=out.get((v,u),Q(0))+c/(t+1)
    return {t:c for t,c in out.items() if c}

def interpolation_power(p,k):
    """Tensor interpolation from exact INTEGRAL VALUES on rational nodes."""
    vn=[Q(i,8) for i in range(9)]
    un=[Q(i,k) for i in range(k+1)] if k else [Q(0)]
    vb,ub=lagrange(vn),lagrange(un);out={}
    for i,v in enumerate(vn):
        for j,u in enumerate(un):
            f=integral_value(p,k,Q(99,100)+v/100,u)
            for x,b in enumerate(vb[i]):
                for y,c in enumerate(ub[j]):out[x,y]=out.get((x,y),Q(0))+f*b*c
    return {t:c for t,c in out.items() if c}

def bernstein(power,k):
    return [[sum(c*Q(comb(i,x),comb(8,x))*Q(comb(j,y),comb(k,y))
                 for (x,y),c in power.items() if x<=i and y<=j)
             for j in range(k+1)] for i in range(9)]

def inverse_bernstein(b,k):
    out={}
    for i,row in enumerate(b):
        for j,c in enumerate(row):
            for x in range(i,9):
                for y in range(j,k+1):
                    z=c*comb(8,i)*comb(8-i,x-i)*(-1)**(x-i)
                    z*=comb(k,j)*comb(k-j,y-j)*(-1)**(y-j)
                    out[x,y]=out.get((x,y),Q(0))+z
    return {t:c for t,c in out.items() if c}

def ga(x):return x if isinstance(x,tuple) else (Q(x),Q(0))
def plus(x,y):x,y=ga(x),ga(y);return (x[0]+y[0],x[1]+y[1])
def times(x,y):x,y=ga(x),ga(y);return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,c):return times(x,c)
def derivative(a,z,I):
    """Definition-level univariate t multiplication for ANY distinct I."""
    ts=[ga(1)]
    for j in range(8):
        if j in I:continue
        out=[ga(0)]*(len(ts)+1)
        for i,c in enumerate(ts):
            out[i]=plus(out[i],c);out[i+1]=plus(out[i+1],times(c,scale(z[j],-a)))
        ts=out
    total=ga(0)
    for i,c in enumerate(ts):total=plus(total,scale(c,Q(9)*(-a)**len(I)/Q(i+len(I)+1)))
    return total

def subset_derivatives(a,z):
    return {mask:derivative(a,z,{j for j in range(8) if mask>>j&1}) for mask in range(256)}

def taylor_checks():
    r=[Q(9,2)]+[Q(1,2)]*7
    h=[(Q((-1)**j,j+50),Q(j-3,100)) for j in range(8)]
    q=[plus(r[j],h[j]) for j in range(8)]
    d0=subset_derivatives(Q(1),r);d1=subset_derivatives(Q(1),q)
    for I in range(256):
        total=ga(0)
        for J in range(256):
            if I&J:continue
            term=d0[I|J]
            for j in range(8):
                if J>>j&1:term=times(term,h[j])
            total=plus(total,term)
        need(total==d1[I],'entire finite Taylor identity')
    q=[ga(x) for x in r];q[1]=(Q(63,130),Q(16,130))
    g=derivative(Q(1),r,{1})
    need(g==ga(Q(1971,3584)),'signed high-arm gradient')
    loss=derivative(Q(1),r,set())[0]-derivative(Q(1),q,set())[0]
    need(loss==Q(1971,3584*65) and loss>0,'strict actual one-slot envelope loss')
    need(q[1][0]**2+q[1][1]**2==Q(1,4),'phase radius')
    controls=[(Q(1),r),(Q(1),q),(Q(99,100),[Q(1,2)]*8),
              (Q(199,200),[(Q(j+2,10),Q(3-j,50)) for j in range(8)])]
    return [[a,subset_derivatives(a,z)] for a,z in controls],loss

def build():
    faces=[];maxima=[Q(0)]*9;coeff_count=0
    for p in range(1,9):
        for k in range(9-p):
            x=definition_power(p,k);y=interpolation_power(p,k)
            need(x==y,'whole tensor interpolation differs from definition')
            b=bernstein(y,k);need(inverse_bernstein(b,k)==x,'whole inverse basis')
            need(len(b)==9 and all(len(r)==k+1 for r in b),'full tensor size')
            peak=max(abs(c) for row in b for c in row)
            maxima[p]=max(maxima[p],peak);coeff_count+=9*(k+1)
            faces.append({'p':p,'k':k,'power':x,'bernstein':b,'peak':peak})
    need(len(faces)==36 and coeff_count==1080,'full face coverage')
    margins=[M[p]-maxima[p] for p in range(1,8)]
    need(all(t>0 for t in margins) and maxima[8]==1,'uniform signed derivative margin')
    expected=[Q(1894359421947814029,448000000000000000000),Q(87,89600),Q(4707,112000),Q(53,896),Q(7,200),Q(19,1120),Q(19,200)]
    need(margins==expected,'seven full signed margins')
    N=[[M[p+k]/factorial(k) for k in range(9-p)] for p in range(1,9)]
    n=[sum(c*Q(1,8)**k for k,c in enumerate(row)) for row in N]
    need(n[0]==Q(6803677973,10569646080) and n[1]==Q(132505753,188743680),'full complex gradient/Hessian')
    G=Q(753,700)**7
    C=6*(n[0]+G)+10*M[1]+80*n[1]
    C7=6*(n[0]+G)+10*M[1]+70*n[1]
    d0=Q(256)*82/Q(39,5);dr=Q(256)*69/Q(39,5)
    budgets={'complex_gradient':Q(2,3)-n[0],'complex_hessian':Q(3,4)-n[1],
      'product_gradient':2-G,'phase_path':Q(1,64)-161*E,'original_global':82-Q(653,8),
      'retained_constants_global':76-C,'refined_global':69-C7,'initial_E2':28*(1-E)**2-26-Q(7,4),
      'first_bootstrap':Q(7,5)-8*d0*E,'second_E2':28*(1-E)**2-Q(14,5)-25,
      'second_bootstrap':Q(1,10)-Q(14,25)*d0*E,
      'third_E2':28*(1-E)**2-Q(1,5)-27,'third_bootstrap':Q(9,100)-Q(14,27)*d0*E,
      'refined_first':Q(8,7)-8*dr*E,'refined_E2':28*(1-E)**2-Q(16,7)-25,
      'refined_second':Q(2,25)-Q(14,25)*dr*E,
      'refined_second_E2':28*(1-E)**2-Q(4,25)-27,
      'refined_final':Q(3,40)-Q(14,27)*dr*E,
      'normalization_deficit':10-9*(1+Q(3,2)*E),
      'path_phase':161-(160+60*E),
      'lambda_lower':8-3*(2-E),
      'derivative_domain':Q(803,100)-(8+3*E),
      'a_domain':1-E-Q(99,100)}
    need(all(v>0 for v in budgets.values()),'whole-window strict analytic budget')
    controls,loss=taylor_checks()
    return {'faces':faces,'face_count':len(faces),'coefficient_count':coeff_count,
            'signed_margins':margins,'N':N,'complex_endpoint':n,'product_gradient':G,
            'global_coefficient':C7,'uncompressed_mixed_coefficient':C,
            'budgets':budgets,'controls':controls,'positive_loss':loss,'entry_dependencies':seed_penalty(),
            'refined_coarse_coefficient':Q(14,27)*dr}

def encode(x):
    if isinstance(x,Q):return str(x.numerator)+'/'+str(x.denominator)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x

def canonical(x):return json.dumps(encode(x),sort_keys=True,separators=(',',':')).encode()

def summary(record):
    return {'record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
            **{k:encode(record[k]) for k in ('face_count','coefficient_count','signed_margins',
                 'complex_endpoint','product_gradient','global_coefficient','budgets',
                 'positive_loss','refined_coarse_coefficient')}}

if __name__=='__main__':
    x=build()
    if len(sys.argv)>1 and sys.argv[1]=='--full':print(canonical(x).decode())
    else:print(json.dumps(summary(x),sort_keys=True,indent=2))
