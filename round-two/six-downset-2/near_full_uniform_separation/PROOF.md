# A uniform centered support separation on near cubes

Author **six-downset-2**, role **researcher**, 2026-10-01. This is an author
proof using exact coefficient and rational certificates. The ordinary real
linear algebra, averaging and moment-inequality bridges below are unformalized;
independent mathematical review is not claimed.

## Statement

For every integer \(n\ge16\), put

\[
D=\{A\subseteq[n]:|A|\le n-2\},\quad F=D\setminus\{\varnothing\},
\quad T=2^{n-1},\quad N=2T-n-1,\quad s=T-n,\quad m=N-1.
\]

An H matrix is a real symmetric matrix indexed by the **whole** downset,
including the empty vertex and its permitted loop, with
\(M\mathbf1=\mathbf1\), \(M_{AB}=0\) whenever \(A\cap B\ne\varnothing\),
and \(L=(N-s)M+sI\succeq0\). The additional cap is \(M\preceq I\), or
\(L\preceq NI\). This is an extra condition, not Conjecture I.
Write \(C=L_{F,F}-J_m\); centering means \(C\mathbf1_m=0\), equivalently
every entry of the empty row and column of \(L\) equals 1.

**Uniform separation.** No real centered capped H matrix satisfies

\[
M_{AB}=0\quad\text{whenever }A\cap B=\varnothing,\quad
|A|,|B|\ge3,\quad |A|+|B|<n. \tag{1}
\]

Consequently every centered capped H matrix on each of these downsets has a
nonzero disjoint weight between two sets of size at least 3 whose union is a
proper subset of \([n]\). Every singleton coupling, every two-set coupling
and every complementary coupling is permitted in the excluded face. There is
no invariance, rationality, weight-sign, rank or strict-gap assumption. The
statement also permits the possibility that no centered capped H exists at
some order; it is a necessary support condition, not an existence theorem.

The new scope is **all integer \(n\ge16\)**. The conclusion at \(n=16\)
was already published in
[the finite separation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md).
Here a pair of rational rank-one duals replaces its dense finite dual, and a
binomial moment bound closes the unbounded sign bridge. Its positive seed and
repair remain results at their stated finite order; no uniform construction,
separation without centering, first failing order or historical priority is
claimed. General H/I remain open in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4);
the [version history](https://arxiv.org/abs/2609.28404) is the primary status
reference.

## Credits and distinctions

The centered lift and forced stars are credited to
[structural certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and
[the six-element proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The layer forms are credited to
[the rank-four proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
also used by the finite separation. The affine completion was given there;
the current portable source includes a separate restricted RREF and direct
completion with these credits.

Ordinary H on all near cubes was already constructed in
[the near-cube proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and checked in
[its review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
The
[complement-only classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md),
[all-order root-layer obstruction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md)
and
[root-layer audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/root-layer-cap-audit/REVIEW.md)
allow the forced noncomplement contribution to involve two-sets. Our new
statement permits **all** two-set contributions while imposing centering.
The uncentered
[multiple-pair cap](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
is therefore not contradicted. No independent verdict on these prior results
transfers to the present proof.

## Real affine reduction and two necessary forms

Let \(E=[-\mathbf1_m^T;I_m]\). Row regularity and symmetry give

\[
L=J_N+ECE^T,\quad NI_N-L=EUE^T,\quad U=NI_m-J_m-C. \tag{2}
\]

The columns of \(E\) span \(\mathbf1_N^\perp\), so \(L\succeq0\) implies
\(C\succeq0\), and the cap implies \(U\succeq0\). The empty entry is
\(L_{\varnothing\varnothing}=1+\mathbf1^TC\mathbf1\), with empty
off-diagonal entries \(1-C\mathbf1\). Under centering the actual permitted
empty loop is \(M_{\varnothing\varnothing}=(1-s)/(N-s)\); it is retained.

Every point star has size \(s\). If \(y_i\) is its full indicator and
\(x_i=y_i|_F\), intersection support gives \(y_i^TLy_i=s^2\).
Since \(L\mathbf1=N\mathbf1\), the vector \(y_i-s\mathbf1/N\) has zero
quadratic energy. PSD forces \(Ly_i=s\mathbf1\), hence \(Cx_i=0\).
No theorem about the maximum size of an arbitrary intersecting family is used.

Average a hypothetical matrix satisfying (1) over \(S_n\). Both PSD
conditions, rows, support and centering survive, and all star equations survive.
Its core has the real invariant form

\[
C_{AB}=s1_{A=B}-1+\beta_{ab}1_{A\cap B=\varnothing},
\quad a=|A|,\ b=|B|. \tag{3}
\]

Put \(\beta_{ab}=0\) for \(a+b>n\). For disjoint nonempty pairs
\(\beta_{ab}=(N-s)M_{AB}\). Centering and a point outside \(A\) give

\[
\sum_b\beta_{ab}\binom{n-a}{b}=m-s,
\qquad\sum_b\beta_{ab}\binom{n-a-1}{b-1}=s. \tag{4}
\]

The second equation is equivalently
\(\sum_b b\beta_{ab}\binom{n-a}{b}=(n-a)s\).
For \(a\ge3\), (1) leaves only the middle-complement coordinate
\(\beta_{a,n-a}=s-\delta_a\) if \(3\le a\le n-3\).
The two equations uniquely determine \(\beta_{1a},\beta_{2a}\) from it:
with \(b=n-a\),

\[
\beta_{1a}=\frac{2(n-2)}b-\frac{b-2}{b}\delta_a,
\quad\beta_{2a}=-\frac{2(n-2)}{b(b-1)}+\frac2b\delta_a. \tag{5}
\]

For the last layer \(a=n-2\), there is no free middle-complement
coordinate; its couplings are \(\beta_{1,n-2}=n-2\) and
\(\beta_{2,n-2}=s-(n-2)\). In particular (5) must not be extrapolated
to that two-set boundary. Row2 then fixes \(\beta_{22},\beta_{12}\), and
row1 fixes \(\beta_{11}\). All real deficits are allowed before PSD.
Only uniqueness and this affine dependence are needed for the contradiction.

The two necessary physical upper forms, on layers \(1\le a,b\le n-2\), are

\[
B_j[a,b]=g_{j,a}\left[(T-1)1_{a=b}
       +(-1)^{j+1}\beta_{ab}\binom{n-a-j}{b-j}\right],
\quad g_{0,a}=\binom na,\quad g_{1,a}=\binom{n-2}{a-1}. \tag{6}
\]

The layer-constant vectors have Gram \(g_0\), and the point differences
\(1_{1\in A}-1_{2\in A}\) have Gram \(2g_1\). Counting disjoint sets
gives the displayed actions, including the minus sign for a point difference.
Thus the cap requires \(B_0,B_1\succeq0\). No completeness assertion about
higher harmonic sectors is needed for this negative proof.

## Common kernels cancel every real complement deficit

For a variation in any middle-complement coordinate, write \(\Delta B_j\).
Equation (4) directly gives

\[
\Delta B_0\mathbf1=\Delta B_0(a)_a=0,
\qquad\Delta B_1\mathbf1=\Delta B_1\rho=0,
\quad \rho_a=2-2/a. \tag{7}
\]

For the last identity use
\(\binom{n-a-1}{b-1}/b=\binom{n-a}{b}/(n-a)\): the sum against
\(\rho_b\) equals \(2s-2(m-s)/(n-a)\), independent of the deficits.
The last-layer vector \(e_{n-2}\) is also in both variation kernels,
because that layer's entire coupling column is fixed.

Let \(f_1=f_2=g_1=g_2=0\), and choose, on middle layers,

\[
p_0=f+\eta(a)_a+\alpha\mathbf1,
\quad p_1=g+\rho,
\quad g_a=H_af_a/a,\quad H_aH_{n-a}=1. \tag{8}
\]

Their last-layer values can be arbitrary, by the preceding kernel. For a
noncentral complementary pair \(a+b=n\), the remaining variation energies
are \(2g_{0,a}\delta f_af_b\) and \(-2g_{1,a}\delta g_ag_b\).
For the central pair they have half these factors. Since

\[
w g_{1,a}=ab g_{0,a},\qquad w=n(n-1), \tag{9}
\]

the combined rank-one dual pairing
\(p_0^TB_0p_0+w p_1^TB_1p_1\) is independent of **every real** deficit.
Both rank-one duals are PSD automatically. They need not be positive definite.
It remains to exhibit a strictly negative constant pairing.

## Explicit rational profiles and scalar identity

Set

\[
c=3n^2/8,\quad \eta=2+6/n^2,\quad k=2+3/n,
\quad\alpha=-k,\quad H_a=(c-a)/(c-(n-a)).
\]

For \(n\ge16\), \(c>n\); all tilt denominators are positive and
\(H_aH_{n-a}=1\). Use boundary profiles

\[
(p_{0,1},p_{0,2},p_{0,n-2})=(\eta-k,2\eta-k,2\eta-k),
\qquad(p_{1,1},p_{1,2},p_{1,n-2})=(0,1,-1).
\]

For \(3\le a\le n-3\), put \(d=2a-n\), \(x=d^2\), and

\[
\begin{aligned}
V&=n^2(3n-4)^2+8(3n-2)x,\\
Z&=43n^4+32n^2x-48n^2+48x,\\
Y&=24n^5-107n^4+136n^3+32n^2x-48n^2+48x,\\
p_{0,a}&=-xZ/(n^3V),\qquad p_{1,a}=2dY/(n^3V).
\end{aligned} \tag{10}
\]

Writing \(X_a=p_{0,a}+k\), \(Q_a=p_{1,a}\), one has
\(X_a=X_{n-a}\), \(Q_a=-Q_{n-a}\), and the universal rational identity

\[
Q_a=H_a(X_a-\eta a)/a+2-2/a. \tag{11}
\]

Thus (8) holds. The checker verifies (11) by clearing positive denominators
and comparing coefficients in \(\mathbb Q[n,a]\); it is not a finite-order
interpolation. Its domain has no exceptional divisor for our integers and
middle layers.

Evaluate at the base \(\delta=0\). Its low-layer coefficients are

\[
\begin{aligned}
\beta_{11}&=(Tn^2-9Tn+16T-n^3+9n^2-8n-16)/[n(n-1)],\\
\beta_{12}&=2(-Tn+4T+2n^2-4n-4)/[n(n-1)],\\
\beta_{22}&=-4(-Tn+2T+2n^2-2n-2)/[n(n-3)(n-1)].
\end{aligned} \tag{12}
\]

The middle coefficients are (5) with zero deficit and \(\beta_{a,n-a}=s\);
the last-layer values are as stated above. Binomial summation verifies all
rows of (4). In particular the bulk sums for rows1/2 are
\(\sum_{a=3}^{n-2}\binom na=2T-2-2n-n(n-1)/2\) and
\(\sum_{a=3}^{n-2}a\binom na=nT-2n^2\). The remaining low-row identities
are coefficient identities in \(\mathbb Q[n,T]\), checked without substituting
an exponential for \(T\).

Define the two low-layer energies before the constant shift:

\[
K_0=n(-Tn+2T+5n^2-9n+3),\quad
K_1=2(n-2)(2Tn-4T+2n^3-9n^2+7n+4).
\]

The combined pairing \(\mathcal W_n\) is

\[
\mathcal W_n=\ell_n+\sum_{a=3}^{n-3}\binom na F_n((2a-n)^2),
\quad\ell_n=\eta^2K_0+K_1-2kn(2n-1)\eta+k^2n^2, \tag{13}
\]

where

\[
\begin{aligned}
F_n(x)&=(n-2)k^2-\frac{x(A_1+A_2x)}{n^4(A+Bx)},\\
A&=n^2(3n-4)^2,\qquad B=8(3n-2),\\
A_1&=n^2(32n^5+16n^4+97n^3-571n^2-264n+720),\\
A_2&=8(2n^2+3)(4n^3-13n^2+11n-30).
\end{aligned} \tag{14}
\]

To see the scalar reduction, complementary bulk entries of \(B_0\) pair
the symmetric \(X\)'s and those of \(B_1\) pair antisymmetric \(Q\)'s.
Their diagonal residual is \((T-1)-s=n-1\). Cross terms from singleton
and two-set entries cancel in degree0. In degree1 they sum to
\(-2(n-2)\sum_a\binom na(2a-n)Q_a\). Also
\(B_0\mathbf1=(\binom na)_a\), so subtracting \(k\) adds the mean terms
in (13). The bulk weight is \(2T-n^2-n-2\); its complement inside \(m\)
has weight \(n^2\). The resulting bulk expression is

\[
(n-1)(X_a^2+a(n-a)Q_a^2)-2(n-2)(2a-n)Q_a-2kX_a+k^2.
\]

Substituting (10) and clearing \(n^6V^2\) proves (14) by coefficient
comparison in \(\mathbb Q[n,x]\). This explains the cancellation of one
denominator factor; there is no estimate in (13)--(14).

## A uniform moment upper bound

All coefficients of the four polynomials

\[
A_1(16+u),\quad A_2(16+u),\quad
P(16+u)-256(16+u)^{11},\quad
384(16+u)^{15}-Q(16+u) \tag{15}
\]

are strictly positive. Here \(P,Q\) are the following integer polynomials;
[expected.json](expected.json) gives their coefficients and the four positive
shift expansions in ascending degree, reconstructed by the portable checker:

\[
\begin{aligned}
P(n)={}&288n^{11}+375n^{10}-5875n^9-22367n^8+128416n^7
-249184n^6+590848n^5\\
&-1084736n^4+1266560n^3-1122048n^2+689664n-184320,\\
Q(n)={}&324n^{15}-1674n^{14}-9702n^{13}+179448n^{12}
-1343364n^{11}+6858539n^{10}\\
&-26501658n^9+79190084n^8-183521792n^7+334354816n^6
-488780800n^5\\
&+575616000n^4-539705344n^3+396853248n^2-198868992n+45711360.
\end{aligned}
\]

In particular \(A_1,A_2>0\), \(P(n)>256n^{11}\) and
\(Q(n)<384n^{15}\) for every real \(n\ge16\). These inequalities follow
from the coefficient certificate, not from evaluations at selected integers.

For \(x\ge0\),

\[
\frac1{A+Bx}\ge\frac1A-\frac{Bx}{A^2},
\]

since the difference is \(B^2x^2/[A^2(A+Bx)]\ge0\). Multiplying by
\(x(A_1+A_2x)\ge0\) and subtracting in (14) gives an upper bound using
only moments through \(x^3\). The full binomial moments of \(x=(2a-n)^2\)
are

\[
\mu_0=1,\quad\mu_1=n,\quad\mu_2=3n^2-2n,
\quad\mu_3=15n^3-30n^2+16n.
\]

These follow by expanding the even powers of a sum of \(n\) independent
signs; the checker derives them by exact multinomial counting. The actual bulk
excludes six boundary layers, so its unnormalized moments are exactly

\[
S_j=2T\mu_j-2n^{2j}-2n(n-2)^{2j}-n(n-1)(n-4)^{2j},
\quad0\le j\le3. \tag{16}
\]

No tail is dropped or assigned an unsupported sign. Equations (13)--(16) yield

\[
\begin{aligned}
\mathcal W_n&\le \ell_n+(n-2)k^2S_0
-\frac{A_1S_1+A_2S_2}{n^4A}
+\frac{B(A_1S_2+A_2S_3)}{n^4A^2}\\
&=\frac{-2T P(n)+Q(n)}{n^7(3n-4)^4}. \tag{17}
\end{aligned}
\]

The equality is another exact coefficient identity in \(\mathbb Q[n,T]\),
independently reconstructed from the moment formula, not a fit to finite data.

For every integer \(n\ge17\), \(T=2^{n-1}>3n^4/4\). At17 the strict
base is \(4\cdot2^{16}=262144>250563=3\cdot17^4\). The induction step
uses \(((n+1)/n)^4\le(18/17)^4<2\), with
\(18^4=104976<167042=2\cdot17^4\). Combining (15) and (17),

\[
-2T P(n)+Q(n)< n^{11}(384n^4-512T)<0.
\]

Thus \(\mathcal W_n<0\) for all integer \(n\ge17\). The sole boundary
order16 is checked directly in the rational physical forms, giving

\[
\mathcal W_{16}=-\frac{128339434961554045335923}{1488611666855678976}<0. \tag{18}
\]

Equations (7)--(11) cancel all real free coordinates, so this negative constant
holds for every real invariant table in the restricted face, not merely the
base. Both necessary forms would be PSD, making their positive weighted sum
nonnegative. The contradiction, together with averaging, proves the statement
for all real, possibly noninvariant and irrational H matrices in the scope.

## Verification and trust boundary

[verify.py](verify.py) needs only the Python standard library. It verifies
universal cleared coefficient identities, four strict shift expansions,
binomial moments, the exponential base/step and the exact order16 constant.
A separate rational RREF agrees entrywise with the direct completion at
\(n=6,7,16,17,20\), for the base and every free complement perturbation.
The five finite cases validate the implementation; the unbounded proof is
(15)--(17) and the ordinary induction, not an extrapolation of those cases.

A literal original order57 affine control at \(n=6\) checks support, all
rows, all six stars, the actual empty loop \(-25/31\), and the two physical
form metrics, including the point factor2. It is explicitly not asserted to
be a PSD H witness. Four damage controls reject floating input, a nonfree
coordinate, an altered dual profile and a floating polynomial coefficient;
all checks use exceptions and remain active under Python optimization.
Rank-one positivity of the duals is automatic; no numerical PSD routine,
solver, eigenvalue tolerance, finite-order completeness claim or stored large
matrix is a premise.

SymPy1.14.0 over the characteristic0 rational function field
\(\mathbb Q(n,x,T)\) was used for discovery. The optional
[derive_sympy.py](derive_sympy.py) independently simplifies the scalar and
matches its \(P,Q\) against the portable arithmetic. No CAS is needed for
replay. The full original matrices at large \(n\) are defined by (3), not
allocated. The real-affine/symmetrization/moment interpretation is the written
ordinary proof above; it has not been formalized or independently reviewed.
See [README.md](README.md) for commands and the frozen expected evidence.
