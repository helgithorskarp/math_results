# Sharp relative Gaussian moment gaps under contractions

## Statement and scope

Fix an integer `n>=1` and a variance `s>0`. Write

\[
\gamma_s(x)=C\exp(-|x|^2/(2s)),\qquad C=(2\pi s)^{-n/2}.
\]

Let `mu` be a bounded-support Borel probability measure on `R^n`, and let
`T:R^n -> R^n` be 1-Lipschitz. Set `f=mu*gamma_s`,
`g=(T_#mu)*gamma_s`, and, for integers `m>=2`, define the normalized gap

\[
d_m=C^{1-m}\left(\int g^m-\int f^m\right).
\tag{1}
\]

**Theorem 1 (sharp relative gaps).** For all integers `2<=p<q`,

\[
0\le d_q\le K_{n,p,q}d_p,\qquad
K_{n,p,q}=\frac{q-1}{p-1}\left(\frac pq\right)^{n/2}.
\tag{2}
\]

The upper constant is optimal over bounded-support probability measures
and contractions, at every fixed `n,s`. The infimum of `d_q/d_p` among
pairs with `d_p>0` is zero. No common radius bound on the entire class of
measures is imposed here; each measure individually has bounded support.

**Theorem 2 (complete two-power energy classification).** For real `a,b`,
put

\[
U(\rho)=a\rho^p+bC^{p-q}\rho^q.
\]

The comparison `integral U(f) <= integral U(g)` holds for every pair in
Theorem 1 if and only if

\[
\boxed{a\ge0\quad\hbox{and}\quad a+K_{n,p,q}b\ge0.}
\tag{3}
\]

In particular **every cubic polynomial `U` with `U(0)=0` that is convex
on `[0,C]` has the desired Gaussian-contraction comparison, in every
dimension**. The same conclusion even holds for cubics with nonnegative
pressure on `[0,C]`.

**Theorem 3 (an exponential family in dimension three).** If `n=3` and

\[
0\le a\le (3/2)^{5/2}=\sqrt{243/32},
\]

then the convex energy

\[
U_a(\rho)=C\big(e^{-a\rho/C}-1+a\rho/C\big)
\tag{4}
\]

satisfies the same comparison for every bounded input law and contraction.
For `2<a<=sqrt(243/32)` this energy fails the source paper's `PC_2`
condition already on the attained density range `[0,C]`.
The upper endpoint in Theorem 3 is a sufficient bound, **not** asserted
to be optimal for this energy family.

These results settle energy classes within the dimension-three problem.
They do not prove full majorisation or provide a convex counterexample.
The sharpness examples for (3) concern energies outside the classified
cone and must not be mistaken for counterexamples to majorisation.

## Replica identity and an auxiliary Euclidean interpolation

Let `X_1,X_2,...` be independent samples from `mu`, and set `Y_i=T(X_i)`.
Completing the square in a product of Gaussians gives the standard replica
identity

\[
C^{1-m}\int f^m
=m^{-n/2}\mathbb E\exp\!\left(-\frac1{2ms}
  \sum_{i<j}|X_i-X_j|^2\right).
\tag{5}
\]

This is equation (61) of Aishwarya--Li; it is not a new identity.

Write

\[
\delta_{ij}=|X_i-X_j|^2-|Y_i-Y_j|^2\ge0,
\qquad Z_i(t)=(\sqrt{1-t}\,X_i,\sqrt t\,Y_i)\in\mathbb R^{2n}.
\]

Define the sample variance sum

\[
Q_m(t)=\sum_{i=1}^m|Z_i(t)-\overline Z_m(t)|^2
=\frac1m\sum_{i<j}|Z_i(t)-Z_j(t)|^2.
\tag{6}
\]

Its squared distances are affine in `t`, so differentiating the scalar
exponential in (5), integrating over `t`, and using exchangeability gives

\[
\boxed{\frac{m^{n/2}}{m-1}d_m
=\frac1{4s}\mathbb E\left[
\delta_{12}\int_0^1e^{-Q_m(t)/(2s)}\,dt\right].}
\tag{7}
\]

Bounded support and the contraction bound justify differentiation and
Fubini. Alternatively the integrated, nonnegative scalar identity permits
Tonelli directly. Notice that the factor `m^{-n/2}` remains that of the
original dimension `n`. We are interpolating a scalar replica expression,
not claiming that the intermediate distributions are densities in `R^n`.

The ordinary online sample-variance identity is

\[
Q_{m+1}(t)=Q_m(t)+\frac m{m+1}
|Z_{m+1}(t)-\overline Z_m(t)|^2\ge Q_m(t).
\tag{8}
\]

Use the same first `m` replicas in (7) for adjacent indices and an
independent extra replica for `m+1`. The nonnegative multiplier
`delta_12` is unchanged. Therefore

\[
\frac{(m+1)^{n/2}}m d_{m+1}
\le\frac{m^{n/2}}{m-1}d_m.
\tag{9}
\]

Iteration proves (2). This proof requires no monotone motion in `R^n`
and no sign assumption on a higher pressure derivative.

## Sharpness and the complete two-power cone

For the upper endpoint, take

\[
\mu_\varepsilon=\tfrac12\delta_0+
\tfrac12\delta_{\varepsilon e_1},\qquad T\equiv0.
\]

For each fixed `m`, expansion of the finite sum in (5) gives

\[
d_m=\frac{\varepsilon^2}{8s}(m-1)m^{-n/2}
 +O(\varepsilon^4),\qquad\varepsilon\downarrow0.
\tag{10}
\]

Indeed the expected squared distance of two unscaled Bernoulli samples
is `1/2`. Thus `d_q/d_p -> K_(n,p,q)`.

For the lower endpoint, take two equally weighted atoms at `0` and
`(R+1)e_1`, and contract by the homothety `R/(R+1)`. The target atoms
are at `0,R e_1`. The normalized `m`-th moment at separation `r` is

\[
J_m(r)=m^{-n/2}2^{-m}\sum_{j=0}^m
\binom mj\exp\!\left(-\frac{j(m-j)r^2}{2ms}\right).
\tag{11}
\]

Terms `j=0,m` cancel in `d_m=J_m(R)-J_m(R+1)`.
Among the others the least exponential rate is
`alpha_m=(m-1)/(2ms)`, at `j=1,m-1` (a single term if `m=2`). Hence

\[
d_m\sim c_m e^{-\alpha_m R^2},\qquad c_m>0.
\]

Since `alpha_q>alpha_p`, the ratio tends to zero as `R->infinity`.
Each member of this family is a bounded measure, and the homothety is a
global contraction.

The gap for the energy in Theorem 2 is

\[
C^{p-1}(a d_p+b d_q).
\]

If `d_p=0`, (2) makes it zero. Otherwise divide by `d_p` and use
`0<=d_q/d_p<=K`. A linear function is nonnegative throughout that interval
exactly when its endpoint values are nonnegative. The two limiting
families above prove both necessary inequalities in (3), including when
the proposed coefficient condition fails by an arbitrarily small amount.

Now write a cubic, up to an irrelevant linear term, as
`U(rho)=A rho^2+B rho^3`. Convexity on `[0,C]` says
`A>=0` and `A+3BC>=0`. If `B<0`, this implies
`A+2(2/3)^(n/2)BC>=0`, since `2(2/3)^(n/2)<3`.
If `B>=0`, (3) is immediate. Nonnegative pressure instead requires
`A>=0,A+2BC>=0`, which also implies (3).

## An analytic comparison cone and the exponential example

The preceding argument supplies more than two-power comparisons. Let

\[
u(z)=\sum_{m=2}^{\infty}c_m z^m,\qquad
\sum_{m=2}^{\infty}|c_m|<\infty,
\]

and assume all weighted prefix sums are nonnegative:

\[
S_M=\sum_{m=2}^M c_m(m-1)m^{-n/2}\ge0\quad(M\ge2).
\tag{12}
\]

For `U(rho)=C u(rho/C)`, the energy gap equals `sum c_m d_m`.
This interchange is legitimate: `0<=f,g<=C`, and
`C integral (f/C)^m<=1`, likewise for `g`, so absolute integration is
bounded by `2 sum |c_m|`. By (9),

\[
b_m=\frac{m^{n/2}}{m-1}d_m
\]

is nonnegative and nonincreasing. Finite Abel summation gives

\[
\sum_{m=2}^M c_m d_m
=S_M b_M+\sum_{m=2}^{M-1}S_m(b_m-b_{m+1})\ge0.
\tag{13}
\]

Pass to the absolutely convergent limit. Convexity is not needed for
this sufficient comparison criterion, although it holds in (4).
This cone is not claimed to characterize all comparable energies.

For (4), `c_m=(-a)^m/m!`. In dimension three the absolute summands in
(12) have adjacent ratio

\[
\frac{a m}{m^2-1}\left(\frac m{m+1}\right)^{3/2}.
\tag{14}
\]

The factor multiplying `a` decreases for real `m>=2`: its logarithmic
derivative is

\[
\frac{-2m^2+3m-5}{2m(m^2-1)}<0.
\]

Thus (14) is at most one when
`a <= (3/2)^(5/2)`. The alternating series begins with a positive term,
so every prefix sum (12) is nonnegative. This proves Theorem 3.

In normalized coordinates `z=rho/C`, the pressure of `u_a` is
`P(z)=1-(1+az)e^(-az)`, and

\[
(z\partial_z)^2P(z)=a^2z^2(2-az)e^{-az}.
\tag{15}
\]

It is negative inside `[0,1]` when `a>2`. Hence Theorem 3 supplies actual
convex energy comparisons outside the paper's dimension-three `PC_2`
sufficient class. No modification outside `[0,1]` removes that interior
failure.

## Context, dependencies, and trust boundary

Primary source: G. Aishwarya and D. Li, *Gaussian Convolution, Internal
Energies, and the Kneser--Poulsen Conjecture*, arXiv:2609.07041v2,
13 September 2026, <https://arxiv.org/html/2609.07041v2>.
The source supplies the conjecture, pressure hierarchy, replica identity,
and the continuous-contraction energy formula. We use its elementary
Gaussian-product computation explicitly, with a new comparison across
replica counts. Its arbitrary-contraction theorem supplies `PC_2` in
dimension three; its continuous-contraction theorem has a different
hypothesis and does not settle the arbitrary maps treated here.

Team B's separate analytic lane develops a complete hinge/Hankel hierarchy.
The present result does not claim that reduction and does not reuse an
unproved Hankel-positivity assertion. Adversarial quartic and higher-degree
searches motivated the present gap bound, but their finite negative outcomes
are not used in any theorem.

The proofs above are uniform mathematical arguments. `verify.py` checks
the variance identity in exact rational arithmetic, enclosed two-atom
moment ratios, finite sharpness witnesses, and the exponential endpoint.
Those computations audit normalization and implementation; they are not
a finite substitute for the universal proof. The numerical trust boundary
is Python-FLINT/Arb ball arithmetic and its exact rational inputs. No Monte
Carlo estimate, floating-point search output, solver, or external data is
part of the proof. Independent mathematical review is pending.
