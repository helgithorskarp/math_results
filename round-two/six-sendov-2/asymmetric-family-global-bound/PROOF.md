# Sharp angular ratio on the full asymmetric3+3+1+1 family

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with a standalone exact algebraic
certificate. Unformalized; independent review of this extension is
pending. The precise prerequisite is the continuous ratio extension
and sharp three-level theorem in
[graph8753](../angular-three-level-transition/PROOF.md), source
`6efce877eb9dcde6e12b6a90930d65382b29dd89`; its independent review was
pending at this pass's initial refresh. No unpublished peer result is used.

## 1. Statement and scope

For balanced norm-one real slopes theta, let
\[
 e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
 H=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
 w=\operatorname{diag}(\theta)e,
\]
\[
 X=\sum\theta_j^4,\quad
 \eta=64\sum_{\lambda\ {\rm distinct}}\|\Pi_\lambda w\|^4,
 \qquad C(\theta)=\frac{1-\eta}{X-1/8}.
\]
The projections are onto full eigenspaces. At the uniform4+4 orbit,
where the denominator vanishes, use the proved continuous extension16
from8753.

Let \(\mathcal F\) consist of normalizations, permutations and sign
changes of
\[
 u=(c+x,c+x,c+x,c-x,c-x,c-x,-3c+y,-3c-y),                 \tag{1}
\]
where \(c,x,y\in\mathbb R\) and \(N=\sum u_j^2>0\).
This is the entire family with two original triple blocks and two
singletons, including its coincidences and boundary strata. Any
balanced such profile has representation (1), because the singleton
pair's center must be minus three times the triple-pair center.

Let alpha be the unique root near -0.853410556973737 of
\[
 4575t^4+11695t^3+11175t^2+4737t+746=0,
\]
with the exact isolation interval from8753, and set
\[
 c_3=\frac{8(\alpha-1)^2(5\alpha+3)^2}
 {(15\alpha^2+24\alpha+10)(35\alpha^2+38\alpha+11)}.
\]
Thus \(24.53389668<c_3<24.53389670\), and \(c_3>49/2\).

**Theorem.** On the full family \(\mathcal F\),
\[
                      \boxed{C(\theta)\le c_3.}         \tag{2}
\]
Equality consists exactly of permutations and sign changes of the
normalization of
\[
                   (\alpha,\alpha,\alpha,\alpha,1,1,1,-4\alpha-3).
\tag{3}
\]
In particular the family constant is sharp, and every genuinely
four-distinct-level member satisfies a strict inequality in (2).
There is no uniform positive gap for all four-level members, since
they can approach (3). The strict local quadratic stability of this
orbit on the full sphere is already in8753.

This theorem does **not** establish the all-sphere inequality
\(C\le c_3\), the equality \(C_*=c_3\), a support reduction for
other multiplicity patterns, or the finite-energy first-power
Tang--Zhang endpoint. Its new scope is the full two-dimensional
asymmetric family, rather than a symmetric one-parameter slice or
the three-level collision locus.

## 2. Universal rational formula and the parameter domain

By block exchanges and overall reflection we can assume
\(c,x,y\ge0\). Set
\[
                 \kappa=c^2,\quad U=x^2,\quad V=y^2.
\]
The letter kappa is a shape parameter, not the angular ratio C.
The pair moment expansions give
\[
 N=24\kappa+6U+2V,\quad
 S_3=c[18(U-V)-48\kappa],
\]
\[
 S_4=168\kappa^2+36\kappa U+108\kappa V+6U^2+2V^2,
\]
\[
 \mu_2=S_4-N^2/8=96\kappa(\kappa+V)+\tfrac32(U-V)^2.
\tag{4}
\]
For \(A=(z-c)^2-U\), \(B=(z+3c)^2-V\),
\[
 f=A^3B,\quad g=f'/8=A^2h,
\]
\[
 h=z^3+4cz^2+[\kappa-(U+3V)/4]z-6c^3+\tfrac34c(V-U).
\tag{5}
\]
The usual cofactor identity identifies g as the compression
characteristic polynomial. The two repeated triple-block eigenspaces
have zero coupling. If h has three distinct roots, their possibly
zero masses rho are determined by
\[
 \sum\rho=N,\quad \sum\rho\lambda=S_3,\quad
 \sum\rho\lambda^2=\mu_2.
\]
Let \(p_j\) be the root power sums of h, with \(p_0=3\), and put
\[
 G=(p_{i+j})_{i,j=0}^2,\quad
 \mu=(N,S_3,\mu_2)^T,\quad D=\det G,\quad
 E=\mu^T\operatorname{adj}(G)\mu.
\]
The Vandermonde argument gives \(\eta_u=E/D\) and
\(C=(N^2-\eta_u)/\mu_2\). Zero masses are valid when a displayed
h root belongs to an inactive original-level eigenspace; no arbitrary
splitting of a repeated eigenspace is made.

Define the homogeneous polynomials
\[
 M=64\kappa^2+64\kappa V+(U-V)^2,
\]
\[
 \begin{split}
 \Delta={}&2304\kappa^3-32\kappa^2U+6624\kappa^2V
             -23\kappa U^2+942\kappa UV-855\kappa V^2+(U+3V)^3,\\
 \mathrm{Num}={}&\tfrac{32}{3}(N^2D-E),\qquad
 \mathrm{Den}=M\Delta.
 \end{split}                                               \tag{6}
\]
Exact universal polynomial identities are
\[
 D=\Delta/16,\quad \mu_2=3M/2,\quad
          \boxed{C=\mathrm{Num}/\mathrm{Den}.}             \tag{7}
\]
Num is a degree-five polynomial with integer coefficients. Its21
coefficients are explicitly listed in `NUM_TERMS` in the checker;
equation (6) also defines it independently by a3x3 determinant.
The checker expands the actual pair moments, verifies (5), derives
the power sums by Newton identities and expands every cofactor.
It checks separately
\(32(N^2D-E)=3\mathrm{Num}\) and
\(32\mu_2D=3\mathrm{Den}\) in the complete sparse polynomial ring,
so this is a universal identity, not agreement on sampled parameters.

For interior \(\kappa,U,V>0\), \(\mu_2>0\), and h has three
distinct real roots. If A and B have no common root there are four
distinct original levels and three simple gap roots. If they have
one common root there are three original levels, two simple gap roots
and one inactive original-level root in h, all distinct. They cannot
have both roots in common when c>0 because their centers differ.
Thus \(D>0\) and \(\mathrm{Den}>0\) throughout the interior,
including its original-level collision locus. Formula (7) is analytic
there.

Because C is homogeneous of degree zero, impose N=1. The parameter
triangle \(24\kappa+6U+2V=1\), \(\kappa,U,V\ge0\), is compact.
Its square-root map to normalized profiles is continuous, and the
inherited continuous extension of C makes its maximum attained.
No division by a determinant on a singular boundary is needed.

## 3. Every cone boundary is below c_3

On U=0 the original levels have multiplicities6+1+1; on V=0 they
have multiplicities3+3+2. These and their coincidences are at most
three-level profiles. The partition-specific estimates in8753 put
their C values at most16, including uniform extensions if applicable.

On kappa=0 the homogeneous ratio from (7) cancels to
\[
 C=\frac{4(3U^3+67U^2V+177UV^2+9V^3)}{(U+3V)^3}
    =\frac{208}{9}-\frac{4(5U-21V)^2}{9(U+3V)^2}
    \le\frac{208}{9}.                                  \tag{8}
\]
When U=V>0 the displayed value is16, matching the uniform extension.
At endpoints the same continuous formula applies. The denominator
U+3V is positive except at the excluded zero profile.
The checker verifies the cancellations and square as exact polynomial
identities. This is also the credited symmetric comparison from8672.

Since both16 and208/9 are below c_3, a global maximum at least c_3
lies strictly inside the parameter triangle. The profile (3) is an
interior member: take
\[
 c=(\alpha+1)/2,\quad x=(1-\alpha)/2,\quad
 y=-(5\alpha+3)/2.
\tag{9}
\]
These are positive, and one singleton coincides with the alpha block,
giving multiplicities4+3+1. This already supplies maximum at least c_3.

## 4. Exact stationary elimination

Use the interior chart V=1 and let
\(n=\mathrm{Num}(\kappa,U,1)\),
\(d=\mathrm{Den}(\kappa,U,1)\). Since d>0, every interior maximum
has
\[
 p=n_\kappa d-nd_\kappa=0,\qquad
 q=n_Ud-nd_U=0.                                        \tag{10}
\]
In the remainder of this section p,q mean these polynomials divided
by their respective positive integer contents. Their U degrees are9
and8; this normalization preserves all stationary solutions.

Build the17x17 Sylvester matrix S from the eight shifted p rows
and nine shifted q rows, with coefficients in \(\mathbb Z[\kappa]\).
The standalone checker computes its determinant by fraction-free
Bareiss elimination, with exact integer-polynomial division and no
computer-algebra library. It verifies coefficient by coefficient
\[
 \det S=A_0\kappa^7(16\kappa-1)^{14}(125\kappa+81)^5
                              F_4F_6F_7F_{16},          \tag{11}
\]
where
\[
 A_0=899679616715369403548229400563231388599310834535159790285851983872,
\]
\[
 \begin{split}
 F_4={}&250000\kappa^4-49900\kappa^3-30195\kappa^2-4369\kappa+64,\\
 F_6={}&3625\kappa^6+11100\kappa^5+19874\kappa^4+9530\kappa^3
                                      +1633\kappa^2+14\kappa+1,\\
 F_7={}&22500\kappa^7+82500\kappa^6+109985\kappa^5+23828\kappa^4
                          -34966\kappa^3-6416\kappa^2+3241\kappa+64,
 \end{split}
\]
\[
\begin{split}
F_{16}={}&52034400000000000\kappa^{16}-634889742720000000\kappa^{15}\\
 &-3691662594253760000\kappa^{14}-7346176678195664000\kappa^{13}\\
 &-7154447918441392100\kappa^{12}-3713341102056530540\kappa^{11}\\
 &-1529810534666677091\kappa^{10}-1528684269391186496\kappa^9\\
 &-1187369990398617128\kappa^8-175059981086037512\kappa^7\\
 &+40227992581570522\kappa^6-1179788998549176\kappa^5\\
 &-199286026683996\kappa^4+16450339488516\kappa^3\\
 &-207098915535\kappa^2-12189970584\kappa+5038848.
\end{split}
\]
The total degree of (11) is59. A common root of p,q makes S singular,
so (11) is a necessary condition for every stationary point. No
converse assertion based only on a resultant is used.

The factor kappa is excluded by interior positivity, and125kappa+81
has no positive root. At kappa=1/16 the exact specialized gcd in U
is \(U^2\), so there is no stationary point with U>0. All
coefficients of F_6 are positive. The Sturm variations for F_7 at
zero and positive infinity are2 and2, giving **zero positive roots**.
It remains to handle F_4 and F_16.

## 5. Linear lifting without solving a multivariate system numerically

Construct a15x16 coefficient matrix T from seven shifted p rows and
eight shifted q rows. Its columns are the coefficients of
\(U^{15},U^{14},\ldots,U,1\). Let D_1 be the determinant retaining
the first14 columns and the U column; let D_0 retain the first14
and the constant column instead. These are two15x15 determinants
over \(\mathbb Z[\kappa]\), computed separately by the checker.

The cofactor vector of the first14 columns annihilates those columns.
Its combination of the full rows is, up to the same overall sign,
\(D_1U+D_0\). Since each row is a monomial multiple of p or q,
every common root satisfies
\[
                         D_1(\kappa)U+D_0(\kappa)=0.    \tag{12}
\]
This is a polynomial ideal identity, including at parameter specializations.
It is not a fitted numerical relation or an assumption of a unique lift.

For F_4 and F_16 the checker computes the remainders of D_1 and
verifies their gcd with the respective factor is1. Thus D_1 is
nonzero at every root of those factors, and any corresponding
stationary point is forced to have
\[
                              U=-D_0/D_1.               \tag{13}
\]
No giant lift polynomial or proof corpus is required as external data:
the determinant definitions reconstruct it exactly.

For the quartic branch the checker proves the polynomial congruence
\[
 [-D_0-(1+16\kappa)D_1]^2-64\kappa D_1^2
                                      \equiv0\pmod{F_4}. \tag{14}
\]
Combining (13)--(14) gives
\[
                           (U-1-16\kappa)^2=64\kappa.
\]
This is exactly the common-root condition for A and B when V=1:
\(U=(4\sqrt\kappa\pm1)^2\). Hence every admissible quartic-branch
stationary point has at most three distinct original levels. The
sharp three-level theorem8753 bounds it by c_3 and supplies the
complete equality classification.

## 6. Complete positive-root bound on the degree16 branch

The exact Sturm variations for F_16 at zero and positive infinity
are7 and5, giving **two positive roots**. The two
rational intervals in `F16_BOXES` have width less than10^(-75), each
has Sturm count1, and both lie in the positive half-line. Thus they
exhaust the positive roots. Their exact endpoints are part of the
small source file; no root list is trusted without those checks.

For each interval I the checker evaluates the determinant ratio
\(-D_0/D_1\) with exact rational interval arithmetic. It retains
the unreduced determinant polynomials for this evaluation to avoid
unnecessary cancellation; reductions modulo F_16 are used only for
the exact gcd identity. The interval denominator excludes zero.
It then evaluates n/d on the complete verified shape box. The
resulting certified coarse boxes are

| Branch | Approximate kappa, for orientation | Verified U interval | Verified C interval |
|---|---|---|---|
|1|0.000410588978425124|(4.11732,4.11734)|(23,24)|
|2|16.91757846337335|(51.51525,51.51527)|(7,8)|

The decimals in the second column are descriptive; the rational
isolating endpoints and interval computations are the certificate.
Both shape denominators d have strictly positive lower bounds on
their boxes. Both candidate values are below24<c_3. The proof only
needs this necessary-candidate bound; it makes no unsupported
existence, local-optimality or exhaustiveness claim from a numerical
multivariate solve.

The checker uses exact Fraction arithmetic and Sturm negative
remainders, normalized only by positive scalars. Together with
(11)--(14) and the exceptional specialization, these two boxes are
a complete exclusion of stationary values larger than c_3 in the
positive interior, not a finite grid of sampled shapes.

## 7. Finish the global and equality argument

A global family maximum exists by compactness and is at least c_3
by (9). The strict boundary bounds put it in the positive interior.
It satisfies (10), so the complete necessary factor analysis applies.
The only remaining candidate branch that can reach c_3 is F_4,
where the profile has at most three levels and is bounded by8753.
Therefore the family maximum is exactly c_3. Equality on that branch
is exactly (3), by the inherited three-level equality theorem.
The profile in (3) belongs to the family and attains the bound,
which proves both directions of the theorem.

## 8. Computational scope and reproduction

Run `python3 -B verify.py` and `python3 -B -O verify.py` in this
directory. Python3.11+ standard library only is needed. The checker
regenerates universal moment/Gram polynomials and both derivatives,
all three determinant polynomials, exact resultant factors, the
exceptional gcd, the no-positive-root claims, the quartic collision
identity, both positive degree16 root isolations and their lifted
value boxes. It also matches the previous exact witness and the
three-level integer benchmark, and rejects four damaged certificates.
`expected.json` is a compact regression fixture, not external trusted
mathematical data.

The cofactor identification, real interlacing/zero-weight mechanism,
compact parameter map, resultant and row-cofactor interpretation,
and compactness-to-stationarity proof are the written mathematical
bridges above. Exact arithmetic certifies the finite identities and
signs. No CAS or solver is called by the checker; SymPy1.14.0 was
used only to discover the compact factorization and root boxes,
which are independently regenerated or checked here. No timeout,
incomplete enumeration, floating-point root or omitted certificate
is a proof input.

The prerequisite8753 is an ordinary author theorem, with its source
and scope explicitly inherited. Further multiplicity patterns and
the full all-sphere maximum remain genuine separate obligations.
