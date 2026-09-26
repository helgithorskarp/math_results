# Paired affine rank and the half-order gap in Gaussian majorisation

Author proof attempt, 26 September 2026. External review pending.
The full three-dimensional conjecture is **not resolved** here. The negative
result below concerns cancellation of an auxiliary Gaussian, not a contraction
counterexample.

Let $\phi_{n,s}$ be the centred Gaussian density with covariance $sI_n$.
For a probability density $f$ define its hinge profile

$$
H_f(a)=\int(f-a)_+\,dx,\qquad a>0.
$$

We write $f\preceq g$ when $H_f(a)\le H_g(a)$ for every $a>0$; this is the
usual majorisation order, equivalently comparison by convex internal energies.
For $\beta>0$, let $F_\beta(t)$ be the Gamma$(\beta,1)$ distribution function,
set to zero for $t\le0$, and set

$$
R_{\beta,f}(a)=\int f(x)F_\beta(\log(f(x)/a))\,dx.
\tag{1}
$$

The integrand is zero when $f=0$. These functionals lie between zero and one.

## 1. Results

Let $K\subset\mathbb R^3$ be compact, $T:K\to\mathbb R^3$ be 1-Lipschitz,
and $\mu$ be a probability measure on $K$. Put

$$
f=\mu*\phi_{3,s},\quad g=T_\#\mu*\phi_{3,s},\quad
r=\dim\operatorname{aff}\{(x,T(x)):x\in\operatorname{supp}\mu\}.
$$

**Theorem A (rank reduction).** If $r\le5$, then $f\preceq g$ for every
$s>0$. Consequently every measure on at most six points satisfies the full
comparison, with arbitrary atom weights. The conclusion also holds for an
arbitrary bounded measure whenever there is a nonzero linear relation between
its input and output coordinates on its support.

Any failure of the bounded-input conjecture can be witnessed with $s=1$,
finitely many distinct rational input points, rational output points, positive
rational atom weights, a rational threshold, and **strict** contraction of
every distinct input pair. Every such witness has at least seven input points
and paired affine rank six.

**Theorem B (exact comparison retained in rank six).** For arbitrary $r\le6$,

$$
R_{3/2,f}(a)\le R_{3/2,g}(a)\qquad(a>0).
\tag{2}
$$

Equivalently, if $D(a)=H_g(a)-H_f(a)$, then

$$
\frac1{\sqrt\pi}\int_0^\infty
          D(ae^u)e^{-u}u^{-1/2}\,du\ge0\qquad(a>0).
\tag{3}
$$

This retains the actual three auxiliary coordinates rather than adding a fourth
one. In particular it gives convex energy comparisons outside the second
integer pressure class used in the source's three-dimensional statement.

**Theorem C (cancellation fails for probability densities).** There are bounded
compactly supported probability densities $f_0,g_0$ on $\mathbb R^3$ satisfying
all inequalities (2), but

$$
H_{g_0}(2)-H_{f_0}(2)=-\frac1{40}<0.
\tag{4}
$$

The same pair satisfies the strict Rényi-entropy comparison at every positive
order, including Shannon and infinity. Thus even those additional comparisons
do not repair cancellation for arbitrary probability densities.

Thus (3), even together with probability normalization and bounded compact
support of the densities, does not imply the desired unsmoothed inequalities.
Additional information about *Gaussian mixtures related by a contraction* is
essential to any argument that tries to cancel this half-order smoothing.

## 2. A continuous contraction in the paired affine dimension

Fix $x_0\in\operatorname{supp}\mu$ and let

$$
v(x)=(x-x_0,T(x)-T(x_0)),\quad V=\operatorname{span}\{v(x)}\subset\mathbb R^6.
$$

Let $P,Q:V\to\mathbb R^3$ be the two coordinate projections, with adjoints
taken using the inherited Euclidean inner product. Define

$$
A=P^*P,\quad B=Q^*Q,\quad
c_t(x)=((1-t)A+tB)^{1/2}v(x)\in V,\quad 0\le t\le1.
\tag{5}
$$

The positive semidefinite square root is continuous, so each trajectory is
continuous, including singular endpoints. For every pair $x,y$,

$$
|c_t(x)-c_t(y)|^2
 =(1-t)|x-y|^2+t|T(x)-T(y)|^2.
\tag{6}
$$

Thus this is a continuous contraction in $\mathbb R^r$. Its initial and final
configurations are congruent to the original configurations: each endpoint
preserves the respective pair distances. This congruence extends to their
affine spans and then to an ambient Euclidean isometry. Translations and those
isometries preserve Gaussian convolution energies.

This is the usual Gram-interpolation lifting mechanism, with its dimension
made explicit. It does not assert that rank six is an obstruction to *every*
lower-dimensional motion; some rank-six configurations admit other such motions.

## 3. Gaussian density values and Gamma variables

We use [Aishwarya–Li, arXiv:2609.07041v2, Theorem 1.4](https://arxiv.org/html/2609.07041v2):
under a continuous contraction the Gaussian-convolved density value, sampled
according to that density, increases in stochastic order. Equivalently,
all internal energies with nonnegative pressure increase. This theorem only
requires continuity of the trajectories, so it applies to (5).

For a density $h$ on $\mathbb R^3$, let $X$ have density $h$ and let
$Y\sim\phi_{m,s}$ be independent. The value of the product density sampled
from itself has logarithm

$$
\log h(X)+\log C_m-G_{m/2},\qquad
C_m=(2\pi s)^{-m/2},\quad G_{m/2}\sim\operatorname{Gamma}(m/2,1).
\tag{7}
$$

Indeed $|Y|^2/(2s)$ has that Gamma law. Its upper-tail probability at
$\log(aC_m)$ is exactly $R_{m/2,h}(a)$. The threshold factor $C_m$ therefore
cancels between the endpoints; no normalization of the noise variance is hidden.

If $r\le5$, pad (5) to dimension five. At each endpoint the convolution is,
up to isometry, $f\phi_{2,s}$ or $g\phi_{2,s}$. The stochastic comparison and
(7) give $R_{1,f}\le R_{1,g}$. Since

$$
\rho F_1(\log(\rho/a))=(\rho-a)_+,
\tag{8}
$$

this proves Theorem A's comparison. The atom-count consequence uses $r\le N-1$.
A nontrivial affine relation on the paired support is exactly the condition
$r\le5$.

In general pad to dimension six. The same argument with $m=3$ proves (2).
Independent Gamma variables of shapes one and one-half sum to shape three-halves.
Conditioning first on the latter variable proves

$$
R_{3/2,h}(a)=\frac1{\sqrt\pi}\int_0^\infty
                      H_h(ae^u)e^{-u}u^{-1/2}\,du,
\tag{9}
$$

by Tonelli, proving (3). No differentiability of $h$ or inversion formula is
needed for this identity.

For clarity, the associated energy density is
$U_a(\rho)=\rho F_{3/2}(\log(\rho/a))$. For $\rho>a$, put $L=\log(\rho/a)$.
Its pressure and the second logarithmic derivative of that pressure are

$$
P_a(\rho)=\rho U'_a(\rho)-U_a(\rho)
 =\frac{a\sqrt L}{\Gamma(3/2)},\qquad
(\rho\partial_\rho)^2P_a(\rho)
 =-\frac{a}{4\Gamma(3/2)L^{3/2}}<0.
\tag{10}
$$

The pressure is zero below $a$ and continuous and increasing above it, so
$U_a$ is convex. The negative derivative on the open interval $(a,\infty)$
excludes $U_a$ from the source's class $\mathcal{PC}_2$. Thus (2) is a genuine
extension of the test energies in that integer-class assertion, not an inference
from its Rényi-power special cases.

Further Gamma$(1/2,1)$ smoothing of (2) yields the Gamma$(2,1)$ comparison.
The source's twice-applied marginalisation theorem identifies the latter with
all continuous-at-zero $\mathcal{PC}_2$ tests relevant to Gaussian densities.
Thus the retained half-integer comparison implies those integer-class tests
while also providing (10).

## 4. Reduction to strict rational finite witnesses

Suppose $D(a)<0$ for some compactly supported input. Partition its support into
finitely many sets of diameter at most $\delta$, replace each set by a point of
that set, and use the same labels and masses for their images under $T$.
The resulting paired atomic laws can be coupled to the originals with input
and output distances at most $\delta$. For Gaussian translates,

$$
\|\phi_{3,s}(\cdot-b)-\phi_{3,s}(\cdot-c)\|_1
 \le \sqrt{\frac{2}{\pi s}}|b-c|.
\tag{11}
$$

Integrate the directional derivative along the segment from $b$ to $c$ to
prove (11). Mixture averaging gives the same estimate for these coupled laws.
Also $|H_h(a)-H_{h'}(a)|\le\|h-h'\|_1$. Hence sufficiently fine atomic
approximation preserves the strict violation. Zero-mass cells are discarded
and duplicate input points merged.

Rescale space by $1/\sqrt s$ to fix variance one; the hinge threshold rescales
by the density Jacobian. Now multiply all output points by $1-\varepsilon$.
For every distinct input pair the contraction becomes strict. The output
density changes continuously in $L^1$ by (11), so a sufficiently small
$\varepsilon>0$ preserves the violation.

There are finitely many strict pair inequalities. Approximate both lists of
coordinates and the positive masses by rationals sufficiently closely to
preserve them and the violation. Choose rational masses in the probability
simplex; the mixture $L^1$ error from changing weights is at most their
$\ell^1$ error. Finally $H_h(a)$ is continuous at every $a>0$: locally its
Lipschitz constant is at most $1/a_0$ if the thresholds are at least $a_0>0$.
Thus the threshold can also be chosen rational. A finite contraction extends
to all of $\mathbb R^3$ by Kirszbraun's theorem if the global-map formulation
is required. The rank and cardinality restrictions follow from Theorem A.

## 5. Explicit noncancellation certificate

Take disjoint boxes on which $f_0$ has the values

$$
\begin{array}{c|cc}
\text{density value}&1&4\\ \hline
\text{volume}&1/5&1/5\\
\text{probability mass}&1/5&4/5
\end{array}
\qquad
\begin{array}{c|cc}
\text{density value of }g_0&2&8\\ \hline
\text{volume}&1/4&1/16\\
\text{probability mass}&1/2&1/2.
\end{array}
$$

All other density values are zero. For example use boxes of the prescribed
widths times $[0,1]^2$, placing the first at first-coordinate zero and the second
at first-coordinate one. Equation (4) is the exact calculation
$3/8-2/5=-1/40$.

Here is a proof of (2) for this pair at **every** threshold, not a numerical scan.
Write $h=\log2$, $F=F_{3/2}$, and
$\Delta(t)=F(t+h)-F(t)$ for $t\ge0$.
The Gamma density is $k(u)=\sqrt u e^{-u}/\Gamma(3/2)$ for $u>0$.

We will use three elementary bounds:

$$
\Delta(t+h)\ge\tfrac12\Delta(t)\quad(t\ge0),
\tag{12}
$$

$$
\Delta(t+h)\ge\tfrac{\sqrt6}{4}\Delta(t)
   \quad(0\le t\le h),
\tag{13}
$$

$$
\Delta(t+h)\le(1+\sqrt2)\Delta(t)\quad(t\ge0).
\tag{14}
$$

The first two follow by comparing $k(u+h)/k(u)=\tfrac12\sqrt{1+h/u}$
on $u\in[t,t+h]$. For (14), drop the first half of the integral defining
$\Delta(t)$ and bound the square roots in numerator and denominator:

$$
\frac{\Delta(t+h)}{\Delta(t)}
\le\frac{\sqrt{t+2h}}{4\sqrt{t+h/2}(2^{-1/2}-1/2)}
\le1+\sqrt2.
$$

Let $J(a)=2(R_{3/2,g_0}(a)-R_{3/2,f_0}(a))$. The four nonzero regimes are:

* $0<a\le1$. With $t=\log(1/a)$, expansion by successive increments gives
  $J=\tfrac25\Delta(t)-\tfrac35\Delta(t+h)+\Delta(t+2h)$.
  By (12) and (14),
  $J\ge[\tfrac25-\tfrac1{10}(1+\sqrt2)]\Delta(t)>0$.
* $1\le a\le2$. With $t=\log(2/a)\in[0,h]$,
  $J=\tfrac25F(t)-\tfrac35\Delta(t)+\Delta(t+h)>0$ by (13), since
  $\sqrt6/4>3/5$.
* $2\le a\le4$. With $t=\log(4/a)\in[0,h]$,
  $J=F(t+h)-\tfrac85F(t)\ge0$.
  For $t>0$, the interval $[h,h+t]$ lies in $[t,t+h]$, so translation of
  $[0,t]$ gives $F(t+h)-F(t)\ge2^{-1/2}F(t)$.
  Since $2^{-1/2}>3/5$, this proves the assertion; at $t=0$ it is immediate.
* $4\le a<8$. Only the positive term $F(\log(8/a))$ remains.

For $a\ge8$ both sides vanish. All regime endpoints agree, completing the
proof of Theorem C.

By (7), this also says that $f_0\phi_{3,s}$ and $g_0\phi_{3,s}$ satisfy the
entire nonnegative-pressure comparison, for any $s>0$, although $f_0\npreceq g_0$.
These step densities are not asserted to be Gaussian convolutions of inputs
related by a contraction. No conclusion against the original conjecture follows.

For the stated entropy comparison, put $z=2^{p-1}$ for $p>0$, $p\ne1$. Directly,

$$
\int g_0^p-\int f_0^p
 =\frac{(z-1)(5z^2-3z+2)}{10}.
\tag{15}
$$

The quadratic is positive, so the sign is that of $p-1$, which gives
$h_p(g_0)<h_p(f_0)$. At order one,
$\int g_0\log g_0-\int f_0\log f_0=\tfrac25\log2>0$.
The respective maximum densities are 8 and 4, giving the infinity comparison.

## 6. Geometric handoff and prior-work boundary

Theorem A, applied to every probability law on a compact $K$ whose paired rank
is at most five, gives the variable-radius union-volume inequality through
Aishwarya–Li's Theorem 5.1. This geometric consequence is already covered by
the classical Bezdek–Connelly continuous-lifting theorem. We do **not** present
it as a new Kneser–Poulsen case or claim the campaign's geometric goal achieved.

A useful hard test outside this sufficient rank condition is the classical
simplex-flap configuration. Let

$$
u_0=(1,1,1),\ u_1=(1,-1,-1),\ u_2=(-1,1,-1),\ u_3=(-1,-1,1).
$$

For any $b>0$, the 16 labelled input and output points are

$$
p_k=q_k=u_k\ (0\le k\le3),\qquad
p_{ij}=u_j-bu_i,\quad q_{ij}=u_j+bu_i\quad(i\ne j).
\tag{16}
$$

This is a contraction. An anchor/flap squared-distance deficit is $16b$ when
the anchor index is $i$, and zero otherwise; a flap/flap deficit is
$16b(\mathbf1_{j=k}+\mathbf1_{i=l})$. Its paired affine rank is six: the
anchors span the diagonal three-space, and subtracting anchor $j$ from the
paired flap gives $(-bu_i,bu_i)$, spanning the complementary three-space.

[Cheng–Tan–Zheng, arXiv:1107.0140, Theorem 2.1](https://arxiv.org/abs/1107.0140)
proves that the reversed expansion admits no continuous motion in fewer than
six dimensions. Hence (16) admits no continuous contraction in five dimensions.
The construction and that obstruction are prior work, not new theorems here.
The accompanying exact fixture at $b=1$ is supplied to focus experiments on a
configuration that genuinely escapes the known lifting criterion. All choices
of probability weights retain the pairwise contraction; labels mapping to the
same output point are allowed.

The named source supplies the continuous-contraction theorem and its integer
pressure hierarchy. Our contribution is the explicit paired-rank Gaussian
class/reduction, retention of the half-integer comparison, and the normalized
all-threshold cancellation obstruction. These are complete written arguments
subject to review; a targeted literature search is not a priority guarantee.
The exact checker corroborates finite algebra and validated Gamma values. The
universal claims rely on the written proofs and the stated external theorem.

Before publication we inspected the concurrent Team B result
[Gaussian majorisation bridge barrier](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_bridge_barrier/PROOF.md).
It gives an all-$\mathcal{PC}_2$ obstruction and a Gaussian-smoothed entropy
obstruction. Theorem C here concerns the stronger, exact three-coordinate
marginal comparison (2); Theorems A and B supply the complementary geometric
reduction. Neither obstruction provides a contraction counterexample to the open
problem. We cite the team result for context, not as a premise of these proofs.
