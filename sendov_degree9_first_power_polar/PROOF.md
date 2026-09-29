# Proof and scope

Let `p` have degree nine and all roots in `|z| <= 1`. Multiplying by a
nonzero constant and rotating the variable preserve the quantities below, so
take `p` monic and the distinguished root `a` real in `[0,1]`. If `a` is a
multiple root, one reciprocal term is infinite and every lower bound here is
immediate. Otherwise set

\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\qquad
p'(z)=9\prod_{j=1}^8(z-\zeta_j),\qquad
q_j=(a-\zeta_j)^{-1},\qquad
\mu=\frac18\sum_j|q_j|.
\]

All denominators in `q` and `a-z_j` are nonzero. Repeated critical points and
repeated other roots are counted with multiplicity.

## 1. Polar identity with a first-moment hypothesis

For `0<a<1` put `b=1-a^2`. Computing `p(1/a)/p'(a)` by factorization and by
integrating `p'` on the segment from `a` to `1/a` gives the prior polar identity

\[
\prod_{j=1}^8\frac{1-az_j}{a-z_j}
 =\int_0^1\prod_{j=1}^8(a+btq_j)\,dt.\tag{1}
\]

This is Lemma 6(ii) in Tao's 2026 exposition and Lemma 3.1(ii) in Zhang's
arXiv:2609.19126. Neither its identity nor the next disk inequality requires
`|q_j| <= 1` or a bound on their second moment. Indeed,

\[
|1-az|^2-|a-z|^2=b(1-|z|^2)\ge0.
\]

Triangle inequality, followed by AM-GM applied to eight nonnegative real
numbers, now yields the necessary scalar inequality

\[
\begin{split}
1&\le\int_0^1\prod_j|a+btq_j|\,dt\\
 &\le\int_0^1\prod_j(a+bt|q_j|)\,dt\\
 &\le H(a,\mu):=\int_0^1(a+b\mu t)^8\,dt.\tag{2}
\end{split}
\]

For fixed `0<=a<1`, `H(a,u)` is strictly increasing for `u>=0`, starts at
`a^8<1`, and tends to infinity. Thus there is a unique `u_*(a)>0` with
`H(a,u_*(a))=1`, and (2) proves `mu >= u_*(a)`.

For degree nine and `0<a<1`, equality is impossible. If `H(a,mu)=1`, every
inequality from (1) through (2) must be an equality. Equality in the disk
inequality forces all eight `z_j` onto the unit circle. Equality in the
integrated triangle and AM-GM bounds forces every `q_j` to be the same
positive real number `u`: the pointwise nonnegative gaps are continuous, so
zero integrated gap is zero at each `0<t<1`. Hence every critical point is
`c=a-1/u`, and

\[
p(z)=(z-c)^9-u^{-9}.
\]

Its nine distinct roots lie on the circle with center `c` and radius `1/u`.
Eight of them would also lie on the unit circle. Two distinct circles have
at most two points in common, so the circles must coincide. That would put
`a` on the unit circle, a contradiction. Consequently

\[
\mu>u_*(a)\qquad(0<a<1).\tag{3}
\]

## 2. A uniform exact constant

Take `c_0=46643/50000`. The binomial formula is

\[
H(a,c_0)=\sum_{k=0}^8\frac{\binom8k}{k+1}
 a^{8-k}\bigl(c_0(1-a^2)\bigr)^k.\tag{4}
\]

It is a degree-sixteen rational polynomial. Its value at `a=1` is one, so

\[
P(a)=\frac{1-H(a,c_0)}{1-a}
\]

is a degree-fifteen rational polynomial, with the quotient understood
algebraically also at `a=1`.

The certificate in this directory covers `[0,1]` by

\[
[0,1/2],\ [1/2,3/4],\ [3/4,25/32],\ [25/32,13/16],\
[13/16,7/8],\ [7/8,1].
\]

On each interval all sixteen degree-fifteen Bernstein coefficients of `P`
are strictly positive, as checked with exact rational arithmetic by
`verify.py`. A Bernstein polynomial is a nonnegative weighted sum of its
coefficients, with weights summing to one. Therefore `P>0` on `[0,1]` and
`H(a,c_0)<1` for `0<=a<1`. Equation (2) proves `mu>c_0` in the interior.

At `a=0`, evaluation of `p'(0)` gives

\[
9\prod_j|\zeta_j|=\prod_j|z_j|\le1,
\qquad \prod_j|q_j|\ge9.
\]

Thus AM-GM gives `mu>=9^(1/8)>1`. At `a=1`, the boundary argument in section
4 gives `mu>=1`. This proves, at every root,

\[
\sum_j|q_j|>8c_0=\frac{46643}{6250}.
\]

## 3. The full first-power bound on a central disk, and the scalar barrier

On `0<=a<=1/2`, the function `a+(1-a^2)t` increases with `a` for every
`0<=t<=1`, and increases strictly on a set of positive length. Hence
`H(a,1)` is strictly increasing there. Its endpoint values are `H(0,1)=1/9`
and `H(1/2,1)=72319/65536>1`. There is exactly one root `rho` of `H(a,1)=1`
in `(0,1/2)`. Exact evaluations give

\[
H(2199/5000,1)<1<H(4399/10000,1),
\qquad 0.4398<\rho<0.4399.
\]

For `0<a<rho`, (2) forces `mu>1`. At `a=rho`, (3) gives the same strict
conclusion, and `a=0` was covered above. Thus `sum_j |q_j|>8` whenever
`|a|<=rho`.

Define `c_pol` to be the infimum of `u_*(a)` over `0<=a<1`. The uniform
certificate proves `c_pol>=46643/50000`. For `a_0=377/500` and
`c_1=93287/100000`, exact rational evaluation gives

\[
H(a_0,c_1)>1.
\]

Strict increase in `u` proves `u_*(a_0)<c_1`, and hence

\[
0.93286\le c_{\rm pol}<0.93287.
\]

Thus a necessary condition consisting only of (2) permits means below one.
The rational witness is a scalar pair, not the critical data of a polynomial
whose roots have been shown to lie in the disk. This proves a limitation of
this scalar relaxation; it does not disprove the first-power conjecture.

## 4. Boundary first-power inequality and its equality condition

For a simple root at `a=1`, the logarithmic derivative identity gives

\[
\sum_jq_j=\frac{p''(1)}{p'(1)}
 =2\sum_j\frac1{1-z_j}.
\]

For `|z|<=1`, `z!=1`,

\[
\operatorname{Re}\frac1{1-z}-\frac12
 =\frac{1-|z|^2}{2|1-z|^2}\ge0.
\]

Consequently `sum_j |q_j|>=Re sum_j q_j>=8`. Equality holds exactly when
all eight other roots lie on the unit circle and all the critical points
are real (therefore in `[-1,1)` by Gauss-Lucas). This follows by equality
term by term: `|q_j|=Re q_j` means `q_j` is positive real, and the displayed
root defect is zero exactly on the unit circle. The converse follows from
the same identities. Undoing rotation gives the corresponding condition
on the radius through the distinguished boundary root.

For example, `p(z)=(z-1)(z+1)^8` has critical points `-1` seven times and
`7/9` once, and its first-power sum at one is `7/2+9/2=8`. This illustrates
that the first-power equality family is broader than the reciprocal-square
equality family in Zhang's theorem. The identities used here are classical;
no novelty is claimed for the boundary argument.

## 5. An exact polar refinement retaining two defects

Suppose now `0<a<1` and a putative failure has `mu<=1`. Set

\[
r_j=|q_j|,\quad
D=\frac18\sum_j(r_j-\operatorname{Re}q_j),\quad
v=\frac18\sum_j(r_j-\mu)^2,\quad
R=\frac{1+8a}{1+a}.
\]

Gauss-Lucas gives `|zeta_j|<=1`, hence `r_j>=1/(1+a)`. Since `sum r_j<=8`,
also `r_j<=8-7/(1+a)=R`. The following stronger necessary inequality holds:

\[
1\le\int_0^1(a+b\mu t)^8
 \exp\!\left[-\frac{8\left(abtD+\frac12b^2t^2v\right)}
 {(a+btR)^2}\right]dt.\tag{5}
\]

To prove it, put `A_j=a+bt r_j`. The identity

\[
|a+btq_j|^2=A_j^2-2abt(r_j-\operatorname{Re}q_j)
\]

and `sqrt(1-s)<=exp(-s/2)` for `0<=s<=1` give

\[
\prod_j|a+btq_j|
 \le\prod_j A_j\exp\!\left[-\frac{8abtD}{(a+btR)^2}\right].
\]

If a factor on the left vanishes, this inequality holds directly; otherwise
the same argument follows by logarithms. On `[1/(1+a),R]`, the second
derivative of `log(a+bt r)` is at most `-(bt)^2/(a+btR)^2`. Taylor's
inequality about `mu` and cancellation of `sum_j(r_j-mu)` therefore imply

\[
\prod_jA_j\le(a+b\mu t)^8
 \exp\!\left[-\frac{4b^2t^2v}{(a+btR)^2}\right].
\]

Combine these bounds with the first line of (2) to obtain (5). This proof
uses only finite sums and integrals of continuous functions.

## 6. A necessary variance budget approaching the boundary

Consider any sequence of putative first-power failures as in section 5 with
`a_k -> 1`, and put `delta_k=1-a_k`. Equation (2) first forces
`1-mu_k=O(delta_k)`. Indeed, uniformly for `mu` in `[1/(1+a),1]`,

\[
H(a,\mu)=1+8(\mu-1)\delta+O(\delta^2),
\]

by the finite binomial formula. The following coarse bounds give an explicit
domain for the uniform estimates. For `0<delta<=1/100`, write
`a+b mu t=1+x`; then `|x|<=101 delta/100`. Taylor's theorem gives a remainder
at most `64 delta^2` after `1+8x`: the second derivative is
`56(1+x)^6`, and `(1+101/10000)^6<2`. Hence

\[
H(a,\mu)\le1-8(1-\mu)\delta+64\delta^2,
\qquad (1-\mu)/\delta\le8.
\]

For the right side of (5), drop the variance term. On `t in [1/2,1]`,
`ab>=delta`, `(a+btR)^2<2`, and the angular exponent
`E=8abtD/(a+btR)^2` satisfies `2delta D<=E<1`. Here use `R<=9/2`, `D<=2`,
`b<=1/50`, and `a>=99/100`. Moreover `(a+b mu t)^8>=a^8>1/2`.
The inequality `1-exp(-E)>=E/2` then proves that the right side of (5) is at
most `H(a,mu)-delta D/4`. Combining with the previous bound proves
`D/delta<=256`. Also `v<=R^2<=81/4`.

Write `s_k=(1-mu_k)/delta_k` and `d_k=D_k/delta_k`. These two nonnegative
sequences are bounded. The exact integrand on the right of (5), with
`mu=1-s delta`, `D=d delta`, and `b=2delta-delta^2`, has the uniform expansion

\[
1+8(2t-1)\delta+
\left[28(2t-1)^2-8t-16st-16dt-16t^2v\right]\delta^2
 +O(\delta^3).
\]

The remainder is uniform for `0<=delta<=1/100`, `0<=t<=1`, `0<=s<=8`,
`0<=d<=256`, and `0<=v<=81/4`. On this compact parameter rectangle the
denominator is bounded away from zero, `R=(9-8delta)/(2-delta)` is smooth,
and the exponential and polynomial have bounded third derivatives.
Taylor's theorem therefore gives a fixed remainder constant independent
of the sequence. Integrating gives

\[
1\le1+8\left(\frac23-s_k-d_k-\frac23v_k\right)\delta_k^2
 +O(\delta_k^3).
\]

Thus

\[
\limsup_{k\to\infty}\left(
 \frac{1-\mu_k+D_k}{1-a_k}+\frac23v_k\right)\le\frac23,
\qquad \limsup_{k\to\infty}v_k\le1.\tag{6}
\]

This is a necessary condition for such failures, not an existence statement.
It excludes failures converging to any boundary equality configuration whose
reciprocal-modulus variance is greater than one. For instance the example
in section 4 has `v=(7*(1/2-1)^2+(9/2-1)^2)/8=7/4`, and so cannot be such
a limiting configuration. A neighborhood conclusion follows by contradiction
and compactness of the bounded reciprocal coordinates. The binomial
configuration `p(z)=z^9-1` has variance zero and remains a possible limiting
obstruction to this argument.

## 7. Boundary equality classification and concentration of possible failures

The boundary equality condition in section 4 admits the following explicit
classification in every degree `n>=4`. For a polynomial with all roots in
the unit disk and a distinguished unit-modulus root `a`,

\[
\sum_{j=1}^{n-1}|a-\zeta_j|^{-1}=n-1
\]

holds if and only if, for some nonzero constant `C`,

\[
p(z)=C(z^n-a^n)
\quad\hbox{or}\quad
p(z)=C(z-a)(z+a)^{n-1}.\tag{7}
\]

Here a multiple distinguished root has infinite sum and is automatically
excluded. The boundary inequality and equality condition from section 4
work identically with `m=n-1` in place of eight.

For the classification, rotate to `a=1` and make `p` monic. Boundary
equality forces the other roots onto the unit circle and the critical
points onto the real interval `[-1,1)`. Therefore `p'` has real coefficients,
and `p(1)=0` makes `p` real as well. Set

\[
u_j=\frac1{1-z_j}=\frac12+it_j,\qquad
q_j=\frac1{1-\zeta_j}\ge\frac12,\qquad
x_j=q_j-\frac12\ge0.
\]

The multiset of `t_j` is invariant under negation, so the monic polynomial

\[
T(X)=\prod_j(X-it_j)
\]

has only powers congruent to `m` modulo two. Write its first terms as
`T(X)=X^m+A X^(m-2)+...`. On expanding `p(1+w)` and differentiating,

\[
\prod_j(1+q_jw)=\frac{d}{dw}\left[w\prod_j(1+u_jw)\right],
\]

so `e_k(q)=(k+1)e_k(u)`. Equivalently, with
`U(S)=prod_j(S-u_j)=T(S-1/2)` and `Q(S)=prod_j(S-q_j)`,

\[
Q(S)=(m+1)U(S)-S U'(S).
\]

Substitute `S=X+1/2` and compare the first four coefficients:

\[
\prod_j(X-x_j)=X^m-\frac m2X^{m-1}
 +3A X^{m-2}-\frac{m-2}{2}A X^{m-3}+\cdots.
\]

Thus `e_1(x)=m/2`, `e_2(x)=3A`, and
`e_3(x)=(m-2)e_2(x)/6`. These formulas also apply when `m=3` and the
fourth displayed coefficient is constant.

If `e_2(x)=0`, nonnegativity shows that at most one `x_j` is nonzero.
The sum forces that one value to be `m/2`. Hence the reciprocal multiset
is `q=(1/2,...,1/2,(m+1)/2)`, and the critical points are `-1` with
multiplicity `n-2`, and `(n-2)/n` once. Integrating the derivative and
using the root at one gives `p(z)=(z-1)(z+1)^(n-1)`.

Otherwise put `E_k=e_k(x)/binom(m,k)`. The coefficient relation gives
`E_3/E_2=1/2=E_1`. Maclaurin's inequalities for the nonnegative `x_j` give

\[
\frac{E_3}{E_2}\le\sqrt{E_2}\le E_1.
\]

Both inequalities must be equalities, so `E_2=E_1^2`. Equivalently the
variance of the `x_j` is zero. All `x_j=1/2`, all `q_j=1`, and all critical
points are zero. Integration and `p(1)=0` give `p(z)=z^n-1`. Both families
in (7) do attain the stated sum, proving the converse and the classification.

The degree restriction matters: in degree three,
`p(z)=(z-1)(z^2+(8/5)z+1)` has unit-circle roots and real critical points,
so it attains the boundary first-power sum two but belongs to neither
family. The two critical points have discriminant `216/25>0` and lie
strictly between minus one and one. There is no third elementary
symmetric function when `m=2`, so the coefficient saturation argument
does not apply.

Return to degree nine. Any sequence of putative failures with `a_k -> 1`
has `mu_k -> 1` and `D_k -> 0` by section 6. Monic polynomials with roots
in the unit disk form a compact coefficient set. The reciprocal bounds
`1/(1+a_k)<=|q_j|<=R` prevent a derivative root from approaching `a_k`;
indeed `|p'_k(a_k)|=9/prod_j|q_j|>=9/(9/2)^8>0`.

Each coefficient limit therefore has a simple root at one and a finite
reciprocal sum equal to eight. Classification (7) permits only `z^9-1`
and `(z-1)(z+1)^8`. Their reciprocal-modulus variances are respectively
zero and `7/4`. The latter is excluded by (6), since its variance exceeds
one. Every convergent subsequence consequently has limit `z^9-1`, and
compactness gives the full conclusion

\[
p_k\longrightarrow z^9-1\quad\hbox{coefficientwise},\qquad
\max_j|\zeta_{j,k}|\longrightarrow0.\tag{8}
\]

The root multisets also converge to the ninth roots of unity. Thus possible
near-boundary failures of the **first-power** inequality are reduced to
the binomial configuration, even though the hypothesis is weaker than
requiring every critical distance to be at least one. This is a conditional
concentration theorem; it does not assert that failures exist or exclude
all perturbations of the binomial configuration.

## Trust boundary

Sections 1, 3--6 are written analytic arguments. Section 2 uses a finite
exact certificate, independently reproducible by two standard-library
checkers using different coefficient algorithms. Section 7 uses a symbolic
coefficient argument and Maclaurin's inequalities; `verify_boundary.py`
checks exact positive families and the degree-three exception, not the
universal analytic step. The coefficient identity
and every positivity decision are exact;
no search completeness or floating-point tolerance is assumed. No external
formalization is imported as a mathematical dependency. Neither the full
first-power conjecture nor the already solved Sendov theorem is claimed as
a new result of this contribution.
