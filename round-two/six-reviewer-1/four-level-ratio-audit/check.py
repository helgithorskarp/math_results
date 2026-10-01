#!/usr/bin/env python3
"""six-reviewer-1: original resolvent, rational Gaussian and Krylov audit.
Only SymPy1.14 exact QQ polynomial rings support universal algebra; all
root/interval/determinant/full-coordinate checks below use Fraction arithmetic.
No researcher proof module is imported. See REVIEW.md for ordinary bridges.
"""
from fractions import Fraction as Q
from math import comb,factorial,gcd
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys,time

COUNT=0
def need(ok,label):
    global COUNT
    if not ok:raise ValueError(label)
    COUNT+=1
def trim(p):
    p=list(map(Q,p))
    while len(p)>1 and not p[-1]:p.pop()
    return p
def add(a,b):
    out=[Q(0)]*max(len(a),len(b))
    for i,c in enumerate(a):out[i]+=c
    for i,c in enumerate(b):out[i]+=c
    return trim(out)
def scale(a,c):return trim([v*c for v in a])
def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)
def rem(a,b):
    a=trim(a);b=trim(b);need(b!=[0],'nonzero polynomial divisor')
    while a!=[0] and len(a)>=len(b):
        j=len(a)-len(b);v=a[-1]/b[-1]
        for k,c in enumerate(b):a[k+j]-=v*c
        a=trim(a)
    return a
def divrem(a,b):
    a=trim(a);b=trim(b);out=[Q(0)]*max(1,len(a)-len(b)+1)
    need(b!=[0],'nonzero Euclidean divisor')
    while a!=[0] and len(a)>=len(b):
        j=len(a)-len(b);v=a[-1]/b[-1];out[j]+=v
        for k,c in enumerate(b):a[k+j]-=v*c
        a=trim(a)
    return trim(out),a
def ev(a,x):
    out=Q(0)
    for c in reversed(a):out=out*x+c
    return out
def deriv(a):return trim([i*a[i] for i in range(1,len(a))] or [0])
def pgcd(a,b):
    while b!=[0]:a,b=b,rem(a,b)
    return scale(a,1/a[-1])
def invmod(a,h):
    r0,r1=h,a;t0,t1=[Q(0)],[Q(1)]
    while r1!=[0]:
        q,r=divrem(r0,r1);r0,r1=r1,r;t0,t1=t1,add(t0,scale(mul(q,t1),-1))
    need(len(r0)==1 and r0[0]!=0,'squarefree cyclic minimal polynomial')
    return rem(scale(t0,1/r0[0]),h)
def sturm(a):
    norm=lambda p:scale(p,1/abs(p[-1]))
    a=norm(trim(a));b=norm(deriv(a));chain=[a,b]
    while True:
        r=scale(rem(a,b),-1)
        if r==[0]:return chain
        r=norm(r);chain.append(r);a,b=b,r
def variation(chain,x):
    signs=[1 if v>0 else -1 for p in chain if (v:=ev(p,x))]
    return sum(a!=b for a,b in zip(signs,signs[1:]))
def roots(chain,box):return variation(chain,box[0])-variation(chain,box[1])
def gaussian_det(matrix):
    # Rational row elimination, independent of author's integer Bareiss route.
    A=[list(map(Q,row)) for row in matrix];n=len(A);result=Q(1)
    for j in range(n):
        pivot=next((i for i in range(j,n) if A[i][j]),None)
        if pivot is None:return Q(0)
        if pivot!=j:A[j],A[pivot]=A[pivot],A[j];result=-result
        p=A[j][j];result*=p
        for i in range(j+1,n):
            if not A[i][j]:continue
            fac=A[i][j]/p
            for k in range(j+1,n):A[i][k]-=fac*A[j][k]
            A[i][j]=0
    need(result.denominator==1,'integer determinant under rational elimination')
    return result
def linear_solve(matrix,rhs):
    A=[list(map(Q,row))+[Q(v)] for row,v in zip(matrix,rhs)];n=len(A)
    for j in range(n):
        pivot=next((i for i in range(j,n) if A[i][j]),None);need(pivot is not None,'independent Krylov basis')
        A[j],A[pivot]=A[pivot],A[j];p=A[j][j];A[j]=[v/p for v in A[j]]
        for i in range(n):
            if i!=j:
                c=A[i][j];A[i]=[v-c*w for v,w in zip(A[i],A[j])]
    return [row[-1] for row in A]
def poly_v(p):
    m=max(j for i,j in p);out=[[Q(0)] for _ in range(m+1)]
    for (i,j),c in p.items():
        if len(out[j])<=i:out[j]+=[Q(0)]*(i+1-len(out[j]))
        out[j][i]+=Q(str(c))
    return [trim(row) for row in out]
def sylvester(p,q,deleted=None):
    # Ascending columns and ascending shifts, unlike author's conventions.
    m=len(p)-1;n=len(q)-1;cut=0 if deleted is None else 1
    width=m+n-cut;rows=[]
    for f,shifts in [(p,n-cut),(q,m-cut)]:
        for j in range(shifts):
            row=[[Q(0)] for _ in range(width)]
            for k,v in enumerate(f):row[k+j]=v
            if deleted is not None:row=[v for k,v in enumerate(row) if k!=deleted]
            rows.append(row)
    return rows
def determinant_at(rows,x):return gaussian_det([[ev(a,x) for a in row] for row in rows])
def imul(a,b):
    vals=[x*y for x in a for y in b];return min(vals),max(vals)
def ihorner(p,box):
    out=(Q(0),Q(0))
    for c in reversed(p):
        out=imul(out,box);out=(out[0]+c,out[1]+c)
    return out
def bernstein(n,d,box,constant,curved):
    raw={k:Q(str(v)) for k,v in (d*constant-n).items()};power=[]
    for j in range(6):
        poly=[Q(0)]*(1+max(i for i,l in raw))
        for (i,l),v in raw.items():
            if l==j:poly[i]+=v
        if curved:
            for _ in range(2*j):poly=mul(poly,[2,1])
        power.append(trim(poly))
    bounds=[]
    for k in range(6):
        poly=[Q(0)]
        for j in range(k+1):poly=add(poly,scale(power[j],Q(comb(k,j),comb(5,j))))
        bounds.append(ihorner(poly,box))
    return bounds
def reduce_interpolation(values,start,h):
    # Exact forward interpolation at an independent negative-point grid.
    col=list(values);fall=[Q(1)];out=[Q(0)]
    for j in range(len(values)):
        out=rem(add(out,scale(fall,col[0]/factorial(j))),h)
        col=[b-a for a,b in zip(col,col[1:])]
        fall=rem(mul(fall,[-start-j,1]),h)
    return out
def literal_pinching(u):
    # Full original8x8 operator, with an independently generated cyclic
    # minimal polynomial. Collisions automatically reduce its degree.
    u=list(map(Q,u));need(len(u)==8 and sum(u)==0 and any(u),'literal balanced original profile')
    H=[[Q(int(i==j))*u[i]-(u[i]+u[j])/8 for j in range(8)] for i in range(8)]
    need(all(sum(row)==0 for row in H),'original empty e mode')
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    act=lambda x:[dot(row,x) for row in H]
    vectors=[u]
    for degree in range(1,8):
        candidate=act(vectors[-1]);G=[[dot(x,y) for y in vectors] for x in vectors]
        coeff=linear_solve(G,[dot(x,candidate) for x in vectors])
        residual=[candidate[j]-sum(coeff[k]*vectors[k][j] for k in range(degree)) for j in range(8)]
        if not any(residual):break
        vectors.append(candidate)
    else:raise ValueError('missing full cyclic recurrence')
    h=[-x for x in coeff]+[Q(1)];mom=[dot(u,v) for v in vectors]
    numerator=[Q(0)]*degree
    for k in range(degree):numerator[degree-1-k]=sum(h[degree-j]*mom[k-j] for j in range(k+1))
    weights=rem(mul(numerator,invmod(deriv(h),h)),h);square=rem(mul(weights,weights),h)
    powers=[Q(degree)]
    for k in range(1,len(square)):
        powers.append(-k*h[degree-k]-sum(h[degree-j]*powers[k-j] for j in range(1,k)))
    pinching=sum(a*powers[i] for i,a in enumerate(square))
    N=dot(u,u);m2=sum(x**4 for x in u)-N*N/8
    return {'pinching':pinching,'ratio':(N*N-pinching)/m2 if m2 else Q(16),'cyclic_degree':degree}
def polyval(p,x,y):return sum(Q(str(v))*x**i*y**j for (i,j),v in p.items())

def audit(name,data,alg):
    out=alg.family(name);r=out['ring'];x,V=r.gens;n,d=out['n'],out['d']
    p=alg.primitive(n.diff(x)*d-n*d.diff(x))[0];q=alg.primitive(n.diff(V)*d-n*d.diff(V))[0]
    pp,qq=poly_v(p),poly_v(q)
    need([len(pp)-1,len(qq)-1]==[9,8],'full stationary degrees')
    wp=max(i+2*j for i,j in p);wq=max(i+2*j for i,j in q)
    need(wp<=19 and wq<=18,'universal weighted degree bound')
    need(8*wp+9*wq-2*(136-28-36)<=170,'resultant degree at most170')
    factors=data['factors'];constant=data['resultant_constant'];rows=sylvester(pp,qq)
    need(len(rows)==17 and all(len(a)==17 for a in rows),'full17x17 original Sylvester')
    need(sum((len(f)-1)*m for f,m,b in factors)<=170,'proposed product degree bound')
    values=[]
    for a in range(-85,86):
        determinant=determinant_at(rows,a);expected=Q(constant)
        for f,m,boxes in factors:expected*=ev(f,a)**m
        need(determinant==expected,'universal resultant at independent integer grid')
        values.append(str(determinant))
    chart=(Q(0),Q(4,3)) if name=='321' else (Q(-2),Q(0))
    records=[];quartic=None
    for f,m,boxes in factors:
        degree=len(f)-1
        if degree==1:
            root=Q(-f[0],f[1])
            need(root in ([Q(1)] if name=='321' else [Q(-1),Q(-5,3)]) or not chart[0]<root<chart[1],'complete exceptional linear coverage')
            continue
        chain=sturm(f);need(ev(f,chart[0])!=0 and ev(f,chart[1])!=0,'nonroot chart endpoints')
        need(roots(chain,chart)==len(boxes),'exhaustive chart root count')
        previous=chart[0]
        for raw in boxes:
            box=tuple(map(Q,raw));need(previous<box[0]<box[1]<chart[1],'ordered disjoint root isolations');previous=box[1]
            need(all(ev(f,z)!=0 for z in box) and roots(chain,box)==1,'whole exact root isolation')
            if name=='421' and degree==4:quartic=list(map(Q,f));continue
            bound=bernstein(n,d,box,Q(49,2),name=='421')
            need(all(lo>0 for lo,hi in bound),'all six whole-strip Bernstein bounds')
            # A lower threshold is tested separately; unsuccessful candidates
            # would only be a limitation of this positivity certificate.
            tighter=bernstein(n,d,box,Q(24),name=='421')
            records.append({'degree':degree,'box':[str(z) for z in box],'upper49/2_bounds':[[str(a),str(b)] for a,b in bound],
                            'upper24_certified':all(lo>0 for lo,hi in tighter),'upper24_bounds':[[str(a),str(b)] for a,b in tighter]})
    minors={}
    if name=='421':
        need(quartic is not None,'quartic branch retained')
        for col,bound,start in [(0,135,-68),(1,137,-69)]:
            minor=sylvester(pp,qq,deleted=col)
            need(len(minor)==15 and all(len(a)==15 for a in minor),'literal15x15 coefficient minor')
            expected_bound=7*19+8*18-2*((120 if col==0 else 119)-49)
            need(expected_bound==bound,'specialized minor degree bound')
            vals=[determinant_at(minor,z) for z in range(start,start+bound+1)]
            coeff=reduce_interpolation(vals,start,quartic)
            minors[str(col)]=[str(v) for v in coeff]
        A=list(map(Q,minors['0']));B=list(map(Q,minors['1']))
        need(pgcd(A,quartic)==[1],'quartic leading minor universally nonzero')
        need(rem(add(B,mul(A,[4,8,4])),quartic)==[0],'forced original-label collision on every quartic root')
        for a,wanted in [(Q(-1),[0,0,0,0,1]),(Q(-5,3),[Q(-16,9),1])]:
            actual=pgcd([ev(v,a) for v in pp],[ev(v,a) for v in qq]);need(actual==wanted,'actual exceptional specialized gcd')
    return {'n':alg.encode(n),'d':alg.encode(d),'h':[alg.encode(v) for v in out['h']],
            'positive_scale':str(out['scale']),'stationary_p':alg.encode(p),'stationary_q':alg.encode(q),
            'resultant_integer_grid':[-85,85],'resultant_identity_checks':171,'resultant_value_hash':hashlib.sha256(json.dumps(values).encode()).hexdigest(),
            'strips':records,'minor_remainders':minors,'all_strips_upper24':all(x['upper24_certified'] for x in records)},out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--vendor',type=Path);parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'));parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.vendor:sys.path.insert(0,str(args.vendor.resolve()))
    spec=importlib.util.spec_from_file_location('independent_resolvent_algebra',Path(__file__).with_name('algebra.py'));alg=importlib.util.module_from_spec(spec);spec.loader.exec_module(alg)
    need(alg.sympy.__version__=='1.14.0','pinned exact polynomial library')
    cert=json.loads(Path(__file__).with_name('certificate.json').read_text());record={'agent':'six-reviewer-1','role':'independent mathematical reviewer','families':{}};outputs={};start=time.monotonic()
    for name in ['321','421']:
        rec,out=audit(name,cert['families'][name],alg);record['families'][name]=rec;outputs[name]=out
        need(rec['all_strips_upper24'],'every noncollision stationary strip has the stronger ceiling24')
        print('Completed original-resolvent/'+name+' and necessary stationary certificate.',file=sys.stderr,flush=True)
    pair=alg.paired();A,T,B=pair['A'],pair['T'],pair['B'];K=A*A-4*B;I=A*A+12*B;Delta=128*A**3-432*T*T
    need(256*pair['discriminant']==Delta,'paired cubic discriminant')
    need(pair['m2']==2*K,'paired fourth-moment excess')
    need(((16*pair['d']-pair['n'])*A*A-12*K*pair['d'])*Delta*K==576*T*T*I*I*pair['d'],'universal exact paired residual')
    record['paired']={'n':alg.encode(pair['n']),'d':alg.encode(pair['d']),'h':[alg.encode(v) for v in pair['h']]}
    rr,x,y,z=alg.ring('x,y,z',alg.sympy.QQ);w=-x-y-z;labels=[x,y,z,w]
    AA=-sum(labels[i]*labels[j] for i in range(4) for j in range(i+1,4));BB=x*y*z*w
    sos=((x-y)**2*(z-w)**2+(x-z)**2*(y-w)**2+(x-w)**2*(y-z)**2)/2
    need(AA*AA+12*BB==sos,'original paired-label sum of squares')
    # All unbalanced moment candidates, including discarded orders/supports.
    signrows=[]
    for n0 in (7,8):
        for k in (1,2,3):
            m=n0-k;X=Q(m**3+k**3,m*k*n0*n0);need(X>=Q(13,84),'every two-level sign moment candidate');signrows.append([n0,k,str(X)])
        for m in range(1,n0-1):
            k=n0-1-m;valid=False;moment=None
            if m>1 and k>1:
                u=Q(m-1,k-1);middle=1-u
                valid=-1<middle<u and middle!=0 and min(m+int(middle<0),k+int(middle>0))<=3
                if valid:
                    N=m+middle**2+k*u*u;moment=Q(m+middle**4+k*u**4)/N**2;need(moment==Q(7,44)>Q(13,84),'every admissible three-level sign candidate')
            signrows.append([n0,m,1,k,valid,str(moment) if moment else None])
    need(len(signrows)==17,'all six two-level plus eleven three-level cases')
    # Quantitative heavy-block refinement, independent rational square bound.
    aa=Q(464,5);bb=Q(71);coeff=[aa*aa,-2*aa*bb-8000,bb*bb+8000]
    discriminant_gap=4*coeff[2]*coeff[0]-coeff[1]**2
    need(discriminant_gap==Q(18432000,25)>0,'sharp-sign heavy4/25 square certificate')
    need(aa-bb>0,'legitimate square comparison on whole[0,1]')
    record['sign_moment_candidates']=signrows;record['heavy_refinement']={'linear_tau_coefficient':'4/25','orbit_quadratic_coefficient':'2/25','square_polynomial':[str(a) for a in coeff],'discriminant_gap':str(discriminant_gap)}
    # Independent full original-coordinate controls, actual Krylov ranks1..3.
    profiles=[]
    for a in [-2,-1,1,2]:
        for b,c in [(-3,-1),(-1,2),(1,3),(2,-2)]:
            profiles.append(('321',[a]*3+[b]*2+[c]*2+[-3*a-2*b-2*c],Q(a),Q((b-c)**2,4),Q(-(b+c),2)))
    for b,y0 in [(-3,1),(-2,0),(-1,0),(-1,1),(0,1),(1,2),(2,3),(-4,2)]:
        profiles.append(('421',[1]*4+[b]*2+[-2-b+y0,-2-b-y0],Q(b),Q(y0*y0),Q(1)))
    literal=[]
    for name,u,x0,V0,scale0 in profiles:
        result=literal_pinching(u);out=outputs[name]
        if name=='321' and scale0==0:
            # No projective normalization at zero negative-pair mean.
            actual=None
        else:
            xx=x0/scale0 if name=='321' else x0;vv=V0/(scale0*scale0) if name=='321' else V0
            num=polyval(out['n'],xx,vv);den=polyval(out['d'],xx,vv);actual=num/den if den else None
            if den:need(actual==result['ratio'],'full literal Krylov/resolvent ratio match')
        literal.append({'family':name,'original_profile':u,'pinching':str(result['pinching']),'ratio':str(result['ratio']),'cyclic_degree':result['cyclic_degree'],'universal_ratio_compared':actual is not None})
    need({x['cyclic_degree'] for x in literal}=={1,2,3},'all active collision ranks exercised')
    # Direct invariant controls include singular6+2/uniform and double mergers.
    for lab in [[-3,-1,1,3],[-5,1,1,3],[1,1,1,-3],[1,1,-1,-1],[0,0,1,-1]]:
        u=[x for x in lab for _ in range(2)];result=literal_pinching(u)
        A0=-sum(lab[i]*lab[j] for i in range(4) for j in range(i+1,4));T0=sum(lab[i]*lab[j]*lab[k] for i in range(4) for j in range(i+1,4) for k in range(j+1,4));B0=lab[0]*lab[1]*lab[2]*lab[3]
        def val(p):return sum(Q(str(v))*Q(A0)**i*Q(T0)**j*Q(B0)**k for (i,j,k),v in p.items())
        den=val(pair['d'])
        if den:need(val(pair['n'])/den==result['ratio'],'full original paired invariant control')
        else:need(result['ratio'] in (0,16),'singular collision handled without division')
        literal.append({'family':'paired','original_profile':u,'pinching':str(result['pinching']),'ratio':str(result['ratio']),'cyclic_degree':result['cyclic_degree'],'universal_ratio_compared':bool(den)})
    record['full_original_krylov_controls']=literal
    damages=[]
    def reject(condition,label):
        try:need(condition,label)
        except ValueError:damages.append(label)
        else:raise ValueError('Damaged identity accepted '+label)
    strip=tuple(map(Q,record['families']['321']['strips'][0]['box']))
    bad_bounds=bernstein(outputs['321']['n'],outputs['321']['d'],strip,Q(-1),False)
    reject(all(lo>0 for lo,hi in bad_bounds),'negative stationary ceiling fails the actual whole-strip certificate')
    reject(roots(sturm(cert['families']['321']['factors'][-1][0]),(Q(0),Q(4,3)))==0,'missing degree34 chart root')
    A0=list(map(Q,record['families']['421']['minor_remainders']['0']))
    B0=list(map(Q,record['families']['421']['minor_remainders']['1']))
    quartic=next(f for f,m,boxes in cert['families']['421']['factors'] if len(f)==5)
    reject(rem(add(B0,scale(mul(A0,[4,8,4]),-1)),quartic)==[0],'reversed quartic collision identity')
    reject(discriminant_gap<0,'heavy square sign reversed')
    reject(pair['m2']==K,'missing paired fourth-moment factor two')
    reject(literal_pinching([1]*4+[-1]*4)['pinching']==Q(64,2),'artificially split uniform full eigenspace')
    record.update(exact_checks=COUNT,damage_labels=damages,solver=None,formal_kernel=False,library='SymPy1.14.0 exact QQ polynomial rings; Fraction Gaussian/Sturm/interval/Krylov checks')
    normalized=json.loads(json.dumps(record));raw=(json.dumps(normalized,sort_keys=True,separators=(',',':'))+'\n').encode()
    if args.write:args.fixture.write_bytes(raw)
    else:need(json.loads(args.fixture.read_text())==normalized,'complete independently frozen record')
    print(json.dumps({'exact_checks':record['exact_checks'],'damage_controls':len(damages),'literal_original_controls':len(literal),'resultant_determinants':342,'minor_determinants':274,'seconds':time.monotonic()-start,'record_sha256':hashlib.sha256(raw).hexdigest(),'all321_strips_upper24':record['families']['321']['all_strips_upper24'],'all421_strips_upper24':record['families']['421']['all_strips_upper24']},sort_keys=True))
if __name__=='__main__':main()
