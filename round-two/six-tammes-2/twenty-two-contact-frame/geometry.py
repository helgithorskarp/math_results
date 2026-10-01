"""Exact G22 frame derivation, Q(t)[z,f]/(f^2-D*G).

Actual author six-tammes-2, researcher. A generic symbolic identity is
separate from the packing-to-frame coverage proof and from exclusions.
"""
import hashlib,json,math,signal,time
import sympy as sp
from sympy.polys.rings import ring

def derive():
    started=time.monotonic()
    t=sp.Symbol('t');K=sp.QQ.frac_field(t);T=K.from_sympy(t)
    R,z=ring('z',K);zero,one=R.zero,R.one
    def c(a):return R.ground_new(K.convert(a))
    def need(ok,message):
        if not ok:raise ValueError(message)
    D=(1-T)**2*(1+2*T)
    r=2*T/(1+T)
    k=T*(9*T*T-2*T-3)/(1+T)**2
    gamma=k/(1+k)
    mu=(T-1)*(T+1)*(2*T+1)*(3*T-1)/(9*T**3-T*T-T+1)
    den=(2*r-1)*(r+1)
    H=[[one if i==j else c(T) for j in range(3)] for i in range(3)]
    HI=[[c((1/(1-T) if i==j else 0)-T/((1-T)*(1+2*T))) for j in range(3)] for i in range(3)]
    def mv(M,x):return [sum((a*b for a,b in zip(row,x)),zero) for row in M]
    def dot(x,y):return c(1-T)*sum((a*b for a,b in zip(x,y)),zero)+c(T)*sum(x,zero)*sum(y,zero)
    def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
    B={i:[one if j==s else zero for j in range(3)] for s,i in enumerate((1,2,4))}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        B[n]=[c(r)*(a+b)-v for a,b,v in zip(B[i],B[j],B[o])]
    d=mv(HI,cross(B[12],B[1]));C=one+c(D)*z*z
    N=[c(T)*a*C+(c(D)*z*z-one)*(b-c(T)*a)+c(2*D)*z*v for a,b,v in zip(B[12],B[1],d)]
    S=dot(N,B[10]);E=C*C-S*S
    G=C*C-S*S-c(k*k+T*T)*C*C+c(2*k*T)*S*C
    rad=c(D)*G
    need(dot(N,N)==C*C,'reciprocal chart unit identity')
    need(dot(N,B[12])==c(T)*C,'chart contact 7-12')
    need(S==c(D)*(c(T)*z*z-2*z)+c(T*(2*T-1)),'explicit S polynomial')
    need(dot(N,B[1])-c(T)*C==c((1-T)*(1+2*T))*((c((1-T)**2)*z*z)-one),'bounded chart packing inequality')
    need(c(mu*mu*(1+k)**2)==c(D*(1+2*k)),'orientation square identity')
    need(c(1+2*k)==c((3*T-1)**2*(2*T+1)/(1+T)**2),'positive outer Gram determinant factor')
    need(c(k-T)==c(4*T*(2*T+1)*(T-1)/(1+T)**2),'k-t factor')
    need(c(k+T)==c(2*T*(5*T*T-1)/(1+T)**2),'k+t factor')
    def sign_certificate(value,sign):
        numerator=value.numer.as_expr()
        denominator=value.denom.as_expr()
        def coefficients(p):
            p=sp.Poly(p,t,domain=sp.QQ)
            lo=sp.Rational(14,25);width=sp.Rational(593,1000)-lo
            power=sp.Poly(p.as_expr().subs(t,lo+width*t),t,domain=sp.QQ)
            n=power.degree()
            return [sum(power.nth(i)*sp.Rational(math.comb(j,i),math.comb(n,i)) for i in range(j+1)) for j in range(n+1)]
        nb,db=coefficients(numerator),coefficients(denominator)
        if all(a<0 for a in db):nb=[-a for a in nb];db=[-a for a in db]
        need(all(a>0 for a in db),'strict denominator Bernstein certificate')
        need(all(sign*a>0 for a in nb),'strict numerator Bernstein certificate')
        return {'numerator_degree':len(nb)-1,'denominator_degree':len(db)-1,'signed_numerator_min':str(min(sign*a for a in nb)),'denominator_min':str(min(db))}
    parameter_signs={'k_plus_3_10':sign_certificate(k+K.convert(sp.Rational(3,10)),1),'k_plus_1_5':sign_certificate(k+K.convert(sp.Rational(1,5)),-1)}
    VN0=[(c(k)*C-c(T)*S)*a+(c(T)*C-c(k)*S)*C*b for a,b in zip(N,B[10])]
    VN1=mv(HI,cross(N,B[10]))
    # Pair (a,b) denotes a+b*f, with f^2=rad. Every vector has a
    # single displayed rational denominator; no symbolic division in z.
    def pa(a,b):return (a[0]+b[0],a[1]+b[1])
    def pm(a,b):return (a[0]*b[0]+rad*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def scale(x,q):return [(a*q,b*q) for a,b in x]
    def pcross(x,y):return [pa(pm(x[1],y[2]),scale_pair(pm(x[2],y[1]),-1)),pa(pm(x[2],y[0]),scale_pair(pm(x[0],y[2]),-1)),pa(pm(x[0],y[1]),scale_pair(pm(x[1],y[0]),-1))]
    def scale_pair(a,q):return (a[0]*q,a[1]*q)
    def psum(x):
        out=(zero,zero)
        for v in x:out=pa(out,v)
        return out
    def pdot(x,y):return pa(scale_pair(psum([pm(a,b) for a,b in zip(x,y)]),c(1-T)),scale_pair(pm(psum(x),psum(y)),c(T)))
    def pmv(M,x):
        out=[]
        for row in M:
            v=(zero,zero)
            for a,b in zip(row,x):v=pa(v,scale_pair(b,a))
            out.append(v)
        return out
    W=[(a,zero) for a in N];V=list(zip(VN0,VN1))
    need(pdot(V,V)==(E*E,zero),'unit V for both radical conjugates')
    need(pdot(W,V)==(c(k)*C*E,zero),'W-V equilateral contact for both radical conjugates')
    need(pdot(V,[(a,zero) for a in B[10]])==(c(T)*E,zero),'V-B10 retained contact for both radical conjugates')
    contacts=sorted([(0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(8,13),(9,10),(9,11),(10,12)])
    need(len(contacts)==22,'literal contact set size')
    for i,x in B.items():need(dot(x,x)==one,'unit B'+str(i))
    Bsigns={}
    for ii,i in enumerate(sorted(B)):
        for j in sorted(B)[ii+1:]:
            gap=dot(B[i],B[j])-c(T)
            if (i,j) in contacts:need(gap==zero,'B contact')
            else:
                need(gap.degree()<=0,'B gap independent of z')
                Bsigns[f'{i}-{j}']=sign_certificate(gap.get((0,),K.zero),-1)
    # Independent small Gram-matrix reconstruction: use an abstract
    # equilateral U,W,V rather than repeatedly expanding their coordinates.
    Arows={6:[1,0,0],7:[0,1,0],9:[0,0,1],0:[r/den,r/den,(1-r)/den],5:[(1-r)/den,r/den,r/den],11:[r/den,(1-r)/den,r/den]}
    def adot(x,y):return sum((K.convert(a)*K.convert(b)*(K.one if i==j else k) for i,a in enumerate(x) for j,b in enumerate(y)),K.zero)
    for i,x in Arows.items():need(adot(x,x)==K.one,'abstract A unit '+str(i))
    h=4*T*T/(1+T)-1
    for ii,i in enumerate(sorted(Arows)):
        for j in sorted(Arows)[ii+1:]:
            product=adot(Arows[i],Arows[j])
            expected=T if (i,j) in contacts else (k if i in (6,7,9) and j in (6,7,9) else h)
            need(product==expected,'complete abstract A Gram table')
    for new,a,b,old in ((6,0,11,5),(7,0,5,11),(9,5,11,0)):
        need(all(K.convert(Arows[new][i])==r*(Arows[a][i]+Arows[b][i])-Arows[old][i] for i in range(3)),'inverse reflection relation')
    need(h-T==(3*T+1)*(T-1)/(1+T),'strict internal A gap factor')
    labels=sorted(list(B)+[0,5,6,7,9,11])
    def encoded(q):
        # Canonical rational coefficients with increasing z-degree.
        return [str(q.get((i,),K.zero)) for i in range(max(q.degree(),0)+1)]
    def pair_encoded(q):return [encoded(q[0]),encoded(q[1])]
    fingerprints={};counts={};degrees={}
    for eta in (-1,1):
        normal=pmv(HI,pcross(W,V))
        U=[pa(scale_pair(pa(scale_pair(w,E),scale_pair(v,C)),c(gamma)),scale_pair(n,c(eta*mu))) for w,v,n in zip(W,V,normal)]
        common=C*E
        P={i:([(a,zero) for a in b],one) for i,b in B.items()}
        P[6]=(U,common);P[7]=(W,C);P[9]=(V,E)
        Wup=scale(W,E);Vup=scale(V,C)
        for label,coeffs in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):
            points=[]
            for j in range(3):
                value=(zero,zero)
                for a,x in zip(coeffs,(U,Wup,Vup)):value=pa(value,scale_pair(x[j],c(a)))
                points.append(value)
            P[label]=(points,c(den)*common)
        table=[];maxdeg=[0,0]
        for i in sorted(Arows):
            for j in sorted(B):
                if tuple(sorted((i,j))) in contacts or (i,j)==(7,1):continue
                x,a=P[i];y,b=P[j];gap=pa(pdot(x,y),(-c(T)*a*b,zero))
                for h in (0,1):maxdeg[h]=max(maxdeg[h],int(gap[h].degree()) if gap[h] else 0)
                table.append([i,j,pair_encoded(gap)])
        need(len(table)==39,'all remaining intercluster inequalities')
        digest=hashlib.sha256(json.dumps(table,separators=(',',':')).encode()).hexdigest()
        fingerprints[str(eta)]=digest;counts[str(eta)]={'implied_units':len(labels),'implied_contacts':len(contacts),'remaining_intercluster_gaps':len(table)};degrees[str(eta)]=maxdeg
    out={'format':1,'agent':'six-tammes-2','role':'researcher','domain':'Q(t)[z,f]/(f^2-D*G)','interval':['14/25','593/1000'],'deleted_contacts':[[6,8],[9,13]],'labels':labels,'contacts':[list(pair) for pair in contacts],'chart_polynomials':{name:encoded(p) for name,p in [('C',C),('S',S),('E',E),('G',G)]},'conjugate_epsilon_branches':[-1,1],'eta_branches':[-1,1],'identity_counts':counts,'pair_gap_z_degrees':degrees,'pair_gap_coefficient_sha256':fingerprints,'generic_kernel_identities':11,'parameter_signs':parameter_signs,'B_noncontact_signs':Bsigns,'generic_A_Gram_checks':21,'generic_A_reflection_checks':9}
    return out

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda s,f:(_ for _ in ()).throw(TimeoutError('160-second exact derivation guard')))
    signal.alarm(160)
    print(json.dumps(derive(),indent=2))
