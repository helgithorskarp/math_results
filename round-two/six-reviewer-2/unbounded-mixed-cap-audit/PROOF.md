# Independent all-count mixed-cap audit and a strict unit-gap repair

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
Target: LEMMA9751, `bafkreiep47z5ooqbgiecuarmjiujjyjlxwaitwean3eswa7vhbqiqs7fym`,
researcher six-downset-1, source `e295072308c0501913c27e678f0a88c6ad267d8a`.
The r=2 boundary is LEMMA9683,
`bafkreieccs7da4qvw4gik7npjeonvoo4dmx7h4r6bqf4nlrmpdg5plcbye`, source
`c718a6f93f944d1a7513856d2e9c2233743a125c`.
This document gives the ordinary mathematical audit and proved strengthening;
[REVIEW.md](REVIEW.md) records the final verification status and trust boundary.
Shared signing identity does not establish independent authorship.

## Exact family and conclusion

Let integers r,l>=2 and n>=r+l. Choose distinct old marks x_i,z_j in an
n-set X and mutually distinct private u_i,v_i,b_j outside X. Define
\[
 D=2^X\cup\bigcup_{i=1}^r2^{\{x_i,u_i,v_i\}}
       \cup\bigcup_{j=1}^l2^{\{z_j,b_j\}},\quad
 q=2^{n-1},\ N=2q+6r+2l,\ s=q+3,\ h=N-s,\ P=I-J_N/N.
\]
The target claims a rational symmetric ORIGINAL matrix M, retaining actual
empty and its allowed loop, with M1=1, M_AB=0 when A intersects B,
L=hM+sI PSD, rank L=N-r greatest among ALL real ordinary H competitors,
rank(I-M)=N-1 and h(I-M)>=(3/4)P. The new author scope is r>=3;
r=2 is explicitly imported from9683. The audit handles both cases separately.

The proved refinement is that for each family member there is an explicit
rational greatest-rank M with
\[
 h(I-M)\succeq(1+\zeta/2)P,\qquad\zeta>0
\]
where a rational inverse-trace formula below defines zeta. This is a
parameter-dependent strict excess, without a uniform positive excess over
all n,r,l, a sharpness assertion, or an efficient large-N algorithm claim.
It does not cover l=1, repeated old marks, nonprivate facets or general H/I.
The subsequently published l=1 claim9778 is outside this audit.

## Whole original lift and old cube

For a Gram core C on ALL nonempty actual sets, with C_AA=s-1 and
C_AB=-1 for distinct intersecting sets, let
\[
 E_0=[-\mathbf1^T;I_{N-1}],\ Q=E_0CE_0^T,\ L=J_N+Q,
 \quad M=(L-sI)/h.
\]
Then Q1=0, L1=N1, all mandatory support entries vanish, and
rank L=1+rank C. The actual empty vector is minus the sum of all nonempty
vectors. Every empty entry and loop is determined by this lift. If the
COMPLETE physical frame, including empty, is strictly below (N-1)I on its
span, the nonzero spectra of AA^T and A^TA give Q<(N-1)I on its image.
On its orthogonal complement Q=0. Therefore
\[
 B=(N-1)P-Q+J_N/N
\]
is PD on the entire N-dimensional original space. This strict statement is
needed for the improvement; a quotient-only or non-strict cap is insufficient.
The original lift and cube mechanism are credited to7578 and prior attachment
work, without novelty claimed for them.

For old nonempty cube vectors take C0=(q+3)I+(q-3)Pc-J, where Pc pairs
proper nonempty complements and has zero full-set row. Direct complement
counting gives G=sum_A g_A, f=g_X, H_i=-sum_{i in A}g_A,
\[
 G^2=f^2=q+2,\ G\cdot f=4-q,\ H_i\cdot H_j=3q\delta_{ij},
 \quad G\cdot H_i=f\cdot H_i=-3,
 \quad H_i\cdot g_A=3(1-2\mathbf1_{i\in A}).
\]
There are q-2 pair-constant zero-sum directions with eigenvalue2q,
q-1 antisymmetric directions with eigenvalue6, and a remaining plane of
Gram diag(q-1,3), using gp=(G-f)/2,h0=-(G+f)/2. Thus C0 is PD.
Write A_i=H_i-h0, so A_i.A_j=3(q delta_ij-1). The marked A plane is PD
because q>r+l. The untouched antisymmetric complement has dimension
q-r-l-1. Both untouched spaces are orthogonal to new and empty vectors,
and their complete-frame eigenvalues2q and6 are strictly below N-1.

## Rational projections and the balanced private residual

For each triangle let h_i=H_xi/3 and take an independent plane of T_ia
with Gram s(I3-J3/3) and sum zero. Marked rows are h_i+T_ia.
Each pendant marked row is V_j=H_zj/3+Z_j with Z_j^2=2s/3. All these
residual spaces are mutually orthogonal and old-orthogonal. Marked norms
are w=q+2. Define
\[
 m=3r+l,\ \ell=m+1,\ t=r+l-1,\ \rho=(q-1)/(q+1),
\]
\[
 \bar h=r^{-1}\sum_i h_i,\quad\bar v=l^{-1}\sum_jV_j,
 \quad E=\bar h-\rho\bar v,\quad D_i=h_i-\bar h,\quad J_j=V_j-\bar v,
 \quad K=G+3\sum_i h_i+\sum_jV_j.
\]
K is orthogonal to E, both standards and all T planes;
K^2=ell q+2-6r, K.h_i=q-1, K.V_j=q+1,
E^2=q/(3r)+rho^2 w/l, D_i^2=q(r-1)/(3r), J_j^2=w(l-1)/l.
Put
\[
 d=\frac{3(q-\ell-1)}{\ell q},\quad
 g=\frac{q-\ell+1}{\ell w},\quad F_p=-g/\rho,\quad
 A=(-d-lF_p/r)/2,\quad a=-d/3,
\]
\[
 a_*=(ra-A)/(r-1),\qquad c=(a-d)q/s,
 \qquad c_0=K^2/\ell^2.
\]
The projections of the three private triangle rows and private pendant row
are
\[
 p_{i1}=-K/\ell+AE+a_*D_i+cT_{i2},\quad
 p_{i2}=-K/\ell+AE+a_*D_i+cT_{i1},
\]
\[
 p_{i3}=-K/\ell+dE+dD_i+(c/t)\sum_{k\ne i}T_{k3},\quad
 p_j=-K/\ell+F_pE+gJ_j+(c/t)\sum_iT_{i3}.
\]
Their sum is -mK/ell: r(2A+d)+lFp=0 and every transfer occurs
r-1+l=t times. Mandatory private/marked pairings follow from
-(q-1)/ell+dq/3=-1, -(q-1)/ell+(aq-cs)/3=-1 and
-(q+1)/ell+gw=-1. These cover every such intersection, including full
triangle private sets; other old/private and cross-private groups are disjoint.

The norms etaL,etaF,etaP, pair,mu,alpha,beta are given as COMPLETE rational
formulas in [forms.py](forms.py), directly from these projection norms:
\[
 \eta_L=w-c_0-A^2E^2-a_*^2D_i^2-2sc^2/3,
\]
\[
 \eta_F=w-c_0-d^2(E^2+D_i^2)-2sc^2(r-1)/(3t^2),
\]
\[
 \eta_P=w-c_0-F_p^2E^2-g^2w(l-1)/l-2sc^2r/(3t^2),
\]
\[
 p=-1-c_0-AdE^2-a_*dD_i^2,\quad
 \mu=(2p+\eta_F)/3,\quad\alpha=2(2\eta_L-p-\eta_F),\quad\beta=\eta_F-\mu.
\]
Use the harmonic Cmean, abbreviated C in this section,
\[
 C=\frac1{2\{l/(3r\mu)+3r/(l\eta_P)+m/q\}},\quad
 a_M=\frac{lC-3\mu}{3(r-1)},\quad b_M=\frac{3rC-\eta_P}{l-1},
\]
\[
 \nu_T=\mu-a_M=\frac{r\mu-lC/3}{r-1},\qquad
 \nu_L=\eta_P-b_M=\frac{l\eta_P-3rC}{l-1}.
\]
Triangle means M_i have diagonal mu, off-diagonal aM; pendant means N_j
have diagonal etaP, off-diagonal bM; cross-products are -C. Independent
internal vectors WA_i,WF_i have norms alpha,beta. Actual private residuals
are W_i1=M_i+(WA_i-WF_i)/2, W_i2=M_i+(-WA_i-WF_i)/2,
W_i3=M_i+WF_i and N_j. Their m-row Gram W has eigenvalues alpha/2,
3beta/2,3nuT,nuL,mC on the leaf, internal, triangle standard, pendant
standard and nonzero fixed-mean types. Their multiplicities are
r,r,r-1,l-1,1, plus one zero direction, totaling m. The zero direction
is precisely 1_m. Thus W PSD and rank m-1 once the stated scalar signs
hold. Means cancel 3sum M_i+sum N_j=0. Adding the residuals to projections
makes all nonempty norms w and all intersecting private leaf/full pairings
-1. Nonempty vectors sum to K/ell, so actual empty is -K/ell before repair.
All Gram entries are rational although an optional Euclidean factorization
may use square roots.

## Complete physical reduction and inverse identities

With TA_i=T_i1-T_i2 and TS_i=T_i1+T_i2-2T_i3, the complete changed space
splits into r leaf-flip2 blocks, a fixed8 block, r-1 triangle-standard4
blocks and l-1 pendant-standard3 blocks. Its dimension is6r+3l+1.
Together with the two untouched spaces it has dimension N-r-2, exactly
seed core rank. Permutation standards tensor a positive metric on their
full zero-sum coefficient spaces; difference vectors are not orthonormal.
All blocks are orthogonal in BOTH Gram and the complete frame. This follows
by summing displayed projections and their class counts, rather than assuming
finite-case orthogonality extends. The literal audit checks the whole metric,
all cross entries and all tensor entries for multiple copies.

For H=N-1 the leaf-flip cap is congruent to
\[
 \begin{pmatrix}H/(2s)-(1+c^2)/2&c/2\\c/2&H/\alpha-1/2\end{pmatrix}.
\]
Pendant Schur2 has Bp=q/[6(H-6)]+s/(3H) and entries
(1/2-Bp,-gBp; -gBp,1/2-g^2Bp-nuL/(2H)).
Triangle Schur2 is diag(1/4,1/2)-(LL,LF;LF,FF), with
\[
 LL=a_*^2q/[6(H-q-6)]+c^2s/[12(H-q-3)]+\nu_T/(2H)+\beta/(8H),
\]
\[
 FF=d^2q/[6(H-q-6)]+c^2s/[3t^2(H-q-3)]+\nu_T/(2H)+\beta/(2H),
\]
\[
 LF=a_*dq/[6(H-q-6)]+c^2s/[6t(H-q-3)]+\nu_T/(2H)-\beta/(4H).
\]
These follow by eliminating the positive diagonal bases in physical Gram
coordinates. No approximation to a whole matrix is being made.

The fixed8 basis is gp,h0,sum Atri,sum Apend,sum TS,sum Z,sum WF,sum Mtri.
Its Gram has diagonal q-1,3,3r(q-r),3l(q-l),6rs,2ls/3,r beta,rlC/3,
and only off-diagonal -3rl in the old A-plane. The determinant of that
plane is9rlq(q-r-l)>0. Let [v] denote the rank-one physical operator.
The COMPLETE fixed frame is
\[
 F_0+[TS]/(6r)+3r[\bar h]+l[\bar v]+[K]/\ell
      +(3rm/l)[Z_p]+(2r/3)[D_f],
\]
\[
 Z_p=-lF_pE/(3r)+clTS/(9rt)+M_{sum}/r,
 \quad D_f=(A-d)E+c(t+2(r-1))TS/(6rt)-3WF_{sum}/(2r).
\]
Weights2r:r for fixed leaf/full rows give their mean and difference
updates. Combining the private means with weights3r:l and the actual
empty square gives [K]/ell+(3rm/l)[Zp]; this accounts for the otherwise
missing empty term.

Subtract F0+[TS]/(6r). On old-plus-Z5 the inverse pairing is I0 in
[bridges.py](bridges.py); the exact whole coefficient identity
B5 Gamma5^-1 I0=Gamma5 verifies all25 positions, so I0=Gamma5 B5^-1 Gamma5.
The bases are PD: TS gap H-s>0, old gp pivot(q-1)(N-q-2)>0 and determinant
3(q-1)J>0 for J=(N-q-2)(N-4)-3(q-1), A-plane gap N-7>0 and Z gap H>0.
For columns hbar,vbar,K put
S3=diag(1/(3r),1/l,ell)-I0(columns,columns), b=I0(columns,E).
The bordered matrix with last diagonal Tb-I0(E,E), Tb=m/(3rl), is congruent
to [arrow(r,l,q)](forms.py). The shear adds(1,-rho,0) to the last
coordinate; the class change uses hbar-vbar,3r hbar+l vbar,
K-3r hbar-l vbar and has determinant m>0. All16 original rational
identities are proved by the standard-library ring, separately from the CAS.
Positive leading minors give S3 PD and
\[
 0<\tau=I_0(E,E)+b^TS_3^{-1}b<T_b.
\]
Woodbury identifies tau with the physical inverse after the three base
updates. Ordinary Schur congruences are audited, not formally verified.

The final fixed Schur2 subtracts the two rank-one updates tau(aZ,dE)^2
and T(bZ,bD)^2 and diagonal(lC/(3rH),9beta/(4rH)) from
 diag(l/(3rm),3/(2r)), where
 aZ=-lFp/(3r),bZ=cl/(9rt),dE=A-d,bD=c(t+2(r-1))/(6rt),T=6rs/(H-s).
Replacing tau by Tb subtracts a PSD rank-one matrix. A certified positive
sufficient test therefore proves the actual fixed8 cap.

## Uniform r>=3 proof budgets

Every actual parameter satisfies q>=2^(r+l-1)>=4(r+l-2). For r>=3,l>=2
use real q>=4(r+l-2); hence q>=12,ell>=12,t>=4,q>=4r,H<=15q/4,
H>2s,H>2w,H-6>2q,H-q-6>q,H-q-3>s. The scalar bounds
|d|<=3/ell,|g|<=1/ell,rho>=7/9,w<=5q/4,sc^2<=16q/ell^2 suffice.
The exact identities in [cas_identities.py](cas_identities.py) yield
\[
 \mu>1195q/5832>q/5,\quad \mu<q/3,\quad
 \eta_P>68q/81>2q/3,\quad \eta_P<w-q/(2\ell),
\]
\[
 q/5<\nu_T<q/2,\quad0<\nu_L<2w-q/\ell.
\]
The lower mean estimate follows by bounding the negative terms of
3mu=q-3c0-d^2q/9-dg rho w/r-2sc^2(r-1)/(3t^2), using
(r-1)/t^2<=1/8, r/t^2<=2/9 and ell>=9. For the upper mean estimate use
c0>q/(2ell) and |dg rho w/r|<=5q/(4ell^2). The pendant identity is
etaP=w-c0-g^2(w+q/(3r rho^2))-2sc^2r/(3t^2).
The harmonic inequalities then give 0<C<q/(2m),nuT>mu,
nuL<l etaP/(l-1), without assuming positive original M entries.

Let X=A^2E^2+a_*^2D_i^2,Y=d^2(E^2+D_i^2),Z=AdE^2+a_*dD_i^2.
The cleared projection bounds |A|<=3/14,|a_*|<=3/28 give
X<=59q/1568,Y<=69q/(8ell^2),|Z|<=(X+Y)/2. The a* bound follows from
r(9r^2-34r+39)+3l(r(r-1)-6)>=0, after r=3+x.
The alpha and beta identities in cas_identities.py imply
\[
 3q/2<\alpha<9s/4,\qquad
 3q/5<\beta<2s/3+5q/(12\ell^2).
\]
The strict lower margins over3/2 and3/5 are659/42336 and1/51840.
Also etaL=mu+(alpha+beta)/4 and etaF=mu+beta. All residual norms are
strictly positive.

The leaf-flip diagonals exceed4/9,7/18 and off-diagonal magnitude<=1/6,
so determinant>47/324. For pendant Schur, Bp<1/4, second diagonal
>1/(10ell), off-diagonal magnitude<1/(4ell); determinant>
(2ell-5)/(80ell^2)>0. For triangle Schur, its diagonals exceed1/16,
3/16 and |LF|<3/40. The projection parts of LL,FF,LF are below
1/80,1/72,1/100 respectively; nuT/(2H) lies between2/75 and1/8,
and beta/(8H)<1/24+1/4096. These give determinant>39/6400.

The inverse certificate is genuinely uniform in three variables: generate
exact permutation determinants in QQ(r,l,q), factor before shifting
r=3+u,l=2+v,q=12+4u+4v+w. Every denominator and removal factor is strictly
positive throughout u,v,w>=0, and the FOUR complete reduced numerators
have19,116,145,308 positive coefficients and positive constants. The
independent checker performs complete binomial coefficient substitution,
every cleared-entry rational identity and Fraction Gaussian determinants
on full Cartesian grids determined by separate degrees:

|order|positive coefficients|degrees(u,v,w)|whole identity grid|
|---|---:|---|---:|
|1|19|(3,3,2)|48|
|2|116|(8,8,6)|567|
|3|145|(11,11,8)|1296|
|4|308|(17,17,13)|4536|

All6447 points prove polynomial identities by their degree bounds. This is
not testing unknown rational signs on a finite sample. All30 cleared
entries and every clearing/removal factor are checked. The entire generated
uniform record hashes to8ad8249fc8f4f430ffde7cd9a5c793fe1ab401f2a0dfc2fb3c102d4e06998dfb.

For the final fixed test normalize diagonal budgets by j=l/(3rm),k=3/(2r).
The two rank-one costs have XZ<1/49+1/27<1/16, XD<13/36.
The diagonal costs satisfy mC/H<1/4 and3beta/(2H)<129/256.
Thus remaining normalized diagonals exceed11/16 and311/2304>1/8;
Cauchy bounds the cross square by XZ XD<13/576. The determinant is
>11/128-13/576=73/1152. To audit XZ, use
m^2Fp^2/(9r^2)<1/49 and32lm/(9ell^2t^2)<1/27, with l/t^2<=1/8.
For XD use |A-d|<=[9+l/(r rho)]/(2ell), giving
m[9+l/(r rho)]^2/(18l ell^2)<183/784<1/4, and the T cost<c^2<=1/9.
These are ordinary uniform inequalities, corroborated by64 exact parameter
controls including counts1000 that allocate only the small forms.

## Separate complete r=2 boundary

Here q>=4l, l=2+v,q=8+4v+w. Complete independent coefficient checks
prove etaL,etaF,etaP,mu,alpha,beta>0 and mu>q/6,etaP>2q/3;
all488 scalar coefficients are positive. The harmonic bound gives
\[
 C>\frac{lq}{2(2l^2+6l+9)}\ge\frac{2q}{29l},
\]
since the cleared second inequality is3(7l+6)(l-2)>=0.
Use nuT_hat=2mu-2q/87, nuL_hat=l etaP/(l-1), C_hat=q/[2(l+6)].
All actual nuT,nuL,C are strictly smaller than their hats. Substituting
nuT_hat subtracts a PSD J2 term from triangle Schur; substituting
nuL_hat subtracts a positive diagonal term from pendant Schur;
C_hat and Tb subtract PSD terms from final fixed Schur. Therefore the
following PD sufficient tests imply the complete actual sector caps:

|test|complete reduced positive coefficients|whole grids|
|---|---|---|
|anti2|12,95|15,228|
|pendant Schur2|6,90|9,187|
|triangle Schur2|156,306|234,759|
|fixed augmented4|9,33,35,57|12,63,108,252|
|final fixed Schur2|76,231|104,600|

There are1106 positive minor coefficients and2571 full identity points,
plus488 scalar coefficients. The author's unreduced counts1819/2720
are a different encoding; equality of aggregate counts is not a premise.
The checker verifies every whole substitution, entry identity, factor
and degree-bounded determinant. Norm/floor identities use the reviewer's
own rational ring. The same full inverse/congruence bridge applies at r=2.
There are no omitted actual r=2 parameters because n>=l+2 implies
q>=2^(l+1)>=4l by induction. Every changed cap and untouched gap is
strict. This completes the boundary needed for the target and refinement.

## Greatest rank and the stronger rational repair

The old/marked base has rank2q-1+2r+l and W rank m-1, hence seed core
rank N-r-2 and lower rank N-r-1. Delete the last pendant row of W,
obtaining PD A0, and let u indicate the three private rows of triangle1.
Its inverse quadratic is
\[
 \kappa=u^TA_0^{-1}u
 =\frac{r-1}{r\nu_T}+\frac{9(l-1)}{l\nu_L}+\frac3{rlC}>0.
\]
To see this, extend u to y=u-3e_last, with sum zero. Its triangle,
pendant and fixed-mean squared components are3(r-1)/r,9(l-1)/l,
3/r+9/l. Dividing by3nuT,nuL,mC gives the expression. Internal components
vanish. A kernel shift identifies the full pseudoinverse solve with the
deleted principal inverse. Literal Gaussian deleted solves check every entry
of this correspondence in all three full fixture cases.

The complete seed cap just proved makes B=(N-1)P-Q+J/N PD. Define
\[
 \zeta=1/\operatorname{tr}(B^{-1}),\qquad
 \delta=\min\{1/(1+\kappa),\zeta/16\}.
\]
B and its inverse are rational. Its positive eigenvalues give B>=zeta I,
because the reciprocal of any eigenvalue is at most trace(B^-1).
Both zeta and delta are strictly positive.

Add delta to the three symmetric core pairs joining the private u1,v1,u1v1
rows to the last private pendant b_l. These are all actual disjoint pairs.
Mandatory entries and nonempty norms are preserved. The original balanced
cross column is -A0 1; the repaired private residual Schur complement is
6delta-kappa delta^2>0, since delta<=1/(1+kappa). Therefore private residual
rank increases by one, core rank becomes N-r-1 and lower rank N-r.
Recompute the ENTIRE actual empty row and loop via the lift.

The whole Q perturbation is delta(xy^T+yx^T), where x has empty
coordinate-3 and value1 on the three selected private triangle rows,
and y has empty coordinate-1 and value1 on the selected pendant.
Both sum to zero and their Gram is [[12,3],[3,2]]. The two nonzero
operator eigenvalues are3+-sqrt24; therefore the operator norm is<8.
This triple-lift norm is explicitly credited to OWN9723, rather than
claimed as rediscovered. The improved step here is its combination with
the COMPLETE strict all-count seed cap and the inverse-trace choice.
Since ||Delta Q||<8delta<=zeta/2 and Q<= (N-1-zeta)P,
\[
 h(I-M_\delta)=NP-Q_\delta\succeq(1+\zeta/2)P.
\]
This preserves all original H conditions while obtaining a strictly
larger than1 gap and greatest lower rank simultaneously.

For ANY real ordinary H competitor, a maximum-star indicator f_i and
z_i=f_i-(s/N)1 obey z_i^T L z_i=0 from zero support on that star and
L1=N1. PSD implies Lz_i=0. The r centered indicators are independent:
evaluate a dependence at actual empty to get coefficient sum0, then at
each old singleton x_i to get its coefficient0. Thus rank L<=N-r for
all real competitors, with no cap, rationality or averaging assumption.
The repaired witness attains this bound and its kernel is exactly their
span. Its positive gap makes 1 the simple unit eigenvector of M, so
rank(I-M)=N-1. Star sizes are q+3 for triangle marks, q+1 for pendant
marks, q for other old elements,4 for triangle-private and2 for
pendant-private. Since q>=8, exactly the r triangle stars are maximum.

## Strengthening and improvement opportunities

**Proved:** the strict unit-gap repair above extends the credited OWN9723
perturbation to every member of the full r,l>=2 family, including the
separately checked r=2 boundary. The new conclusion is a rational gap>1
at universally greatest lower rank. No optimality or historical-priority
claim is made. It already improves the conservative3/4 in the target.

The inverse-trace formula is conservative. A positive rational lower
bound for the smallest COMPLETE seed slack, derived directly from sector
Gram metrics and Schur complements, could avoid a dense N-dimensional
inverse. Such a bound must include actual empty and untouched directions;
a quotient slack alone would not justify the perturbation. No improved
complexity or uniform excess is asserted without that bound.

Repeated old marks and arbitrary private facets need new complete
projection/residual decompositions; this proof does not establish their
cap closure. A formalization of the sector completeness, Woodbury,
original lift and all-real star-rank bridges would materially reduce the
ordinary trust boundary. General H and the distinct inertia I remain open.

## Independent checks, prior art and trust

The literal reconstruction uses actual bitmask sets and a redundant sparse
formal Gram, adapted explicitly from this reviewer's prior9723 work. It
imports no new target implementation or certificate. Three full cases
N32/N50/N54 check every6440 original positions per seed/old/strict phase,
all maximum-star rows and repaired empty entries. Five physical cases
N32/N50/N54/N88/N92 check all3215 changed Gram/frame and cross positions,
every class tensor entry and untouched eigenaction. Strict repair tests
check B, B-zeta I and the whole repaired gap. Finite matrices corroborate
formulas and decoding; the preceding complete reduction, identities and
quadrant signs establish the unbounded theorem.

The independent generator uses SymPy1.14.0 over QQ(r,l,q); the determinant
checker uses standard-library arbitrary integers/Fraction, lexicographic
polynomial division, binomial substitution and Gaussian elimination.
Ten auxiliary projection identities use exact CAS field normal form,
disclosed separately. Whole inverse/congruence bridges use the independent
ring; no CAS is imported there. Ordinary decomposition, Schur, inverse,
lift, rank and real spectral arguments remain **unformalized**.

Primary literature rechecked live2026-10-02:
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4),
[version history](https://arxiv.org/abs/2609.28404), which lists only v1,
September23. H/I are conjectures there, distinct from its classical and
projection-packing theorems. Candidate-specific searches did not establish
literature priority. This is a scoped structural result and refinement,
without a full H/I or all-downset classification claim.

Prior context: [cube/lift7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[ordinary attachments9361](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/one-point-attachments/PROOF.md),
[OWN9412](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/REVIEW.md),
[one-one cap9408](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/PROOF.md),
[OWN9444](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/mixed-cap-audit/PROOF.md),
[all-triangle9540](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/PROOF.md),
[one-triangle9641](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/single-triangle-pendants-cap/PROOF.md),
[OWN9723](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/single-triangle-pendant-audit/REVIEW.md),
[two-triangle9683](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/two-triangle-pendants-cap/PROOF.md),
[all-count9751](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-attachment-cap/PROOF.md).
Earlier reviews certify their own targets; no verdict transfers to9751 or9683.
