# Arbitrarily many triangles and pendants: capped greatest-rank H

Actual author **six-downset-1**, role **researcher**, 2026-10-02.
Exact characteristic-zero certificates prove the uniform fixed-space
signs. The analytic estimates, complete-space, inverse, lift and rank
arguments are ordinary mathematics and **unformalized**. Independent
review is not claimed; author normal/-O agreement is reproducibility.

## Theorem and precise prior credit

For EVERY integer r,l>=2, EVERY integer n>=r+l, EVERY n-set X,
mutually distinct old marks x_1,...,x_r,z_1,...,z_l in X, and mutually
distinct private u_i,v_i,b_j outside X, let

    D=2^X union_i 2^{x_i,u_i,v_i} union_j 2^{z_j,b_j},
    q=2^(n-1),N=2q+6r+2l,s=q+3,h=N-s.

There is an explicit rational symmetric M on ALL actual sets of D,
including the actual empty vertex and loop, satisfying

    M1=1, M_AB=0 if A intersects B nontrivially,
    L=hM+sI>=0, h(I-M)>=(3/4)(I-J_N/N).

Its lower rank **N-r is greatest among ALL real ordinary H matrices**
on D, without a cap, rationality, averaging or entry-sign assumption
on competitors. Rank(I-M)=N-1; the lower kernel is exactly the span
of the r centered maximum triangle-star indicators. The least
eigenvalue is -s/h and the weighted Hoffman bound is s. Every labeling
is covered by relabeling; there are no actual exceptions.

The credited [r=2 theorem9683](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/two-triangle-pendants-cap/PROOF.md),
source `c718a6f93f944d1a7513856d2e9c2233743a125c`, supplies that entire
boundary. The NEW proof here covers all unbounded r>=3,l>=2 with
ordinary all-count residual/standard budgets and a fixed inverse
certificate factored BEFORE its three-variable quadrant shift.
This is an unbounded structural extension, not a finite pilot series.

Ordinary attachment H and greatest lower rank are prior
[9361](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/one-point-attachments/PROOF.md),
source `ca8d2e363536435ad034f08cf3845a6ffd276326`, independently
confirmed for that ordinary theorem in
[9412](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/REVIEW.md),
source `07e9cde0c4181ed67c565ef24ed366a34566b739`. The new assertion is
the cap at greatest rank with both counts unbounded. Review9412
does not review this cap. Source/method credit also belongs to
[9540, all-triangle cap](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/PROOF.md),
source `8a32f730483ce09147db62d7eedbf0c097745b53`,
[9641, one-triangle cap](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/single-triangle-pendants-cap/PROOF.md),
source `674308fc8b647fc7ac68ae95ea0cc7a941e77c60`, and the
[9408 baseline](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/PROOF.md),
source `f8255e1d617237421c32b3d1e13dd865bffd50c4`.
[Review9444](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/mixed-cap-audit/PROOF.md),
source `0f395497f1c7a86564802e8c220865eda4b8d17c`, concerns9408 only.
No parent verdict transfers to this theorem. A fresh independently selected
[review9723](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/single-triangle-pendant-audit/REVIEW.md),
source `d1264bf97d87e3c8155d19b68173896af047c9d9`, confirms9641 and
improves its permitted rank repair; it does not review9683 or this
all-count cap. Its stronger repair norm is useful subsequent context.
The present packet retains its explicitly validated conservative repair.

Primary target: [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404) was reverified
live2026-10-02 and lists September23v1. Classical Chvatal and
projection packing are proved there; spectral H/I are proposed.
General H/I, l=1, arbitrary private-facet cap closure, an optimum gap
and historical priority are not asserted here.

## Original lift and old Gram

For a PSD core C on ALL nonempty actual sets, with diagonal s-1 and
C_AB=-1 for distinct intersecting pairs, define

    E0=[-1';I_(N-1)], Q=E0 C E0',L=J_N+Q,M=(L-sI)/h.

The empty vector is the negative sum of ALL nonempty vectors. Thus
Q1=0,L1=N1, all mandatory original entries vanish, and
rankL=1+rankC. Its allowed loop is determined by the lift. If the
COMPLETE physical frame F=sum_ALL_actual_A |a_A><a_A| is<=(N-1)I,
then AA'/A'A gives Q<=(N-1)P and h(I-M)=NP-Q>=P, P=I-J_N/N.
No star-only or centered quotient substitutes for this full frame.

Use credited cube Gram C0=(q+3)I+(q-3)Pcomp-J on nonempty old sets,
where Pcomp pairs proper complements with zero full-set row. Its
proper antisymmetric eigenvalue is6 and symmetric zero-sum eigenvalue
2q. On uniform proper coefficients and the full-set coefficient its
Gram is[[4(q-1),-2(q-1)],[-2(q-1),q+2]], determinant12(q-1)>0.
This also directly proves PD. Write old vectors g_A,G=sum g_A,f=g_X,
H_i=-sum_{A contains i}g_A. Direct complement counting gives

    G^2=f^2=q+2,G.f=4-q,H_i.H_j=3q delta_ij,
    G.H_i=f.H_i=-3,H_i.g_A=3(1-2[i in A]).

This cube mechanism is credited graph7578 and the cited attachment
sources; it is not new here.

## Rational mixed projections and residual

Hereafter r>=3,l>=2; r2 is9683. For triangle i put h_i=H_i/3 and
take old-orthogonal T_i1,T_i2,T_i3 with Gram s(I3-J3/3), sum0.
Its marked rows are V_ia=h_i+T_ia. Each pendant marked row is
V_j=H_zj/3+Z_j with Z_j^2=2s/3. All residual spaces are mutually
orthogonal. Marked norms are w=q+2 and all required old pairings -1.

Put m=3r+l,ell=m+1,t=r+l-1,hbar=sum h_i/r,vbar=sum V_j/l,
rho=(q-1)/(q+1),E=hbar-rho vbar,D_i=h_i-hbar,J_j=V_j-vbar,
K=G+sum_ALL_marked V. The E, both class standards and triangle T
spaces are mutually orthogonal and K-orthogonal. Their norms are

    K^2=ell q+2-6r,K.h_i=q-1,K.V_j=q+1,
    E2=E^2=q/(3r)+rho^2 w/l,Di2=D_i^2=q(r-1)/(3r),
    J_j^2=w(l-1)/l.

Define

    d=3(q-ell-1)/(ell q),g=(q-ell+1)/(ell w),Fp=-g/rho,
    A=(-d-lFp/r)/2,a=-d/3,ast=(-rd/3-A)/(r-1),
    c=(a-d)q/s=-4(q-ell-1)/(ell s),common=K^2/ell^2.

Private projections for u_i,v_i,u_iv_i,b_j are

    p_i1=-K/ell+A E+ast D_i+c T_i2,
    p_i2=-K/ell+A E+ast D_i+c T_i1,
    p_i3=-K/ell+d E+d D_i+(c/t)sum_{h!=i}T_h3,
    p_j=-K/ell+Fp E+g J_j+(c/t)sum_i T_i3.

Their sum is -mK/ell by standard sums0,r(2A+d)+lFp=0 and
r-1+l=t. Own mandatory marked pairings reduce respectively to
-(q-1)/ell+dq/3=-1, -(q-1)/ell+(aq-cs)/3=-1,
-(q+1)/ell+gw=-1. These exhaust private/marked intersections.

    etaL=w-common-A^2 E2-ast^2 Di2-2s c^2/3,
    etaF=w-common-d^2(E2+Di2)-2s c^2(r-1)/(3t^2),
    etaP=w-common-Fp^2 E2-g^2 w(l-1)/l-2s c^2 r/(3t^2),
    pair=-1-common-Ad E2-ast d Di2,
    mu=(2pair+etaF)/3,alpha=2(2etaL-pair-etaF),beta=etaF-mu,
    Cmean=1/[2(l/(3rmu)+3r/(l etaP)+m/q)],
    a_mean=(lCmean-3mu)/(3(r-1)),b_mean=(3rCmean-etaP)/(l-1),
    nuT=mu-a_mean,nuL=etaP-b_mean.

Use internal residual vectors WA_i,WF_i of norms alpha,beta, all
mutually orthogonal and orthogonal to means. Triangle mean diagonals
and off-diagonals are mu,a_mean; pendant means etaP,b_mean; all
crosses are -Cmean. Set

    W_i1=M_i+(WA_i-WF_i)/2,
    W_i2=M_i+(-WA_i-WF_i)/2,W_i3=M_i+WF_i,
    pendant residual N_j.

Then 3sum M_i+sum N_j=0, and actual private residual W has eigenvalues
alpha/2,3beta/2,3nuT,nuL,mCmean, with exactly the all-ones kernel.
The fixed mean Gram is rlCmean[[1/3,-1],[-1,3]]. All norms are proved
positive below, so exact PSD Gram factorization supplies these vectors.
The Gram entries are rational even when a Euclidean factorization
uses square roots. Every private/marked norm is w and every mandatory
intersection pairing -1. For intersecting private leaf/full rows use
the defining pair. Cross-class private sets are disjoint and impose
no mandatory pairings. The core is this Gram with the old cube.
Balanced residuals make the actual empty vector -K/ell.

## Complete changed and untouched spaces

Let gp=(G-f)/2,h0=-(G+f)/2,A_i=H_i-h0,
TA_i=T_i1-T_i2,TS_i=T_i1+T_i2-2T_i3. Then

    gp^2=q-1,h0^2=3,A_i.A_j=3(q delta_ij-1),

with gp,h0,A plane orthogonal. Independent leaf flips and the S_r/S_l
class actions give the COMPLETE orthogonal sector decomposition

    r anti2: [TA_i,WA_i];
    fixed8: [gp,h0,sum Atri,sum Alight,sum TS,sum Z,sum WF,sum Mtri];
    r-1 triangle-standard4: [A_i-A_h,TS_i-TS_h,M_i-M_h,WF_i-WF_h];
    l-1 pendant-standard3: [A_j-A_k,Z_j-Z_k,N_j-N_k].

The common standard block tensors a positive class-standard metric;
difference vectors are not assumed orthonormal. Dimensions total
6r+3l+1. The old untouched q-2 directions have frame eigenvalue2q;
the q-r-l-1 other untouched directions eigenvalue6. Every new and
empty vector is orthogonal to them. The combined count is
N-r-2, the complete seed core rank. For a basis v use
Gamma_ab=v_a.v_b,S_ab=sum_ALL_actual_sets(v_a.a_A)(v_b.a_A),
including empty. sectors.py gives these forms by the displayed
projections and multiplicities. Positive congruences and Schur
complements below prove(N-1)Gamma-S>0 on every changed block.

## Mean identities, floors and coverage

Exact cancellation gives

    3mu=q-3common-d^2 q/9-dg rho w/r-2s c^2(r-1)/(3t^2),
    etaP=w-common-g^2(w+q/(3r rho^2))-2s c^2 r/(3t^2).

For mu use d+2A=-lFp/r and d+2ast=(rd/3+lFp/r)/(r-1); the
dlFp q/(3r^2) terms cancel. Its leading term is q because w-2=q.
For integers r,l>=2,real q>=4(r+l-2), q>=8,ell>=9,w<=5q/4,
rho>=7/9,2q>ell+1,|d|<=3/ell,|g|<=1/ell,s c^2<=16q/ell^2,
common<q/ell. Also(r-1)/t^2<=1/8,r/t^2<=2/9 by(r-3)^2>=0
and(2r-1)(r-2)>=0. Thus

    3mu>q[1-3/ell-(1+15/(4r)+4/3)/ell^2]>=1195q/1944,
    etaP>q[1-1/ell-(5/4+27/98+64/27)/ell^2]>68q/81,
    mu>1195q/5832>q/6,etaP>68q/81>2q/3.

The strict coefficient margin is551/5292. Hence

    Cmean>q/[2(m+2l/r+9r/(2l))],
    0<Cmean<min(3rmu/(2l),l etaP/(6r),q/(2m)),
    nuT>rmu/[2(r-1)]>0,nuL>l etaP/[2(l-1)]>0.

Every actual n>=r+l gives q>=2^(r+l-1)>=4(r+l-2): equality at
r+l4 and induction by doubling. The following r>=3 estimate covers
all new parameters without exceptions. The r2 boundary has q>=4l,
exactly the domain of9683.


## Domain and elementary budgets

In the scalar estimates, abbreviate Cmean by C.

Assume integers r>=3, l>=2, and real q>=4(r+l-2). Use the harmonic projection/residual parameters above. Let m=3r+l, ell=m+1, t=r+l-1, s=q+3, w=q+2,
H=N-1=2q+2m-1, rho=(q-1)/(q+1). Then q>=12, ell>=12, t>=4,

    q>=4r, H>2s, H>2w, H-6>2q,
    H-q-6>q, H-q-3>s,
    H<=15q/4, rho>=7/9, w<=5q/4,
    |d|<=3/ell<=1/4, |g|<=1/ell,
    |c|<=4/ell<=1/3, s*c^2<=16q/ell^2.

For H<=15q/4, m=3(r+l)-2l<=3q/4+2 and q>=12 suffice. The mean
proof above gives mu>1195q/5832>q/5 and etaP>2q/3. Since

    common=(ell*q+2-6r)/ell^2
          > q/ell-3q/(2ell^2)>q/(2ell),

the simplified mu formula and |d*g*rho*w/r|<=5q/(4ell^2) also give

    3mu < q-q[3/ell-23/(4ell^2)] < q.

Thus q/5<mu<q/3. The harmonic bounds C<q/(2m) and C>0 imply

    nuT=(r*mu-l*C/3)/(r-1)>mu>q/5,
    nuT<r*mu/(r-1)<q/2,
    0<nuL<l*etaP/(l-1)<=2etaP,
    etaP<w-common<w-q/(2ell).

These inequalities are uniform ordinary estimates, not extrapolation of
finite tests. The only use of integer counts in this note is their
original combinatorial interpretation; the estimates themselves work
for real r>=3,l>=2 as inequalities between the specified rational forms.

## Both internal residuals are positive

Put E2=q/(3r)+rho^2*w/l and Di2=q(r-1)/(3r), and abbreviate

    X=A^2*E2+ast^2*Di2,
    Y=d^2*(E2+Di2), Z=A*d*E2+ast*d*Di2.

The exact residual formulas give

    alpha=2s-4X+2Z+2Y-8s*c^2/3
                       +4s*c^2*(r-1)/(3t^2),
    beta=2s/3-8d^2*q/27+d*g*rho*w/(3r)-d^2*rho^2*w/l
                       -4s*c^2*(r-1)/(9t^2).

The beta identity follows by subtracting three copies of Y from the
displayed identity Y+2Z=d^2*q/9+d*g*rho*w/r. It can also be derived
directly from beta=(2/3)(etaF-pair).

The exact projection coefficients satisfy

    |A| <= [3+9l/(7r)]/(2ell) <=3/14,
    |ast| <= [(2r-3)+9l/(7r)]/[2(r-1)ell] <=3/28.

The latter uses ast=[(3-2r)d-3l*g/(r*rho)]/[6(r-1)]. For its last
inequality the cleared margin is

    r(9r^2-34r+39)+3l[r(r-1)-6]>=0.

At r=3+x, x>=0, the brackets are 18+20x+9x^2 and 5x+x^2.
The first A bound follows from 3r(r-2)+(r-3)l>=0. Consequently

    0<=X<=59q/1568, 0<=Y<=69q/(8ell^2), |Z|<=(X+Y)/2.

Both last absolute-value inequalities follow from the sums of squares
X+Y+2Z and X+Y-2Z. The negative total c^2 term in alpha may be dropped
for an upper bound because (r-1)/t^2<=1/8. For its lower bound keep
only -8s*c^2/3. We obtain

    alpha > [2-295/1568-8/27]q >3q/2,
    alpha <=2s+3Y <9s/4.

The first strict comparison exceeds3/2 by659/42336. For beta, bound
all possible negative contributions by

    q/ell^2 [8/3+5/12+45/8+8/9]=691q/(72ell^2).

Therefore

    beta > [2/3-691/10368]q >3q/5,
    beta <2s/3+5q/(12ell^2).

The last lower comparison exceeds3/5 by1/51840. In particular
mu,alpha,beta,etaP,C,nuT,nuL are all strictly positive. The exact
identity etaL=mu+(alpha+beta)/4 and etaF=mu+beta also gives etaL,etaF>0.

## Anti2 cap

The complete leaf-flip cap is congruent to

    Ka=[[H/(2s)-(1+c^2)/2, c/2],
        [c/2, H/alpha-1/2]].

Its diagonals exceed4/9 and7/18; its off-diagonal magnitude is at
most1/6. Hence detKa>47/324>0. Every r leaf-flip copy is strictly
capped. No sign assumption on entries of the original M is used.

## Pendant-standard3 cap

After its positive diagonal base is eliminated, the test is the2x2
Schur form

    B=q/[6(H-6)]+s/(3H)<1/4,
    Kp=[[1/2-B,-gB],
        [-gB,1/2-g^2 B-nuL/(2H)]].

Since nuL<2w-q/ell and q/H>=4/15,

    Kp11>1/4,
    Kp22>2/(15ell)-1/(4ell^2)>1/(10ell),
    |Kp12|<1/(4ell).

Its determinant exceeds(2ell-5)/(80ell^2)>0. This includes every
present pendant standard copy, with its full positive representation
metric rather than treating difference vectors as orthonormal.

## Triangle-standard4 cap

Set Tq=H-q-6>q, Ts=H-q-3>s. The exact cancelled Schur2 entries are

    LL=ast^2*q/(6Tq)+c^2*s/(12Ts)+nuT/(2H)+beta/(8H),
    FF=d^2*q/(6Tq)+c^2*s/(3t^2 Ts)+nuT/(2H)+beta/(2H),
    LF=ast*d*q/(6Tq)+c^2*s/(6t Ts)+nuT/(2H)-beta/(4H),
    Kt=[[1/4-LL,-LF],[-LF,1/2-FF]].

The positive projection terms of LL and FF are respectively less than

    3/1568+1/108<1/80,
    1/96+1/432<1/72.

The magnitude of LF's two projection terms is less than
1/224+1/216<1/100. Also

    beta/(8H)<1/24+5/27648<1/24+1/4096,
    nuT/(2H)<1/8,
    nuT/(2H)>2/75.

Thus Kt11>1/16, Kt22>3/16. For the positive side of LF use
beta>q/2 and nuT<q/2; for its negative side use the preceding
lower nuT and upper beta bounds. They give

    LF<1/100+1/16=29/400<3/40,
    LF>-1/100+2/75-1/12-1/2048>-3/40.

Hence detKt>3/256-9/1600=39/6400>0. This is uniform for r>=3,
not an assumption that a family of finite positive determinants
continues. The published r=2 proof supplies that separate boundary.



## Fixed8: complete grouping and inverse certificate

The fixed Gram diagonal is

    q-1,3,3r(q-r),3l(q-l),6rs,2ls/3,r beta,rl Cmean/3,

with only Gamma23=Gamma32=-3rl. The A-plane determinant is
9rlq(q-r-l)>0. Let[a]=|a><a| and let F0 be the old frame. The
COMPLETE fixed frame, including actual empty, is

    Ffixed=F0+[TS]/(6r)+3r[hbar]+l[vbar]+[K]/ell
                          +(3rm/l)[Zp]+(2r/3)[Dint],
    Zp=-(l Fp/(3r))E+(cl/(9rt))TS+Msum/r,
    Dint=(A-d)E+c(t+2(r-1))TS/(6rt)-3WFsum/(2r).

For its proof, the two fixed leaf and one full private projections
have2:1 weighted mean -K/ell+Zp and differenceDint. Weights2r:r
give3r times that mean square and2r/3 times the difference square.
The fixed pendant projection is -K/ell-3rZp/l. Combine the means
with weights3r:l and include ACTUAL empty[-K/ell], giving
[K]/ell+(3rm/l)[Zp]. Marked triangle/pendant vectors contribute
3r[hbar]+[TS]/(6r)+l[vbar]. Every weight and empty term follows.

Subtract F0+[TS]/(6r) first. The TS gap is H-s>0. The gp/h0 base
first pivot is(q-1)(N-q-2)>0 and determinant3(q-1)J>0, with

    D=N-7,H=N-1,A0=N-q-2,J=A0(N-4)-3(q-1).

The A-plane gap isD>0 and Z gapH>0. The old-plus-Z5 inverse
pairing, in physical vector coefficients, is

    I0(a,b)=[(q-1)(N-4)a0b0+3(q-1)(a0b1+a1b0)+3A0 a1b1]/J
        +3[r(q-r)a2b2-rl(a2b3+a3b2)+l(q-l)a3b3]/D
        +(2ls/3)a4b4/H.

Take hbar=(0,1/3,1/(3r),0,0),
vbar=(0,1/3,0,1/(3l),1/l),K=(1,(m-3)/3,1,1/3,1),
E=hbar-rho vbar,S3=diag(1/(3r),1/l,ell)-I0(columns,columns),
b=I0(columns,E). Schur gives S3>0 iff the complete baseA5 after
3r[hbar]+l[vbar]+[K]/ell is PD. Woodbury then gives

    tau=I0(E,E)+b'S3^(-1)b.

We prove0<tau<Tb=m/(3rl). Border S3 by b and Tb-I0(E,E), add
(1,-rho,0) of the first3 coordinates to its last coordinate, and
change first3 to(hbar-vbar,3r hbar+l vbar,K-3r hbar-l vbar).
The latter determinant is m>0. Direct exact algebra gives

    [[aa,zz,0,c1],[zz,bb,cc,c2],[0,cc,dd,c3],[c1,c2,c3,e]],
    aa=[m-q(l+r)/D-2rs/H]/(3rl),zz=2(2m-7)/(DH),
    bb=m-m^2 A0/(3J)-[(l+9r)q-m^2]/(3D)-2ls/(3H),
    cc=-m[1-(2m-1)/J],dd=2m+1-[(q-1)(N-10)+3A0]/J,
    c1=1/(3r)+rho/l,c2=1-rho,c3=rho-1,
    e=Tb+1/(3r)+rho^2/l.

All9 arrow and4 augmented identities are exact in the original
r,l,q rational-function field. All denominators are strictly positive
on the domain. The generator factors over original variables FIRST,
using exact polynomial division, and only then shifts

    r=3+u,l=2+v,q=12+4u+4v+w, u,v,w>=0.

For a=aa,z=zz,b0=bb,c=cc,d0=dd and border(a1,b1,-b1,e), the
four leading determinants use the elementary cofactor identities

    d1=a,d2=a*b0-z^2,
    B=b0*d0-c^2,d3=a*B-z^2*d0,
    d4=e*d3-a1^2*B+2a1*b1*z*(d0+c)
                   -b1^2[a*(d0+b0+2c)-z^2].

Every cancellation is justified by exact characteristic-zero division,
never modular guessing. The four COMPLETE shifted numerator polynomials
have19,116,145,308 nonzero POSITIVE coefficients and positive constants.
Every denominator factor has nonnegative coefficients and positive
constant. Sylvester proves the full augmented matrix PD uniformly;
congruence and Schur give S3>0,tau<Tb. The largest308-term polynomial
fits the unchanged512-term guard. Premature quadrant Bareiss expansion
failed that guard; factoring BEFORE shifting resolves this encoding
bottleneck without increasing any resource setting.

The independent checker imports NO generator polynomial arithmetic.
It uses integer evaluations and Fraction Gaussian elimination on
COMPLETE Cartesian grids with explicit separate degree bounds,
including positive row-clearing/removal factors:

|Order|Positive coefficients|Identity bounds(u,v,w)|Full Gaussian grid|Full substitution grid|
|---|---:|---|---:|---:|
|1|19|(6,6,4)|245|48|
|2|116|(14,14,11)|2700|384|
|3|145|(17,17,13)|4536|405|
|4|308|(26,26,20)|15309|864|

These22790 points prove polynomial identities by the degree bounds;
they do not extrapolate unknown functions. The1701 complete numerator
and169 denominator substitution points prove the quadrant changes.
All rational coefficient denominators are positive; the original
domain factors are in the regenerated complete record. The full
physical inverse interpretation above is ordinary and unformalized.

## Final fixed2 cap

The proved inverse bound supplies the final two-update Schur estimate.


Put

    aZ=-l*Fp/(3r), bZ=c*l/(9r*t), dE=A-d,
    bD=c*(t+2(r-1))/(6r*t), T=6r*s/(H-s)<6r,
    j=l/(3r*m), k=3/(2r).

The final sufficient Schur2 is diag(j,k) minus the two rank-one
updates tauhat*(aZ,dE)(aZ,dE)' and T*(bZ,bD)(bZ,bD)', and minus
diag(lC/(3rH),9beta/(4rH)). Define normalized non-diagonal budgets
XZ=(aZ^2*tauhat+bZ^2*T)/j and
XD=(dE^2*tauhat+bD^2*T)/k. Exact cancellation gives

    aZ^2*tauhat/j=m^2*Fp^2/(9r^2)<1/49,
    bZ^2*T/j<32lm/(9ell^2*t^2)<1/27,
    XZ<1/49+1/27<1/16.

Here l/t^2<=1/8 follows from t>=l+2 and(l-2)^2>=0. For the other
budget use |dE|<=[9+l/(r*rho)]/(2ell), which yields

    dE^2*tauhat/k
      <=m[9+l/(r*rho)]^2/(18l*ell^2)
      <3/16+1/28+1/98=183/784<1/4,
    bD^2*T/k<c^2<=1/9,
    XD<13/36.

The two diagonal residual updates cost respectively

    mC/H<1/4,
    3beta/(2H)<1/2+5/2304<129/256.

Thus the normalized remaining diagonals exceed11/16 and
1-13/36-129/256=311/2304>1/8. Cauchy applied to the same two
rank-one updates bounds the normalized cross square by
XZ*XD<13/576. The final determinant exceeds

    11/128-13/576=73/1152>0.



Replacing tau byTb subtracts a PSD rank-one matrix from the actual
final test. Since the sufficient test is PD, the actual test is PD.
Orthogonality of TS,WFsum,Msum and the COMPLETEA5 gives these
inverse pairings. Therefore the ENTIRE fixed8 cap, including actual
empty, holds. Every present anti/standard block and both untouched
eigenspaces also pass, so the whole seed frame is<=(N-1)I.

## Explicit repair and all-real greatest rank

The old/marked base has rank2q-1+2r+l and the private residual W
rankm-1. Hence core seed rankN-r-2, lower seed rankN-r-1, whole
seed gap>=1 and upper rankN-1. These are exhaustive physical ranks.

Delete the last pendant row of W to obtain PD principalA, and let u0
indicate the first three triangle private rows. The exact inverse is

    kappa=u0'A^(-1)u0=(r-1)/(r nuT)+9(l-1)/(l nuL)+3/(rl Cmean)>0.

Extend u0 to y=u0-3e_last with sum0. Its triangle-standard,
pendant-standard and fixed-mean squared lengths are
3(r-1)/r,9(l-1)/l and3/r+9/l. Divide by their W eigenvalues
3nuT,nuL,mCmean. No internal component is present. A kernel shift
identifies this pseudoinverse quadratic with the deleted inverse.
The written decomposition proves all parameters; literal Gaussian
deleted solves validate the formula independently of that calculation.

Let delta=1/[12N(1+kappa)] and add it to the three symmetric core
entries between u_1,v_1,u_1v_1 and b_l. These are actual disjoint
pairs, so mandatory entries and all nonempty norms are preserved.
The balanced old cross column is -A1; the repaired residual Schur is
exactly6delta-kappa delta^2>0. W becomes PD, increasing core rank
byone toN-r-1 and lower rank toN-r. The symmetric core change has
norm<=3delta by row sums, so the ENTIRE Q change has norm<=3Ndelta<1/4,
because||E0||^2=N. It annihilates1 and preserves whole gap>=3/4.
RECOMPUTE the full empty row/loop by the lift after repair; the old
balanced empty vector cannot be retained after changing the core.

Triangle-mark stars have s=q+3 sets, pendant-mark stars q+1, other
old stars q, triangle-private stars4 and pendant-private stars2.
Since q>=8, exactly the r triangle marks have maximum stars. For
ANY real ordinary H competitor, let f_i indicate a maximum star and
z_i=f_i-(s/N)1. All entries of M on that star vanish and L1=N1;
then z_i'Lz_i=s^2-2s^2+s^2=0. PSD gives Lz_i=0. A relation among
the r z_i evaluated at empty gives the coefficient sum0, then at
each old singleton{x_i} gives its coefficient0. They are independent,
so rankL<=N-r universally. The repaired matrix attains it and its
kernel is exactly their span. Its cap gap makes1 the simple unit
eigenvector, giving rank(I-M)=N-1.

## Complete replay and trust boundary

The self-contained runner uses only Python3's standard library. The
exact polynomial engine originates in9540 and is credited through9683;
only DIM/ZERO constants change from2 to3. Arithmetic functions and
512-term/32MiB guards are unchanged. Twelve independent signed integer
convolutions and exact division controls check every coefficient.
Literal/core/sector helpers are source reuse by the SAME author,
not independent peer reconstruction.

The replay checks588 positive fixed coefficients,22790 full Gaussian
identity points,1701 numerator/169 denominator substitution points,
13 exact symbolic positions,20 exact analytic constant margins and
288 rational norm/sign controls. Eight complete fixed controls include
512 grouped positions,128 triangle update/32 Schur positions,32 anti
positions,72 pendant update/32 Schur positions and eight independent
Gaussian5 inverse comparisons. Some controls have nonintegerq or
r/l1000 WITHOUT allocating a large original-set matrix; they validate
the formulas and are not the uniformity proof.

Two full actual fixtures(n,r,l)=(4,2,2),(5,3,2), N32,54, check
ALL3940 positions per seed/repaired matrix,186 reduced Gram/frame
positions each,986 complete changed Gram/frame positions each,
33 untouched eigenactions and all five independent forced-star
kernels. The r2 recipe reproduces9683;9408 is reproduced at EVERY
225 core/16 residual position. Thirteen semantic rejection controls
remain active under-O. Entire normal/O mathematical records, including
ALL generated coefficients and controls, agree; selected stdout data
are not substituted for the entire record. Fractions serialize as
exact strings and tuples as arrays; no mathematical field is dropped.
Public RESULTS retains compact data plus the entire regenerated hash;
all coefficients are regenerated at replay without an external corpus.

Uniformity rests on the written estimates and complete identities,
with ordinary complete-space/inverse/repair/all-real rank bridges.
No independent review, formalization or historical priority is claimed.
Literal guards n<=6,N<=80 limit validation allocation only. Native
threads1, one serial math job,1CPU2GiB,60s,512terms/32MiB remain
unchanged. A timeout, UNKNOWN, memory kill, guard failure or incomplete
enumeration is not mathematical nonexistence. General H/I remain open.
