"""Independent whole-budget/phase reconstruction of LEMMA9857.

Written formulas exposed. ONLY OWN345e13e exact primitives are imported.
No new target executable/fixture is imported. Universal analytic bridges
are ordinary mathematics, not formalized by these finite coefficient maps.
"""
from fractions import Fraction as F
from math import comb
from owned_effective import K,P,G,OMEGA_POWERS,cosine,variable,real,evaluate,greal,digest,require


class R:
    """Separate rational sparse polynomial; monomials are sorted variable tuples."""
    def __init__(self,v=0):
        self.d=dict(v.d)if isinstance(v,R)else ({k:F(x)for k,x in v.items()if x}if isinstance(v,dict)else ({():F(v)}if v else {}))
    def __add__(self,b):
        d=dict(self.d)
        for k,v in R(b).d.items():
            d[k]=d.get(k,F(0))+v
            if not d[k]:del d[k]
        return R(d)
    __radd__=__add__
    def __neg__(self):return R({k:-v for k,v in self.d.items()})
    def __sub__(self,b):return self+-R(b)
    def __rsub__(self,b):return R(b)+-self
    def __mul__(self,b):
        d={}
        for k,v in self.d.items():
            for l,w in R(b).d.items():
                m=tuple(sorted(k+l));d[m]=d.get(m,F(0))+v*w
        return R(d)
    __rmul__=__mul__
    def __truediv__(self,b):return self*(1/F(b))
    def __pow__(self,n):
        require(isinstance(n,int)and n>=0,'rational polynomial power')
        a=R(1)
        for _ in range(n):a=a*self
        return a
    def __eq__(self,b):return self.d==R(b).d
    def pack(self):return [[list(k),str(v)]for k,v in sorted(self.d.items())if v]


def rv(name):return R({(name,):1})


def build(config=None):
    cfg={'alpha':F(7,8),'final_variance':F(5),'pair_coefficient':F(4,5),
         'fine_normal':F(9,8),'objective':F(243),'physical':F(272),
         'new_objective':F(238),'new_physical':F(268),
         'imaginary_quadratic':F(31),'motion_delta':F(19,2),'lower_degree3_present':True}
    cfg.update(config or {})
    margins={};identities=[];equalities={};phase=[];records={}
    def positive(name,value):
        value=F(value);require(value>0,'strict whole-window margin: '+name)
        margins[name]=str(value);return value
    def identity(name,lhs,rhs):
        lhs=P(lhs);rhs=P(rhs);require(lhs==rhs,'WHOLE identity: '+name)
        data=lhs.pack();identities.append({'name':name,'whole_map':data,'sha256':digest(data)})
    def ratid(name,lhs,rhs):
        lhs=R(lhs);rhs=R(rhs);require(lhs==rhs,'WHOLE rational identity: '+name)
        data=lhs.pack();identities.append({'name':name,'whole_rational_map':data,'sha256':digest(data)})
    def equal(name,lhs,rhs):
        lhs=F(lhs);rhs=F(rhs);require(lhs==rhs,'rational equality: '+name)
        equalities[name]=str(lhs)
    e=F(1,16000);a=1-e;h=F(1,375);rho=F(1,54);r0=F(3999,4000)
    alpha=cfg['alpha']
    def root_budget(name,rho,v):
        lo=a-rho;hi=1+rho;s=hi+v/2
        A={j:F(9,8*j)*comb(8,9-j)*rho**(7-j)for j in range(1,7)}
        A[7]=F(9,14);Cd=sum(j*A[j]*s**(j-1)for j in A)
        Bd=9*lo**8-18*s**7*v-Cd*v
        positive(name+'RMS',8*rho*rho-v)
        positive(name+'circle separation',F(4,9)*lo-v)
        positive(name+'entire Rouche',F(9,2)*lo**8-9*s**7*v-sum(A[j]*(s**j+hi**j)for j in A))
        positive(name+'Bd',Bd)
        return {'rho':rho,'v':v,'lo':lo,'hi':hi,'s':s,'A':A,'Cd':Cd,'Bd':Bd}
    broad=root_budget('broad ',rho,h)
    lo,hi,s,A,Cd,Bd=[broad[n]for n in ['lo','hi','s','A','Cd','Bd']]
    tau0=F(1,19)
    positive('broad centered tail radius',tau0*tau0-h)
    Nc=F(7,4)*sum(A[j]*hi**j for j in [1,2,4,5,7])
    positive('broad cube displacement',Bd/5-Nc);positive('broad cube linear displacement',9*lo**8/5-Nc)
    Be=F(4,25)*s**7/lo**8+Cd/(45*lo**8)
    Bs={5:F(63,32),4:F(63,32)*rho,2:F(9,128)*rho*h,1:F(9,4096)*h*h}
    lt=sum(Bs[j]*lo**(j-7)for j in Bs)
    bp=(1+2*rho)*Be+F(1,50)+lt/6
    bi=(1+2*rho)*Be+F(1,50)+lt/5
    positive('broad complete pair error4over5',cfg['pair_coefficient']-bp)
    positive('broad complete individual error7over8',F(7,8)-bi)
    beta=F(4,7)-1/(2*r0**3)-tau0/((r0-tau0)*r0**3)
    kap=beta-F(1216,225)*h
    positive('adopted exact fixed mean-square coefficient',kap-F(1,1000))
    positive('broad complete first tail3over5',F(3,5)-(1/(2*lo**3)+tau0/((lo-tau0)*lo**3)))
    positive('broad r0',(1-r0)-(3*e+F(3,5)*h)/8)
    positive('broad Q coefficient sign',F(3,4)/hi**3-F(4,7))
    positive('preliminary t1over375',(F(1,375)-F(2,15)*h)**2-(e/12+e*e/3))
    positive('sqrt eta1over126',F(1,126)**2-e)
    positive('preliminary sqrt budget361over1250',F(361,1250)**2-(F(1,12)+e/3))
    positive('preliminary t square1over9',F(1,3)-(F(28,630)+F(361,1250)))
    alpha_p=F(42,5*375)+F(4,5)*42**2*e
    alpha_i=F(42,5*375)+F(7,8)*42**2*e
    positive('early upper r1plus3eta',F(6)-(F(16,3)+e/3+F(4,3)*alpha_p))
    early=1-F(141,40)*e
    positive('early lower radius',early-tau0)
    positive('EARLY inverse cube11',11-F(423,40)/early**4)
    positive('early complex mean upper3',3-(F(3,40)*42-F(5,8)+F(1,18)/a))
    positive('early complex mean lower4',4-(F(2,3)+3+F(2,3)*alpha_p)/a)
    tau=F(6,125);tail=tau/((early-tau)*early**3)
    positive('early centered radius',tau*tau-F(7,8)*42*e)
    positive('early whole individual slack3over5',F(3,5)-(F(1,16)+(F(45,16)+F(21,8)*42)*e+F(3,16)*42*tail+alpha_i))
    positive('sqrt3 individual weight',F(7,6)**2-F(4,3))
    positive('early D15over4',F(15,4)-(3+F(7,10))/a)
    positive('early mean norm11over2',F(11,2)**2-16-F(15,4)**2)
    rows=[(F(42),F(6,125),F(38)),(F(38),F(23,500),F(28)),
          (F(28),F(1,25),F(16)),(F(16),F(3,100),F(10)),
          (F(10),F(3,125),F(8)),(F(8),F(21,1000),F(15,2)),
          (F(15,2),F(41,2000),F(7))]
    boot=[]
    for old,tau,new in rows:
        divisor=F(4,7)-1/(2*r0**3)-tau/((r0-tau)*r0**3)-F(16,3)*(F(11,2)*e/5+cfg['pair_coefficient']*old*e)
        positive('bootstrap radius '+str(old),tau*tau-F(7,8)*old*e)
        positive('bootstrap positive divisor '+str(old),divisor)
        positive('bootstrap next '+str(new),new*divisor-(F(1,3)+F(4,3)*e))
        boot.append({'previous':str(old),'tau':str(tau),'next':str(new),'divisor':str(divisor)})
    positive('final lower r1minuseta',1-(3+F(3,5)*7)/8)
    coarseEp=F(11,2)*7/5+F(4,5)*49
    positive('final upper r1pluseta',2-(F(1,3)+e/3+F(4,3)*coarseEp*e))
    positive('FINAL inverse cube4',4-(3-3*e+e*e)/a**3)
    tauv=F(1,50);Gv=1/((a-tauv)*a**4);Kv=F(3,2)/a**4
    positive('two-square centered tail',tauv*tauv-F(7,8)*7*e)
    Bv=F(976,225)+alpha*(Gv+F(7,10)*Kv*Kv)
    divisor=F(1,14)-4*e-7*Bv*e
    positive('two-square positive divisor',divisor)
    positive('two-square V below5eta',cfg['final_variance']*divisor-(F(1,3)+F(4,3)*e))
    fineV=cfg['final_variance']
    tau=F(1,60);qstar=tau/((a-tau)*a**3)
    positive('final tail radius1over60',tau*tau-F(7,8)*fineV*e)
    equal('final pair51over2 endpoint',F(51,2),F(11,2)*fineV/5+F(4,5)*fineV**2)
    equal('final individual219over8 endpoint',F(219,8),F(11,2)*fineV/5+F(7,8)*fineV**2)
    positive('final joint mean variance12',12-(F(28,3)+(F(112,3)+112*fineV)*e+28*fineV*qstar+F(448,3)*F(51,2)*e))
    positive('final joint J bound5over2',F(25,4)-6)
    positive('final individual slack1over12',F(1,12)-(F(1,16)+(F(45,16)+F(21,16)*fineV)*e+F(3,16)*fineV*qstar+F(219,8)*e))
    positive('final imaginary mean1over3',F(1,3)-(F(7,72)+F(5,28))/a)
    positive('final real mean lower4over5',F(4,5)-(F(2,3)+F(1,14)+F(2,3)*F(51,2)*e)/a)
    positive('final real mean negative',a*a/4-1/(18*a))
    equal('final mean norm13over15',F(13,15)**2,F(4,5)**2+F(1,3)**2)
    # Fine RMS uses equality rather than a false strict margin.
    equal('fine RMS8rho2',8*F(1,160)**2,5*e)
    # root_budget's RMS check is strict; h-fine is known STRICTLY smaller
    # than5e from V<5eta. Pass a symbolic endpoint equality separately.
    vf=5*e;rf=F(1,160);fl=a-rf;fh=1+rf;fs=fh+vf/2
    positive('fine mean within1over160',rf-F(13,15)*e)
    FA={j:F(9,8*j)*comb(8,9-j)*rf**(7-j)for j in range(1,7)};FA[7]=F(9,14)
    FC=sum(j*FA[j]*fs**(j-1)for j in FA);FBd=9*fl**8-18*fs**7*vf-FC*vf
    FN=2*sum(FA[j]*fh**j for j in FA)
    positive('fine root circles separation',F(4,9)*fl-vf)
    positive('fine whole Rouche',F(9,2)*fl**8-9*fs**7*vf-sum(FA[j]*(fs**j+fh**j)for j in FA))
    positive('fine quarter displacement',FBd/4-FN);positive('fine quarter linear displacement',9*fl**8/4-FN)
    BF=fs**7/(4*fl**8)+FC/(36*fl**8)
    FBS={5:F(63,32),4:F(63,32)*rf,3:F(21,128)*vf,2:F(9,128)*rf*vf,1:F(9,4096)*vf**2}
    lower=sum(FBS[j]*fl**(j-7)for j in FBS)
    positive('fine all-phase COMPLETE half-normal9over8',cfg['fine_normal']-((1+2*rf)*BF+F(1,32)+F(2,9)*lower))
    positive('fine all-phase COMPLETE motion',1-(BF+F(2,9)*lower/a))
    FCube=F(7,4)*sum(FA[j]*fh**j for j in [1,2,4,5,7])
    positive('fine cube1over6 displacement',FBd/6-FCube);positive('fine cube1over6 linear',9*fl**8/6-FCube)
    FCBe=fs**7/(9*fl**8)+FC/(54*fl**8)
    cubelower=sum(FBS[j]*fl**(j-7)for j in [1,2,4,5])
    positive('fine cube COMPLETE pair',1-((1+2*rf)*FCBe+F(1,72)+cubelower/6))
    positive('fine cube COMPLETE individual',1-((1+2*rf)*FCBe+F(1,72)+cubelower/5))
    fullR3=F(1,2)+F(3,2)*F(4,5)+F(3,2)*F(169,225)+F(13,15)*5/6+25
    fullR4=F(1,2)+2*F(4,5)+2*F(169,225)+F(13,15)*5/4+cfg['fine_normal']*25
    fullDrop=8*F(4,5)*(2-e)/a**2+4*F(169,225)/a**3+20
    positive('fine whole cube29',29-fullR3);positive('fine whole fourth33',33-fullR4)
    positive('fine individual cube26',26-(F(13,15)*5/6+25))
    positive('fine whole reciprocal36',36-fullDrop)
    cl,ch=F(15,16),F(47,50);cubic=lambda z:8*z**3-6*z-1
    positive('cosine lower sign',-cubic(cl));positive('cosine upper sign',cubic(ch));positive('cosine branch increasing',24*cl*cl-6)
    w3lo=F(2,3)*(16*cl-9)/(2*cl-1);w3hi=F(2,3)*(16*ch-9)/(2*ch-1)
    w4lo=1/(ch+2*ch*ch-1);w4hi=1/(cl+2*cl*cl-1)
    positive('dual w3 lower4',w3lo-4);positive('dual w3 upper23over5',F(23,5)-w3hi)
    positive('dual w4 lower1over2',w4lo-F(1,2));positive('dual w4 upper3over5',F(3,5)-w4hi)
    positive('whole190 normal cost',190-(36+29*w3hi+33*w4hi))
    Gfinal=1/((a-F(1,60))*a**4);Kfinal=F(3,2)/a**4+F(3,20)/a
    positive('original OBJECTIVE243',cfg['objective']-(190+25*alpha*(Gfinal+Kfinal*Kfinal/2)))
    positive('original PHYSICAL272',cfg['physical']-(190+25*alpha*(Gfinal+Kfinal*Kfinal)))
    fullNormal=fullDrop+w3hi*fullR3+w4hi*fullR4
    obj=fullNormal+25*alpha*(Gfinal+Kfinal*Kfinal/2)
    phys=fullNormal+25*alpha*(Gfinal+Kfinal*Kfinal)
    positive('PROVED retained OBJECTIVE238',cfg['new_objective']-obj)
    positive('PROVED retained PHYSICAL268',cfg['new_physical']-phys)
    positive('original rational141over50',F(826,291)-cfg['objective']*e-F(141,50))
    positive('refined rational141over50',F(826,291)-cfg['new_objective']*e-F(141,50))
    positive('sharp slope below3',3-F(8,3)-F(16,93))
    for physical,label in [(cfg['physical'],'original '),(cfg['new_physical'],'refined ')]:
        positive(label+'sqrt Delta at least16',physical-256)
        positive(label+'cube residual3over8',F(3,8)-(F(1,4)+29/physical))
        positive(label+'fourth residual1over2',F(1,2)-(33/physical+5/(32*a)))
        positive(label+'Cramer mean8over5',F(8,5)-(F(62,651)*F(3,8)+F(128,217)*F(5,2)))
        positive(label+'Cramer Q9over5',F(9,5)-(F(24832,32550)*F(3,8)+F(128,217)*F(5,2)))
        positive(label+'trace26',26-14*F(9,5))
        equal(label+'variance34 strict-input endpoint',34,26+8)
        positive(label+'H35',1-8*F(169,225)/physical)
        positive(label+'imaginary sqrt1',1-F(80,196)/a**2)
        positive(label+'imaginary Delta1',1-F(7,24)/a)
        positive(label+'imaginary eta2 coefficient31',cfg['imaginary_quadratic']-F(91,3)/a)
        positive(label+'unrotated real energy13',1-(F(384,25)+4*e/a**2)/physical)
        positive(label+'motion full88',88-(62+25+F(896,1395)/a))
        positive(label+'mu3 square21over2',F(21,2)**2-F(7,8)*125)
        positive(label+'motion Delta19over2',cfg['motion_delta']-(F(26,5)+F(26,7)/a+88/physical))
        positive(label+'motion sqrt7over2',F(7,2)-(2+F(9,7)/a+F(7,96)/a**2))
    records.update(endpoint=str(e),whole_broad={k:({str(j):str(x)for j,x in v.items()}if isinstance(v,dict)else str(v))for k,v in broad.items()},broad_Nc=str(Nc),broad_Be=str(Be),broad_Bj={str(j):str(x)for j,x in Bs.items()},broad_pair=str(bp),broad_individual=str(bi),adopted_beta=str(beta),adopted_kappa=str(kap),early_radius=str(early),early_alpha_pair=str(alpha_p),early_alpha_individual=str(alpha_i),whole_variance_bootstrap=boot,two_square_Bv=str(Bv),two_square_divisor=str(divisor),fine_A={str(j):str(x)for j,x in FA.items()},fine_Bj={str(j):str(x)for j,x in FBS.items()},fine_Cd=str(FC),fine_Bd=str(FBd),fine_N=str(FN),fine_Bf=str(BF),fine_cube_Be=str(FCBe),full_R3=str(fullR3),full_R4=str(fullR4),full_reciprocal_cost=str(fullDrop),full_normal_cost=str(fullNormal),refined_objective_cost=str(obj),refined_physical_cost=str(phys),G=str(Gfinal),K=str(Kfinal),alpha=str(alpha))
    # Full ordinary identities in the openly credited OWN cyclotomic field.
    c=-cosine(4);d=cosine(1);y=1/(K(3)*(1+c));x=K(F(2,3))-y;C=K(F(8,3))+y
    w4=1/(c+d);w3=F(2,3)*(7-(1-d)*w4)
    A3,A4=1-cosine(3),1-cosine(4);B3,B4=1-cosine(6),1-cosine(8)
    for name,lhs,rhs in [
        ('cosine cubic',8*c**3-6*c,1),('double angle',d,2*c*c-1),
        ('sharp cube optimum',A3*x+B3*y,1),('sharp fourth optimum',A4*x+B4*y,1),
        ('dual mean',w3*A3+w4*A4,8),('dual variance',w3*B3+w4*B4,7),
        ('dual sharpC',8-w3-w4,C),('dual weight monotone form',w3*(2*c-1),F(2,3)*(16*c-9)),
        ('Cramer determinant',A4*B3-A3*B4,F(3,2)*(c+d))]:
        identity(name,lhs,rhs)
    au=variable('a');u=variable('u');ub=variable('ub');m=au-u;mb=au-ub
    M=(m+mb)/2;T=variable('T');U=variable('U3');Q=real(T*ub*variable('u',-1));H3=real(U*ub*variable('u',-2))
    for k,w in enumerate(OMEGA_POWERS):
        wn=OMEGA_POWERS[-k%9];z=m+u*w;zm=m+u*wn
        base=(z*z.conjugate()+zm*zm.conjugate()-2)/4;Ak=1-cosine(k)
        identity('whole base pair '+str(k),base,(au*au-1)/2-Ak*(au*M-m*mb))
        residual=sum((variable('d'+str(j))*u**j*(w**j-1)for j in range(1,8)),P())
        direct=-residual*variable('u',-8)*w**-8/9
        whole=sum((variable('d'+str(j))*variable('u',j-8)*(w-w**(j-8))/9
                   for j in range(1,8)if j!=3 or cfg['lower_degree3_present']),P())
        identity('whole all-lower displacement '+str(k),direct,whole)
        def principal(w):
            dd=-T*variable('u',-1)*(w-w**-1)/14-U*variable('u',-2)*(w-w**-2)/18
            return real(ub*w.conjugate()*dd)
        expected=-(1-cosine(2*k))*Q/14+(cosine(3*k)-1)*H3/18
        identity('whole second-third pair '+str(k),(principal(w)+principal(wn))/2,expected)
        phase.append({'k':k,'A':Ak.pack(),'B':(1-cosine(2*k)).pack(),'cubic':((cosine(3*k)-1)/18).pack()})
    # All eighth centered coordinates are ELIMINATED, not assumed zero-sum.
    xs=[rv('x'+str(j))for j in range(7)];ys=[rv('y'+str(j))for j in range(7)]
    xs.append(-sum(xs,R()));ys.append(-sum(ys,R()))
    ns=[xx*xx+yy*yy for xx,yy in zip(xs,ys)];V=sum(ns,R())
    fourth=sum((z*z for z in ns),R());sos=R()
    for j in range(8):
        inner=sum(((xs[k]-xs[l])**2+(ys[k]-ys[l])**2
                   for k in range(8)for l in range(k+1,8)if k!=j and l!=j),R())
        ratid('entire seven-complement variance '+str(j),inner,7*V-8*ns[j])
        sos=sos+ns[j]*inner
    ratid('WHOLE centered quartic SOS',7*V*V-8*fourth,sos)
    vx=sum((z*z for z in xs),R());vy=sum((z*z for z in ys),R())
    xy=sum((xx*yy for xx,yy in zip(xs,ys)),R())
    wedges=sum(((xs[j]*ys[k]-xs[k]*ys[j])**2 for j in range(8)for k in range(j+1,8)),R())
    ratid('WHOLE covariance Gram',V*V-(vx-vy)**2-4*xy*xy,4*wedges)
    X,Y=rv('X'),rv('Y')
    ratid('WHOLE signed Legendre cubic Cauchy',F(9,4)*X*X*(X*X+Y*Y)**2-(X**3-F(3,2)*X*Y*Y)**2,F(5,4)*X**6+F(15,2)*X**4*Y**2)
    ratid('WHOLE real cubic Cauchy',9*X*X*(X*X+Y*Y)**2-(X**3-3*X*Y*Y)**2,8*X**6+24*X**4*Y**2)
    tt,vv,ee,kv,wc=[rv(z)for z in ['t','V','sqrtE','K','Wc']]
    ratid('WHOLE mean square',4*tt*tt-F(16,15)*tt*vv,4*(tt-F(2,15)*vv)**2-F(16,225)*vv*vv)
    ratid('WHOLE contraction real-energy square',F(5,14)*ee*ee-kv*wc*ee,F(5,14)*(ee-F(7,5)*kv*wc)**2-F(7,10)*kv*kv*wc*wc)
    ratid('WHOLE physical E-quarter square',ee*ee/4-kv*wc*ee,(ee/2-kv*wc)**2-kv*kv*wc*wc)
    ratid('WHOLE objective E-half square',ee*ee/2-kv*wc*ee,(ee-kv*wc)**2/2-kv*kv*wc*wc/2)
    # Independent complete bridge coefficients, not evaluations on a grid.
    eta=1-au;t2=m*mb;rr=u*ub
    pp=-eta+eta**2/2-F(3,2)*au*M+F(3,2)*t2-F(3,28)*Q
    identity('WHOLE anchored radial constraint',rr-(1-F(2,3)*eta+eta**2/3-t2+Q/7),F(4,3)*pp)
    ep=variable('Ep');vvP=variable('V');tailP=variable('tail');rminus3=variable('r',-3)
    mean_bound=-F(5,8)*au**2*eta+t2*variable('a',-1)/2-au**2*(vvP+3*Q)*rminus3/32+au**2*tailP/8
    substituted=eta-eta**2/2+F(3,2)*au*mean_bound-F(3,2)*t2+F(3,28)*Q
    whole_slack=eta-eta**2/2-F(15,16)*au**3*eta-F(3,4)*t2-F(3,64)*vvP-F(15,448)*Q+F(3,64)*(1-au**3*rminus3)*(vvP+3*Q)+F(3,16)*au**3*tailP
    identity('WHOLE individual-slack substitution',substituted,whole_slack)
    identity('WHOLE joint variance retained coefficients',(vvP+3*Q)/4-F(4,7)*Q,vvP/4+F(5,28)*Q)
    identity('WHOLE two-square real-energy coefficients',(vvP+3*Q)/4-F(4,7)*Q,vvP/14+F(5,14)*(vvP+Q)/2)
    L3=-A3*M-B3*Q/14;L4=-A4*M-B4*Q/14
    identity('WHOLE dual linear elimination',w3*L3+w4*L4,-8*M-Q/2)
    ss3,ss4,R3,R4=[variable(z)for z in ['s3','s4','R3','R4']]
    # Replace L3/L4 by the ACTUAL disk equations including the signed cubic.
    replacement=w3*(eta-ss3-R3)+w4*(eta-ss4+H3/12-R4)
    elimination=8*eta-replacement-Q/2+(vvP+3*Q)/4
    identity('WHOLE physical signed-cubic coercivity',elimination,C*eta+w3*ss3+w4*ss4+(vvP+Q)/4+w3*R3+w4*R4-w4*H3/12)
    dm,dq,l3,l4=[variable(z)for z in ['dm','dq','l3','l4']]
    det=A3*B4-A4*B3
    solm=(-B4*l3+B3*l4)/det;solq=(A4*l3-A3*l4)/det
    identity('WHOLE Cramer first residual',-A3*solm-B3*solq,l3)
    identity('WHOLE Cramer second residual',-A4*solm-B4*solq,l4)
    qq,hh=rv('Q'),rv('eta')
    ratid('WHOLE joint imaginary-trace conic',(12*hh-5*qq)**2-49*qq**2,294*hh**2-24*(qq+F(5,2)*hh)**2)
    mr,di=rv('M'),rv('D')
    actual=sum(((mr+xx)**2+(di+yy)**2 for xx,yy in zip(xs,ys)),R())
    ratid('WHOLE actual critical-energy decomposition',actual,V+8*(mr*mr+di*di))
    # Homogeneous Legendre maps built by THREE unrelated finite formulas.
    radius2=X*X+Y*Y;leg=[R(1),X];legendre=[]
    for n in range(2,13):leg.append((2*n-1)*X*leg[-1]/n-(n-1)*radius2*leg[-2]/n)
    for n in range(13):
        gen=sum((F(comb(2*m,m),4**m)*comb(m,n-m)*(2*X)**(2*m-n)*(-radius2)**(n-m)for m in range((n+1)//2,n+1)),R())
        lap=sum((F(comb(n,2*j)*comb(2*j,j),4**j)*(-1)**j*X**(n-2*j)*Y**(2*j)for j in range(n//2+1)),R())
        ratid('Legendre recurrence/generating WHOLE degree'+str(n),leg[n],gen)
        ratid('Legendre recurrence/Laplace WHOLE degree'+str(n),leg[n],lap)
        legendre.append({'degree':n,'whole_coefficients':leg[n].pack()})
    ww,base,shift=[rv(z)for z in ['w','base','shift']]
    telescoping=[]
    for n in range(1,10):
        direct=ww**n-base**n
        factor=(ww-base)*sum((ww**(n-1-j)*base**j for j in range(n)),R())
        ratid('WHOLE telescoping degree'+str(n),direct,factor)
        telescoping.append({'degree':n,'whole_factor':sum((ww**(n-1-j)*base**j for j in range(n)),R()).pack()})
    ratid('WHOLE principal nonlinear two-integral Taylor',(base+shift)**9-base**9-9*base**8*shift,sum((F(72*comb(7,j),(j+1)*(j+2))*base**(7-j)*shift**(j+2)for j in range(8)),R()))
    controls=fresh_controls(alpha)
    return {'schema':'independent-wider-quadratic-audit-v1','agent':'six-reviewer-1','role':'independent mathematical reviewer','whole_arithmetic':records,'strict_margins':margins,'rational_equalities':equalities,'whole_identities':identities,'whole_phase_table':phase,'whole_Legendre_through_degree12':legendre,'whole_telescoping_through_degree9':telescoping,'fresh_Gaussian_controls':controls,'proved_objective_remainder':str(cfg['new_objective']),'proved_physical_remainder':str(cfg['new_physical']),'trust':'Ordinary universal analytic bridges unformalized; OWN345e13e primitive ancestry exposed; no new target code/fixture import.'}


def fresh_controls(alpha=F(7,8),datasets=None):
    """Entire subset-product and independently multiplied literal controls.

    These algebra tuples are NOT low-objective or original-disk witnesses.
    Only the first has evident disk feasibility, and it is in the HIGH arm.
    """
    e=F(1,16000)
    if datasets is None:
        datasets=[
          ('total centered collision; actual HIGH-objective disk case',G(),[G()]*8),
          ('E-zero imaginary repeated centered tuple',G(-e/4),[G(0,F(y,4096))for y in [1,-1,2,-2,3,-3,0,0]]),
          ('nonconjugate Gaussian centered tuple',G(-e/2,e/9),[G(F(x,8192),F(y,8192))for x,y in [(1,2),(3,-2),(-2,4),(4,1),(-3,-1),(-1,-3),(2,0),(-4,-1)]]),
          ('multiple-collision nonconjugate centered tuple',G(-2*e/3,-e/11),[G(F(x,16384),F(y,16384))for x,y in [(1,1),(1,1),(1,1),(-2,3),(-2,3),(4,-1),(0,-2),(-3,-6)]]),
          ('complex two-level quartic ratio43over56',G(-e/5,e/13),[G(F(1,8192),F(2,8192))]*7+[G(F(-7,8192),F(-14,8192))])]
    def rational(g):
        require(g.i==0 and all(x==0 for x in g.r.v[1:]),'literal real rational scalar')
        return g.r.v[0]
    out=[]
    for name,mean,nus in datasets:
        require(len(nus)==8 and sum(nus,G())==0,'literal full centered tuple')
        au=G(1-e);u=au-mean
        # Direct subset expansion, separately checked by eight-factor folding.
        subset=[G()for _ in range(9)]
        for bits in range(256):
            term=G(1);count=0
            for j in range(8):
                if bits>>j&1:term=term*nus[j];count+=1
            subset[8-count]=subset[8-count]+(-1)**count*term
        fold=[G(1)]
        for nu in nus:
            nxt=[G()for _ in range(len(fold)+1)]
            for j,z in enumerate(fold):nxt[j]=nxt[j]-nu*z;nxt[j+1]=nxt[j+1]+z
            fold=nxt
        require(fold==subset,'WHOLE independent critical-product routes')
        integrated=[G()]+[9*z/(j+1)for j,z in enumerate(subset)]
        integrated[0]=-sum((integrated[j]*u**j for j in range(1,10)),G())
        require(sum((integrated[j]*u**j for j in range(10)),G())==0,'literal ACTUAL marked root')
        require([(j+1)*integrated[j+1]/9 for j in range(9)]==subset,'WHOLE derivative recovery')
        T=sum((z**2 for z in nus),G());U3=sum((z**3 for z in nus),G())
        norms=[rational(z*z.conjugate())for z in nus];V=sum(norms,F());fourth=sum((z*z for z in norms),F())
        require(integrated[7]==-9*T/14 and integrated[6]==-U3/2,'full Newton second-third coefficient')
        require(sum((rational((mean+z)*(mean+z).conjugate())for z in nus),F())==V+8*rational(mean*mean.conjugate()),'literal actual H decomposition')
        quartic_gap=alpha*V*V-fourth
        require(quartic_gap>=0,'literal universal quartic coefficient')
        sos=F()
        for j in range(8):
            inner=sum((rational((nus[k]-nus[l])*(nus[k]-nus[l]).conjugate())for k in range(8)for l in range(k+1,8)if k!=j and l!=j),F())
            require(inner==7*V-8*norms[j],'literal seven-complement variance')
            sos+=norms[j]*inner
        require(sos==7*V*V-8*fourth,'literal entire quartic SOS')
        rotated=T*u.conjugate()/u;Q=greal(rotated);J=(rotated-rotated.conjugate())/G(0,2)
        r2=rational(u*u.conjugate());energy=sum((rational(greal(z*u.conjugate())**2)for z in nus),F())/r2
        require(G(energy)==(G(V)+Q)/2,'literal rotated real energy')
        cubic=greal(U3*u.conjugate()/u**2)
        require(cubic==greal(sum(((z*u.conjugate())**3 for z in nus),G()))/(r2*r2),'literal WHOLE complex cubic rotation')
        values={'a':au,'u':u,'ub':u.conjugate(),'T':T,'Tb':T.conjugate(),'U3':U3,'U3b':U3.conjugate()}
        values.update({'d'+str(j):integrated[j]for j in range(1,8)})
        phase=[]
        for k,wK in enumerate(OMEGA_POWERS):
            w=G(wK);z=mean+u*w
            pv=sum((integrated[j]*(u*w)**j for j in range(10)),G())
            direct=-pv/(9*(u*w)**8)
            formal=sum((variable('d'+str(j))*variable('u',j-8)*(wK-wK**(j-8))/9 for j in range(1,8)),P())
            require(direct==evaluate(formal,values),'literal entire phase displacement')
            half=greal(z.conjugate()*direct)
            phase.append({'k':k,'base':z.pack(),'whole_displacement':direct.pack(),'whole_linear_half_normal':half.pack()})
        item={'name':name,'mean':mean.pack(),'centered': [z.pack()for z in nus],'whole_product': [z.pack()for z in subset],'whole_anchored_integral':[z.pack()for z in integrated],'T':T.pack(),'U3':U3.pack(),'V':str(V),'fourth':str(fourth),'SOS':str(sos),'quartic_gap':str(quartic_gap),'Q':Q.pack(),'J':J.pack(),'E':str(energy),'whole_rotated_cubic':cubic.pack(),'whole_nine_phase_values':phase,'trust':'Algebra controls only; no low-sublevel or generic original-disk feasibility claim.'}
        out.append({**item,'whole_sha256':digest(item)})
    return out
