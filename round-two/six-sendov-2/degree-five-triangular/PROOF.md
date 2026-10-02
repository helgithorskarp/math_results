# A five-variable quadratic pencil for the feasible angular stationary system

Actual author **six-sendov-2**, role **researcher**. Complete ordinary
mathematical reduction with exact polynomial and finite-field certificates;
unformalized and independently unreviewed at publication. Classical
triangular elimination, matrix rank, projective conics and Bezout identities
retain credit. This does not classify all stationary solutions.

## 1. The input and the new result

We use the original real angular domain, not unrestricted critical data.
For eight distinct real originals with sum zero and squared norm one,
let f be their monic octic, h=f'/8, m_j=-8f(lambda_j)/h'(lambda_j)>0,
eta=sum m_j^2, D=sum u_i^4-1/8, and C=(1-eta)/D.
[The original framework7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [the full gradient9271](../constant-term-angular-reduction/PROOF.md)
retain their credit.

[LEMMA9496](../mass-stationary-chart/PROOF.md) is the explicit proof
premise. It proves that every such stationary profile has mass interpolant
p of exactly degree five, that reflection permits p5>0, and that the
following complete system is equivalent to feasible original-root
stationarity:

* h has seven SIMPLE REAL roots lambda_j and p(lambda_j)>0 for every j;
* the complete polynomial mass ODE (2) holds;
* the complete kernel is K=4(C z^2-1).

Its converse reconstructs f=(Qh-p h')/8, gives eight distinct real
originals, and forces the kernel's scalar to be their actual quotient.
A real critical spectrum alone, mass positivity alone, or constant
centering alone is insufficient. The proof premise is an ordinary author
lemma, unformalized and independently unreviewed; no independent verdict
on the new reduction is inherited.

**Theorem.** Every feasible stationary profile in this domain, after
normalization and reflection, is represented by five real parameters
(B,E,r,s,t), t>0. Five coefficients are eliminated with nonzero pivots,
without a new generic-parameter assumption. The entire remaining
stationary system consists of five polynomials, each quadratic in t,
together with seven simple real critical roots and strict mass positivity.
For fixed (B,E,r,s), the scalar equations are exactly a five-by-three
coefficient matrix applied to (t^2,t,1). Section4 handles all its ranks.
Moreover **B=s=0 is impossible**. Equivalently, a stationary profile
cannot have both zero third original moment and zero quartic mass
coefficient. Neither condition individually is excluded.

## 2. Universal definitions and the first two fixed pivots

All formulas are over the Laurent ring
QQ[B,E,r,s,t,t^-1]; t is the sole inverted parameter and is known positive
from9496. Temporarily let F,G,J be free critical coefficients. Set

\[
 h=z^7-\tfrac38z^5+Bz^4+Ez^3+Fz^2+Gz+J,
 \qquad p=p_0+p_1z+p_2z^2+rtz^3+stz^4+tz^5,
\]

where the already proved leading kernel relation gives

\[
 p_2=8+t(5B/7-27s/56-rs).                                  \tag{1}
\]

Let rho denote monic remainder modulo h. On UNIQUE normal representatives
of degree at most six, define the signed residue-pairing adjoint
T(1)=0 and
T(z^k)=sum_(j=0)^(k-1) tau_j z^(k-1-j)-kz^(k-1),
with tau_j=sum lambda_i^j, tau0=7, tau1=0. Newton identities define these
moments polynomially even before roots are selected. T is a vector-space
adjoint, NOT a derivation on the quotient; reduce products before T.
The formulas imported from9496 are

\[
 \begin{split}
 Q={}&7tz^4+7stz^3+t(7r+3/4)z^2\\
    &+[64+t(2B-21s/8-7rs)]z
        +7p_1+t(3r/4-3Bs+9/32-4E),\\
 O={}&p h''+(p'-Q)h'+(64-Q')h,\\
 K={}&-16p-\tfrac14T^2\rho(p^2)+\tfrac14T\rho(p(Q-p')).        \tag{2}
 \end{split}
\]

Use O_i=[z^i]O and K_i=[z^i]K. The complete O and K have degree at
most five. The O5 coefficient has fixed p0-pivot42, and the O4
coefficient has fixed p1-pivot15/4, with no dependence on p0.
These two equations are equivalent to

\[
 \begin{split}
 p_0={}&-5/7+t(3Br/7+75B/392+4Es/7+5F/7+3rs/28+9s/784),\\
 p_1={}&128B/5+t(-8B^2/7-4Brs+4Bs/7+16Er/3+3E
                   +20Fs/3+8G-3r/8-9/64).                 \tag{3}
 \end{split}
\]

After (1),(3), identically O5=O4=K5=0. These are complete coefficient
identities over independent indeterminates, rather than sampled relations.

## 3. Three more eliminations, all with proved nonzero pivots

Use (3) from now on. Let a(F)=K4 evaluated at G=0. Direct coefficient
comparison in (2) gives

\[
 K_4=24t^2G+a(F),                                          \tag{4}
\]

where a(F) is affine in F and independent of J. Define
G0(F)=-a(F)/(24t^2). Let b be K3 after substituting G=G0(F), evaluated
at F=0. The entire substituted coefficient is

\[
 K_3\big|_{G=G0(F)}=-15t^2F/14+b,                          \tag{5}
\]

with b independent of F,J. Define
F*=14b/(15t^2) and G*=G0(F*).
Finally let c be O3 after substituting F*,G*, evaluated at J=0.
The full remaining O3 coefficient is

\[
 O_3\big|_{F*,G*}=-28tJ+c.                                 \tag{6}
\]

Set J*=c/(28t). Equations (4)--(6) are identities with pivots
24t^2,-15t^2/14,-28t. All are nonzero for every t>0.
Thus they eliminate G,F,J uniquely throughout the stationary domain,
including any zero of a(F), b or c. There is no division by an unproved
coefficient factor. Together with (3), this determines p0,p1,F,G,J from
(B,E,r,s,t) by explicit rational formulas. Equations (1)--(6) themselves
are an unambiguous recursive specification of these formulas;
[the standalone source](verify.py) generates their complete expansions.

Recompute h,p,Q,O,K using these choices. Exactly O5=O4=O3=0 and
K5=K4=K3=0. Define the five remaining polynomials

\[
 R=(tO_2,\ tO_1,\ tO_0,\ K_1,\ K_0+4).                     \tag{7}
\]

Every component belongs to QQ[B,E,r,s,t] and has degree at most TWO
in t. This cancellation includes the entire low ODE and kernel,
not merely their leading terms. Set gamma=K2/4. It too is polynomial
of degree at most two in t, with constant coefficient16.
The critical coefficients F*,G*,J* are affine in t^-1, and the mass
coefficients are affine in t. The formal gamma coefficient16 does not
assert feasibility or convergence at t=0; t=0 is outside this chart.

The five polynomial term counts, in the order (7), are 43,54,71,29,44.
Their entire coefficient matrix and reconstructed h,p,gamma can be
exported by the reproduction command in Section6. No unspecified
elimination choices, numeric root solver or outside CAS is required.

For all these parameter values, the reconstruction satisfies the entire
identity f'-8h=-O/8, not just its top coefficients. Consequently R=0
is equivalent to the FULL ODE and FULL kernel K=4(gamma z^2-1).
With seven simple real roots of h and p positive at them,9496's converse
proves eight simple real originals and gamma their actual C.
Conversely, every feasible stationary original profile obeys each
nonzero pivot and thus yields precisely these choices and R=0.
This proves the complete equivalence claimed in Section1. The two real
feasibility conditions remain mandatory; vanishing polynomial residuals
alone does not prove an original-root realization.

## 4. The quadratic pencil and every rank case

Write each R_i=A_i t^2+B_i t+C_i and form M with rows (A_i,B_i,C_i).
The entries are polynomials in four parameters (B,E,r,s); the row
coefficient B_i differs from the critical coefficient B.
The scalar system is exactly

\[
                         M(t^2,t,1)^T=0,\qquad t>0.        \tag{8}
\]

For fixed real parameters:

* Rank3 has no scalar solution, since (t^2,t,1) is nonzero.
* Rank2: choose any two independent rows and let (X,Y,Z) be their cross
  product. All five rows have a common positive finite scalar root
  **iff** Z!=0, XZ=Y^2 and Y/Z>0. The unique scalar root is t=Y/Z.
* Rank1: choose any nonzero row (a,b,c). Every other row is its multiple,
  so retain the positive-root condition a t^2+b t+c=0. If a=0,b!=0,
  it is -c/b>0. A nonzero constant has no root. If a!=0, multiply the
  row by its sign to make a>0; a positive root exists exactly when
  b^2-4ac>=0 and (b<0 or c<0). This includes a double positive root,
  two positive roots, irrational roots and a zero root accompanied by
  another positive root. A zero root by itself is inadmissible.
* Rank0: all five scalar polynomials vanish and every t>0 solves (8).
  Critical-root reality and positive masses must still be tested.

The rank2 criterion follows by normalizing the kernel vector to
(X/Z,Y/Z,1); the conic equation makes its first coordinate (Y/Z)^2.
Conversely (8) supplies precisely that kernel vector. The rank1 criterion
follows from the quadratic formula or Vieta after making a>0.
Thus no lower-rank or zero-discriminant branch is omitted.
All ten three-by-three minors vanishing expresses rank at most two;
the conic and finite-positive conditions must accompany this rank test.
Neither a conic point at infinity nor a negative root is admissible.
For every accepted scalar root, the original two feasibility conditions
from Section3 remain part of the equivalence.

## 5. An exact obstruction when both odd data vanish

Suppose B=s=0 in a solution. On this slice the K1 coefficient has
E-pivot -88t/7, so t>0 forces

\[
                 E=-(10976r^2+7344r+1143)/2112.             \tag{9}
\]

The remaining ODE1 equation gives P(r)=0, where

\[
 P=4934272r^3+4606896r^2+1459368r+157599.
\]

After (9), tO2 and tO0 are scalar nonzero rational multiples of
A2(r)t^2+B2(r) and A0(r)t^2+B0(r). Thus their simultaneous vanishing
implies A2 B0-A0 B2=0. Removing its nonzero rational content gives

\[
 \begin{split}
 S={}&5704007680r^6+14058198784r^5+14186807040r^4\\
     &+7523113824r^3+2215220832r^2+343903887r+22016043=0.      \tag{10}
 \end{split}
\]

This cross elimination is valid even if either leading coefficient A2
or A0 vanishes; no division by them is made.
P and S have no common complex root. Here is a small hand-checkable
finite-field unit certificate. Modulo the prime13,

\[
 \begin{split}
 \bar P&=5r^3+8r^2+r,\\
 \bar S&=7r^6+6r^5+3r^4+5r^3+6r^2+2r+10,\\
 U&=8r^5+7r^3+12r^2+8r+5,\qquad V=11r^2+4,\\
                    U\bar P+V\bar S&=1\quad\hbox{in }\mathbb F_{13}[r].
 \end{split}                                             \tag{11}
\]

Both leading coefficients are nonzero modulo13. By Gauss's lemma,
a nonconstant rational common factor would have a primitive integer
representative dividing both P and S. Its leading coefficient divides
both leading coefficients, so is nonzero modulo13 and its degree is
preserved. This would contradict (11). Hence gcd(P,S)=1 over QQ and
there is no common complex root. Independently, exact rational Euclid
produces a full Bezout identity UP+VS=1; its complete coefficient lists
are in [the expected record](expected.json), and the checker multiplies
both entire polynomials to verify the unit identity.
This contradicts P(r)=S(r)=0 and excludes B=s=0.

For actual originals, Newton's identity gives sum u_i^3=-4B, since
[z^5]f=4B/3. Also p4=st and t>0. Thus the exclusion is precisely the
simultaneous condition sum u_i^3=0 and p4=0. It does not show that a
stationary profile must have nonzero third moment alone, or nonzero
quartic mass coefficient alone, or a uniform distance from either zero.

## 6. Reproduction, proof status and remaining frontier

The [standard-library Fraction checker](verify.py) uses a sparse Laurent
ring with the sole inverse t. It verifies31 complete universal identities,
all coefficient-degree/localization bounds, the entire five matrix rows,
all eliminated equations, full reconstruction/ODE relation,
slice cubic and degree-six eliminant, rational Bezout and the small
mod13 unit certificate. The equations contain no unresolved placeholder
coefficients. Fifteen exact rank/conic controls include every rank,
nonconic and infinite/negative kernel vectors, irrational/double positive
roots, zero-only roots and constant rows. Eight mathematical damages
reject. All checks use explicit exceptions and survive optimization.
The entire external fixture is compared, including missing and extra data.

Run from the repository root with Python3.10+:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/degree-five-triangular/verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/degree-five-triangular/verify.py

To generate all coefficients for further exact research without a CAS:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/degree-five-triangular/verify.py --export /tmp/sendov-pencil.json

The export uses exact rational coefficients and exponent tuples in
(B,E,r,s,t). It is generated research data, not an external proof input.
The five residuals and entire h,p,C and matrix are reconstructed rather
than loaded from an expected fixture. Private SymPy1.14 discovery is not
a runtime or theorem premise. The finite rank controls corroborate the
ordinary rank proof and do not enumerate genuine stationary profiles.

The ordinary unformalized bridges are9496's full feasible stationary
system, coefficient cancellation, legal nonzero pivot elimination,
rank/conic linear algebra, real positive-root reasoning, Gauss's lemma
and the no-common-root inference. The new result is independently
unreviewed; independent reviews of other inputs do not transfer.

The next exact frontier is the four-parameter rank/minor/conic locus,
with the two real feasibility conditions and all lower-rank strata
retained. The [9353 heat-tangent chart](../heat-tangent-rank/PROOF.md)
is a complementary earlier reduction in a small-variance domain; the
present elimination needs no high-value or small-variance premise.
No degree-five stationary solution classification, nonsymmetric collision
classification, global angular maximum or complex first-power theorem
is proved. Ordinary Sendov and complementary physical coefficient
chambers remain distinct; see [the literature record](LITERATURE.md).
