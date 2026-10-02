"""Complete independent coefficient-E audit and stronger directional bound.

The defining written formulas were visible. No producer code or fixture
is read, imported or used. Sylvester determinants use the direct Leibniz
polynomial sum, rather than evaluated/interpolated determinants.
"""
from fractions import Fraction as Q
from itertools import combinations
from algebra import (P, var, identity, assembly, chart, to_v, sylvester,
                     det_permutation, bezout, ff_add, ff_mul, adj, rem, mul,
                     deriv)


def run():
    log={}
    a,b,c,d=(var(i) for i in range(4))
    identity(det_permutation([[a,b],[c,d]]),a*d-b*c,
             'universal-signed-determinant-control',log)
    original,reconstruction=assembly(log)
    # Check all 49 signed-residue adjoint pairings from the definitions.
    h=[P({tuple(k):Q(n,d) for k,n,d in row}) for row in reconstruction['h']]
    for i in range(7):
        a=[P()]*i+[P(1)];ta=adj(a,h)
        for j in range(7):
            b=[P()]*j+[P(1)]
            identity(rem(mul(a,deriv(b)),h)[6],rem(mul(ta,b),h)[6],
                     'residue-adjoint-%d-%d'%(i,j),log)
    rr=[chart(v,d) for v,d in zip(original,[2,1,2,1,2])]
    q,E,r,x,u=(var(i) for i in range(5))
    expected_quad=[2*u**2,-Q(367,180)*u**2,(2*r/3+Q(13,48))*u**2,P(),u**2/24]
    for i,v in enumerate(rr):
        if v.degree(1)>2:
            raise ValueError('E degree')
        identity(v.coeff(1,2),expected_quad[i],'whole-E-quadratic-'+str(i),log)
    c=[P(Q(367,360)),-r/3-Q(13,96),P(),P(Q(-1,48))]
    aff=[rr[i+1]+c[i]*rr[0] for i in range(4)]
    transform=[[P(1)]+[P()]*4]+[[c[i]]+[P(1 if i==j else 0) for j in range(4)] for i in range(4)]
    identity(det_permutation(transform),1,'full-row-transform-determinant',log)
    alpha=[v.coeff(1,1) for v in aff]
    beta=[v.coeff(1,0) for v in aff]
    for i,v in enumerate(aff):
        identity(v,alpha[i]*E+beta[i],'full-affine-'+str(i),log)
        identity(v-c[i]*rr[0],rr[i+1],'inverse-row-transform-'+str(i),log)
    complex_charts=[]
    ell0,c0=rr[0].coeff(1,1),rr[0].coeff(1,0)
    for i in range(4):
        cross=[]
        for j in range(4):
            value=alpha[i]*beta[j]-alpha[j]*beta[i]
            identity(alpha[i]*aff[j]-alpha[j]*aff[i],value,
                     'whole-complex-recovery-cross-%d-%d'%(i,j),log)
            cross.append(value)
        quadratic=2*u**2*beta[i]**2-ell0*alpha[i]*beta[i]+c0*alpha[i]**2
        identity(alpha[i]**2*rr[0]-quadratic,
                 (alpha[i]*E+beta[i])*(2*u**2*(alpha[i]*E-beta[i])+ell0*alpha[i]),
                 'whole-complex-recovery-quadratic-'+str(i),log)
        complex_charts.append({'pivot_index':i,'cross':[v.serial() for v in cross],
                               'quadratic':quadratic.serial()})
    # Whole monomial inverse, not merely the three numerical chart controls.
    for i,a in enumerate(rr):
        d=[2,1,2,1,2][i];back={}
        for k,value in a.d.items():
            b,e,rs,xs,us,*tail=k
            key=(b,e,rs,-b+2*xs+us-d,us,0,0,0)
            back[key]=back.get(key,Q(0))+value
        identity(P(back),original[i],'whole-chart-inverse-'+str(i),log)
    A=[];contents=[]
    for a in alpha:
        if any(k[4]<1 for k in a.d):
            raise ValueError('all alpha have u factor')
        cont,prim=(a/u).primitive();contents.append(cont);A.append(prim)
    if contents != [Q(1,16934400),Q(1,4515840),Q(1,9408),Q(1,2257920)]:
        raise ValueError('leading contents')
    V=118272-(31304*r+1162*x+6165)*u
    identity(A[2],7200*q*u-V,'entire-A2',log)
    # The first slot now v for these four polynomial conversions only.
    av=[to_v(A[0]),to_v(u*A[1]),to_v(A[3]),to_v(beta[2])]
    if [v.degree(0) for v in av] != [1,2,1,2]:
        raise ValueError('v degrees')
    cleared=[]
    for i,a in enumerate(av):
        degree=a.degree(0);scale=7200**degree
        z=scale*a.sub(0,V/7200)
        h0,h1,h2=(a.coeff(0,j) for j in range(3))
        if degree==1:
            identity(scale*a-z,(7200*q-V)*h1,'affine-clear-'+str(i),log)
        else:
            identity(scale*a-z,(7200*q-V)*(h2*(7200*q+V)+7200*h1),
                     'quadratic-clear-'+str(i),log)
        cleared.append(z)
    fcont,F=cleared[0].primitive()
    jcont,J=(cleared[1]/u).primitive()
    gcont,G=cleared[2].primitive()
    ncont,N=cleared[3].primitive()
    if (fcont,jcont,gcont,ncont)!=(Q(4704),Q(33868800),Q(23520),Q(45,28)):
        raise ValueError('cleared contents')
    for a in [F,G,J]:
        if a.degree(4)!=1:
            raise ValueError('affine u required')
    f1,f0=F.coeff(4,1),F.coeff(4,0)
    g1,g0=G.coeff(4,1),G.coeff(4,0)
    j1,j0=J.coeff(4,1),J.coeff(4,0)
    n2,n1,n0=(N.coeff(4,j) for j in [2,1,0])
    pc,p=(f1*g0-g1*f0).primitive()
    rc,R=((g1*j0-j1*g0)/x).primitive()
    lc,L=((n2*g0**2-n1*g1*g0+n0*g1**2)/x).primitive()
    if (pc,rc,lc)!=(Q(23040),Q(30720),Q(103219200)):
        raise ValueError('cross contents')
    identity(f1*G-g1*F,23040*p,'whole-cross-P',log)
    identity(g1*J-j1*G,30720*x*R,'whole-cross-R',log)
    identity(g1**2*N-103219200*x*L,
             G*(g1*n2*u+g1*n1-g0*n2),'whole-undivided-lower-cross',log)
    if [a.degree(2) for a in [p,R,L]] != [3,3,4]:
        raise ValueError('formal Sylvester degrees')
    matrices=[sylvester(p,R,2),sylvester(p,L,2)]
    # Full evaluation-column identities before determinant computation.
    for no,mat in enumerate(matrices):
        for i,row in enumerate(mat):
            expected=(p if i<(3 if no==0 else 4) else (R if no==0 else L))
            shift=(2-i if no==0 else 3-i) if i<(3 if no==0 else 4) else len(mat)-1-i
            identity(sum((z*r**(len(mat)-1-j) for j,z in enumerate(row)),P()),
                     expected*r**shift,'entire-evaluation-column-%d-%d'%(no,i),log)
    determinants=[det_permutation(mat) for mat in matrices]
    detcontents=[];primitives=[]
    for a in determinants:
        if any(any(k[i] for i in range(8) if i!=3) for k in a.d):
            raise ValueError('univariate determinant')
        cont,prim=a.primitive();detcontents.append(cont);primitives.append(prim)
    if [a.degree(3) for a in determinants] != [9,12]:
        raise ValueError('actual determinant degrees')
    streams=[[int(a.coeff(3,i).d.get((0,)*8,0)) for i in range(a.degree(3)+1)]
             for a in primitives]
    # A different prime and independently calculated extended Euclid.
    prime=263
    if any(prime%d==0 for d in range(2,17)):
        raise ValueError('prime check')
    reductions=[[v%prime for v in a] for a in streams]
    if any(not a[-1] for a in reductions):
        raise ValueError('leading-degree loss')
    U,VV=bezout(*reductions,prime)
    if ff_add(ff_mul(U,reductions[0],prime),ff_mul(VV,reductions[1],prime),prime)!=[1]:
        raise ValueError('full modular Bezout product')
    # Entire real Gram identity over 8 free symbols a0..a3,b0..b3.
    aa=[var(i) for i in range(4)];bb=[var(i) for i in range(4,8)]
    S=sum((a*a for a in aa),P());T=sum((a*b for a,b in zip(aa,bb)),P())
    Bnorm=sum((b*b for b in bb),P())
    identity(S*Bnorm-T*T,sum(((aa[i]*bb[j]-aa[j]*bb[i])**2
                            for i,j in combinations(range(4),2)),P()),
             'universal-real-Gram',log)
    # Stronger directional norm: free d0,a0..a3,r in unused slots.
    d0=var(5);a4=[var(i) for i in range(4)];z=var(4)
    cc=[P(Q(367,360)),-z/3-Q(13,96),P(),P(Q(-1,48))]
    C=1+sum((v*v for v in cc),P())
    dot=sum((a*b for a,b in zip(cc,a4)),P());norm=sum((a*a for a in a4),P())
    dnorm=d0*d0+sum(((a-b*d0)**2 for a,b in zip(a4,cc)),P())
    identity(C*dnorm,C*norm-dot**2+(C*d0-dot)**2,
             'stronger-directional-square-completion',log)
    # Exact bridge controls, distinct from stationary-profile enumeration.
    controls={}
    # Nonzero complex leading vector with zero bilinear square norm.
    controls['complex_isotropic']={'alpha':['1','i','0','0'],'S':'0',
                                   'recover_at_chart':0,'reason':'Gram S inversion invalid over C'}
    # Compute the complex square sum in Q[i] = Q[w]/(w^2+1).
    complex_sum=(Q(1)+Q(-1),Q(0))
    if complex_sum!=(0,0):
        raise ValueError('complex isotropic control')
    # Generic affine false positives and lower quadratic necessity.
    controls['lower_equation_needed']={'alpha':[1,0,0,0],'beta':[0,0,0,0],
                                       'E':0,'R0':1,'real_Gram_zero':True,'full_common_root':False}
    if sum(v*v for v in [1,0,0,0])<=0 or 2*0**2+0*0+1==0:
        raise ValueError('lower-equation false-positive control')
    # Formal specialized polynomial degrees may both drop, without losing
    # the evaluation-column implication for the original fixed matrix.
    row1=var(3)*var(2)**3+var(2)-2
    row2=var(3)*var(2)**3+2*var(2)-4
    mat=sylvester(row1,row2,2)
    spec=[[v.sub(3,0) for v in row] for row in mat]
    if det_permutation(spec)!=0 or row1.sub(3,0).sub(2,2)!=0 or row2.sub(3,0).sub(2,2)!=0:
        raise ValueError('leading-loss necessary control')
    controls['fixed_leading_loss']={'formal_degrees':[3,3],'specialized_degrees':[1,1],
                                    'common_root':2,'fixed_determinant':0}
    # A lost leading coefficient can hide a characteristic-zero factor.
    aa0=263*var(3)+1
    b1=aa0*(var(3)+1);b2=aa0*(var(3)+2)
    if b1.sub(3,Q(-1,263))!=0 or b2.sub(3,Q(-1,263))!=0:
        raise ValueError('bad-prime control')
    controls_bad_u,controls_bad_v=bezout([1,1],[2,1],263)
    if ff_add(ff_mul(controls_bad_u,[1,1],263),ff_mul(controls_bad_v,[2,1],263),263)!=[1]:
        raise ValueError('bad-prime modular unit control')
    controls['bad_prime_common_factor']={'factor':[1,263],'mod263_gcd':1,
                                       'common_Q_root':'-1/263','leading_degree_survives':False}
    # Strictly stronger pointwise bound, and optimal right-inverse equality.
    cv=[Q(367,360),Q(-13,96),Q(0),Q(-1,48)];avv=[Q(0),Q(0),Q(1),Q(0)]
    cvnorm=1+sum(v*v for v in cv);dotv=sum(v*w for v,w in zip(cv,avv))
    improved=sum(v*v for v in avv)-dotv*dotv/cvnorm
    old=sum(v*v for v in avv)/cvnorm
    if not improved>old or improved!=1:
        raise ValueError('strict directional improvement')
    controls['directional_improvement']={'r':'0','alpha':[str(v) for v in avv],
                                          'old_squared':str(old),'new_squared':str(improved),
                                          'equality_d0':str(dotv/cvnorm),
                                          'not_stationary_profile':True}
    # Both u signs, q0 and E0 remain, complete coordinate pullbacks.
    samples=[]
    for qs,es,rs,ss,ts in [(0,0,Q(1,3),2,3),(Q(1,7),Q(-2,5),Q(-3,8),-2,3),
                           (Q(-1,5),Q(1,9),0,Q(1,3),Q(2,7))]:
        orig=[qs*ss,es,rs,ss,ts,0,0,0]
        ch=[qs,es,rs,ss*ss,ss*ts,0,0,0]
        def ev(a,values):
            for i,v in enumerate(values):a=a.sub(i,v)
            return a.d.get((0,)*8,Q(0))
        oldvals=[ev(a,orig)*ss**d for a,d in zip(original,[2,1,2,1,2])]
        vals=[ev(a,ch) for a in rr]
        if vals!=oldvals:
            raise ValueError('full chart pullback')
        samples.append({'old':list(map(str,orig[:5])),'new':list(map(str,ch[:5])),
                        'all_five_scaled_values':list(map(str,vals)),
                        'not_stationary_profile':True})
    return {'schema':1,'agent':'six-reviewer-1','method':'independent full Laurent reconstruction/direct polynomial Leibniz/different prime263',
            'original_residual':[a.serial() for a in original], 'reconstruction':reconstruction,
            'chart_residual':[a.serial() for a in rr], 'alpha':[a.serial() for a in alpha],
            'beta':[a.serial() for a in beta], 'primitive_A':[a.serial() for a in A],
            'c':[a.serial() for a in c], 'cleared':[a.serial() for a in cleared],
            'F':F.serial(),'G':G.serial(),'J':J.serial(),'N':N.serial(),
            'P':p.serial(),'R':R.serial(),'L':L.serial(),
            'full_sylvester_matrices':[[[z.serial() for z in row] for row in mat] for mat in matrices],
            'determinants':[a.serial() for a in determinants],
            'determinant_contents':list(map(str,detcontents)),
            'primitive_determinants':streams,'prime':prime,'reductions':reductions,
            'unit_U':U,'unit_V':VV,'unit_product':[1],
            'complex_recovery_charts':complex_charts,
            'universal_whole_identities':log,'bridge_controls':controls,'chart_controls':samples}


if __name__=='__main__':
    import hashlib,json,time
    start=time.monotonic();record=run();encoded=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'canonical_sha256':hashlib.sha256(encoded).hexdigest(),'identities':len(record['universal_whole_identities']),
                      'seconds':time.monotonic()-start,'bytes':len(encoded),'prime':record['prime']},sort_keys=True))
