"""Independent general-cutoff original-entry certificate, with free kernel defect.
Polynomial kernel is this reviewer's prior published algebra.py; no target imports.
"""
from fractions import Fraction as Q
import hashlib
import json
from math import comb
from algebra import vars,zero


def need(ok,label):
    if not ok:raise ValueError(label)


def symbolic():
    n,s,K,A,S,V,J,mu=vars(8);h=s+n-1;G=2*s-2-2*K
    # Entire original-coordinate norm expansions; multiply by h^2.
    U0h=n*h+(h+s)*J+h*V
    normh2=n*h*h+(h*h+s*s)*A+h*h*S
    wh=U0h-n*s*h
    wnorm_and_complements=h*h*(n*n*G/2-2*n*V+2*S)
    wnorm_and_complements+=(h+s)**2*A-2*n*(h+s)*h*J+n*n*K*h*h
    lower=s*(G+4*K)+s*G-(G+2*K)**2
    direct=(h+s)*normh2-U0h**2-s*wnorm_and_complements+wh**2+mu*h*h*lower
    target=h*h*(n*h-n*(n-1)*s+(n-1)*S+mu*(4*s-4))+(h**3-h*s*s)*A
    zero(direct-target,'whole general-k original constant')
    zero(lower-(4*s-4),'entire lower-test constant')
    # Free individual edge coefficient and explicit cardinality defect.
    a,b,ua,ub,la,lb,m=vars(7)
    raw=2*(m*la*lb-ua*ub)
    shifted=2*(m*la*lb-(ua-a)*(ub-b))
    defect=2*(a*b-ua*b-ub*a)
    zero(raw-shifted-defect,'free original coefficient including kernel defect')
    # An arbitrary high root r; cleared completion gives exact minimizer.
    hh,ss,aa,rr=vars(4)
    completion=hh**2*rr**2-ss**2*aa**2-2*ss*aa*(hh*rr-ss*aa)
    zero(completion-(hh*rr-ss*aa)**2,'whole high-root square excess')
    n,s=vars(2);h=s+n-1;q=n*(n-1)/2;mu=(n/2-Q(5,4))**2
    original_upper=4*n*h*(n*h-n*(n-1)*s+mu*(4*s-4))
    original_upper+=4*n*(h*h-s*s)*4*q+h*(n-1)*(s+n)*(9*n-1)
    Fclear=h*(-s*(3*n*n-15*n-1)+n*(16*n**3-23*n*n+22*n-24))
    zero(original_upper-Fclear+16*n*q*(n-1)**2,'full k2 moment bound with retained root gain')
    n,T=vars(2);s=T-n
    F_times_4n=-s*(3*n*n-15*n-1)+n*(16*n**3-23*n*n+22*n-24)
    improved_times_4n=T*(-n*n+13*n+1)+n*(16*n**3-20*n*n+7*n-25)
    zero(F_times_4n+2*n*(n-1)*T-improved_times_4n,'log2 tail numerator')
    t=vars(1)[0]
    positive=[]
    for name,p,start in [
        ('R12 induction',12*n*n-23*n-13,12),
        ('original coefficient versus n/3',5*n*n-45*n-3,12),
        ('original remainder below4n3',23*n*n-22*n+24,12),
        ('R16 greater3T/4',12*n*n-23*n-13,16),
        ('new tail margin versus nT/80',11*n*n-260*n-20,24),
        ('new residual below4n3',20*n*n-7*n+25,24),
        ('T greater320n2 induction',n*n-2*n-1,24),
    ]:
        shifted=p.sub([start+t,0]);need(all(c>0 for c in shifted.d.values()),name)
        positive.append({'name':name,'start':start,'entire_shifted_polynomial':shifted.record()})
    need(2**11-12-12*12**2>0,'R12 base')
    need(2**13-16-12*16**2>0,'R16 strengthened base')
    need(2**23>320*24**2,'new exponential bound base')
    need(Q(8,3)**8>2304,'exact logarithm endpoint witness')
    return {'general_k_entire_constant_zero':True,'lower_entire_constant_zero':True,'free_entry_kernel_defect_zero':True,'high_root_square_zero':True,'k2_full_moment_bound_zero':True,'improved_tail_numerator_zero':True,'positive_induction_polynomials':positive,'exponential_base_margin':2**23-320*24**2,'log_endpoint_power_margin':str(Q(8,3)**8-2304)}


def profile(n,k):
    need(type(n) is int and n>=6 and type(k) is int and 2<=k<=(n-2)//2,'integer cutoff domain')
    T=2**(n-1);s=T-n;h=T-1;N=s+h;mu=Q((2*n-5)**2,16)
    v={a:max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n)) for a in range(k+1,n-k)}
    f={a:Q(a)-v[a] for a in v}
    ell={a:Q(0 if a<=k else 2 if a>=n-k else 1) for a in range(1,n-1)}
    u={a:Q(a) if a<=k else Q(s*(n-a),h) if a>=n-k else v[a] for a in range(1,n-1)}
    A=sum(a*a*comb(n,a) for a in range(2,k+1));B=A-4*comb(n,2)
    S=sum((comb(n,a)*x*x for a,x in v.items()),Q(0))
    eta=n*h-n*(n-1)*s+(h-Q(s*s,h))*A+(n-1)*S+mu*(4*s-4)
    return {'n':n,'k':k,'T':T,'N':N,'s':s,'h':h,'mu':mu,'v':v,'f':f,'ell':ell,'u':u,'A':A,'B':B,'S':S,'eta':eta}


def layer_record(n,k):
    p=profile(n,k);mu=p['mu'];f=p['f'];u=p['u'];ell=p['ell'];s=p['s'];h=p['h'];N=p['N']
    counts=proper=low_triple=0;rho=[]
    for a in range(1,n-1):
        for b in range(a,min(n-a,n-2)+1):
            raw=2*(mu*ell[a]*ell[b]-u[a]*u[b])
            defect=2*(a*b-u[a]*b-u[b]*a)
            shift=2*(mu*ell[a]*ell[b]-(u[a]-a)*(u[b]-b))
            need(raw==shift+defect,'entire individual edge coefficient')
            if a<=k or b<=k:
                need(shift==0,'all individual low-touching coefficients cancel')
                if a==3 or b==3:low_triple+=1
            elif a+b<n:
                need(a in f and b in f,'every remaining proper pair is bulk')
                r=1-f[a]*f[b]/mu;need(0<r<1,'strict whole proper weight');rho.append(r);proper+=1
                need(shift==2*mu*r,'original proper-pair multiplier')
            else:
                need(a in f and b in f and shift>=0,'whole complement deficit sign')
            counts+=1
    if rho:need(max(rho)==1-f[k+1]**2/mu,'exact maximal proper weight from first bulk layer')
    need(all(f[a]>0 for a in f),'positive f')
    need(all(f[a+1]>f[a] for a in list(f)[:-1]),'strict f monotonicity')
    # Literal cardinality sums, not the asserted closed constant as an input.
    norm_u=sum((comb(n,a)*u[a]**2 for a in u),Q(0));sum_u=sum((comb(n,a)*u[a] for a in u),Q(0))
    w={a:u[a]-a for a in u};norm_w=sum((comb(n,a)*w[a]**2 for a in w),Q(0));sum_w=sum((comb(n,a)*w[a] for a in w),Q(0))
    low_const=s*sum(comb(n,a)*ell[a]**2 for a in ell)-sum(comb(n,a)*ell[a] for a in ell)**2
    comp=sum((comb(n,a)*(mu*ell[a]*ell[n-a]-w[a]*w[n-a])*s for a in range(2,n-1)),Q(0))
    counted=N*norm_u-sum_u**2-s*norm_w+sum_w**2+mu*low_const+comp
    need(counted==p['eta'],'full independently counted original constant')
    moments=[sum((comb(n,a)*Q((2*a-n)**power,2**power) for a in range(n+1)),Q(0)) for power in [2,4]]
    need(moments==[2**n*Q(n,4),2**n*Q(3*n*n-2*n,16)],'entire finite binomial moment sums')
    if n>=12 and 6*p['B']<=s-12*n*n:
        need(p['eta']<-Q(s-12*n*n,3),'original sufficient margin')
    return {'n':n,'k':k,'original_pair_types':counts,'proper_bulk_pair_types':proper,'low_touching_triple_types':low_triple,'A':p['A'],'B':p['B'],'S':str(p['S']),'eta':str(p['eta']),'counted_eta':str(counted),'rho_max':str(max(rho)) if rho else None,'conditional_positive_mass_floor':str(-p['eta']/(2*h*mu*max(rho))) if rho else None,'conditional_weighted_floor':str(-p['eta']/(2*h*mu)),'binomial_moments':list(map(str,moments))}


def literal(n,k):
    p=profile(n,k);s=p['s'];N=p['N'];full=(1<<n)-1
    masks=[a for a in range(1,full+1) if a.bit_count()<=n-2];size=[a.bit_count() for a in masks];m=len(masks);index={a:i for i,a in enumerate(masks)}
    # Credited ordinary complement-family8106 affine control, redecoded here.
    B=[[Q(0) for _ in masks] for _ in masks]
    for i,a in enumerate(masks):
        for j in range(i+1,m):
            b=masks[j]
            if a&b:continue
            if size[i]==size[j]==1:z=Q(s-(2**(n-2)-2))
            elif min(size[i],size[j])==1:z=Q(1)
            elif a|b==full:z=Q(s-1)
            else:z=Q(0)
            B[i][j]=B[j][i]=z
    C=[[s*int(i==j)-1+B[i][j] for j in range(m)] for i in range(m)];rows=[sum(row) for row in C]
    L=[[1+sum(rows)]+[1-x for x in rows]]+[[1-rows[i]]+[1+x for x in C[i]] for i in range(m)]
    originals=[0]+masks;need(len(L)==N,'complete actual vertex census')
    star_checks=0
    for i,a in enumerate(originals):
        need(sum(L[i])==N,'actual empty and nonempty row')
        for j,b in enumerate(originals):
            need(L[i][j]==L[j][i],'literal matrix symmetry')
            if a&b:need(L[i][j]==s*int(i==j),'literal original support')
        for bit in range(n):
            need(sum(L[i][j] for j,b in enumerate(originals) if b&(1<<bit))==s,'each individual original star');star_checks+=1
    u=[p['u'][a] for a in size];ell=[p['ell'][a] for a in size];card=list(map(Q,size))
    def form(x,y,matrix):
        return sum((x[i]*sum((matrix[i][j]*y[j] for j in range(m)),Q(0)) for i in range(m)),Q(0))
    def evaluate():
        matrix=[[s*int(i==j)-1+B[i][j] for j in range(m)] for i in range(m)]
        phi=N*sum(x*x for x in u)-sum(u)**2-form(u,u,matrix)+p['mu']*form(ell,ell,matrix)
        defect=form([card[i]-2*u[i] for i in range(m)],card,matrix)
        rhs=p['eta'];proper=Q(0);deficits=Q(0)
        for i,a in enumerate(masks):
            if size[i] in p['f']:
                j=index[full^a];deficits+=(p['mu']-p['f'][size[i]]*p['f'][n-size[i]])*(s-B[i][j])
            for j in range(i+1,m):
                b=masks[j]
                if not(a&b) and a|b!=full and min(size[i],size[j])>k:
                    proper+=(p['mu']-p['f'][size[i]]*p['f'][size[j]])*B[i][j]
        rhs+=2*proper-deficits
        need(phi==rhs+defect,'whole original identity with free kernel defect')
        return list(map(str,[phi,rhs,defect,deficits]))
    clean=evaluate();need(Q(clean[2])==0,'unrestricted-row valid cardinality kernel')
    i,j=(index[7],index[120]) if k>=3 else (index[1],index[2]);B[i][j]+=Q(1,7);B[j][i]+=Q(1,7)
    damaged=evaluate();need(Q(damaged[2])!=0 and damaged[0]!=damaged[1],'missing kernel premise exposed')
    need(L[0][0]>N,'affine control is explicitly uncapped')
    return {'n':n,'k':k,'actual_vertices':N,'all_original_positions':N*N,'individual_star_equations':star_checks,'actual_empty_L':str(L[0][0]),'empty_upper_energy':str(N-L[0][0]),'clean_entire_identity':clean,'damaged_nonkernel_identity':damaged}


def trade(n=11,k=3):
    p=profile(n,k)
    def side(offset):
        a=sum(1<<(offset+i) for i in range(3));b=1<<(offset+3);c=1<<(offset+4)
        return {a|b:1,a|c:1,a:-1,a|b|c:-1}
    x,y=side(0),side(5)
    for z in [x,y]:
        need(sum(z.values())==0,'trade preserves each original row')
        for bit in range(n):need(sum(w for a,w in z.items() if a&(1<<bit))==0,'trade preserves each individual star')
    edges=[(a,b,xx*yy) for a,xx in x.items() for b,yy in y.items()]
    need(all(not(a&b) and a|b<(1<<n)-1 for a,b,w in edges),'allowed proper original trade positions')
    ux=sum(w*p['u'][a.bit_count()] for a,w in x.items());uy=sum(w*p['u'][a.bit_count()] for a,w in y.items())
    lx=sum(w*p['ell'][a.bit_count()] for a,w in x.items());ly=sum(w*p['ell'][a.bit_count()] for a,w in y.items())
    phi=2*(p['mu']*lx*ly-ux*uy)
    rhs=2*sum((w*(p['mu']-p['f'][a.bit_count()]*p['f'][b.bit_count()]) for a,b,w in edges if min(a.bit_count(),b.bit_count())>k),Q(0))
    need(phi==rhs!=0,'noninvariant general-k low-touching cancellation')
    return {'n':n,'k':k,'ordered_positions':32,'changed_low_three_touching_ordered_positions':14,'Phi_change':str(phi),'proper_weighted_M_change':str(rhs/(2*p['h']*p['mu'])),'literal_original_edges':[[a,b,w] for a,b,w in edges]}


def refinement():
    rows=[]
    for n in [24,25,32,64,128,256,512]:
        T=2**(n-1);s=T-n;h=T-1;mu=Q((2*n-5)**2,16)
        P=4*n**3-5*n*n+Q(7*n,4)-Q(25,4)
        E=Q(-n+13,4)*T+Q(T,4*n)+P
        need(E<-Q(n*T,10),'retained all-window log2 tail margin')
        delta=-E/(2*h*mu);need(delta>Q(1,5*n),'new unweighted positive mass margin')
        rows.append({'n':n,'upper_eta_at_B_le_T_over4':str(E),'strict_negative_margin':str(-Q(n*T,10)-E),'positive_mass_bound':str(delta),'new_simple_floor':str(Q(1,5*n)),'original_simple_floor':str(Q(1,2*n*n)),'simple_floor_improvement_factor':str(Q(2*n,5))})
    # Exact greatest integer satisfying the original sufficient criterion.
    original=[]
    for n in [24,32,64,128,256,512]:
        R=2**(n-1)-n-12*n*n;B=0;k=2
        while k<(n-2)//2:
            trial=B+(k+1)**2*comb(n,k+1)
            if 6*trial>R:break
            B=trial;k+=1
        need(6*B<=R and 6*(B+(k+1)**2*comb(n,k+1))>R,'entire exact last sufficient integer')
        original.append({'n':n,'k':k,'B':B,'margin':R-6*B,'next_failing_margin':6*(B+(k+1)**2*comb(n,k+1))-R})
    return {'new_cutoff':'n/2-sqrt((n/2)*log(2*n^2))','all_n_domain':'every integer n>=24','new_simple_positive_original_mass_floor':'1/(5*n)','sample_exact_bounds':rows,'entire_original_sufficient_cutoff_table':original}


def negative_controls():
    rejected=[]
    def reject(name,f):
        try:f()
        except ValueError:rejected.append(name);return
        raise ValueError('accepted damaged mathematics '+name)
    for n,k in [(True,2),(5,2),(8,True),(8,4),(8,1)]:reject('domain-'+str((n,k)),lambda n=n,k=k:profile(n,k))
    z=trade();reject('unordered-factor-two',lambda:need(Q(z['Phi_change'])==Q(z['proper_weighted_M_change'])*profile(11,3)['h']*profile(11,3)['mu'],'wrong unordered coefficient'))
    p=profile(11,3);a=3;b=4;raw=2*(p['mu']*p['ell'][a]*p['ell'][b]-p['u'][a]*p['u'][b]);defect=2*(a*b-p['u'][a]*b-p['u'][b]*a)
    reject('omit-low-touching-kernel-defect',lambda:need(raw==0,'low coefficient without kernel'))
    need(raw==defect!=0,'actual low triple coefficient requires kernel')
    reject('forced-original-log2-mass-at-n12',lambda:need(2**11>320*12**2,'new proof lower endpoint'))
    return rejected


def record():
    orders=[(6,2),(7,2),(8,2),(8,3),(10,2),(10,3),(10,4),(11,3),(12,2),(12,3),(16,3),(16,6),(24,5),(32,7),(64,17),(128,41)]
    return {'schema':'six-reviewer-1-general-cutoff-independent-v1','symbolic':symbolic(),'original_layer_coefficient_cases':[layer_record(n,k) for n,k in orders],'literal_original_controls':[literal(6,2),literal(9,3)],'noninvariant_trade':trade(),'proved_tail_refinement':refinement(),'mathematical_damage_rejections':negative_controls()}


def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
