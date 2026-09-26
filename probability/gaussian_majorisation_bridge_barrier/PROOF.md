# A precise obstruction to an energy-only majorisation bridge

Author proof, 26 September 2026. Independent review of this new result pending.
All logarithms are natural. Gaussian variance means covariance `s I`.

## 1. Statement and scope

Let

\[
p=(1,1,4,4,4,4)/18,\qquad q=(2,2,2,2,2,8)/18,
\]

and, for `i=0,...,5`, let
`C_i=[3i,3i+1] x [0,1] x [0,1]`. Define probability densities

\[
f_0=\sum_{i=0}^5p_{i+1}1_{C_i},\qquad
g_0=\sum_{i=0}^5q_{i+1}1_{C_i},\qquad
f_s=f_0*\gamma_{3,s},\quad g_s=g_0*\gamma_{3,s}.
\]

Both input measures are supported in the radius-nine ball centered at
`(8,1/2,1/2)`.

**Theorem A (Gaussian entropy obstruction).** At `s=10^-8`,

\[
h_\alpha(f_s)-h_\alpha(g_s)>\frac{4541}{90000}
\quad\text{for every }1\le\alpha\le\infty,                       \tag{1}
\]

but

\[
\int(g_s-1/9)_+-\int(f_s-1/9)_+
 <-\frac{4973}{45000}.                                         \tag{2}
\]

Consequently `f_s` is not majorised by `g_s`. More generally, for every
`a>0` there is `s_a>0` such that, for every `0<s<s_a`, the strict entropy
inequality holds simultaneously for every `alpha>=a`, including infinity,
while the majorisation inequality fails.

The measures in this theorem are not related by a 1-Lipschitz pushforward.
This is an obstruction to a geometry-free entropy implication, **not** a
counterexample to Aishwarya--Li's conjecture.

**Theorem B (complete PC2 obstruction and near equality).** For every energy
density `U` in Aishwarya--Li's second pressure class,

\[
\int U(f_0)\le\int U(g_0),                                    \tag{3}
\]

although the hinge gap at `1/9` is `-1/9`. The same PC2 ordering holds for
the densities with respective cell heights

\[
p_i^\varepsilon=(1-\varepsilon)/6+\varepsilon p_i,\qquad
q_i^\varepsilon=(1-\varepsilon)/6+\varepsilon q_i,
\quad 0<\varepsilon\le1.
\]

Their hinge gap at `(1-epsilon)/6+epsilon/9` equals `-epsilon/9`, while

\[
h_1(p^\varepsilon)-h_1(q^\varepsilon)
 =\varepsilon^2/6+O(\varepsilon^3).                            \tag{4}
\]

They converge to the same uniform density in total variation. Thus even
all PC2 inequalities plus arbitrarily small entropy loss and density
distance do not imply majorisation for general bounded densities.
Theorem B does not assert all-PC2 ordering of `f_s,g_s` for positive `s`.

## 2. The threshold information that is missing

For any two bounded probability densities `f,g`, write

\[
H(t)=\int(g-t)_+-\int(f-t)_+,\qquad
J(t)=\int_t^\infty H(r)r^{-2}\,dr\quad(t>0).
\]

The integrals are finite: each excess-mass integral lies in `[0,1]`, and
both vanish above the larger essential supremum. The excess-mass functions
are continuous at every positive threshold, by dominated convergence.
Hence

\[
J'(t)=-H(t)/t^2.                                               \tag{5}
\]

Majorisation is equivalent to `H(t)>=0` at every positive threshold,
using the usual integral representation of convex functions by hinges.
Equivalently, **J must be nonincreasing**. Its limit at infinity is zero.

Define the convex generator

\[
V_t(u)=\begin{cases}
0,&0\le u\le t,\\
u/t-1-\log(u/t),&u>t.
\end{cases}
\]

Its pressure is `(log(u/t))_+`, which is convex as a function of `log u`;
therefore `V_t` belongs to PC2, including in the source's finite-difference
definition. The identity

\[
V_t(u)=\int_t^\infty (u-r)_+r^{-2}\,dr
\]

and Tonelli give

\[
\int V_t(g)-\int V_t(f)=J(t).                                 \tag{6}
\]

Each of the two integrals is finite, since `0<=V_t(u)<=u/t`.
Thus the currently available PC2 comparisons for a contraction in `R^3`
imply `J>=0`. The missing assertion is the derivative sign in (5).
Differentiating a family of inequalities `J(t)>=0` does not supply it.
Theorem B exhibits precisely this failure, even with every PC2 test allowed.

## 3. An exact PC2 separation

First use the unnormalized cell heights
`p*=(1,1,4,4,4,4)` and `q*=(2,2,2,2,2,8)`. Their difference of hinge sums is

\[
H_*(r)=\begin{cases}
0,&r\le1,\\
2-2r,&1\le r\le2,\\
3r-8,&2\le r\le4,\\
8-r,&4\le r\le8,\\
0,&r\ge8.
\end{cases}                                                   \tag{7}
\]

It is negative on `(1,8/3)` and positive on `(8/3,8)`. Direct integration gives

\[
\int_1^8 H_*(r)r^{-2}dr
 =(1-2\log2)+(-2+3\log2)+(1-\log2)=0.                         \tag{8}
\]

For a smooth PC2 density `U`, the function
`w(r)=r^2 U''(r)` is nonnegative and nondecreasing: it is the derivative
of `P(e^x)` in `x=log r`, and this pressure is convex and nondecreasing.
Since the cell counts and total masses of the two height lists agree,
Taylor's integral formula on `[1,8]` cancels both affine terms and gives

\[
\sum U(q_i^*)-\sum U(p_i^*)
 =\int_1^8 w(r)H_*(r)r^{-2}dr
 =\int_1^8 [w(r)-w(8/3)]H_*(r)r^{-2}dr\ge0.                  \tag{9}
\]

There is no smoothness restriction on the conclusion. Under the source's
PC2 definition, `P(e^x)` has nonnegative second finite differences and is
locally bounded, hence is convex. It is therefore locally absolutely
continuous, with nondecreasing derivative. Since
`dP(r)=r dU'_+(r)` as measures on `(0,infinity)`, the measure `U''`
has a locally integrable density there. The same nondecreasing function
`w(r)=d[P(e^x)]/dx` supplies (9), with its almost-everywhere representative.
Taylor's integral formula on a compact positive interval remains valid.
Possible behavior at zero is irrelevant, since both lists have six
positive entries and both spatial densities vanish elsewhere.

Positive rescaling of the argument preserves PC2. Applying (9) to
`U(r/18)` proves (3). Formula (7) gives the stated negative hinge gap.
It also gives `J(t)>=0` directly: above the sign-change point the remaining
integrand is positive, and below it use the zero total integral (8).

For the near-equality statement, PC2 is also preserved by
`U(r) -> U(A+B r)-U(A)`, where `A>=0, B>0` (with the obvious interpretation
at `A=0`). Indeed its curvature weight is

\[
r^2 B^2 U''(A+Br)
 =\left(\frac{Br}{A+Br}\right)^2 w(A+Br),
\]

a product of nonnegative nondecreasing functions. Apply this with
`A=(1-epsilon)/6`, `B=epsilon/18`. The hinge formula follows by an affine
change of threshold. Taylor expansion of `r log r` around `1/6` has
uniformly bounded third derivative for small epsilon. Constant and first
order terms cancel, and

\[
\sum q_i^2-\sum p_i^2=1/18
\]

gives the coefficient `(6/2)(1/18)=1/6` in (4). This proves Theorem B.

## 4. All positive entropy orders for the finite example

For `alpha>0`, set `r=2^alpha`. Directly,

\[
\sum q_i^\alpha-\sum p_i^\alpha
 =18^{-\alpha}(r^3-4r^2+5r-2)
 =18^{-\alpha}(r-1)^2(r-2).                                   \tag{10}
\]

It has the correct strict sign on either side of `alpha=1`. Differentiation
at one gives

\[
h_1(p)-h_1(q)=\log2/9,
\]

and the infinity-order gap is `log 2`. Consequently the gap is continuous
and strictly positive on every compactified order interval `[a,infinity]`,
`a>0`.

For a uniform lower bound when `alpha>=1`, put

\[
R(r)=\frac{r(r^2+5)}{4r^2+2}.
\]

An exact calculation shows

\[
r\frac{d}{dr}\log R(r)-\frac19
 =\frac{4(r^2-4)(8r^2-5)}{9(r^2+5)(4r^2+2)}\ge0
 \quad(r\ge2).
\]

Since `R(2)=1`, integration yields

\[
h_\alpha(p)-h_\alpha(q)
 =\frac{\log R(2^\alpha)}{\alpha-1}\ge\log2/9,
 \quad 1\le\alpha\le\infty,                                  \tag{11}
\]

with endpoints understood by continuity.

## 5. Gaussian smoothing preserves enough entropy information

Let `k_s=1_[0,1]^3 * gamma_(3,s)`. It has integral one. If a density is a
mixture of translates of `k_s` with weights `v_i`, then, for every positive
Renyi order (also Shannon and infinity),

\[
h_\alpha\left(\sum_i v_i k_s(\cdot-c_i)\right)
 \le H_\alpha(v)+h_\alpha(k_s).                               \tag{12}
\]

For orders above one, use `(sum a_i)^alpha>=sum a_i^alpha` and divide by
`1-alpha<0`; below one use the reversed power inequality. At Shannon order
condition on the finite mixture label, or take the continuous limit. At
infinity, the supremum is at least `max_i v_i` times `||k_s||_infinity`.

Convolution by a probability kernel cannot decrease any positive Renyi
entropy: apply Jensen to the power integral, or to `u log u`, and use the
supremum bound for infinity. Therefore

\[
h_\alpha(f_s)-h_\alpha(g_s)
 \ge H_\alpha(p)-H_\alpha(q)-h_\alpha(k_s).                    \tag{13}
\]

Renyi entropy is nonincreasing in its order. For `alpha>=1`, it remains to
bound `h_1(k_s)`. By product structure this is three times the entropy of
`W=U+sqrt(s)Z`, with `U` uniform on `[0,1]` and `Z` standard normal.

Put `eta=P(W notin [0,1])`. Conditioning on `Z` gives

\[
\eta\le E|\sqrt{s}Z|=\sqrt{2s/\pi}<10^{-4}
 \quad\text{at }s=10^{-8}.
\]

The entropy inside the interval is at most zero. Conditional outside,
the variance is at most `(1/12+s)/eta`, so the Gaussian maximum-entropy
bound and the binary-entropy decomposition yield

\[
h_1(W)\le h_{\rm bin}(\eta)
 +\frac\eta2\log\frac{2\pi e(1/12+s)}\eta
 \le \eta+\frac32\eta\log(1/\eta)+\frac\eta2\log3.
\]

Here `2 pi e(1/12+s)<3`, using `pi<4` and `e<3`. Since
`eta log(1/eta)` increases for `eta<1/e`, `log 10000<10`, and `log3<2`,

\[
h_1(W)<17/10000,\qquad h_1(k_s)<51/10000.                    \tag{14}
\]

Combining (11)--(14) and `log2>1/2` gives (1):
`1/18-51/10000=4541/90000`.

For the more general assertion at every order `alpha>=a>0`, let the
positive minimum of the gap in (10) on `[a,infinity]` be `delta_a`.
As `s` decreases to zero, `h_a(k_s)` tends to zero. To justify this, `k_s`
tends almost everywhere to the unit-cube indicator and is bounded by one.
For `s<=1`, outside a fixed enlargement of the cube it has a common
Gaussian upper bound. Its positive powers thus admit an integrable common
bound; at order one use `|u log u|<=C u^(1/2)` there. Dominated convergence
gives the claim for every fixed positive finite order. If needed at
infinity, the supremum tends to one by evaluating at the cube center.
Since `h_alpha(k_s)<=h_a(k_s)`, (13) gives simultaneous strict positivity
for all `alpha>=a` once `s` is small enough.

## 6. A certified negative hinge gap after smoothing

For equal-mass integrable densities `v,w`,

\[
\left|\int(v-t)_+-\int(w-t)_+\right|
 \le\tfrac12\|v-w\|_1.                                      \tag{15}
\]

Indeed the integrand difference has the sign of `v-w` and is bounded in
absolute value by it; bound either signed integral by its positive part.

For the unit cube `C`, translation by `z` changes its indicator in L1 by
at most `2 sum_j |z_j|`. Averaging over the Gaussian shift gives

\[
\|k_s-1_C\|_1\le6\sqrt{2s/\pi}.
\]

The triangle inequality and the weights summing to one give the same
bound separately for `||f_s-f_0||_1` and `||g_s-g_0||_1`. Applying (15)
twice, at `t=1/9`, proves

\[
H_s(1/9)\le-1/9+6\sqrt{2s/\pi}
 <-1/9+3/5000=-4973/45000
\]

when `s=10^-8`. This also stays negative for all sufficiently small `s`,
completing Theorem A.

## 7. Consequence for the team's named problem

The source theorem in dimension three supplies the PC2 comparisons, hence
`J>=0` for an actual contraction pair. Entropy rigidity supplies geometric
closeness when a deficit is small; the audited quantitative consequence in
AUDIT.md bounds the magnitude of `H` but not its sign. The examples above
show why discarding the contraction geometry cannot supply that sign.

For completeness, the unsmoothed examples cannot themselves be related by
a 1-Lipschitz pushforward. Such a map sends a set of Lebesgue volume at
most `v` into a set of volume at most `v`, and the image has at least the
original probability mass. Taking the supremum over sets of volume `v`
would imply majorisation of the input density by the output density,
contradicting (7). The Gaussian examples therefore lie outside the
contraction hypothesis, as required for the stated scope.

A successful bridge still needs contraction-specific control of `J'`,
or an equivalent signed threshold estimate. No new Kneser--Poulsen case,
all-PC2 Gaussian counterexample, or counterexample to Conjecture 1.1 is
claimed here.
