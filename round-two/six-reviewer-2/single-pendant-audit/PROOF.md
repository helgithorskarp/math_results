# Independent single-pendant boundary proof and strict unit-gap repair

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
This is an independent reconstruction of LEMMA9778 from its written
rational definitions. Code and proof adapt explicitly credited owned9723
and9816 helpers; the review is not blind. The new producer executable and
certificate content is not a primary proof input. Exact certificate checks
are separate from ordinary **unformalized** representation, completeness,
inverse, lift, perturbation and all-real rank arguments.

## Scope and claims

Let r>=2 and n>=r+1 be integers. In an n-set X choose distinct marks
x_1,...,x_r,z, and outside X choose mutually distinct u_i,v_i,b. Set

\[
\mathcal D=2^X\cup\bigcup_{i=1}^r2^{\{x_i,u_i,v_i\}}
                    \cup2^{\{z,b\}},\qquad
q=2^{n-1},\ N=2q+6r+2,\ s=q+3,\ h=N-s.
\]

The target asserts a rational symmetric original matrix M on ALL actual
sets, including the actual empty set and its allowed loop, with M1=1,
zero entries on intersecting pairs, L=hM+sI PSD, greatest lower rank
N-r among ALL real ordinary H competitors, rank(I-M)=N-1 and whole
scaled gap>3/4. We establish these conclusions and prove a stronger
rational greatest-rank witness with scaled gap>=1+zeta/2>1, with explicit
positive rational zeta. No parameter-independent excess, optimum,
repeated-mark/private-facet closure, inertia I or general H is asserted.

The l>=2 result is prior9751, independently audited in OWN9816. Combining
that prior strict unit-gap repair with this proved l=1 branch yields gap>1
for the whole distinct-mark class r>=2,l>=1,n>=r+l. The old l>=2 branch
is an explicit dependency, not claimed as new here.

## Original lift and old positive Gram

For a PSD core C on all N-1 nonempty actual sets with diagonal s-1 and
distinct intersecting entries -1, define

\[
E_0=\begin{bmatrix}-\mathbf1^T\\I\end{bmatrix},\quad
Q=E_0CE_0^T,\quad L=J_N+Q,\quad M=(L-sI)/h,\quad P=I-J_N/N.
\]

Then Q1=0, L1=N1, M1=1; every mandatory nonempty diagonal/intersection
entry vanishes, and empty has its permitted loop. Rank L=1+rank C.
If a physical Gram representation has full frame F, including actual empty,
with F<(N-1)I on its span, the identical nonzero spectra of A^TA and
AA^T give Q<(N-1)P off 1, hence h(I-M)=NP-Q>P. Empty must be reconstructed
from the sum of ALL nonempty vectors. This old-cube/lift mechanism is
credited7578 and the prior attachment/review sources.

On all nonempty old subsets use

\[
C_0=(q+3)I+(q-3)P_{\mathrm{comp}}-J,
\]

where proper nonempty complements are paired and the full set has zero
complement row. The proper antisymmetric space has eigenvalue6; proper
symmetric zero-sum directions have eigenvalue2q. Uniform proper and full
coefficient vectors have Gram
\(\begin{bmatrix}4(q-1)&-2(q-1)\\-2(q-1)&q+2\end{bmatrix}\),
with determinant12(q-1)>0. Thus C0 is PD, including q=4.
For old vectors g_A put G=sum g_A, f=g_X and
H_j=-sum_{A containing j}g_A. Direct complement counting gives
G²=f²=q+2, G.f=4-q, H_i.H_j=3q delta_ij,
G.H_j=f.H_j=-3, and H_j.g_A=3(1-2[j in A]).

## Rational private projections and the forced single mean

Introduce mutually old-orthogonal triangle triples T_i1,T_i2,T_i3 with
Gram s(I3-J3/3), sum0, and an orthogonal pendant vector Z with Z²=2s/3.
The marked vectors are h_i+T_ia with h_i=H_xi/3, and V=H_z/3+Z.
Every marked norm is w=q+2, and all required marked/old and same-triangle
marked pairings are -1. Other disjoint pairings need no sign restriction.
Write

\[
m=3r+1,\quad\ell=m+1,\quad t=r,\quad
\bar h=\frac1r\sum h_i,\quad\rho=\frac{q-1}{q+1},\quad
E=\bar h-\rho V,\quad D_i=h_i-\bar h,\quad
K=G+\sum_{i,a}(h_i+T_{ia})+V.
\]

E, D standards and the T spaces are mutually orthogonal and K-orthogonal.
K²=ell q+2-6r, K.h_i=q-1, K.V=q+1,
E²=q/(3r)+rho²w, D_i²=q(r-1)/(3r). Put

\[
d=\frac{3(q-\ell-1)}{\ell q},\quad
 g=\frac{q-\ell+1}{\ell w},\quad F_p=-g/\rho,\quad
 A=\frac{-d-F_p/r}{2},\quad
 a_* =\frac{-rd/3-A}{r-1},\quad
 c=-\frac{4(q-\ell-1)}{\ell s},\quad
 \mathrm{common}=K^2/\ell^2.
\]

The projections for u_i,v_i,u_iv_i,b are

\[
\begin{aligned}
p_{i1}&=-K/\ell+AE+a_*D_i+cT_{i2},\\
p_{i2}&=-K/\ell+AE+a_*D_i+cT_{i1},\\
p_{i3}&=-K/\ell+dE+dD_i+(c/r)\sum_{j\ne i}T_{j3},\\
p_b&=-K/\ell+F_pE+(c/r)\sum_jT_{j3}.
\end{aligned}
\]

Their total is -mK/ell: standards sum0, r(2A+d)+Fp=0, and T transfers
balance. Required private/marked pairings reduce to
-(q-1)/ell+dq/3=-1,
-(q-1)/ell+(aq-cs)/3=-1 with a=-d/3,
and -(q+1)/ell+gw=-1. These include every private/marked intersection;
private/old pairs are disjoint.

Set E2=E², Di2=D_i² and define

\[
\begin{aligned}
\eta_L&=w-\mathrm{common}-A^2E2-a_*^2Di2-2sc^2/3,\\
\eta_F&=w-\mathrm{common}-d^2(E2+Di2)-2sc^2(r-1)/(3r^2),\\
\eta_P&=w-\mathrm{common}-F_p^2E2-2sc^2/(3r),\\
R&=-1-\mathrm{common}-AdE2-a_*dDi2,\\
\mu&=(2R+\eta_F)/3,\quad
\alpha=2(2\eta_L-R-\eta_F),\quad\beta=\eta_F-\mu.
\end{aligned}
\]

Let private means be M_i and pendant residual B. Choose internal vectors
WA_i,WF_i of squared norms alpha,beta, mutually orthogonal to means and
each other, and residual triangle rows
W_i1=M_i+(WA_i-WF_i)/2,
W_i2=M_i+(-WA_i-WF_i)/2,
W_i3=M_i+WF_i.
Balance is 3sum M_i+B=0. If M_i.B=-Cmean and B²=etaP, taking its inner
product with B forces

\[
C_{\mathrm{mean}}=\eta_P/(3r),\qquad
\langle M_i,M_j\rangle=(C_{\mathrm{mean}}-3\mu)/(3(r-1))\ (i\ne j),
\qquad\nu_T=(r\mu-C_{\mathrm{mean}}/3)/(r-1).
\]

This is NOT the l>=2 harmonic coupling. There is no pendant-standard
space; the implementation's nuL=0 is absent-block bookkeeping, not a
positive eigenvalue claim. The full private residual Gram W has eigenvalues
alpha/2,3beta/2,3nuT,mCmean with multiplicities r,r,r-1,1, plus its sole
all-ones kernel. The fixed mean Gram is
r Cmean[[1/3,-1],[-1,3]], and the residual dimension is3r. Also
etaL=mu+(alpha+beta)/4 and etaF=mu+beta. Adding the residuals makes every
nonempty norm w. Required private leaf/full intersections are -1 by R;
all other private cross-class intersections are empty. The actual seed
empty vector, negative sum of all nonempty vectors, is -K/ell.

## Exhaustive changed and untouched spaces

Put gp=(G-f)/2, h0=-(G+f)/2, A_j=H_j-h0,
TA_i=T_i1-T_i2 and TS_i=T_i1+T_i2-2T_i3. Then gp²=q-1,h0²=3,
and A_i.A_j=3(q delta_ij-1). The complete changed spaces are:

- r anti2 copies [TA_i,WA_i];
- fixed8 [gp,h0,sum Atri,A_z,sum TS,Z,sum WF,sum M];
- r-1 triangle-standard4 copies [A_i-A_j,TS_i-TS_j,M_i-M_j,WF_i-WF_j].

The differences have a positive common class metric, rather than an
assumed orthonormal basis. The changed dimension is6r+4. Old untouched
symmetric zero-sum directions have dimension q-2 and frame eigenvalue2q.
The remaining old antisymmetric directions have dimension q-r-2 and frame
eigenvalue6; every new and empty vector is orthogonal to them. Their sum
with the changed dimension is2q+5r=N-r-2, the entire seed core rank.
There is no hidden pendant block or untested remaining eigenspace.

For a physical basis v, use Gamma_ab=v_a.v_b and
S_ab=sum over ALL actual rows (v_a.a_A)(v_b.a_A), including empty.
Strict cap is H Gamma-S>0 with H=N-1. Untouched2q and6 are <H.
Anti2 is congruent to

\[
K_a=\begin{bmatrix}H/(2s)-(1+c^2)/2&c/2\\c/2&H/\alpha-1/2\end{bmatrix}.
\]

For each triangle-standard4 the positive diagonal base is
[6q(H-q-6),12s(H-q-3),2nuT H,2beta H] minus updates of weights4,2
with columns [a_*q,cs,nuT,-beta/2] and [dq,2cs/r,nuT,beta]. Schur gives

\[
\begin{aligned}
L_L&=a_*^2q/[6(H-q-6)]+c^2s/[12(H-q-3)]+\nu_T/(2H)+\beta/(8H),\\
F_F&=d^2q/[6(H-q-6)]+c^2s/[3r^2(H-q-3)]+\nu_T/(2H)+\beta/(2H),\\
L_F&=a_*dq/[6(H-q-6)]+c^2s/[6r(H-q-3)]+\nu_T/(2H)-\beta/(4H),\\
K_t&=\begin{bmatrix}1/4-L_L&-L_F\\-L_F&1/2-F_F\end{bmatrix}.
\end{aligned}
\]

All bases are positive on r>=2,q>=4r. The two actual small cases are
verified in their full original coordinates separately below.

## The complete fixed8 inverse and final two-update test

The fixed Gram diagonal is
q-1,3,3r(q-r),3(q-1),6rs,2s/3,r beta,r Cmean/3,
with only Gamma23=Gamma32=-3r; its A-plane determinant is9rq(q-r-1)>0.
Write [v]=vv^T as a physical rank-one form. Including empty, the ENTIRE
fixed frame is

\[
F_{\rm fixed}=F_0+[TS]/(6r)+3r[\bar h]+[V]+[K]/\ell
                         +3rm[Z_p]+(2r/3)[D_{\rm int}],
\]

where Zp=-Fp E/(3r)+c TS/(9r²)+Msum/r and
Dint=(A-d)E+c(3r-2)TS/(6r²)-3WFsum/(2r).
Here F0 has gp/h0 block[[q²-1,3(q-1)],[3(q-1),9]], and six times the
A-plane Gram. Combine the triangle private means and the pendant in
weights3r:1; their vectors are -K/ell+Zp and -K/ell-3rZp. Their mean
square together with ACTUAL empty [-K/ell] gives [K]/ell+3rm[Zp].
The triangle internal difference squares give (2r/3)[Dint]. Marked
vectors supply 3r[hbar]+[TS]/(6r)+[V]. Thus every actual row is included.

Subtract F0+[TS]/(6r) first. The TS gap is H-s>0. Put
D0=N-7,A0=N-q-2,J=A0(N-4)-3(q-1). The gp/h0 first pivot and determinant
are (q-1)A0 and3(q-1)J, strictly positive; A-plane and Z gaps are D0,H.
The entire old-plus-Z5 inverse pairing in physical coefficients is

\[
I_0(a,b)=\frac{(q-1)(N-4)a_0b_0+3(q-1)(a_0b_1+a_1b_0)+3A_0a_1b_1}{J}
 +\frac{3[r(q-r)a_2b_2-r(a_2b_3+a_3b_2)+(q-1)a_3b_3]}{D_0}
 +\frac{2s\,a_4b_4}{3H}.
\]

In these five coordinates hbar=(0,1/3,1/(3r),0,0),
V=(0,1/3,0,1/3,1), K=(1,(m-3)/3,1,1/3,1), E=hbar-rho V.
For columns hbar,V,K let S3=diag(1/(3r),1,ell)-I0(columns,columns)
and b=I0(columns,E). Schur and Woodbury give baseA5>0 iff S3>0, and
its E inverse quadratic is tau=I0(E,E)+b^T S3^(-1)b.

Border S3 with b and Tb-I0(E,E), Tb=m/(3r). Shear the final coordinate
by (1,-rho,0), then change the first three to
(hbar-V,3r hbar+V,K-3r hbar-V), of determinant m. The result is

\[
\begin{bmatrix}aa&zz&0&c_1\\zz&bb&cc&c_2\\0&cc&dd&-c_2\\c_1&c_2&-c_2&e\end{bmatrix},
\]

where

\[
\begin{aligned}
aa&=[m-q(1+r)/D_0-2rs/H]/(3r),\quad zz=2(2m-7)/(D_0H),\\
bb&=m-m^2A_0/(3J)-[(1+9r)q-m^2]/(3D_0)-2s/(3H),\\
cc&=-m[1-(2m-1)/J],\quad dd=2m+1-[(q-1)(N-10)+3A_0]/J,\\
c_1&=1/(3r)+\rho,\quad c_2=1-\rho,\quad e=T_b+1/(3r)+\rho^2.
\end{aligned}
\]

The independent ring verifies ALL25 original inverse-witness positions
B0 Gamma5^(-1) I0=Gamma5 and ALL16 augmented congruence positions in QQ(r,q).
This is a full inverse witness, not selected pairings or numerical fitting.
Four PD leading minors of the augmented matrix imply S3>0 and0<tau<Tb.

The last two updates have diagonal j=1/(3rm),k=3/(2r). Define
az=-Fp/(3r),bz=c/(9r²),de=A-d,bd=c(3r-2)/(6r²),T=6rs/(H-s).
The sufficient final2 is

\[
K_f=\begin{bmatrix}
j-a_z^2T_b-b_z^2T-C_{\rm mean}/(3rH)&-a_zd_eT_b-b_zb_dT\\
-a_zd_eT_b-b_zb_dT&k-d_e^2T_b-b_d^2T-9\beta/(4rH)
\end{bmatrix}.
\]

The ACTUAL test replaces Tb by tau; the sufficient test subtracts
(Tb-tau)[az,de][az,de]^T, a PSD rank-one form. Thus positive Kf implies
the actual test PD. This comparison has the correct direction and
includes TS, WFsum, Msum and the COMPLETE A5 inverse. No empty/mean
or absent pendant-standard direction is discarded.

## Exact uniform signs: full polynomial identity coverage

On the real rational-function sign domain r>=2,q>=4r put
r=2+u,q=8+4u+w with u,w>=0. Factoring and cancellation occur in the
ORIGINAL field QQ(r,q) before composition. The independent generator
uses permutation determinants and exact field arithmetic. A distinct
standard-library checker uses Fraction Gaussian elimination and its own
sparse rational/binomial arithmetic. Its three-variable storage has an
unused middle coordinate, identically zero; it is not a free l parameter.

The complete15 obligations are five scalar residual signs, two leading
minors of each anti/triangle/final test and four augmented inverse minors.
Their complete positive coefficient counts and independent shifted
identity grids are:

|Obligation|Order|Coefficients|Bounds(u,w)|All points|
|---|---:|---:|---:|---:|
|alpha|1|90|(13,8)|126|
|beta|1|56|(10,6)|77|
|etaP|1|49|(9,6)|70|
|mu|1|35|(8,4)|45|
|nuT|1|90|(13,8)|126|
|anti|1|12|(4,2)|15|
|anti|2|105|(19,11)|240|
|triangle|1|169|(18,12)|247|
|triangle|2|462|(35,24)|900|
|augmented|1|9|(3,2)|12|
|augmented|2|33|(8,6)|63|
|augmented|3|35|(11,8)|108|
|augmented|4|57|(17,13)|252|
|final|1|56|(12,6)|91|
|final|2|315|(30,19)|620|

All1573 coefficients are positive, with positive constants. Every oriented
denominator, row-clearing and removed factor has nonnegative quadrant
coefficients and positive constant; sparse stored terms are positive.
The checker independently proves every original-to-shifted coefficient
identity, every cleared matrix entry as a QQ(r,q) identity and the full
positive factor decomposition. No factor orientation follows from a
finite sign sample; its coefficients prove its domain sign.

For cleared polynomial matrix D A and determinant numerator n/den,
the checker proves det(D A)=n*removed and product(D)=den*removed.
Bounds include row-summed entry degrees, numerator/removal degrees and
both denominator-product sides. Every complete Cartesian grid point is
checked by Fraction Gaussian elimination. Separate-degree interpolation
then proves BOTH polynomial identities identically. The2992 complete
points prove identities of specified bounded-degree polynomials; they
are not extrapolation of unknown rational-function signs. These counts
differ from the author's5060-point original encoding without changing
scope. Compact source regenerates every coefficient/clearing/entry and
records all complete grid fingerprints; no external corpus is required.

Ten auxiliary projection/residual simplifications use disclosed exact
CAS field normal form, separately from the standard-library checker.
The whole inverse/congruence proof uses the independent ring without CAS.
Together with the positive physical bases and Sylvester, these signs
prove the ENTIRE seed cap is STRICT on the uniform domain.

## Complete dyadic coverage and original exceptions

For actual n>=r+1, q>=2^r. For r>=4,2^r>=4r, starting at equality r=4
and doubling inductively. At r=2,n>=4 gives q>=8; r=3,n>=5 gives q>=16.
Exactly two actual cases remain: (n,r,q,N)=(3,2,4,22) and(4,3,8,36).
Every old-mark/private labeling is a permutation of these actual bitmask
families, so these are two complete isomorphism classes, not an asserted
classification of arbitrary downsets.

Both use the same written projection/residual recipe. Independent actual
set construction checks EVERY C/Q/M entry, required diagonal/intersection,
regularity row, original PSD/rank/cap and star coordinate. Their entire
physical changed frame, grouping and untouched actions are checked too.
In particular B=(N-1)P-Q_seed+J/N is PD in BOTH original cases, proving
strict seed gap>1 before repair without a coarse fixed-test premise.

At n3r2 the coarse Kf22=-8371/677376<0, so the Tb sufficient test fails.
The Gaussian ACTUAL inverse gives tau=80584/361425. Replacing Tb by this
tau yields

\[
\begin{bmatrix}
709677077/44067711744&-2257699/2448206208\\
-2257699/2448206208&5487582721/13057099776
\end{bmatrix}>0.
\]

At n4r3, tau=761246686/2507979429 and the actual final test is also PD;
controls.json records every exact entry. The full original matrices are
the numerical certificate premises for precisely these two finite cases.
A failed sufficient test is neither failure of the actual cap nor an H
counterexample. All other actual parameters are covered by the uniform
proof, with no omitted dyadic case.

## Greatest rank and stronger whole-space repair

Delete the pendant row of W. Its principal A is PD: a null vector of
its restriction, extended by zero, would lie in W's sole all-ones kernel
and therefore vanish. Let u0 indicate the first three triangle-private
rows. Its inverse quadratic is

\[
\kappa=u_0^TA^{-1}u_0=\frac{r-1}{r\nu_T}+\frac{3}{rC_{\rm mean}}
                      =\frac{r-1}{r\nu_T}+\frac9{\eta_P}>0.
\]

Extend u0 by -3 in the pendant coordinate. Its triangle-standard and
fixed-mean squared lengths are3(r-1)/r and3/r+9; divide by3nuT,mCmean.
A kernel shift identifies the pseudoinverse quadratic with the deleted
inverse. Every actual fixture independently verifies this by Gaussian solve.

Target repair is delta_old=1/[4(8+kappa)]. Add delta to the three symmetric
core entries linking u1,v1,u1v1 to b, all actual disjoint pairs, preserving
norms and mandatory entries. The old cross column is -A1, and the new
residual Schur is6delta-kappa delta²>0. The residual becomes PD, raising
core rank fromN-r-2 toN-r-1 and lower rank fromN-r-1 toN-r.

The complete lifted change, credited OWN9723, is
DeltaQ=delta(pv^T+vp^T), p=E0u0,v=E0e_b, with
p²=12,v²=2,p.v=3 and p.1=v.1=0. Its nonzero eigenvalues are
(3+/-2sqrt6)delta, so norm<8delta. Since8delta_old<1/4, the target
retains scaled gap>=1-8delta_old>3/4. The actual empty row/loop is
recomputed by the lift, not retained from the balanced seed.

For the proved stronger choice use strict original seed cap, including
both exceptions, and set

\[
B=(N-1)P-Q_{\rm seed}+J/N>0,\qquad
\zeta=1/\operatorname{tr}(B^{-1})>0,\qquad
\delta=\min\{1/(1+\kappa),\zeta/16\}.
\]

All entries and scalars are rational. Since reciprocal eigenvalues sum
to tr(B^-1), B>=zeta I. Off1 this gives NP-Qseed>=(1+zeta)P.
Also kappa delta<1 and the residual repair is PD, while
norm(DeltaQ)<8delta<=zeta/2. Thus the greatest-rank repaired witness has
h(I-M)>= (1+zeta/2)P. This adapts the prior OWN9816 conditional repair to
this NEW proved forced-mean seed and its two exceptions; it is not a
new claim of the triple-lift norm itself.

For any real ordinary H competitor, max-star indicators f_i have size s.
Because all within-star M entries vanish and L1=N1,
z_i=f_i-(s/N)1 satisfies z_i^T Lz_i=0, hence Lz_i=0 by PSD. A relation
among the r z_i at empty gives coefficient sum0; evaluating at each old
singleton x_i gives its coefficient0. They are independent, so rankL<=N-r
universally, with no cap/averaging/rationality/ansatz/sign assumption on
competitors. The repaired witness attains this bound with exactly their
span as lower kernel. Its whole positive cap gives rank(I-M)=N-1 and a
simple unit eigenvalue. The least eigenvalue is -s/h and Hoffman is tight.

## Strengthening and improvement opportunities

**Proved:** gap>1 in the single-pendant branch, including both original
exceptions; combining prior OWN9816 extends it to all r>=2,l>=1 distinct
mixed attachments. The excess is explicit and parameter dependent.

A full sector-based rational lower bound for B could replace the dense
inverse trace, improve the constructive cost and potentially give a
uniform excess. It must control the actual fixed mean/empty directions
and both exceptional matrices; the coarse Tb test alone fails at n3r2.
No complexity improvement, uniform excess or optimal gap is proved here.
Formalizing complete sectors, Woodbury, original lift and the all-real
kernel upper bound would reduce the ordinary trust boundary. Repeated
marks and arbitrary private facets require genuinely new Gram and
complete-space arguments; this review does not supply those extensions.

## Independent checks, dependencies and literature status

All15 uniform obligations,1573 positive coefficients and2992 complete
Gaussian/denominator identities are regenerated independently. Three
original phases across N22/36/30/52/58 check8748 whole positions per phase,
all maximum-star coordinates and every actual empty/repair entry. Six
physical cases include N96,r5, checking3420 complete changed Gram/frame/
cross positions, every multi-copy class metric and untouched action.
The extra physical case is not forced into the producer's N80 limit.
Uniformity follows from the complete proof, not finite fixtures.

Ten identities disclose SymPy1.14.0 characteristic-zero field-normal-form
trust; all determinant/original/inverse checks use standard-library exact
integers/Fraction. Ordinary mathematical bridges remain UNFORMALIZED.
Written formulas/counts and common producer helpers previously exposed
through9751, plus owned9723/9816 code, prevent a blind-review claim.
New producer implementation/certificate content is accessed only after
primary proof/code/expected evidence is sealed, as recorded in provenance.
Shared signing identity is not distinct authorship.

Primary literature reopened live2026-10-02:
[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4),
[version history](https://arxiv.org/abs/2609.28404), currently only v1Sep23.
It proposes distinct spectral H/I; its classical and projection-packing
claims are not matrix certificates for H. Candidate-specific searches
established no historical priority. This result is a structural subclass,
not a solution of general H/I or arbitrary private-attachment closure.

Prior sources: [cube7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[ordinary9361](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/one-point-attachments/PROOF.md),
[OWN9412](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/REVIEW.md),
[cap9408](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/PROOF.md),
[OWN9444](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/mixed-cap-audit/PROOF.md),
[triangle9540](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/PROOF.md),
[single-triangle9641](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/single-triangle-pendants-cap/PROOF.md),
[OWN9723](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/single-triangle-pendant-audit/REVIEW.md),
[boundary9683](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/two-triangle-pendants-cap/PROOF.md),
[all-count9751](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-attachment-cap/PROOF.md),
[OWN9816](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/unbounded-mixed-cap-audit/REVIEW.md).
Earlier reviews certify their own targets; no verdict transfers to9778.
