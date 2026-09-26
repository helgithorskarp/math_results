# An exact analytic reduction and a transport obstruction

Status: complete author proofs of the reductions and obstruction below;
unformalized, with independent review pending. **The three-dimensional
Gaussian majorisation conjecture remains open.** No negative Gaussian
contraction certificate is supplied here.

## 1. Normalization and the exact Hankel criterion

Let `s>0`, let `mu` be a probability measure on `R^3`, and let `T` be a
global contraction. Write

\[
C=(2\pi s)^{-3/2},\quad f=\mu*\gamma_s,\quad
g=T_\#\mu*\gamma_s,\quad F=f/C,\quad G=g/C.
\]

Thus `0<F,G<=1` and `C integral F=C integral G=1`. The desired
majorisation is equivalent to

\[
H(t):=C\int_{\mathbb R^3}\big[(G(z)-t)_+-(F(z)-t)_+\big],dz\geq0
\quad(0\leq t\leq1).                                      \tag{1}
\]

This is the usual hinge characterization. For clarity about the endpoint
at zero, a convex energy continuous there can first be replaced on
`[0,epsilon]` by its chord from zero, keeping it unchanged above epsilon.
These convex approximants decrease to the original energy and have finite
right derivative at zero. Each is a positive mixture of hinges plus a
linear term; equal masses cancel the linear term. On `[0,1]` all are
bounded above by a common multiple of the density. Monotone convergence
after subtracting them from that multiple gives the extended-valued
statement. If a finite convex energy with value zero at zero is
discontinuous there, its right limit is negative and its integral against
either strictly positive Gaussian-smoothed density is `-infinity`.

Define, for integers `k>=2` and `j>=0`,

\[
d_k=C\int(G^k-F^k),\qquad
a_j=\frac{d_{j+2}}{(j+1)(j+2)},\qquad
\mathsf H_m=(a_{i+j})_{0\leq i,j\leq m}.                    \tag{2}
\]

**Theorem 1.** For this particular pair `(f,g)`, the following are equivalent:

1. `f` is majorised by `g`.
2. Every matrix `H_m` in (2) is positive semidefinite.
3. For every real polynomial `p`, the convex polynomial
   \[
   U_p(r)=\int_0^r(r-t)p(t)^2\,dt                         \tag{3}
   \]
   satisfies `C integral[U_p(G)-U_p(F)]>=0`.

If a matrix fails to be positive semidefinite, its negative quadratic
form may be chosen with **rational coefficients**. The corresponding
`U_p` is globally convex, not just convex on the attained density range.

**Proof.** Dominated convergence, using `(F-t)_+<=F` and `(G-t)_+<=G`,
shows that `H` is continuous on `[0,1]`, with `H(0)=H(1)=0` and `|H|<=1`.
Tonelli, applied to the two nonnegative terms separately, gives

\[
\int_0^1t^jH(t)\,dt
=C\int\frac{G^{j+2}-F^{j+2}}{(j+1)(j+2)}=a_j.             \tag{4}
\]

For `p(t)=sum_(i=0)^m v_i t^i`, another application gives

\[
v^T\mathsf H_m v=\int_0^1p(t)^2H(t)\,dt
=C\int[U_p(G)-U_p(F)].                                   \tag{5}
\]

Nonnegativity of `H` therefore implies both assertions. Conversely, if
`H(t0)<0`, continuity provides a nonnegative continuous function `b`,
supported in a negative interval, with `integral b H<0`. Uniform
polynomial approximation to `sqrt(b)` gives a polynomial `p` with
`integral p^2 H<0`. For completeness, the approximants can be the
Bernstein polynomials: uniform continuity bounds their near-diagonal
error, and the binomial variance bound makes the complementary error
uniformly small. Hence no abstract moment representation theorem or
support-localizing matrix is needed here. Finally a strictly negative
quadratic form remains negative under sufficiently small perturbations
of its finitely many coefficients, which may therefore be rational.
Equation (3) has `U_p(0)=U_p'(0)=0` and `U_p''=p^2>=0` on the whole real
line. This proves all claims. QED.

In physical density coordinates use `V(rho)=C U_p(rho/C)`. Then `V` is
convex, `V(0)=0`, and its internal-energy gap is exactly (5).

The first nontrivial matrix gives the necessary condition

\[
3d_2d_4\geq2d_3^2.                                      \tag{6}
\]

Indeed for `p(t)=t-b`, the gap is
`d4/12-b*d3/3+b^2*d2/2`. If `d2>0`, its minimum occurs at
`b=d3/(3*d2)`. A strict failure of (6) has a nearby rational `b` giving a
strictly negative gap. This quartic subtest was independently identified
in the team's adversarial research lane. The result here is the complete
hierarchy and the finite-witness equivalence, not a claim that (6) fails.

## 2. Finite Gaussian certificates use only labelled distances

Let `mu=sum_(i=1)^N w_i delta_(x_i)` with positive weights summing to one,
and let `y_i=T(x_i)`. Gaussian integration of `k` replicas gives

\[
J_k(x):=C\int F(z)^k,dz
=k^{-3/2}\sum_{i_1,\ldots,i_k}
 \left(\prod_{a=1}^kw_{i_a}\right)
 \exp\!\left[-\frac1{2ks}\sum_{a<b}|x_{i_a}-x_{i_b}|^2\right]. \tag{7}
\]

To check (7), use
`sum_a |z-x_(i_a)|^2=k|z-xbar|^2+k^(-1)sum_(a<b)|x_(i_a)-x_(i_b)|^2`
and integrate the first Gaussian. Thus `d_k=J_k(y)-J_k(x)`.
Each summand increases under a contraction, explaining the familiar
`d_k>=0`. Nonnegative entries alone do not prove that a Hankel matrix is
positive semidefinite.

Grouping the ordered tuples by counts `alpha_i`, `sum alpha_i=k`, rewrites
the sum before its common factor as

\[
\sum_{|\alpha|=k}\frac{k!\prod_iw_i^{\alpha_i}}{\prod_i\alpha_i!}
\exp\!\left[-\frac1{2ks}\sum_{i<j}\alpha_i\alpha_j|x_i-x_j|^2\right].
                                                               \tag{8}
\]

For rational points, weights and variance, this is a finite sum of
exponentials of rational numbers with rational coefficients, multiplied
by `1/(k sqrt(k))`. A rational vector `v`, exact distance comparisons,
and outward enclosures proving `v^T H_m v<0` form a complete finite
counterexample certificate. A finite contraction extends to a global
one by the classical Kirszbraun theorem.

**Theorem 2 (completeness for the named bounded-law problem).** If any
bounded probability measure in `R^3` and global contraction violate
majorisation after Gaussian convolution, then such a violation exists
with `s=1`, finitely many distinct rational input points, rational output
points, positive rational weights, strictly contracted distances between
distinct input points, and a rational polynomial `p` in (3).

**Proof.** Scale space by `1/sqrt(s)` first. A failed hinge comparison has
a strictly negative margin. Approximate the original input by a finite
quantization choosing representatives from its bounded support, carrying
their original images under `T`. The elementary translation bound

\[
\|\gamma_s(\cdot-u)-\gamma_s(\cdot-v)\|_1
\leq\sqrt{2/\pi}\,|u-v|/\sqrt{s}                         \tag{9}
\]

follows by integrating the directional derivative of the Gaussian along
the joining segment. It proves `L1` convergence of both smoothed laws.
Every hinge functional is `1`-Lipschitz in `L1`, so the negative margin
persists. Remove zero weights and combine repeated input points.

Replace all finitely many output points by `(1-epsilon)y_i`. As
`epsilon` decreases to zero the smoothed output converges in `L1`.
For every distinct input pair this replacement makes its squared-distance
deficit strictly positive, even if its output points coincide. Finitely
many strict inequalities and the failed hinge sign persist under small
perturbations of all coordinates and weights. Choose those perturbations
rational, preserving positive weights of sum one (approximate the first
`N-1` and use their complement for the last). Apply Theorem 1 to the
resulting pair, and perturb a negative polynomial vector to rational
coefficients. This gives the asserted data. QED.

Increasing rational-enclosure precision eventually certifies any such
strictly negative finite witness. This is a mathematical completeness
statement, not a feasible time bound for exhaustive search. The supplied
checker has explicit precision and workload limits and can report
inconclusive precision. Passing finitely many tests proves no universal
majorisation assertion.

The strict rational **atomic** reduction was independently established
in the geometric lane's now-published
[paired-rank proof, Section 4](../gaussian_majorisation_rank_abel/PROOF.md).
The argument is included here for a self-contained checker contract;
that atomic reduction is not claimed as a separate new discovery. Its
combination with Theorem 1 supplies the rational globally convex polynomial
certificate. The paired-rank theorem further restricts any counterexample
to at least seven atoms and joined affine rank six. The checker does not
need to assume or implement that screening theorem to validate a witness.

## 3. The exact missing positivity after the standard lift

This section assumes bounded `mu` so all path differentiations are
dominated by Gaussian tails. It identifies the structural obligation
that the analytic proof lane still has to establish.

Use the standard path in `R^6`

\[
c_t(x)=\left(\frac{x+Tx}{2}+\cos(\pi t)\frac{x-Tx}{2},
             \sin(\pi t)\frac{x-Tx}{2}\right).
\]

Put `Delta(x,x')=|x-x'|^2-|Tx-Tx'|^2>=0` and

\[
\omega_t(x,x')=-\partial_t|c_t(x)-c_t(x')|^2
=\frac\pi2\sin(\pi t)\Delta(x,x').                       \tag{10}
\]

Let `C6=(2*pi*s)^(-3)`, `q_t=(c_t)_#mu*gamma_s^(6)`, and

\[
M_t(z)=\iint\omega_t(x,x')\gamma_s^{(6)}(z-c_t(x))
                  \gamma_s^{(6)}(z-c_t(x')),d\mu(x)d\mu(x').
\]

Define a finite positive measure `eta` on `[0,1]` by

\[
\int\psi(u),d\eta(u)
=\int_0^1\int_{\mathbb R^6}
 \psi(q_t(z)/C6)\frac{M_t(z)}{C6},dz,dt.                  \tag{11}
\]

This is well defined: `0<q_t/C6<=1` and
`eta([0,1])<=E Delta/8`, by integrating the product of two Gaussians and
using `integral_0^1 omega_t dt=Delta`.

Differentiating the replica identity (7) in dimension six and using
exchangeability gives

\[
C6\int\left[(q_1/C6)^k-(q_0/C6)^k\right]
=\frac{k-1}{4s}\int u^{k-2},d\eta(u).                    \tag{12}
\]

One can verify the coefficient directly: differentiating the exponential
gives `1/(2ks)`, and there are `k(k-1)/2` identical pair terms. Reassembling
the Gaussian product yields (11). Bounded support justifies differentiation
and Fubini; the integrands involve bounded center velocities times
Gaussian tails.

At either endpoint the density is the corresponding three-dimensional
density times an independent three-dimensional Gaussian. Its normalized
`k`-th moment has an extra factor `k^(-3/2)`. Consequently (12) is exactly

\[
\boxed{\displaystyle
a_j=\frac{\sqrt{j+2}}{4s}\int u^j,d\eta(u).}              \tag{13}
\]

Thus the full dimension-three conjecture is equivalent to positivity of
every Hankel matrix of the sequence in (13) **for measures `eta` that
actually arise from (11)**. This is an exact one-dimensional analytic
target, retaining the geometric constraint instead of discarding it.

The square-root multiplier is a real obstruction to an abstract positivity
argument. For an arbitrary positive measure `eta=delta_r`, `0<r<=1`,
the determinant of its first transformed Hankel matrix is

\[
\frac{r^2}{16s^2}(2\sqrt2-3)<0.                          \tag{14}
\]

This artificial measure is **not** asserted to arise from a contraction.
It proves only that positivity and total-mass bounds for `eta` do not
suffice. In the corresponding two-dimensional lift, the multiplier is
`1` rather than `sqrt(j+2)`, and the matrices are automatically positive.
This matches the dimension boundary in Aishwarya--Li.

Already the quartic test demands, writing `m_j=integral u^j d eta`,

\[
2\sqrt2\,m_0m_2\geq3m_1^2.                              \tag{15}
\]

Ordinary Cauchy--Schwarz gives only `m0*m2>=m1^2`; it misses the factor
`3/(2 sqrt(2))>1`. Establishing (15), or the full hierarchy, from the
specific Gaussian geometry in (11) remains an open step here.

There is an exact connection to the geometric lane's retained half-order
comparison. Define its normalized profile

\[
B(t)=\frac1{\sqrt\pi}\int_0^\infty H(te^v)e^{-v}v^{-1/2}\,dv,
\]

with `H=0` above one. That lane proves `B>=0` using the three auxiliary
Gaussian coordinates. Direct substitution gives
`integral_0^1 t^j B(t)dt=a_j/sqrt(j+2)`.
Comparing (13) therefore yields the **measure identity**
`d eta(t)=4s B(t)dt`, since finite signed measures on `[0,1]` with the same
polynomial moments agree by uniform polynomial approximation. Thus (13)
does not purport to establish a stronger qualitative comparison than
that half-order result. It supplies its exact moment-matrix form and a
finite polynomial certificate for failure of the missing unsmoothed sign.

## 4. Every fixed orthogonal common-noise alignment can fail

The following obstruction concerns a particular attempted transport
proof. It is not a counterexample to majorisation.

Let `X~mu`, `Z~N(0,s I3)` independently, and fix any orthogonal matrix `Q`.
Couple the smoothed laws by

\[
A=X+Z,\qquad B=T(X)+QZ.                                  \tag{16}
\]

Let `K_Q(b, da)` be the conditional law of `A` given `B=b`. This is a
Markov kernel taking density `g` to density `f`. For finite `mu`, its
action on Lebesgue measure has density

\[
R_Q(a)=\int\frac{\gamma_s(a-x)}
 {g(Tx+Q(a-x))},d\mu(x).                                \tag{17}
\]

Indeed the conditional probability of label `x` at `b` is
`gamma_s(b-Tx)dmu(x)/g(b)`, and for that label
`a=x+Q^T(b-Tx)`. Changing variables has unit Jacobian and gives (17).
The standard sub-bistochastic Jensen proof of majorisation would require
`R_Q(a)<=1` almost everywhere. This row condition, together with the
Markov column condition, ensures that convex functions with value zero
at zero contract after integration.

**Theorem 3.** For every `r>0`, `0<epsilon<1`, take

\[
\mu=(1-\epsilon)\delta_0+
 \frac\epsilon2(\delta_{-r e_1}+\delta_{r e_1}),\qquad
T(x_1,x_2,x_3)=(|x_1|,x_2,x_3).
\]

Then `R_Q(0)>1` for **every** `Q in O(3)`. Consequently every coupling
(16) fails the required row condition on a nonempty open set.

**Proof.** Write `A0=r^2/s`, `h=exp(-A0/2)` and
`c=<e1,Qe1> in [-1,1]`. Define

\[
Z_0=1-\epsilon+\epsilon h,\qquad
Z_\pm=(1-\epsilon)e^{-A0(1\mp c)}+\epsilon h.
\]

Substitution in (17) gives

\[
R_Q(0)=\frac{1-\epsilon}{Z_0}
 +\frac{\epsilon h}{2}\left(\frac1{Z_+}+\frac1{Z_-}\right).
                                                               \tag{18}
\]

The arithmetic mean of `Z+` and `Z-` is at most

\[
\bar Z=(1-\epsilon)\frac{1+e^{-2A0}}2+\epsilon h<Z_0,
\]

because `cosh(A0*c)<=cosh(A0)` and `A0>0`. The arithmetic-harmonic
mean inequality now yields the uniform strict lower bound

\[
R_Q(0)\geq\frac{1-\epsilon}{Z_0}+\frac{\epsilon h}{\bar Z}>1.
                                                               \tag{19}
\]

For each `Q`, (17) is continuous, so the violation is not confined to a
single point. The map `T` is globally 1-Lipschitz. QED.

This obstruction persists arbitrarily close to the rigid equality regime.
For this family the optimal squared rigid-motion error and the second
normalized moment gap are, exactly,

\[
\rho^2=r^2\epsilon(2-\epsilon),\qquad
d_2=\frac{\epsilon^2(1-e^{-r^2/s})}{4\sqrt2}.              \tag{20}
\]

The first formula follows from zero centered cross-covariance and the
two variances; the second follows because only the pair `(-r e1,r e1)`
changes its distance in (7). Both vanish as `epsilon` tends to zero,
while (19) stays strictly greater than one for each positive epsilon.
Thus choosing a Procrustes alignment, even with the covariance-free
rigidity estimate, does not repair this exact transport condition.
Other, input-dependent or randomized couplings are not ruled out.

## 5. Scope of the handoff

Theorems 1--2 give an exact finite certificate format for any negative
answer to the named bounded-law problem. Equation (13) identifies the
additional positivity that a proof must extract from the lifted geometry.
Theorem 3 eliminates one natural route from approximate rigid alignment
to a sub-bistochastic kernel.

No matrix has been proved positive for all three-dimensional contractions.
No admissible negative certificate has been found. No new Kneser--Poulsen
case follows from the present reductions alone. A positive resolution of
(13) for all admissible lifts would give full majorisation, and the
geometric implication would then follow from Aishwarya--Li's theorem.
