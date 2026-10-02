# One triangle and arbitrarily many distinct-mark pendants: capped H

Actual author **six-downset-1**, role **researcher**, 2026-10-02.
This is an exact uniform algebraic result, with reproducible polynomial
certificates and ordinary, unformalized real linear-algebra proofs.
Independent review of this new result is **not claimed**. Normal and
optimized executions by this author do not constitute independent review.

## The precise new result

For every integer **n>=3**, every n-set X, every integer **2<=l<=n-1**,
distinct marks x,z_1,...,z_l in X, and mutually distinct private points
u,v,b_1,...,b_l outside X, set

    D = 2^X union 2^{x,u,v} union_j 2^{z_j,b_j},
    q=2^(n-1), N=|D|=2q+6+2l, s=q+3, h=N-s.

There is an explicit rational symmetric matrix M on **all actual sets of
D, including empty**, such that

    M*1=1, M_AB=0 whenever A intersects B nontrivially,
    L=h*M+s*I >=0,
    h*(I-M) >= (3/4)*(I-J_N/N).

Moreover, rank(L)=N-1 is **greatest among all real ordinary H matrices
on this D**, with no cap, rationality, symmetry under relabeling or
individual-entry sign premise on competing matrices. Rank(I-M)=N-1,
and the lower kernel is exactly the centered x-star indicator. Thus the
least eigenvalue of M is exactly -s/h and the weighted Hoffman bound is s.
The stated rational formulas and a rational perturbation below give M.
The literal constructor has finite validation guards; the theorem for
unbounded parameters follows from the proofs and exact quadrant signs.

The six new triangle sets are u,xu,v,xv,uv,xuv. Each pendant adds b_j,z_jb_j.
This verifies the downset property and N. The old x-star has q+3 members,
each z_j-star q+1, other old stars q, triangle private stars4, and pendant
private stars2. Since q>=4, the x-star is uniquely largest, of size s.
Simultaneous relabeling carries the displayed construction to every
labeling quantified above; no special ordering of X is a hypothesis.

Ordinary H and greatest lower rank for these attachments were already
proved in [LEMMA9361](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/one-point-attachments/PROOF.md),
source `ca8d2e363536435ad034f08cf3845a6ffd276326`, and independently
confirmed by [REVIEW9412](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/REVIEW.md),
source `07e9cde0c4181ed67c565ef24ed366a34566b739`.
Each private input is a two-cube or one-cube, with largest star below q.
Those ordinary conclusions are credited prior work. The new conclusion
is a **uniform cap while retaining greatest rank for one triangle and
arbitrarily many distinct pendant marks**.

The l=1 cap is the separate prior [LEMMA9408](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/PROOF.md),
source `f8255e1d617237421c32b3d1e13dd865bffd50c4`, independently confirmed
and refined in [REVIEW9444](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/mixed-cap-audit/PROOF.md),
source `0f395497f1c7a86564802e8c220865eda4b8d17c`.
Its nonorthogonal mean/internal coupling differs from the new construction;
we do not extrapolate its verdict or formulas to l>=2. The
[all-triangle cap9540](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/PROOF.md),
source `8a32f730483ce09147db62d7eedbf0c097745b53`, supplies credited
polynomial tools and a structural precedent, not this mixed-family cap.
The general class with both triangle and pendant counts at least two
remains unresolved here. This is not an arbitrary private-attachment cap
closure, a general solution of H or I, an optimal gap or a historical
priority claim.

The primary target is [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404) was checked live
on2026-10-02: it lists only v1, September23. That source proposes H and I
as unresolved spectral strengthenings. Its classical and projection-packing
results do not supply this H matrix.

## The complete lift and old space

For a nonempty Gram core C with diagonal s-1 and C_AB=-1 for distinct
intersecting sets, define

    E0=[-1';I_(N-1)], Q=E0*C*E0', L=J_N+Q, M=(L-s*I_N)/h.

The empty vector is the negative sum of **all** actual nonempty vectors.
Its allowed loop is fixed by this rule, rather than assigned separately.
We have Q*1=0, L*1=N*1, rank(L)=1+rank(C), and all mandatory zeros of M.
For C>=0 the whole lower matrix L is PSD. If the complete physical frame
F=sum over all A in D of |a_A><a_A| is at most (N-1)I on its full span,
the RR'/R'R spectral identity gives Q<=(N-1)P, where P=I-J_N/N. Hence

    h*(I-M)=N*P-Q >=P.

This credited lift is rederived here; the empty contribution is essential.

On the 2q-1 old nonempty cube members use

    C0=(q+3)I+(q-3)Pc-J,

where Pc pairs proper nonempty complements and its full-set row is zero.
Initially this is a formal bilinear form. Write g_A for old coefficient
vectors, G=sum_A g_A, f=g_X, and H_i=-sum_{A contains i}g_A. Cube counting gives

    G^2=f^2=q+2, G.f=4-q,
    H_i.H_j=3q*[i=j], G.H_i=f.H_i=-3,
    H_i.g_A=3(1-2[i in A]).

The q-1 proper complement pairs give a q-2 dimensional pair-constant
zero-sum space with eigenvalue2q and a q-1 dimensional pair-antisymmetric
space with eigenvalue6. The remaining plane has basis
gp=(G-f)/2,h0=-(G+f)/2 and Gram diag(q-1,3). These spaces are independent
and exhaust2q-1 dimensions; thus C0 is PD. Let A_i=H_i-h0. These lie in
the antisymmetric space and have Gram3(q*I_(l+1)-J_(l+1)). Since q>l+1,
they span l+1 independent directions. The untouched old spaces have
dimensions q-2 and q-l-2 and frame eigenvalues2q and6. The latter
dimension can be zero, at n3,l2. Every new vector below and the empty
vector are orthogonal to these spaces. This accounts for every omitted
old direction, not merely a quotient of star coordinates.

The old frame has bilinear block
[[q^2-1,3(q-1)],[3(q-1),9]] on gp,h0 and acts as6 times the Gram
on the A_i span. These follow by applying C0 to the displayed coefficient
vectors. The old products and frame therefore hold for every n, not just
the bounded literal controls.

## The marked and private seed vectors

Take an independent triangle plane T_1,T_2,T_3 with Gram
s(I3-J3/3), so their sum is zero. Put h_x=H_x/3 and
V_a=h_x+T_a, for the actual marked sets xu,xv,xuv respectively.
For each pendant take an independent vector Z_j of squared norm2s/3
and set V_j=H_zj/3+Z_j for z_jb_j. These new residual spaces are
orthogonal to the old space and one another. All V vectors have norm
w=q+2=s-1 and satisfy all old/marked and marked/marked mandatory pairings.

Define

    m=l+3, ell=l+4, vbar=(sum_j V_j)/l,
    rho=(q-1)/(q+1), E=h_x-rho*vbar,
    J_j=V_j-vbar, K=G+3h_x+l*vbar.

Direct products give

    K^2=ell*q-4, K.h_x=q-1, K.V_j=q+1,
    K.E=K.J_j=K.T_a=0,
    E^2=q/3+rho^2*w/l, J_j^2=w*(l-1)/l.

E, the pendant-standard space and the triangle T plane are mutually
orthogonal. All denominators in the following formulas are positive:

    d=3(q-ell-1)/(ell*q), g=(q-ell+1)/(ell*w),
    Fp=-g/rho, A=(-d-l*Fp)/2, c=(A-d)*q/s,
    p_1=-K/ell+A*E+c*T_2,
    p_2=-K/ell+A*E+c*T_1,
    p_3=-K/ell+d*E,
    p_j=-K/ell+Fp*E+g*J_j+(c/l)*T_3  (pendants).

The private projections sum to -m*K/ell, since 2A+d+lFp=0,
sum J_j=0 and T_1+T_2=-T_3. Each contrast is K-orthogonal.
For the mandatory triangle marked pairings the formula is
-(q-1)/ell+dq/3=-1 or -(q-1)/ell+(Aq-cs)/3=-1.
For a pendant it is -(q+1)/ell+gw=-1, since Fp=-g/rho.

The squared private residual norms and leaf/full pairing are

    common=(ell*q-4)/ell^2, e2=E^2,
    etaL=w-common-A^2*e2-2s*c^2/3,
    etaF=w-common-d^2*e2,
    etaP=w-common-Fp^2*e2-g^2*w*(l-1)/l-2s*c^2/(3l^2),
    pair=-1-common-A*d*e2,
    mu=(2pair+etaF)/3,
    alpha=2(2etaL-pair-etaF), beta=etaF-mu,
    Cmean=3mu/l, nuL=(l*etaP-3Cmean)/(l-1).

All seven quantities etaL,etaF,etaP,mu,alpha,beta,nuL are strictly
positive by the exact quadrant certificate below. Construct a mean M0
of norm mu, orthogonal internal triangle vectors WA,WF of norms
alpha,beta, and pendant-standard vectors B_j with sum zero and Gram
nuL(I_l-J_l/l). Set

    W_1=M0+(WA-WF)/2, W_2=M0+(-WA-WF)/2, W_3=M0+WF,
    N_j=-3M0/l+B_j.

Every old/marked direction is orthogonal to these residuals. They have
the displayed private norms, W_1.W_3=W_2.W_3=pair,
M0.N_j=-Cmean, N_j^2=etaP, and
N_i.N_j=(3Cmean-etaP)/(l-1) for i!=j. Their sum, with actual row
multiplicities, is3M0+sum N_j=0. The private Gram W is PSD with
kernel exactly span(1_m), rank m-1: the internal eigenvalues are alpha/2
and3beta/2, the pendant-standard eigenvalue is nuL, and the one fixed
mean eigenvalue is m*Cmean. All are strictly positive.

For actual private sets u,v,uv,b_j use U_a=p_a+W_a and U_j=p_j+N_j.
Norms are w. U_1 meets V_1,V_3,U_3; U_2 meets V_2,V_3,U_3;
U_3 meets all three triangle V's. The displayed projections and residual
pairing make every such inner product -1. Each pendant private vector
meets only its own marked vector. Old/private and different private
groups are disjoint. Together with old/marked pairings, these exhaust
every intersection type, including nonempty diagonals in the lift.
The nonempty vectors sum to K/ell; the **actual empty seed vector is
-K/ell**, with squared norm(ell*q-4)/ell^2.

## Exhaustive sector decomposition

The changed old span has l+3 dimensions, the marked residuals l+2,
and private residuals l+2. Their independent sum has dimension3l+7.
Together with both untouched spaces the seed core rank is

    (3l+7)+(q-2)+(q-l-2)=2q+2l+3=N-3.

Let TA=T_1-T_2 and TS=T_1+T_2-2T_3. Leaf exchange and pendant
permutation split the changed span into anti2, fixed8, and l-1 standard3
copies. They are mutually orthogonal both in Gram and complete frame.
The total count2+8+3(l-1)=3l+7 exhausts it. For pendant zero-sum
coefficients z with sum z_j^2=2, take the standard basis
(sum z_j A_zj,sum z_j Z_j,sum z_j N_j). For two coefficient vectors
all products scale by their dot product/2. Thus the small standard
matrix tensors a positive metric on the whole zero-sum coefficient
space; positivity of one3-block proves the complete standard space.
This direct product identity also covers l=2; there is no missing
representation type or assumed orthogonality of a difference basis.

Write Gamma for a physical basis Gram and F for its complete frame
bilinear. The cap test is (N-1)Gamma-F. For anti2=(TA,WA), Gamma is
diag(2s,alpha); congruence by Gamma inverse gives the equivalent2-test

    [[(N-1)/(2s)-(1+c^2)/2, c/2],
     [c/2, (N-1)/alpha-1/2]].

On a standard3 basis, Gamma=diag(6q,4s/3,2nuL). The cap is
D0-2bb'-2pp', with

    D0=diag(6q(N-7),4s(N-1)/3,2nuL(N-1)),
    b=(q,2s/3,0), p=(gq,2sg/3,nuL).

D0 is PD. The Schur complement equivalence yields the smaller test

    B=q/[6(N-7)]+s/[3(N-1)],
    [[1/2-B,-gB],[-gB,1/2-g^2 B-nuL/[2(N-1)]]].

Both tests have exact uniform PD certificates below. The empty vector
has zero pairing with anti and standard sectors.

## Fixed8: exact grouping and an inverse bound

Use basis (gp,h0,A_x,sum A_zj,TS,sum Z_j,WF,M0). Its Gamma has diagonals

    q-1,3,3(q-1),3l(q-l),6s,2ls/3,beta,mu

and only off-diagonal entries Gamma23=Gamma32=-3l (zero-based indices).
The old A-plane determinant is9lq(q-l-1)>0, so the full Gram is PD.
Let F0 be the old frame: its gp/h0 block is the one above, its A-plane
is6 times Gamma, and other entries are zero. In physical rank-one
operator notation [a]=|a><a|, the **entire** fixed frame is

    Ffixed=F0+[TS]/6+3[h_x]+l[vbar]+[K]/ell
                         +(3m/l)[Zp]+(2/3)[Dint],
    Zp=-(l*Fp/3)E+(c/9)TS+M0,
    Dint=(A-d)E+(c/6)TS-(3/2)WF.

Here an operator [a] has bilinear matrix(Gamma*a)(Gamma*a)' when a
is expressed in this basis. To prove the grouping, the two fixed leaf
vectors uL and the full vector uF satisfy
2[uL]+[uF]=3[(2uL+uF)/3]+(2/3)[uL-uF]. Their weighted mean is
-K/ell+Zp and their difference Dint. The fixed pendant private vector
is -K/ell-3Zp/l. Their3:l weighted sum, **plus actual empty [-K/ell]**,
is [K]/ell+(3m/l)[Zp]. Marked triangle vectors give
3[h_x]+[TS]/6; pendant marked vectors give l[vbar]. These identities
prove every update and cancellation. Omitting empty changes the K
weight and invalidates this reduction.

Subtract F0+[TS]/6 first. The resulting base of(N-1)I is PD: on the
old gp/h0 plane its first diagonal is(q-1)(N-q-2)>0 and determinant
3(q-1)J>0, where

    J=(N-q-2)(N-4)-3(q-1).

On the A-plane it is(N-7)I, on the summed Z line(N-1)I, on TS
(N-1-s)I, and on both WF and M0 lines(N-1)I. These factors and J
are positive for the domain below.

On the five old-plus-Z coordinates (gp,h0,A_x,sum A_zj,sum Z_j),
the inverse pairing of physical vectors with coefficients a,b is

    I0(a,b)=[(q-1)(N-4)a0b0+3(q-1)(a0b1+a1b0)
                 +3(N-q-2)a1b1]/J
          +3[(q-1)a2b2-l(a2b3+a3b2)+l(q-l)a3b3]/(N-7)
          +(2ls/3)a4b4/(N-1).

This follows by inverting the displayed2-block and scalar eigenspaces.
In these coordinates

    h_x=(0,1/3,1/3,0,0),
    vbar=(0,1/3,0,1/(3l),1/l),
    K=(1,l/3,1,1/3,1), E=h_x-rho*vbar.

For columns C=(h_x,vbar,K), let

    S3=diag(1/3,1/l,ell)-I0(C,C), b=I0(C,E).

The two Schur complements of a block matrix imply that S3>0 iff
subtracting3[h_x]+l[vbar]+[K]/ell leaves a PD base A5. Its E inverse
quadratic is the exact Woodbury expression

    tau=I0(E,E)+b'*S3^(-1)*b.

We prove uniformly **tau<Tb=(l+3)/(3l)**. The corresponding augmented
matrix is [[S3,b],[b',Tb-I0(E,E)]]. Add the first-three combination
(1,-rho,0) to its last coordinate. Its new cross is(1/3,-rho/l,0),
and its last diagonal Tb+1/3+rho^2/l. Next change the first3 coordinates
to(h_x-vbar,3h_x+l*vbar,K-3h_x-l*vbar). This invertible change has
determinant l+3>0 and produces the arrow matrix

    C3=[[aa,zz,0],[zz,bb,cc],[0,cc,dd]],
    D=N-7, H=N-1, A0=N-q-2,
    aa=[m-q(l+1)/D-2s/H]/(3l),
    zz=2(2l-1)/(D H),
    bb=m-m^2 A0/(3J)-[(l+9)q-m^2]/(3D)-2ls/(3H),
    cc=-m[1-(2l+5)/J],
    dd=2m+1-[(q-1)(N-10)+3A0]/J.

The transformed augmented4 matrix has first block C3, last cross
(1/3+rho/l,1-rho,rho-1), and last diagonal Tb+1/3+rho^2/l.
All nine rational first-block identities are checked symbolically, not
inferred from samples. Its four certified leading minors prove PD.
Congruence, then the Schur complement, prove S3>0 and tau<Tb.

Only the two Zp,Dint updates remain. Put

    a=-l*Fp/3, dInt=A-d, T=6s/(N-1-s),
    ZZ=a^2 tau+c^2 T/81+mu/(N-1),
    DD=dInt^2 tau+c^2 T/36+(9/4)beta/(N-1),
    ZD=a*dInt*tau+c^2 T/54.

Orthogonality of TS,WF,M0 and A5 proves these inverse pairings directly.
The final Schur test is

    S2=[[l/(3m)-ZZ,-ZD],[-ZD,3/2-DD]].

Substitute Tb for tau. This changes S2 by subtracting the PSD matrix
(Tb-tau)*(a,dInt)(a,dInt)', so positivity of the substituted test is
sufficient for the actual one. The substituted2-test has two uniform
certified positive leading minors. This proves the entire fixed8 cap.
The Schur, inverse and grouping implications are ordinary mathematics,
not a claim that the polynomial replay formalizes the surrounding proof.

## Exact signs and coverage of every actual parameter

All uniform signs use Q[u,v] in characteristic zero with

    l=2+u, q=4l-4+v, u>=0,v>=0.

Each rational denominator/row clearing factor is strictly positive on
this quadrant; the verifier checks its coefficients and positive constant.
Registering and exactly removing common positive factors controls
expansion without increasing the512-term guard. Positive row scalings
preserve the sign of every leading determinant of the original symmetric
form, even though the cleared matrix need not be symmetric. Bareiss
computes its leading determinant polynomials using exact division.
Each has nonnegative coefficients and positive constant; stored nonzero
coefficients are strictly positive. Sylvester's criterion therefore
proves PD on the **whole continuous quadrant**.

| Quantity/test | Positive coefficient counts | Full identity-grid points |
|---|---:|---:|
| etaL,etaF,etaP,mu,alpha,beta,nuL numerators |99,39,45,33,63,60,68|Direct exact rational formulas|
| anti2 leading minors |42,261|63,414|
| pendant-standard Schur2 leading minors |14,156|20,234|
| fixed base/inverse augmented4 leading minors |14,63,110,150|20,99,180,252|
| fixed final substituted Schur2 leading minors |85,357|130,567|

There are407 norm coefficients and1252 leading-minor coefficients,
all positive. For each determinant, separate degree bounds are computed
from the cleared matrix and verified for the candidate polynomial.
An independent Fraction Gaussian determinant agrees on **every point**
of the Cartesian grid of those degree bounds:1979 points total. A
polynomial within those bounds is uniquely determined by this grid,
which proves identity rather than providing a random sample. The
polynomial engine is separately compared with direct Fraction convolution
and exact multiplication-back controls, including its packed branch.

Every actual order is covered: q=2^(n-1)>=2^l since n>=l+1, and
2^l>=4(l-1) for every integer l>=2. The latter is equality for l2 and
l3; induction doubles4(l-1), which is at least4l for l>=2.
Thus u=l-2>=0,v=q-4l+4>=0. There are **no actual exceptional points**
requiring an unproved extension of this quadrant. Also q>l+1 and
N-1>max(2q,6), so all old Gram factors and untouched cap gaps are positive.

The full changed decomposition plus untouched spaces now gives the
whole balanced seed cap gap at least1, lower rankN-2 and upper rankN-1.
This is an original-set statement; positivity of a quotient alone would
not suffice.

## Explicit repair, greatest rank and the actual new empty row

Let W be the balanced private Gram. Delete the last pendant row to
obtain a PD principal matrix A, and let u0 indicate the first three
triangle private rows. The exact inverse quadratic is

    kappa=u0'*A^(-1)*u0=9(l-1)/(l*nuL)+3/(l*Cmean)>0.

For a proof, extend u0 to y=u0-3e_last, which has sum zero. Its
pendant-standard squared norm is9(l-1)/l and its fixed mean squared
norm3+9/l=3m/l. Divide by eigenvalues nuL and m*Cmean; internal
triangle components vanish. A kernel shift identifies this pseudoinverse
quadratic with the deleted inverse quadratic. The literal checker also
solves the deleted system by independent rational Gaussian elimination.

Choose

    delta=1/[12N(1+kappa)].

Add delta to the three symmetric core entries between u,v,uv and the
last pendant b_l. All these actual sets are disjoint, so every mandatory
entry and every nonempty norm is preserved. Since the old W cross
column is -A*1, the repaired residual Schur complement is exactly
6delta-kappa*delta^2>0. Thus W becomes PD. The original underlying
old/marked/private direct sum proves core rank increases fromN-3 toN-2,
giving rank(L)=N-1.

The symmetric core perturbation has maximum absolute row sum3delta,
so its operator norm is at most3delta. Since ||E0||^2=N, the whole
Q change has norm at most3Ndelta<1/4. It vanishes on1, and the seed
gap>=1 therefore becomes a gap at least3/4 on1-perp. **Recompute the
entire empty row and loop by the lift after repair**; the balanced
empty vector cannot simply be retained.

For any competing real ordinary H matrix, let f indicate the x-star
and z=f-(s/N)1. All entries of M on that star vanish, including its
diagonal. For its PSD lower matrix L, regularity gives L1=N1 and
z'Lz=s^2-2s^2+s^2=0. Hence Lz=0, with z nonzero, so rank(L)<=N-1.
Our repaired matrix reaches this bound. Its lower kernel is therefore
exactly span(z). The cap gap makes1 the simple unit eigenvector of M,
giving rank(I-M)=N-1. This all-real rank argument uses no competitor
cap or rationality assumption and does not claim an inertia-I result.

## Reproduction and trust boundary

The standalone [runner](verify.py) and [full compact record](RESULTS.json)
use only Python3's standard library, exact integers and Fraction. The
whole record contains the coefficients, clearing data, degree bounds,
all controls and original-matrix hashes. See [README](README.md) for
commands, resource guards and run measurements.

Eight fixed-frame controls verify all512 grouping positions and compare
the3-adjugate Woodbury scalar with an independently solved5-dimensional
Gaussian quadratic. Six complete actual fixtures
(n,l)=(3,2),(4,2),(4,3),(5,4),(6,2),(6,5), of sizes18,26,28,46,74,80,
verify every reduced Gram/frame entry, every complete changed Gram/frame
entry, all158 untouched eigenactions, and all15776 full positions per
seed or repaired matrix. All actual support, regularity, lower/upper
PSD/ranks, seed gap1, repaired gap3/4 and centered-star kernel pass.
The copied n3/l1 baseline reproduces the credited9408 construction,
including225 core and16 residual entries; it is prior validation.
Eighteen semantic rejection controls include false determinant identities,
singular PSD couplings, omitted empty frame, wrong congruence cross sign,
unrepaired rank, excessive repair, malformed labels and unchanged guard.

The finite fixtures validate formulas; they do not prove untested orders.
Infinite coverage rests on the ordinary decomposition/inverse proofs
and the uniform coefficient identities. The result is not formalized,
independently reviewed, or conditional on a numerical eigensolver.
The exact engine and helper provenance are credited in README; code reuse
and normal/-O agreement do not establish independence. Timeout, UNKNOWN,
memory or polynomial guard failure would be operational limits, not
mathematical nonexistence. No large private corpus or external certificate
is needed to reproduce this result.
