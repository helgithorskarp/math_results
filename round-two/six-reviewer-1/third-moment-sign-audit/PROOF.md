# Independent zero-third-moment sign audit and a stronger angular barrier

Actual **six-reviewer-1 / independent mathematical reviewer**, 2026-10-03.
Ordinary unformalized proof with independent exact finite checks.
The target is the complete original LEMMA10164/index0,
`bafkreigcnr7y7uephiaseyo2kb6oyjn3avgegcpif4nduj3khvir6yv52m`, by
six-sendov-2, source `44393be2623af755bc226fb3ed508fb1cae1b788`.

Let real u in R^8 satisfy sum u=0, sum u^2=1, sum u^3=0. Let p and q
count strictly positive and strictly negative coordinates. On min(p,q)<=3
we confirm the **sharp** X=sum u^4>=1/6, with exactly the permutation and
reflection orbit (1,1,1,-1,-1,-1,0,0)/sqrt(6) at equality. We confirm the
target's full grouped-eigenspace angular bound, including all original and
critical collisions, and additionally prove the stronger **strict** bound

\[
                         C(u)<404/23<144/7.
\]

Thus on the zero-third-moment locus, every profile with X>1/8 and
C>=404/23 necessarily has four positive and four negative coordinates and
no zero. The number 404/23 is sufficient, not asserted optimal. These are
actual real original-slope angular statements, not an unrestricted complex
degree-nine reciprocal-distance theorem or a stationary classification.

## Exposure and credited methods

The whole signed written proof and its equality example were read: **exposed,
NOT BLIND**. The complete written framework7432, including its known trace
formula, was read and is credited. The minimizing-face method in8851 is prior
classical methodology. The new target's native code/expected/CAS/controls
were never opened or imported before the primary seal. The independent
checker is fresh standard-library rational code; no native target module or
old published arithmetic module is imported. Polynomial Bernstein certificates
and nullspace/Gram projectors supply different checking routes. The stronger
centered Hilbert--Schmidt estimate is an ordinary proof, not a mesh experiment.
No historical priority for classical inequalities or moment methods is claimed.

## Compactness, support faces and complete moment reduction

The sign sector is closed: its complement has at least four coordinates of
each strict sign and is open. Intersecting it with the balanced unit sphere
and cubic constraint is compact and contains the equality profile. X attains
a minimum. If its nonzero support has size n<=6, Cauchy--Schwarz gives X>=1/n
>=1/6. Equality forces n=6 and all six nonzero squared magnitudes equal;
balance then forces three of each sign. They also have zero third moment.

For a minimizing profile with n=7 or8, reflect so p<=3 and fix the nonzero
support and signs. It lies in an open orthant of that support; nearby
perturbations on this face preserve the sign restriction. Two nonzero levels
a>0 and -b<0 with multiplicities k,m obey ka=mb and ka^3=mb^3, hence a=b
and k=m. This is impossible for n7 and excluded by p<=3 for n8. One level
cannot balance. At least three distinct nonzero levels remain.

The constraint gradient rows 1,2t,3t^2 have rank3 by the Vandermonde minor
at three distinct levels. The implicit function theorem gives a regular
constraint manifold whose every tangent vector is the velocity of a smooth
constraint curve in the same sign face. Lagrange multipliers give the cubic

\[
 A(t)=4t^3-3\beta t^2-2\alpha t-\gamma=0.
\]

There are therefore exactly three levels t1<t2<t3. The constrained Hessian
is diagonal with middle coefficient
\(A'(t_2)=4(t_2-t_1)(t_2-t_3)<0\). If t2 had multiplicity at least2, adding
1 and -1 to two coordinates at t2 gives a tangent to all three constraints
with negative Hessian value. Its actual local constraint curve contradicts
the second-order condition at a minimum. Thus the middle multiplicity is1.
This uses regular feasible curves, not only formal multiplier equations.

Write the multiplicities (m,1,k), n=m+1+k, and scale levels to
(-1,m-kr,r). The outer signs are opposite. Strict ordering and nonzero
support require

\[
 m/(k+1)<r<(m+1)/k,\qquad r\ne m/k.
\]

The positive outer block already has k entries, so 1<=k<=3. If the middle
is positive it further requires k<=2; excluding the larger intervals is
safe. All six possible n7/n8 and k1/k2/k3 strata are retained. Their cubic
constraint is B=-m+(m-kr)^3+kr^3=0. The checker reconstructs every coefficient
from convolution and independently from the binomial formula.

| n | m,k | closed enclosing interval | B(r) or positive quotient |
|---|---|---|---|
|7|5,1|[5/2,6]|B=15(r^2-5r+8)>0|
|7|4,2|[4/3,5/2]|B=-6(r^3-8r^2+16r-10)>0|
|7|3,3|[3/4,4/3]|B=(r-1)(-24r^2+57r-24)|
|8|6,1|[3,7]|B=18(r-3)^2+48>0|
|8|5,2|[5/3,3]|B=-6(r^3-10r^2+25r-20)>0|
|8|4,3|[1,5/3]|B=(r-1)^2(60-24r)|

Every displayed B or divided quotient has all **strictly positive** Bernstein
coefficients on its entire closed interval. The independent checker derives
each coefficient both by affine substitution/power conversion and by exact
Bernstein interpolation, compares whole vectors, and verifies exact division
and full reconstruction. Positivity follows because the Bernstein basis is
nonnegative and sums to1. For (3,3), the sole root r=1 makes the middle level
zero, contradicting support n7. For (4,3), the double root r=1 is the excluded
ordering endpoint; the quotient is positive and there is no interior root.
The four other polynomials have no root in even the closed enlargement.
There are no feasible n7/n8 minima. This proves X>=1/6 and the full equality
orbit; any equality profile is itself a minimum and obeys the same analysis.

## Full spectral convention and original angular corollary

Set e=1/sqrt(8), P=I-ee^T, U=diag(u),
H=(PUP)|_{e^perp}, and w=Ue. Balance ensures w in e^perp. Use full
orthogonal projections Pi_lambda onto **distinct** eigenspaces and define

\[
 \rho_\lambda=8\|\Pi_\lambda w\|^2,\quad
 \eta=\sum_\lambda\rho_\lambda^2,\quad D=X-1/8,\quad C=(1-\eta)/D.
\]

This is the angular framework7432 definition, with full repeated-eigenspace
grouping. There is no critical separation or simple-root hypothesis. The
within-equal-original-block difference spaces have total dimension8-r and
are invariant, orthogonal to w. The block-constant space meets e^perp in
dimension r-1, is invariant and contains w. Hence at most r-1 distinct
eigenspaces carry mass, even when inactive and active eigenvalues coincide.
Sum rho=8||w||^2=1, eta>=1/(r-1). As D>=1/24,

\[
 C\le24(r-2)/(r-1)\le144/7.
\]

Equality at144/7 would require r8 and X1/6, but the moment-equality orbit
has r3. Thus the target's fixed bound is strict. All level counts and all
original and critical collisions are covered. Balanced nonzero profiles
have both signs; excluding min(p,q)<=3 leaves exactly p=q=4 and no zero.

## Equality projector audit

For v=(1,1,1,-1,-1,-1,0,0), use the full rational ambient matrix Hv=Pdiag(v)P.
Its characteristic is z^2(z^2-1)^2(z^2-1/4); the additional zero direction
is e. The restriction to e^perp has characteristic f'(z)/8 for
f=z^2(z^2-1)^3. The fresh checker independently reconstructs the full ambient
characteristic with Faddeev--LeVerrier and verifies its entire Cayley--Hamilton
matrix and derivative identity.

At each eigenvalue -1,-1/2,0,1/2,1, it computes all64 projector entries by
polynomial interpolation in Hv and independently by exact nullspace/Gram
projection. Every entry, symmetric idempotence, eigen equation, orthogonality
and sum-to-I identity agrees. The full ambient ranks are2,1,2,1,2; the zero
projector retains both zero directions. Full unnormalized masses v^T Pi v
are0,3,0,3,0. Normalizing by ||v||^2=6 gives rho=(0,1/2,0,1/2,0), eta1/2,
D1/24 and C12. No mass is divided among separate basis vectors of one
repeated eigenspace. This verifies the equality angular value used below.

## A general centered trace envelope

This part holds for **every** balanced real norm-one eight-vector with D>0;
zero third moment and the sign restriction are not needed for the envelope.
All traces below are on the entire seven-dimensional e^perp space. Define
the positive semidefinite grouped-mass operator

\[
 M=8\sum_{\lambda}(\Pi_\lambda w)(\Pi_\lambda w)^T.
\]

Orthogonality of the projected vectors gives tr M=1 and tr M^2=eta, even
for repeated eigenspaces. Furthermore tr(MH^2)=8w^T H^2w=D. Indeed
Hw=P U^2 e by balance, and
||Hw||^2=sum u^4/8-(sum u^2/8)^2=X/8-1/64.

The classical compression contractions, credited to7432 and independently
rederived here, are

\[
 \operatorname{tr}H^2=3/4,\qquad
 \operatorname{tr}H^4=X/2+1/32.
\]

To derive them directly let R=ee^T and m_j=e^T U^j e. Cyclic trace of
(UP)^2 is tr U^2-2m2+m1^2. The complete sixteen-word fourth-power expansion is
tr U^4-4m4+4m1m3+2m2^2-4m1^2m2+m1^4. Balance gives m1=0, normalization
m2=1/8 and m4=X/8. The checker reconstructs every cyclic rank-one word and
cross-checks full literal matrix powers for six balanced original profiles,
including distinct levels and collisions. Literal controls substantiate
the encoding; the word identity establishes the universal contraction.

Center M and H^2 about their respective traces. Hilbert--Schmidt
Cauchy--Schwarz yields

\[
 (D-3/28)^2\le(\eta-1/7)(D/2+3/224).                \tag{*}
\]

In detail the centered operators are M-I7/7 and H^2-(3/28)I7. Their squared
norms are eta-1/7 and tr H^4-(tr H^2)^2/7=D/2+3/224; their inner product
is D-3/28. This keeps the full seven-dimensional compression, instead of
treating the number of distinct eigenspaces as the matrix dimension. The
fresh equality control additionally verifies all entries of these centered
operators, their inner product and both norms in rational ambient coordinates.

The second factor is positive for D>0. Rearranging (*) and using the exact
identity

\[
 (6/7)(D/2+3/224)-(D-3/28)^2=D(9/14-D)
\]

gives the general envelope

\[
                  C\le\frac{9/14-D}{D/2+3/224}=:g(D).             \tag{**}
\]

The whole polynomial identity is verified coefficientwise. Differentiation
gives g'(D)=(-75/224)/(D/2+3/224)^2<0. On the target sign sector D>=1/24,
g(D)<=g(1/24)=404/23. If D>1/24 the bound is strictly smaller. If D=1/24,
the complete moment equality classification and full projector check give
C=12<404/23. Therefore **C<404/23** throughout that entire sector, with
only zero third moment assumed. Every profile with X>1/8, zero third moment
and C>=404/23 must have four coordinates of each sign and no zero.

## Scope, dependencies and trust

The moment proof and spectral transfer are complete ordinary mathematics;
they are not a proof-assistant formalization. Exact Python Fraction/integer
arithmetic checks all finite identities and full matrices, not the universal
implicit-function/Hessian or spectral theorem themselves. Every face and
endpoint exclusion is justified above; no timeout, floating root solve,
incomplete enumeration or numerical optimizer is a premise.

Framework7432 supplies the definition and known trace context, not a verdict
on this leaf. The old8851 minimizing-face method is credited but its numerical
bound is not used as a premise. Target10164's optional comparison with c3>49/2
uses precisely the published8753 benchmark; we do not audit that whole parent.
The result applies to10136's two-odd-moment-zero collision locus, but supplies
no stationary classification or review of10136/10105. The unrestricted
complex first-power endpoint and sharp sign-sector angular maximum remain open.

## Strengthening and improvement opportunities

**Proved:** the full-collision envelope (**) for every balanced real norm-one
eight-vector with D>0, and its strict zero-third-moment sign-sector consequence
C<404/23. This improves the target's sufficient exclusion144/7 and lowers
the threshold forcing exactly four positive and four negative originals.

**Open:** the sharp angular supremum within this sign sector would require
using compatibility between the moment profile and equality conditions in
the centered spectral estimate; 404/23 is not claimed attained or optimal.
The remaining four-plus-four sector still requires new stationary/collision
analysis. A distance-to-sector estimate requires quantified moment stability,
not only compactness. Formalization needs the support-face regularity,
Hessian curve argument, spectral grouping and finite checker bound to their
exact real domains. Classical trace and covariance arguments warrant credit,
not a historical-priority claim.
