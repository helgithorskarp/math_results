"""Fresh exact payments for the ordinary normalization/clipping bridges."""
from fractions import Fraction as Q
from math import comb
from face import Poly,T,need,constants,root

def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def payment(eps,origin_cap):
    need(eps>0 and origin_cap>0,'positive displacement and gradient caps')
    l,h,m=Q(27,40),Q(11,16),Q(16,27)
    bm,bp,c=1-h*h,1-l*l,l+1-l*l-h
    aa=min(l*(1-l*l),h*(1-h*h))
    need((bm,bp,c,aa)==(Q(135,256),Q(871,1600),Q(851,1600),Q(1485,4096)),'marked endpoint budgets')
    need(m==1/(1+h) and l>Q(1,2) and h<1,'closed radius floor and rotation domain')
    S0=8+eps;R=S0-7*m;u=Q(57,80)-eps/8;E=Q(23,5)+2*(R+1)*eps;sigma=(S0-m)/7
    need(E+16*u-8==8+2*R*eps,'synchronized whole-path coefficients')
    need(u>0 and S0-8*m>0 and sigma>0,'floor-preserving clipping domains')
    # Every coefficient of the removed-slot J polynomial, by two routes.
    jp=bp*T*(h+bp*sigma*T)**7
    jvector=jp.matrix(1,9)[0]
    other=[Q(0)]+[bp*comb(7,i)*h**(7-i)*(bp*sigma)**i for i in range(8)]
    need([Q(x) for x in jvector]==other,'complete eight-term J polynomial')
    LJ=jp.integrated_t()[0]
    need(LJ==sum(x/(i+1) for i,x in enumerate(other)) and LJ<Q(2,3),'whole J gradient integral')
    B=[Q(8,7),-16*l*u/7,h*h*(8+2*R*eps)/7]
    need(B[2]>0 and B[1]+2*B[2]<0 and sum(B)>0,'whole-interval B positive and decreasing')
    cb=Q(107,100);need(cb*cb>Q(8,7),'square root majorant')
    bp3=Poly({(0,j):x for j,x in enumerate(B)})**3
    vector=[Q(x) for x in bp3.matrix(1,7)[0]];other=mul(mul(B,B),B)
    need(vector==other,'entire seven signed O coefficients, distinct literal convolution')
    weighted=sum(x/(i+2) for i,x in enumerate(vector))
    need(weighted==(T*bp3).integrated_t()[0],'whole weighted O integral')
    LO=9*h*cb*weighted;need(0<LO<origin_cap,'fresh paid origin gradient')
    ratio=Q(1);ratio_poly=[Q(1)]
    for _ in range(8):ratio_poly=mul(ratio_poly,[Q(1),1/(8*m)]);ratio*=1+eps/(8*m)
    expected=[Q(comb(8,i))/(8*m)**i for i in range(9)]
    need(ratio_poly==expected,'all nine product ratio coefficients')
    need(ratio==sum(x*eps**i for i,x in enumerate(expected)),'whole positive product ratio value')
    origin_loss=ratio-1+origin_cap*eps;polar_loss=Q(2,3)*eps
    need(origin_loss<Q(1,3100),'origin clipping contradiction paid')
    need(polar_loss<Q(1,2200),'noncircular polar clipping and energy entry paid')
    return dict(epsilon=str(eps),gradient_cap=str(origin_cap),marked_budgets=[str(x) for x in (l,h,m,bm,bp,c,aa)],
      path=dict(R=str(R),u_lower=str(u),E_upper=str(E),sigma=str(sigma)),
      J_vector=jvector,J_gradient=str(LJ),
      B_coefficients=[str(x) for x in B],O_seven_coefficients=[str(x) for x in vector],
      O_weighted_integral=str(weighted),O_gradient=str(LO),
      product_ratio_coefficients=[str(x) for x in expected],product_ratio=str(ratio),
      origin_loss=str(origin_loss),origin_slack=str(Q(1,3100)-origin_loss),
      polar_loss=str(polar_loss),polar_slack=str(Q(1,2200)-polar_loss))

def make():
    # These are rational payments, not sampled checks of the ordinary inequalities.
    c,cinfo=constants()
    even=[Q(7,8)**k+Q(1,8)**k for k in (2,3,4)]
    need(even==[Q(25,32),Q(43,64),Q(1201,2048)],'fresh even centered endpoints')
    need(Q(25,32)/4-Q(1,8)==Q(9,128) and Q(1,8)-Q(1,8)/4==Q(3,32),'REAL quartic norm payment')
    old=payment(Q(1,10000),Q(5,4));new=payment(Q(1,8800),Q(8,7))
    need(Q(1,8800)>Q(1,10000),'strictly larger proved gap')
    return dict(status='PASS',ordinary_unformalized=True,scope='NEW CLOSED adjacent interval [27/40,11/16], all complex original-rooted degree-nine polynomials; earlier union premises remain explicit',
      finite_scope='All rational budgets, entire removed-slot polynomials and integrals, nine product coefficients, strict losses; not a finite proof of communication, Gauss-Lucas, REAL Banach or continuum analytic inequalities.',
      centered=cinfo,even_endpoints=[str(x) for x in even],original_payment=old,strengthened_payment=new)
