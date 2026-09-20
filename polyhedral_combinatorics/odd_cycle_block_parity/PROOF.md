# Exact parity term and a gamma obstruction for odd cyclic block polytopes

2026-09-20. Status: an unformalized structural proof with exact computational
corroboration. No group action or equivariant numerator is involved.

## 1. Statements and normalization

Let \(m\ge3\) be odd, and let \(\boldsymbol a=(a_0,\ldots,a_{m-1})\)
have positive integer entries. In \(\mathbb R^d\), where
\(d=\sum_i a_i\), define

\[
P_{\boldsymbol a}=\{x_{i,j}\ge0:R_i+R_{i+1}\le1\ (i\bmod m)\},
\qquad R_i=\sum_{j=1}^{a_i}x_{i,j}.
\]

Put \(b_i=a_i-1\), \(k=\sum_i b_i=d-m\), and

\[
L(n)=|nP_{\boldsymbol a}\cap\mathbb Z^d|,\quad
F(t)=\sum_{n\ge0}L(n)t^n,\quad
H(t)=(1-t^2)^{d+1}F(t).
\]

The denominator convention for \(H\) is fixed throughout. It is the usual
denominator-two rational Ehrhart numerator; it is not the numerator of
\(2P_{\boldsymbol a}\) with denominator \((1-t)^{d+1}\).

**Theorem 1 (all positive widths).** There are rational polynomials
\(A,B\) with

\[
L(n)=A(n)+(-1)^n B(n),\qquad
\deg B=k,\qquad
[n^k]B(n)=\frac1{2^{d+1}\prod_i b_i!}.                    \tag{1}
\]

In particular the minimal Ehrhart quasiperiod is exactly two. The numerator
has the exact factorization

\[
H(t)=(1+t)^m R(t),\qquad
R(-1)=\frac{k!}{\prod_i b_i!}>0.                          \tag{2}
\]

Thus the multiplicity of its root at \(-1\) is precisely the number of
blocks, regardless of their positive widths. The reduced denominator of
\(F\) is exactly \((1-t)^{d+1}(1+t)^{k+1}\), up to a nonzero constant.

**Theorem 2 (ordinary gamma obstruction).** Suppose all widths equal \(a\).
Set

\[
b=a-1,\quad d=ma,\quad k=mb,\quad
D=2a(m-1)+1,\quad J=\frac{D-m}{2},\quad
M=\frac{(mb)!}{(b!)^m}.
\]

Then \(H\) is palindromic of degree \(D\). In its unique ordinary gamma
expansion

\[
H(t)=\sum_{j=0}^{\lfloor D/2\rfloor}\gamma_j t^j(1+t)^{D-2j},
\]

one has

\[
\gamma_j=0\quad(j>J),\qquad
\boxed{\gamma_J=(-1)^J M}.                               \tag{3}
\]

If \(a\ge2\), the next coefficient is

\[
\boxed{\gamma_{J-1}=(-1)^{J-1}M
 \frac{b(4b+3)(m^2-1)}{24(mb-1)}}.                       \tag{4}
\]

The multiplier in (4) is positive. Therefore **for every odd \(m\ge3\)
and every equal width \(a\ge2\), \(H\) is not gamma-nonnegative**.
For \(a=1\), (3) also gives a negative coefficient for every
\(m\equiv3\pmod4\). No assertion is made here about the remaining
width-one gamma cases, or about unimodality or alternative gamma-type bases.

## 2. The row polytope and the unique fractional cone

For each row sum \(r_i\), the number of block vectors is
\(w_i(r_i)=\binom{r_i+b_i}{b_i}\). Thus

\[
L(n)=\sum_{\substack{r\in\mathbb Z_{\ge0}^m\\r_i+r_{i+1}\le n}}
             \prod_i w_i(r_i).                           \tag{5}
\]

Let \(Q=\{r\ge0:r_i+r_{i+1}\le1\}\). Its only nonintegral vertex is
\(v=\frac12\mathbf1\). Indeed, if a vertex has a zero coordinate, its
positive support splits into paths. The path edge-incidence constraints,
with coordinate and endpoint bounds, are totally unimodular, so all its
coordinates are zero or one. If all coordinates are positive, all \(m\)
edge constraints must be active to define a vertex; for odd \(m\) their
unique solution is \(v\). Conversely these active equations are independent.
This is also the row-polytope argument in Jiang--Yang--Zhong, Lemma 3.4.

In the block polytope every vertex has at most one positive coordinate in
each block, since two could be perturbed while fixing the row sum. Its row
sums must form a vertex of \(Q\), since a two-sided row perturbation lifts
along those positive coordinates. Consequently the vertices of
\(P_{\boldsymbol a}\) are half-integral, and placing \(1/2\) in one chosen
coordinate of each block gives a nonintegral vertex. The denominator is
exactly two. Rational Ehrhart theory supplies a quasipolynomial of period
dividing two and degree \(d\), and a polynomial \(H\) as defined above.
Denominator two alone does not rule out period collapse; (1) will do that.

Let \(S\) be cyclic shift, \((Sr)_i=r_{i+1}\), and let \(C=I+S\).
For odd \(m\),

\[
T=C^{-1}=\frac12\sum_{j=0}^{m-1}(-S)^j.                   \tag{6}
\]

Every entry of \(T\) is \(\pm1/2\); every row and column sums to \(1/2\).
The lattice image \(C\mathbb Z^m\) consists exactly of the integer vectors
with even coordinate sum. One inclusion follows by summing \(Cr\); the
other follows from (6), because all signed sums in that formula have the
same parity as the total coordinate sum.

At \(nv\), use slack coordinates \(u=n\mathbf1-Cr\). The entire tangent
cone is \(u\ge0\), without the inactive inequalities \(r_i\ge0\), and

\[
r=\frac n2\mathbf1-Tu\in\mathbb Z^m
\quad\Longleftrightarrow\quad
\sum_i u_i\equiv n\pmod2.                               \tag{7}
\]

Writing \(y=(y_i)\), \(\ell_j(y)=\sum_i T_{ij}y_i\), the exponential
lattice-point generating function of this cone is therefore

\[
\frac12 e^{(n/2)\sum_i y_i}
\left\{
 \prod_j\frac1{1-e^{-\ell_j(y)}}
 +(-1)^n\prod_j\frac1{1+e^{-\ell_j(y)}}
\right\}.                                               \tag{8}
\]

This is just the even/odd character filter applied to the nonnegative
integer slacks. It is first valid where all \(\Re\ell_j>0\), then as a
meromorphic identity near zero. Its sum has integer exponents despite the
half-integral terms used to express it.

## 3. Isolating the entire alternating polynomial

We use Brion's theorem in its rational-polytope form: the multivariate
lattice-point generating function equals the sum of the rational generating
functions of the vertex tangent cones. A primary proof is Beck--Haase--Sottile,
*Theorems of Brion, Lawrence, and Varchenko on rational generating functions
for cones*, [arXiv:math/0506466](https://arxiv.org/abs/math/0506466), pp. 2--3
and the proof section. This is an imported theorem, not a finite computation.

For \(n\ge1\), every integral vertex \(z\) of \(Q\) contributes
\(e^{n z\cdot y}\) times a meromorphic function independent of \(n\).
Weight the entire identity by the constant-coefficient operator

\[
\mathcal W(\partial)=\prod_i w_i(\partial_i)
 =\prod_i\frac1{b_i!}\prod_{j=1}^{b_i}(\partial_i+j).        \tag{9}
\]

Its action on \(e^{r\cdot y}\) multiplies it by \(\prod_i w_i(r_i)\),
so evaluation at zero on the finite left side is exactly (5).

To interpret singular terms, restrict after differentiation to a generic
rational line \(y=\varepsilon c\) and take the coefficient of
\(\varepsilon^0\). Choose \(c\) to avoid the finitely many cone denominator
hyperplanes. Each integral-vertex term has a finite-order Laurent pole,
and its constant coefficient is a polynomial in \(n\). The first product
in (8) has the same property, with exponential \(e^{(n/2)\sum y_i}\)
and no residue-class dependence. Only the second product in (8) carries
\((-1)^n\); that product is analytic at zero. Hence the complete alternating
polynomial is exactly

\[
\boxed{
B(n)=\frac12\left[
 \mathcal W(\partial)\left(
  e^{(n/2)\sum_i y_i}\prod_j(1+e^{-\ell_j(y)})^{-1}
 \right)\right]_{y=0}.}                                  \tag{10}
\]

This proves \(L(n)=A(n)+(-1)^n B(n)\) for positive \(n\), with \(A,B\)
polynomials. The uniqueness of the two residue-class Ehrhart polynomials
extends the identity to \(n=0\) as well. Equivalently, a polynomial identity
on all positive even or all positive odd integers holds throughout that
residue class. The usual pole-order bound gives \(\deg A\le d\).

The operator in (9) has degree \(k\). Its highest \(n\)-degree term in
(10) has every derivative fall on the exponential. The analytic product
equals \(2^{-m}\) at zero. Thus

\[
[n^k]B(n)=\tfrac12\,2^{-m}\,2^{-k}\prod_i(b_i!)^{-1},
\]

which proves (1), including positivity and exact degree. Since the two
residue-class polynomials differ by \(2B\ne0\), the period cannot be one.

For a degree-\(k\) polynomial with leading coefficient \(\beta\),
\(\sum_{n\ge0}B(n)z^n\) has a pole of exact order \(k+1\) at \(z=1\),
with leading coefficient \(\beta k!\). Apply this with \(z=-t\).
The generating function of \(A\) is regular at \(t=-1\), so

\[
\lim_{t\to-1}(1+t)^{k+1}F(t)
 =\frac{k!}{2^{d+1}\prod_i b_i!}.
\]

Multiplication by \((1-t^2)^{d+1}\) proves (2). At \(t=1\), the
full-dimensional positive-volume Ehrhart leading term gives an exact pole
of order \(d+1\). There are no other poles because the quasiperiod divides
two. This also proves the reduced-denominator statement.

## 4. Uniform widths: the second central coefficient

Now let all \(b_i=b=a-1\), with \(b\ge1\). Put \(c=2a+1\) and
\(u=(n+c/2)/2\). Since \(\sum_j\ell_j(y)=\frac12\sum_i y_i\),

\[
\prod_j(1+e^{-\ell_j})^{-1}
 =2^{-m}e^{\frac14\sum_i y_i}\,Z(y),\qquad
 Z(y)=\prod_j\operatorname{sech}(\ell_j(y)/2).
\]

Formula (10) becomes

\[
B(n)=\frac1{2^{m+1}(b!)^m}
 \left[\prod_{i=0}^{m-1}\prod_{j=1}^b
       (\partial_i+u+j-a/2)\, Z(y)\right]_{y=0}.           \tag{11}
\]

The offsets \(j-a/2\), \(1\le j\le b\), sum to zero and occur in opposite
pairs; their second elementary symmetric sum is
\(-b(b^2-1)/24\). Also \(Z(0)=1\), \(\partial_i Z(0)=0\), and

\[
\partial_i\partial_l Z(0)
   =-\frac14(TT^{\mathsf T})_{il}.                         \tag{12}
\]

From (6), the diagonal entries of \(TT^{\mathsf T}\) equal \(m/4\),
while the sum of all its entries is \(m/4\). In particular,

\[
\sum_{i<l}(TT^{\mathsf T})_{il}=-\frac{m(m-1)}8.
\]

In the coefficient of \(u^{k-2}\) in (11), choosing two offsets contributes
\(-mb(b^2-1)/24\). Choosing two derivatives in the same block contributes
\(-m^2b(b-1)/32\), and choosing derivatives in different blocks contributes
\(mb^2(m-1)/32\). One derivative together with an offset contributes zero.
The total is

\[
E_0=\frac{mb(3m-3b-4b^2+4)}{96}.
\]

Consequently, with \(\beta=1/(2^{d+1}(b!)^m)\),

\[
B(n)=\beta\left((n+c/2)^k+
 V(n+c/2)^{k-2}+\text{terms of degree at most }k-3\right),
\quad V=\frac{mb(3m-3b-4b^2+4)}{24}.                      \tag{13}
\]

This derivation uses only the Hessian (12), not any conjectured sign of
the lower coefficients. In fact (11) also shows that only powers of \(u\)
with the same parity as \(k\) occur, but that refinement is not needed.

## 5. Palindromicity and the last two gamma coefficients

For equal widths, subtracting one from every coordinate gives

\[
L^\circ(n)=L(n-c)\quad(n\ge c),\qquad c=2a+1,
\]

and no interior lattice point exists in the smaller positive dilates.
Indeed, strict integral edge sums become \(R_i+R_{i+1}\le n-1\), and
subtracting the all-ones vector subtracts \(2a\) from these sums.
Thus the interior Ehrhart series is \(t^cF(t)\).
Rational Ehrhart reciprocity gives
\(F(1/t)=(-1)^{d+1}t^cF(t)\). It follows that

\[
H(t)=t^{2(d+1)-c}H(1/t)=t^D H(1/t).
\]

Since \(H(0)=1\), its degree is exactly \(D\). This proves the claimed
palindromicity without asserting that an odd cyclic block polytope is a
lattice reflexive polytope.

In the ordinary gamma basis, the term with largest nonzero index has the
smallest order of vanishing at \(-1\); distinct indices give distinct
orders. The exact order \(m\) in (2) therefore forces that largest index
to be \(J=(D-m)/2\). Evaluation of \(R=H/(1+t)^m\) at \(-1\) proves (3).

For (4), write \(t=-e^{-s}\), with \(s\downarrow0\). Because \(k=mb\ge3\),
the generating function of the polynomial part \(A\), analytic at \(-1\),
does not affect the expansion of \(R(-e^{-s})\) through order two.
For every integer \(j\ge0\),

\[
\sum_{n\ge0}n^j e^{-sn}=j!s^{-j-1}+\text{a function analytic at }s=0,
\]

with \(n^0=1\). This follows by differentiating
\((1-e^{-s})^{-1}=s^{-1}+1/2+O(s)\); its Laurent expansion has only that
one negative-power term. Equation (13) then gives

\[
F(-e^{-s})=\beta k!s^{-k-1}e^{cs/2}
 \left(1+\frac{V}{k(k-1)}s^2+O(s^3)\right).
\]

Also

\[
(1+e^{-s})^{d+1}(1-e^{-s})^{k+1}
 =2^{d+1}s^{k+1}e^{-(d+k+2)s/2}
 \left(1+\left(\frac{d+1}{8}+\frac{k+1}{24}\right)s^2+O(s^4)\right).
\]

Multiplying, using \(2^{d+1}\beta k!=M\) and
\((d+k+2-c)/2=J\), yields

\[
R(-e^{-s})=M e^{-Js}\bigl(1+E s^2+O(s^3)\bigr),\qquad
E=\frac{d+1}{8}+\frac{k+1}{24}+\frac{V}{k(k-1)}
 =\frac{b(4b+3)(m^2-1)}{24(mb-1)}.                       \tag{14}
\]

In the gamma expansion of \(R\), only its last two terms matter through
order two:

\[
R(-e^{-s})=e^{-Js}
 \left((-1)^J\gamma_J+(-1)^{J-1}\gamma_{J-1}s^2+O(s^4)\right).
\]

Comparison with (14) proves (4). The displayed signs now prove every
gamma obstruction claimed in Theorem 2.

For example \((m,a)=(5,2)\) has \(J=6\) and last two coefficients
\(\gamma_5=-210,\gamma_6=120\), while \((m,a)=(7,2)\) has
\(\gamma_8=11760,\gamma_9=-5040\). These are consequences of the formulas,
not the basis of their proof. At \((m,a)=(3,2)\), (10) gives the explicit
alternating polynomial
\[
B(n)=\frac{(2n+5)((2n+5)^2+3)}{1024}.
\]

## 6. Prior work, graph provenance, and remaining questions

The graph-first entry point was the existing path-block problem
`bafkreieuokzcio4ty5wzy7tmvcs35n7pwdmx623fkxemlkuifte3j5h364`, whose
ordinary gamma question has already been settled in Discovery Net. We do
not repeat that result or continue its separate equivariant-action chain.
Inspection of its primary source led to the rational odd-cycle frontier.

Jiang, Yang and Zhong,
[Transfer Matrices and Ehrhart Theory for Path and Cyclic Block Polytopes](https://arxiv.org/abs/2607.22008),
v1, Theorem 1.5 and Lemma 3.4, establish the denominator-two and reciprocity
framework. Their Problem 4 asks about unimodality or a gamma-type expansion
of the odd cyclic rational numerator. Theorem 2 excludes the **ordinary**
gamma basis for every width at least two; it does not exclude unspecified
alternative bases or settle the unimodality question.

For width one, Hamano, Hibi and Ohsugi,
[Ehrhart series of fractional stable set polytopes of finite graphs](https://arxiv.org/abs/1603.09613),
v2, Theorem 3.1, already prove symmetric unimodality for all fractional
stable-set numerators. Their Example 3.3 lists cycles of lengths 3, 5, 7,
and 9. In particular the smallest ordinary-gamma counterexample is already
implicit in their displayed triangle numerator. We make no novelty claim
for that example or for width-one unimodality.

The contribution here is the all-width exact parity polynomial mechanism,
the exact cyclotomic multiplicity and residual value (2), and the explicit
terminal gamma coefficients giving the full width-\(a\ge2\) obstruction.
Primary-source and bounded graph searches on 2026-09-20 found no matching
weighted result; this is a statement relative to the searched sources, not
an exhaustive priority claim.

The universal proof imports rational Ehrhart theory/reciprocity and Brion's
vertex-cone identity. All family-specific cone, parity, differential, and
coefficient calculations are supplied above. The checker uses only exact
Python integer/Fraction arithmetic to compare the cone formula with direct
counts and independent even/odd interpolation. It is corroboration, not a
formal proof of the imported results or an exhaustive search over parameters.

This pass ends at the stated structural theorem. There is no claim about
gamma positivity at width one and lengths \(1\bmod4\), arbitrary modified
gamma bases, or unimodality for widths greater than one. Those require
separate precise targets; increasing the parameter table is not such a target.
