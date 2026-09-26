# The global hinge defect: endpoint coupling and a complete moment criterion

Status: complete author proof of the stated equivalences and bounds;
unformalized and awaiting independent review. The unrestricted
three-dimensional contraction problem remains open. The standard
ingredients are credited in [SOURCES.md](SOURCES.md).

## 1. The quantity and its quantifiers

Fix `s>0`, a bounded probability measure `mu` on `R^3`, and a 1-Lipschitz
map `T` on its support. Write

\[
C=(2\pi s)^{-3/2},\quad f=\mu*\gamma_s^{(3)},\quad
g=T_\#\mu*\gamma_s^{(3)},\quad F=f/C,\quad G=g/C.
\]

Both densities are positive, at most `C`, and integrate to one. For any
probability density `p`, let

\[
\mathcal H_p(a)=\int(p-a)_+,\qquad
H(u)=\mathcal H_g(Cu)-\mathcal H_f(Cu),\qquad
\Delta_s=\max_{0\le u\le1}(-H(u))_+.                  \tag{1}
\]

Dominated convergence gives continuity of `H`, with `H(0)=H(1)=0` and
`|H|<=1`. Thus the maximum exists and `0<=Delta_s<=1`. Thresholds above
`C` contribute zero. The hinge characterization of majorisation says
that the desired comparison is exactly `Delta_s=0`. Equivalently all
convex internal energies, with the usual extended-integral convention,
have the desired order. A positive mixture of hinges proves this first
for energies with finite right derivative at zero; convex chord
approximations at zero give the general case. The earlier
[Hankel proof](../gaussian_majorisation_hankel_transport/PROOF.md)
records these endpoint details.

Everything below holds for a fixed pair and a fixed variance. Full
majorisation for that pair at every variance requires `Delta_s=0` for
**every** `s>0`. A statement uniform over a map's domain requires the
additional quantifier over **every** bounded input law. Neither
quantifier follows from the equivalences alone.

## 2. The exact coupling minimum

Let `X` have density `f`, let `U` be independent and uniform on `(0,1)`,
and put `Z_f=U f(X)/C`. Define the law of `Z_g` similarly. Conditional
integration gives the exact identity

\[
\Pr(Z_f>u)=\int f(x)\left(1-\frac{Cu}{f(x)}\right)_+dx
             =\mathcal H_f(Cu)\quad(0\le u\le1).       \tag{2}
\]

**Theorem 1 (endpoint formulation).** With the indicated marginals,

\[
\Delta_s=\min_{\pi\in\Pi(Z_f,Z_g)}\pi\{z_f>z_g\}.   \tag{3}
\]

There is also an exactly equivalent five-dimensional formulation. Set

\[
p_f(x,z)=f(x)\gamma_s^{(2)}(z),\qquad
p_g(y,w)=g(y)\gamma_s^{(2)}(w).
\]

Then

\[
\Delta_s=\min_{\Pi\in\Pi(p_f\,dx\,dz,p_g\,dy\,dw)}
     \Pi\{p_f(x,z)>p_g(y,w)\}.                         \tag{4}
\]

In particular full majorisation is equivalent to the existence of a
coupling in (4) with no failures. This coupling concerns the values of
the endpoint densities. It imposes no martingale condition on positions,
common Gaussian displacement, deterministic map, or continuous motion
of the underlying centres.

**Proof.** We prove a scalar statement valid for any laws `A,B` on
`[0,1]`. Write their distribution functions as `F_A,F_B`, and let

\[
\delta=\sup_t(F_B(t)-F_A(t))\in[0,1].
\]

For every coupling and threshold `t`,

\[
\Pr(A>B)\ge\Pr(A>t,B\le t)
\ge\Pr(A>t)-\Pr(B>t)=F_B(t)-F_A(t).
\]

For the reverse inequality let `Q_A,Q_B` be the generalized quantiles
and `V` uniform on `(0,1)`. Couple

\[
A=Q_A(V),\quad
B=\begin{cases}
Q_B(V+\delta),&V<1-\delta,\\
Q_B(V+\delta-1),&V>1-\delta.
\end{cases}                                           \tag{5}
\]

The cyclic shift preserves the uniform law. Since
`F_A(t)>=F_B(t)-delta`, generalized inverse monotonicity gives
`Q_A(v)<=Q_B(v+delta)` for `0<v<1-delta`. Indeed at
`t=Q_B(v+delta)` the right-continuity of the distribution function gives
`F_B(t)>=v+delta`, and hence `F_A(t)>=v`. Thus failures are restricted
to a set of measure at most `delta`. The lower bound forces equality.
This includes `delta=0,1`; individual interval endpoints are null.
Equation (2) identifies this scalar `delta` with (1), proving (3).

If `W` has density `gamma_s^(2)`, then `|W|^2/(2s)` is exponential with
mean one. Consequently

\[
\gamma_s^{(2)}(W)/\gamma_s^{(2)}(0)
=\exp(-|W|^2/(2s))
\]

is uniform on `(0,1)`. Under the probability density `p_f`, its own
normalized value `p_f(X,W)/(C gamma_s^(2)(0))` has exactly the law of
`Z_f`. Every spatial coupling therefore projects to a coupling in (3).
Conversely, disintegrate the two spatial probability measures over their
density-value maps, and sample the two conditional positions independently
given a scalar coupling. Euclidean spaces are standard Borel, so these
conditional kernels exist and are concentrated on the respective fibres
for almost every value. This lifts (5) without changing the failure
probability, proving (4). This is the same disintegration mechanism as
Aishwarya--Li, Lemma 3.2; here two Gaussian coordinates turn the original
hinges into density-value tails. QED.

## 3. Complete dual tests from the existing replica moments

For integers `m>=2` and `j>=0`, define

\[
d_m=C\int(G^m-F^m),\qquad
a_j=\frac{d_{j+2}}{(j+1)(j+2)}.
\]

Tonelli applied separately to the nonnegative source and target terms
gives the existing hinge moment identity

\[
a_j=\int_0^1u^jH(u)\,du.                              \tag{6}
\]

For `N>=0` and `0<=k<=N`, put

\[
b_{N,k}=(N+1)\binom Nk\sum_{\ell=0}^{N-k}
                (-1)^\ell\binom{N-k}{\ell}a_{k+\ell}.
                                                               \tag{7}
\]

Expanding `(1-u)^(N-k)` yields

\[
b_{N,k}=\int_0^1\beta_{N,k}(u)H(u)\,du,
\quad\beta_{N,k}(u)=(N+1)\binom Nk u^k(1-u)^{N-k}.     \tag{8}
\]

The weight is the probability density of
`Beta(k+1,N-k+1)`. These are the classical Hausdorff finite differences,
normalized as averages. They are not a new moment representation theorem.

Define `D_N=max(0,-min_k b_(N,k))`. We will prove

\[
0\le D_0\le D_1\le\cdots\uparrow\Delta_s.             \tag{9}
\]

In particular the following are equivalent:

* Full majorisation of this pair at this variance.
* A coupling with zero failures in (4).
* `b_(N,k)>=0` for every `N,k`.
* Positive semidefiniteness of every endpoint Hankel matrix
  `(a_(i+j))_(0<=i,j<=m)` from the earlier complete criterion.

The Hankel equivalence follows because its quadratic form is
`integral q(u)^2 H(u) du`: polynomial approximation to the square root
of a continuous nonnegative test supported in a negative interval of
`H` detects any failure. The beta equivalence will also follow directly
from the quantitative convergence below, without invoking a moment
representation theorem.

A negative `b_(N,k)` is already a convex-energy witness. On `[0,1]` take

\[
U(t)=\int_0^t(t-u)\beta_{N,k}(u)\,du.
\]

Then `U(0)=U'(0)=0`, `U''>=0`, and
`C integral[U(G)-U(F)]=b_(N,k)`. Extend `U` linearly above one to obtain
a convex function on `[0,infinity)`. In physical density coordinates use
`V(rho)=C U(rho/C)`. This witness is polynomial on the attained range;
the polynomial itself need not be globally convex outside that range.

For finite input `mu=sum_i w_i delta_(x_i)` and `y_i=T(x_i)`, Gaussian
integration gives

\[
d_m=m^{-3/2}\sum_{i_1,\ldots,i_m}\prod_{a=1}^m w_{i_a}
\left\{
e^{-\sum_{a<b}|y_{i_a}-y_{i_b}|^2/(2ms)}
-e^{-\sum_{a<b}|x_{i_a}-x_{i_b}|^2/(2ms)}\right\}.       \tag{10}
\]

Thus (7) at degree `N` only uses moments through `m=N+2`. Rational input,
weights and variance make these finite exponential sums available to
rigorous ball arithmetic. The distance inequalities must also be checked
to certify a Gaussian-contraction counterexample. Each `d_m>=0` under
a contraction, but the alternating sums (7) have no established universal
sign. The previous rational finite-data reduction shows that any failure
of the bounded-law conjecture has a finite strictly negative moment
witness after rational perturbation. Equations (8)--(9) show that the
beta tests are also complete for such detection; this is a completeness
statement, not a practical complexity bound.

## 4. A uniform finite-order bound over every threshold

The bounded support assumption ensures `integral sqrt(f)` and
`integral sqrt(g)` are finite. Define

\[
K_s=\sqrt C\left(\int\sqrt f+\int\sqrt g\right).
\]

**Theorem 2 (quantitative global criterion).** For every integer `N>=0`,

\[
D_N\le\Delta_s\le\min\{1,D_N+K_s(N+2)^{-1/4}\}.        \tag{11}
\]

If the two supports, after separate translations, lie in balls of radius
`R`, set `r=R/sqrt(s)`. A common explicit upper bound for `K_s` is

\[
K(R,s)=2\sqrt{2/\pi}
\left[\frac{r^3}{3}+\sqrt\pi r^2+4r+2\sqrt\pi\right]. \tag{12}
\]

**Proof.** Every beta average in (8) is at least `-Delta_s`, so
`D_N<=Delta_s`. Degree elevation gives the identity

\[
b_{N,k}=\frac{N+1-k}{N+2}b_{N+1,k}
           +\frac{k+1}{N+2}b_{N+1,k+1}.                \tag{13}
\]

These coefficients are nonnegative and sum to one. The minimum of the
next row is therefore at most the minimum of the current row, proving
the monotonicity in (9).

To obtain a uniform error, consider the classical Bernstein--Durrmeyer
operator

\[
(M_NH)(t)=\sum_{k=0}^N\binom Nk t^k(1-t)^{N-k}b_{N,k}.
                                                               \tag{14}
\]

Choose `J~Bin(N,t)` and, conditionally on `J`,
`V~Beta(J+1,N-J+1)`. Then `(M_NH)(t)=E H(V)`. The first two conditional
moments are `(J+1)/(N+2)` and `(J+1)(J+2)/((N+2)(N+3))`. Consequently

\[
\mathbb E(V-t)^2
=\frac{2[1+(N-3)t(1-t)]}{(N+2)(N+3)}
\le\frac1{N+2}.                                      \tag{15}
\]

For `N<=3` bound the bracket by one; for `N>=3` use
`t(1-t)<=1/4`. Both give the displayed upper bound, including `N=0`.

Pointwise, for `u,v` in `[0,1]`,

\[
|(f-Cu)_+-(f-Cv)_+|
\le\min\{f,C|u-v|\}\le\sqrt{fC}\,|u-v|^{1/2}.
\]

Apply this to both densities and integrate to obtain
`|H(u)-H(v)|<=K_s |u-v|^(1/2)`. Jensen's inequality and (15) imply

\[
\|M_NH-H\|_\infty\le K_s(N+2)^{-1/4}.                \tag{16}
\]

The polynomial (14) is a convex combination of the `b_(N,k)`, hence
is at least `-D_N` everywhere. Equation (16) now proves (11), and also
`D_N -> Delta_s`. If `Delta_s>0`, every degree with
`K_s(N+2)^(-1/4)<Delta_s` must have a strictly negative beta test.

For completeness, centre the support of `mu` in `B(0,R)`. Then

\[
f(x)\le C\exp[-(|x|-R)_+^2/(2s)].
\]

Radial integration of its square root gives

\[
\begin{aligned}
\sqrt C\int\sqrt f
&\le4\pi C\left[\frac{R^3}{3}
  +\int_0^\infty(R+v)^2e^{-v^2/(4s)}\,dv\right]\\
&=4\pi C\left[\frac{R^3}{3}+R^2\sqrt{\pi s}
                   +4Rs+2\sqrt\pi s^{3/2}\right]\\
&=\sqrt{2/\pi}\left[\frac{r^3}{3}
                   +\sqrt\pi r^2+4r+2\sqrt\pi\right].
\end{aligned}
\]

The identical bound for `g` proves (12). Separate translations do not
change hinges or these integrals. A common `R` always exists for a
bounded law and its contraction image. QED.

This is an absolute bound for the full hinge defect. It introduces no
tail sign assumption or new sufficient subclass. Its rate is deliberately
elementary and may require very large moment orders. It makes no claim
about the normalized tail remainder that is obstructed by the team's
two-atom example.

If certified arithmetic gives `b_(N,k) in [l_k,u_k]`, put

\[
L_N=\max_k(-u_k)_+,\qquad U_N=\max_k(-l_k)_+.
\]

Then `L_N<=Delta_s<=min(1,U_N+K(R,s)(N+2)^(-1/4))`. A rigorously
negative upper endpoint certifies a violation. Nonnegative lower
endpoints at finitely many degrees cannot remove the positive error
term. In particular no interchange of fixed variance and unbounded
moment order is justified by finite tests whose required variance grows
with the order.

## 5. Composition, motions and density orbits

It is convenient to write `Delta(f,g)=sup_(a>=0)(H_f(a)-H_g(a))_+`,
which agrees with (1) and needs no chosen common density bound. Directly
from the definition:

* Independent Euclidean isometries applied to `f,g` preserve `Delta`.
* `Delta(f,h)<=Delta(f,g)+Delta(g,h)`.
* For a mixture of sources and **one common target**,
  `Delta(integral f_i d alpha(i),g)<=integral Delta(f_i,g) d alpha(i)`.
* `|Delta(f,g)-Delta(f',g')|<=TV(f,f')+TV(g,g')`, where
  `TV(p,q)=integral|p-q|/2` for probability densities.

The mixture statement follows from convexity of `(p-a)_+` in `p`.
The total-variation constant follows from
`-integral(q-p)_+ <= H_p(a)-H_q(a) <= integral(p-q)_+` and equal
masses. These rules do not assert closure under arbitrary mixtures of
different targets or convolution by a common kernel.

Suppose the support and its image can be joined by a continuous
contracting motion in `R^5`, with endpoints embedded in their original
three-dimensional subspaces. Aishwarya--Li, Theorem 1.4, supplies a
density-value coupling of the endpoint five-dimensional Gaussian laws
with no failures. Endpoint isometries identify their densities with
`p_f,p_g` in (4). Thus **each such motion certifies `Delta_s=0` for every
variance and every input law on its domain**. Motions in lower dimensions
can be padded to five. This is a sufficient construction of the endpoint
coupling, not a necessary one.

If an alternative contraction `R` has `R_#mu=T_#mu`, a motion for `R`
gives the same endpoint criterion for `T`. If source components have
possibly different such motions to one common output law, the mixture
rule completes the argument. These are exactly the output-relabelling
and common-target mechanisms already present in the team's work.

There is also a direct endpoint certificate. For a finite orthogonal
group `Gamma`, orthogonal invariance gives, at every threshold,

\[
\mathcal H_f(a)-\mathcal H_g(a)
=\frac1{|\Gamma|}\int\sum_{Q\in\Gamma}
       [(f(Qx)-a)_+-(g(Qx)-a)_+]\,dx.                  \tag{17}
\]

Thus a nonpositive orbit sum for every `x,a` proves `Delta_s=0` and
therefore yields the same endpoint coupling (4). More quantitatively,
`Delta_s` is at most the integral of the positive maximum of the sum
in (17), divided by `|Gamma|`. This maximum is measurable by taking
the supremum over rational thresholds and is bounded by
`sum_Q f(Qx)`, so the bound is finite. The orbit condition is sufficient;
its failure need not survive spatial integration.

The newly published
[square-cone density-orbit proof](../gaussian_majorisation_square_cone_orbits/PROOF.md)
uses the 48 signed coordinate permutations to prove the sign in (17)
at **every variance**. Its finite partial-order certificate yields full
majorisation throughout the nine-point `L1` weight ball of radius `1/552`
around `(8,12,7,15,44,21,11,23,43)/184`, and for its stated arbitrary
bounded radial laws with directional weights in two polyhedral cones.
Independent review of that computer-assisted proof is pending; the
present implication uses it at its stated status.

This sharpens the separation of transport mechanisms. The entire
previously reviewed radius-`1/4000` obstruction family is inside the new
positive ball. There (4) has a zero-failure coupling for every variance,
while the proposed position-martingale and deterministic common-output
motion-mixture routes remain obstructed, and the labelled centres have
no `R^5` contracting motion. These are restrictions on different
constructions, not on the existence of the endpoint density-value
coupling. The earlier high-variance result is preserved as valid prior
work; its variance restriction has been removed for this family by the
new orbit proof. This is a consequence of credited team results, not a
newly announced class in this packet.

The exact dependencies, their quantifiers and review status appear in
[DEPENDENCIES.md](DEPENDENCIES.md). In particular the covariance-free
entropy rigidity bound supplies unsigned closeness, not the sign needed
for `Delta_s=0`. It does not close this bridge.

## 6. The remaining obligation

For arbitrary bounded input, arbitrary contraction and fixed `s>0`,
one must either construct the endpoint coupling (4) with zero failures,
or prove all the **endpoint** beta/Hankel tests nonnegative. The existing
`R^6` path representation of the replica gaps may be used inside those
tests, but its complete time-integrated measures must be used. The
published local-lift example invalidates requiring the desired Hankel
positivity at every intermediate time. No universal integrated
positivity proof is supplied here. A single rigorously negative finite
test, with valid contraction data, settles the opposite direction.

Finally, a Kneser--Poulsen consequence needs its own quantifiers.
Aishwarya--Li, Theorem 1.8, applies full majorisation for every input law
on a compact domain and all variances to congruent-ball neighbourhood
volumes. The team's motion proofs separately justify the stated
individual-radius conclusions. A single-law or high-variance zero of
`Delta_s` is not by itself a new Kneser--Poulsen theorem.
