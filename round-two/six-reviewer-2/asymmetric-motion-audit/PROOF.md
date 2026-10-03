# Exact actual-family audit and an open repair region

Actual **six-reviewer-2**, role **independent mathematical reviewer**, pass39,
2026-10-03. Ordinary proof with two fresh exact computational checks; unformalized.
The complete written claim10006 was visible. This is not a blind review.

## Definitions and the actual polynomial

Put c=cos(pi/9), d=2c²−1, y=1/[3(1+c)], x=2/3−y,
C=8/3+y, lambda=12(1+c), k=−7(1+2c)/18 and g=48k.
For independent real M,beta and real s define

m=−x lambda s²+i g s³+M s⁴,
nu_L=7i s+42k s²+7i beta s³,
nu_S=−i s−6k s²−i beta s³,
zeta_L=m+nu_L, zeta_S=m+nu_S, a=1−lambda s².

These are actual polynomials in s. Set

H_s(z)=(z−zeta_S)^9−(9/8)(zeta_L−zeta_S)(z−zeta_S)^8,
p_s(z)=H_s(z)−H_s(a).

Differentiation gives p_s'=9(z−zeta_L)(z−zeta_S)^7. Thus p_s is
monic of degree nine, p_s(a)=0, and its entire eight-critical multiset
is zeta_L once and zeta_S seven times. Their difference is 8i s+O(s²),
so they are distinct for every sufficiently small positive s. No
hypothetical original zeros or unintegrated critical profile is substituted.
At s=0 the full polynomial is z^9−1.

## Full polynomial and original-root jets

Write m2=−x lambda and omega=exp(2pi i j/9). Through order four,
p_s=z^9−1+s²P2+s³P3+s⁴P4+O(s⁵), where

P2=9lambda−9m2(z^8−1)+36(z^7−1),

P3=−9i g(z^8−1)−432i k(z^7−1)+168i(z^6−1),

P4=−36lambda²+lambda(−72m2+252)−9M(z^8−1)
 +(36m2²−1296k²+72beta)(z^7−1)
 +(−252m2+3024k)(z^6−1)−378(z^5−1).

Both implementations retain all ten z-coefficients, all five s-orders,
all twelve rational field coordinates, and all three affine columns
(1,M,beta), including zeros. The primary uses the closed H above in
QQ[T]/(T^12−T^6+1), T=exp(pi i/18). The second directly multiplies the
eight critical linear factors, integrates every coefficient, and anchors
by full Horner evaluation, in QQ[W,I]/(W^6+W^3+1,I²+1).
The bridge T=I W^7, W=T^4 and I=T^9 has rational matrix rank twelve.
It loses no field coefficient and respects complex conjugation.

Since every root of z^9−1 is simple, the analytic implicit-function theorem
supplies nine unique local branches Z_j(s) with Z_j(0)=omega_j. Their
Taylor coefficients are uniquely determined by the root equation. They are

Z=omega+s²L+s³U+s⁴V+O(s⁵),
L=lambda(−omega/3−x−y/omega),
U=i g(1+omega^−1−2omega)−(56i/3)(omega^−2−omega),
V=−[P4(omega)+P2'(omega)L+36omega^7 L²]/(9omega^8).

The second checker substitutes EVERY complete branch into EVERY polynomial
coefficient and checks p_s(Z)=0 through order four, rather than sharing this
recurrence. It separately computes the full product Z conjugate(Z),
including |L|²/2 in the fourth half-normal. Original jets are corroborating
finite identities; analytic branch existence and the remainder estimates
are ordinary arguments, not assertions of a formal-series checker.

Take a common small interval where these nine branches exist and lie in
nine disjoint neighborhoods. Their nine zeros exhaust the degree, all are
simple, and the marked branch is Z_0=a by uniqueness and p_s(a)=0.
There are no other uncounted original zeros.

## Every physical disk constraint and a positive collar

For N_j=(|Z_j|²−1)/2, the second coefficient is

N_j^(2)=−2lambda y(cos(theta_j)+1/2)(cos(theta_j)+c).

It vanishes exactly at j=3,4,5,6. At j=0,1,2 the two factors are positive;
at j=7,8 they are the same positive factors as at j=2,1. Thus ALL five
other originals have strictly negative second half-normal. The third
coefficient is

g sin(theta_j)+48k sin(2theta_j)−(56/3)sin(3theta_j).

It is individually ZERO at all four active labels, as checked exactly in
both field descriptions. Averaging a nonzero opposing pair would not suffice.
The full fourth coefficients at j=3 and4 are

n3=−(431+320c+320c²)/3−(3/2)M+12beta,

n4=−(1636+2842c+1980c²)/9−(1+c)M+8(1−d)beta.

For every real s, p_−s(z)=conjugate(p_s(conjugate(z))). Branch uniqueness
gives Z_j(−s)=conjugate(Z_(9−j)(s)); consequently the fourth coefficients
at j=6 and5 are n3 and n4, respectively. Full jet parity is checked for
all nine labels. This uses the actual family, not a presumed conjugate-root
configuration at positive s.

The displayed target choices are

M*=−(512+1684c+1328c²)/9,
beta*=(86−261c−172c²)/18.

Both full affine equations give n3=n4=−1. Every active half-normal is
therefore −s⁴+O(s⁵), and every inactive half-normal is a strictly negative
constant times s²+O(s³). For each of the finitely many branches, the leading
negative term dominates its remainder on a positive interval. Intersect
all nine intervals with the branch/counting and critical-distinctness
intervals. This yields strict unit-disk feasibility for EVERY positive s
in a common interval, with all nine originals simple. In particular it is
not just a sequence of feasible numerical parameters.

## Full first-power objective and both cuts

For the entire multiplicity-counted first-power objective,

F=|a−zeta_L|^−1+7|a−zeta_S|^−1,

both denominators tend to one. Their positive square roots and inverses
are real analytic near s=0. The actual conjugate parity makes F even,
so its fourth-order jet has remainder O(s⁶), not merely O(s⁵).
The primary expands the full inverse-square-root binomial series. The
second solves D u²=1 coefficient by coefficient with u(0)=1 for each
actual squared distance, independently, before weighting by1 and7.
For eta=lambda s² and the target parameters they give

F=8+C eta+K* eta²+O(eta³),
K*=(19935+47482c−62948c²)/972.

The physical branch c is the root of8c³−6c−1 in (sqrt(3)/2,1).
The cubic is strictly increasing there, and its signs at15/16,47/50
are −17/512 and73/15625. Hence15/16<c<47/50.
K* decreases on that bracket, and

9<5592017/607500<K*<194645/20736<10.

Also C<3 since y<1/3. Positivity of3−C and10−K*, together with the
analytic remainder, gives BOTH F<=8+3eta and F<=8+Ceta+10eta²
for every sufficiently small eta>0. Set epsilon=10eta. Intersect this
collar with the already proved disk collar and0<eta<=1/12000.
There exists eta0 in (0,1/12000] for which EVERY0<eta<eta0 satisfies
all claims. This supplies no explicit width or feasibility at eta=1/12000.

## The motion obstruction and exact quantifiers

Set B_j=omega_j+eta(−omega_j/3−x−y/omega_j).
At BOTH cube labels3 and6, the cubic jet reduces to

U_j=−3i g omega_j=56i(1+2c)omega_j.

The quartic root term is O(eta²), so

(Z_j−B_j)/eta^(3/2) -> i A omega_j,
A=56(1+2c)/[12(1+c)]^(3/2)>0.

For epsilon=10eta retain the original physical defect
Delta=epsilon eta+192eta²=202eta². Therefore

|Z_j−B_j|/Delta -> infinity,
|Z_j−B_j|/sqrt(eta Delta) -> A/sqrt(202)>0.

A bound uniform on the two-cut class of the form K Delta is impossible.
So is K Delta+o(sqrt(eta Delta)) with the little-o uniform as eta->0.
No uniform O(eta^q), q>3/2, can bound these same canonical errors.
The quantifier permits epsilon to vary with eta; this family does not
supply the same obstruction at fixed strictly positive epsilon.
Distinct limiting omega_j force any labeling whose canonical error tends
to zero to agree with these labels for small eta. The real positive marked
a fixes the rotation. Neither relabeling nor an unused rotation removes
this tangency.

The construction and these limits use no numerical graph theorem. Calling
the square-root exponent sufficient as well as necessary is explicitly
RELATIVE to the already published9954 upper estimate and its actual-entry
premise: (19/2)Delta+(7/2)sqrt(eta Delta) for all originals under BOTH cuts
on0<eta<=1/12000. The scoped9988 review confirms that upper chain only;
its verdict is not transported to the new family. We keep192 and202,
not its separate190 refinement. No optimal universal constant follows.

## Proved open repair region and its infimum

Keep lambda,k,g and m2 fixed, while allowing arbitrary real M,beta.
Define q3=−n3 and q4=−n4. The normal-row determinant is
12(c+d)>0, so these are affine coordinates on the entire repair plane.
The objective's fourth coefficient in s is affine with columns8M−56beta;
let K(M,beta) denote that coefficient divided by lambda².
Put

w4=1/(c+d)=−2/3+4c/3,
w3=(2/3)[7−(1−d)/(c+d)]=52/9−4c/9−8c²/9.

Both are positive: c,d>0 and0<(1−d)/(c+d)<1 from the isolated c bracket.
Exactly (3/2)w3+(1+c)w4=8 and12w3+8(1−d)w4=56.
Thus the full affine dual identity is

K(M,beta)=Kinf+(w3 q3+w4 q4)/lambda²,
Kinf=6653/324+23915c/486−15839c²/243.

Both implementations check ALL affine columns, including the two
zero parameter columns on the right constant after cancellation.
The intersection q3=q4=0 occurs at

M0=M*−(1+2d)/[3(c+d)],
beta0=beta*+(2c−1)/[24(c+d)].

The COMPLETE OPEN region of STRICT fourth-order inward repairs with
second objective coefficient strictly below10 is

q3>0, q4>0, w3 q3+w4 q4<lambda²(10−Kinf).

For EACH fixed point in this open simplex, repeat the nine-branch argument:
four active half-normals have negative fourth coefficients, the other
five already have negative second coefficients, the objective has K<10,
and C<3. Thus the actual family has a positive collar under BOTH cuts
with epsilon=10eta, and has the SAME nonzero cube motion constant A.
This is a family of actual feasible constructions, not just feasible jets.
No uniform collar over an unbounded parameter set is asserted.

Kinf is the infimum over this strict repair region. It is approached by
q3=q4=kappa>0 tending to zero, with
M=M0−kappa(M0−M*), beta=beta0−kappa(beta0−beta*).
The independent checker includes kappa=1/2,1,2 and proves9<K<10
for every one. A common rational enclosure follows from the closed K*
bounds above and0<(w3+w4)/lambda²<(16/3)/[12(31/16)]².
The region is nonempty and these are three distinct valid parameter choices.
The boundary q3=0 or q4=0 requires a higher-order physical analysis;
we do not claim actual feasibility or nonexistence there, or attainment of
Kinf. This is not an optimum over all critical profiles or all polynomials.
The previously published6+2 analytic minimizer is a different stronger-budget
problem. We credit the earlier dual weights and quartic chart methods;
this refinement specializes and classifies the present strict1+7 repair plane.
