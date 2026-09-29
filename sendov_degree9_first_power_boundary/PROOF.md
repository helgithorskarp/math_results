# Local first-power coercivity and a degree-nine boundary annulus

Agent: six-sendov-1. Role: researcher. All roots and critical points below
are counted with multiplicity. The proof is analytic; the accompanying
exact checker verifies algebraic coefficients and control families.

## 1. Statements and normalization

Let `p` be monic of degree nine with all roots in the closed unit disk.
Rotate a distinguished root to `a in [0,1]`, and let `zeta_j` be the eight
critical points. Put

\[
\delta=1-a,\quad Q=\sum_{j=1}^8|\zeta_j|^2,\quad
\mu=\frac18\sum_{j=1}^8|a-\zeta_j|^{-1}.
\]

Infinite sums cause no difficulty. They cannot occur in the local
neighborhood considered in the first theorem.

**Theorem 1 (local estimate).** Fix `0<=gamma<1/3` and
`0<=kappa<1/112`. There is `epsilon>0` such that, if

\[
0\le\delta<\epsilon,\qquad \max_j|\zeta_j|<\epsilon,
\]

then `mu>1+gamma delta+kappa Q` whenever `delta+Q>0`. If `delta=Q=0`,
then `p=z^9-1` and `mu=1`.

**Theorem 2 (boundary annulus).** Fix `0<gamma<1/3`. There is
`r_gamma in (0,1)` such that, for every degree-nine disk-root polynomial
and every root with `r_gamma<|a|<1`,

\[
\sum_j|a-\zeta_j|^{-1}>8+8\gamma(1-|a|).
\]

Taking `gamma=1/4` gives `S_1>8+2(1-|a|)` in some universal annulus.
Neither theorem supplies an explicit neighborhood size or annulus radius.

## 2. Uniform coefficient and reciprocal expansions

Write

\[
p(z)=z^9+c_8z^8+c_7z^7+\cdots+c_1z+c_0,
\quad \eta=\max_j|\zeta_j|,
\quad s=\operatorname{Re}c_8,\quad t=\operatorname{Re}c_7.
\]

From `p'(z)=9 prod_j(z-zeta_j)`,

\[
\sum_j\zeta_j=-\frac89c_8,\qquad
\sum_j\zeta_j^2=\frac{64}{81}c_8^2-\frac{14}{9}c_7.\tag{1}
\]

The elementary-symmetric formulas give uniform bounds

\[
|c_8|=O(\sqrt Q),\qquad |c_7|=O(Q),\qquad
\sum_{\ell=1}^6|c_\ell|=O(\eta Q).\tag{2}
\]

Here and throughout the dimension is fixed. For example,
`sum |zeta|<=sqrt(8Q)`, and an elementary symmetric function of degree
`k>=3` is bounded by a fixed constant times
`Q^(k/2)<=8^((k-2)/2) eta^(k-2) Q`. This proves (2), including
`c_1=O(eta^6 Q)`.

For `a>=1/2` and `|zeta|` sufficiently small, the real analytic function
`|a-zeta|^(-1)` has the uniform expansion

\[
|a-\zeta|^{-1}=\frac1a+\frac{\operatorname{Re}\zeta}{a^2}
 +\frac{|\zeta|^2+3\operatorname{Re}(\zeta^2)}{4a^3}
 +O(|\zeta|^3).
\]

Uniformity follows from bounded third partial derivatives on a fixed
compact neighborhood where `|a-zeta|` is bounded away from zero. Summing,
using (1), and expanding the powers of `a=1-delta` gives

\[
\mu=1+\delta-\frac{s}{9}+\frac{Q}{32}-\frac{7t}{48}
 +\frac{2}{27}\operatorname{Re}(c_8^2)
 +O(\delta^2+\delta\sqrt Q+\eta Q).\tag{3}
\]

All constants are independent of the polynomial in this neighborhood.

## 3. A Schwarz-Pick bootstrap under a possible local failure

Suppose, for contradiction to Theorem 1, that a sequence satisfies

\[
\delta_k\to0,\quad\eta_k\to0,\quad h_k=\delta_k+Q_k>0,
\quad\mu_k\le1+\gamma\delta_k+\kappa Q_k.\tag{4}
\]

Suppress the index. Equations (2)-(3) first give

\[
s\ge9(1-\gamma)\delta-CQ-C\delta^2-C\delta\sqrt Q.
\]

Since `gamma<1`, the last two terms can be absorbed into the positive
`delta` term for sufficiently large indices. In particular `s>=-C Q`.
The root equation gives

\[
c_0=-a^9-c_8a^8-c_7a^7-\sum_{\ell=1}^6c_\ell a^\ell.\tag{5}
\]

Therefore `c_0->-1`, and

\[
\operatorname{Re}(1+c_0)
 =1-a^9-a^8s-a^7t+O(\eta Q)=O(h)
\]

as an upper bound. The product of the nine disk roots gives `|c_0|<=1`;
hence

\[
0\le1-|c_0|^2
 =2\operatorname{Re}(1+c_0)-|1+c_0|^2\le C h.\tag{6}
\]

For completeness, define the reversed conjugate polynomial
`p*(z)=z^9 conjugate(p(1/conjugate z))`. If the roots are `r_i`,

\[
B(z)=\frac{p(z)}{p^*(z)}
 =\prod_i\frac{z-r_i}{1-\overline{r_i}z}
\]

is holomorphic on the open unit disk and has modulus at most one there.
When `|r_i|=1`, that factor is the constant `-r_i` after cancellation;
no boundary pole enters the argument. Schwarz-Pick at zero gives

\[
|c_1-c_0\overline{c_8}|=|B'(0)|\le1-|c_0|^2.\tag{7}
\]

The same inequality holds for a constant unit-modulus `B`.
Since `|c_0|` is bounded away from zero, (2), (6)-(7) imply

\[
|c_8|=O(h).\tag{8}
\]

This is the needed bootstrap. It was derived under (4), not assumed for
an arbitrary small critical configuration. Consequently `c_8^2=o(h)`,
and (3) becomes

\[
\mu-1=\delta-\frac{s}{9}+\frac{Q}{32}-\frac{7t}{48}+o(h).\tag{9}
\]

Every remainder divided by `h` tends to zero uniformly along sequences
(4): use `delta^2/h<=delta`, `delta |c_8|/h=O(delta)`,
`eta Q/h<=eta`, and `|c_8|^2/h=O(h)`.

## 4. The two cube-root constraints

By (2), (5), and (8), the coefficient norm of
`g=p-(z^9-1)` is `O(h)`. Each simple root `omega` of `z^9-1` has a unique
nearby root `r_omega` of `p`, and

\[
r_\omega=\omega-\frac{g(\omega)}{9\omega^8}+O(h^2).\tag{10}
\]

Here the constants are uniform over the nine fixed roots. To see the
remainder directly, root continuity and the simple-root factorization
first give `|r_omega-omega|=O(||g||)`. Taylor expansion of
`r_omega^9-1+g(r_omega)=0` then gives (10). Existence and uniqueness can
also be obtained by Rouche on disjoint fixed small circles around the
ninth roots. This involves roots of `p`, which remain simple here; the
collision of critical points at zero causes no singularity.

Since `|r_omega|<=1`,
`Re((r_omega-omega)/omega)<=0`. Divide (10) by `omega` and use `omega^9=1`
to obtain

\[
\operatorname{Re}g(\omega)\ge-O(h^2).\tag{11}
\]

Apply (11) to `omega=exp(2 pi i/3)` and its conjugate, which are both
ninth roots. Averaging these two inequalities removes the imaginary
parts of `c_8,c_7`, because `omega^8=omega^2`, `omega^7=omega`, and
`Re omega=Re omega^2=-1/2`. Equation (5) and (8) give

\[
\operatorname{Re}(1+c_0)=9\delta-s-t+o(h).
\]

The lower coefficients contribute only `O(eta Q)=o(h)`. Thus the averaged
inequality is

\[
9\delta-\frac32(s+t)\ge-o(h),\qquad
s+t\le6\delta+o(h).\tag{12}
\]

Also (1) and (8) give

\[
t=-\frac9{14}\operatorname{Re}\sum_j\zeta_j^2+o(h)
 \le\frac9{14}Q+o(h).\tag{13}
\]

Insert (12) into (9), then (13), noting the negative coefficient of `t`:

\[
\begin{aligned}
\mu-1
&\ge\frac\delta3+\frac Q{32}-\frac5{144}t+o(h)\\
&\ge\frac\delta3+
 \left(\frac1{32}-\frac5{144}\frac9{14}\right)Q+o(h)
 =\frac\delta3+\frac Q{112}+o(h).\tag{14}
\end{aligned}
\]

But (4) and (14) imply

\[
0\ge(1/3-\gamma)\delta+(1/112-\kappa)Q+o(h),
\]

which is impossible: the first two terms are at least a fixed positive
multiple of `h`. This sequential contradiction proves the existence of
the uniform neighborhood in Theorem 1. If `h=0`, all critical points are
zero and `p(1)=0`, so `p=z^9-1`, as asserted.

## 5. Extending the boundary concentration hypothesis

We now prove a stronger input for globalization. Fix `0<=gamma<1/2`.
Consider a sequence of monic disk-root polynomials and simple roots
`a_k in (0,1)` with `delta_k=1-a_k->0` and

\[
\mu_k\le1+\gamma\delta_k.\tag{15}
\]

Put `q_j=(a-zeta_j)^(-1)`, `r_j=|q_j|`, and

\[
D=\frac18\sum_j(r_j-\operatorname{Re}q_j),\qquad
v=\frac18\sum_j(r_j-\mu)^2,\qquad
b=1-a^2,\qquad R=8\mu-\frac7{1+a}.
\]

Gauss-Lucas gives `1/(1+a)<=r_j<=R`. The prior polar identity and
disk inequality imply

\[
1\le H(a,\mu)=\int_0^1(a+b\mu t)^8\,dt.\tag{16}
\]

The angular-loss and strong-concavity estimates from the previous proof
apply with this actual value of `R`, without needing `mu<=1`:

\[
1\le I=\int_0^1(a+b\mu t)^8
\exp\left[-\frac{8(abtD+b^2t^2v/2)}{(a+btR)^2}\right]dt.\tag{17}
\]

Briefly, `|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-Re q_j)` and
`sqrt(1-u)<=exp(-u/2)` retain the angular defect. The second derivative
of `log(a+btr)` is at most `-(bt)^2/(a+btR)^2`; Taylor about the mean
retains the modulus variance. These arguments require only positive `a`
and the displayed lower/upper bounds on the `r_j`.

From (15), Gauss-Lucas, and the uniform finite-binomial expansion of (16),

\[
H(a,\mu)=1+8(\mu-1)\delta+O(\delta^2),
\]

we obtain `mu=1+O(delta)`. In particular `R->9/2`, `v` is bounded, and
`D` is bounded. The angular exponent on `t in [1/2,1]` is bounded below
by `c delta D` and is `O(delta D)`. The polynomial prefactor is bounded
below by a positive constant. Using `1-exp(-u)>=u/2` for sufficiently
small nonnegative `u` proves `I<=H-c' delta D`. Equations (16)-(17), and
`H=1+O(delta^2)`, then yield `D=O(delta)`.

Set `sigma=(1-mu)/delta` and `d=D/delta`. Their ranges lie in fixed
compact intervals, with `sigma>=-gamma` and `d>=0`. In (17),

\[
\mu=1-\sigma\delta,\quad D=d\delta,\quad
b=2\delta-\delta^2,\quad R=8(1-\sigma\delta)-\frac7{2-\delta}.
\]

The denominator stays bounded away from zero on a fixed compact parameter
rectangle. Taylor's theorem with bounded third derivatives gives the
following uniform integrand expansion:

\[
1+8(2t-1)\delta+
\left[28(2t-1)^2-8t-16\sigma t-16dt-16vt^2\right]\delta^2
 +O(\delta^3).
\]

Integration of (17) therefore gives

\[
\limsup\left(\sigma+d+\frac23v\right)\le\frac23,
\qquad \limsup v\le1+\frac32\gamma<\frac74.\tag{18}
\]

This extends the earlier budget from `mu<=1` to (15).

The disk-root coefficient space is compact. The bounds on `r_j` also
give `|p'(a)|=9 prod_j(1/r_j)>=9/R^8`, so every coefficient limit has a
simple root at one. The critical multisets and reciprocals then pass
continuously to the limit. Since `mu->1`, the limiting polynomial has
boundary first-power sum eight.

The previously proved boundary classification says that, in degree nine,
such a monic limit is either

\[
z^9-1\quad\text{or}\quad(z-1)(z+1)^8.
\]

Their reciprocal-modulus variances at one are `0` and `7/4`, respectively.
Equation (18) excludes the second. Every coefficient subsequence has
only the first possible limit; therefore the entire sequence converges
to `z^9-1`, and all its critical points tend to zero.

## 6. Globalization and limitations

Fix `0<gamma<1/3`. If Theorem 2 failed for every annulus, there would be
disk-root polynomials with roots `a_k->1` and `mu_k<=1+gamma delta_k`.
Section 5 applies because `gamma<1/2` and forces all critical points to
zero. Theorem 1, with this `gamma` and any allowed `kappa`, then gives
`mu_k>1+gamma delta_k`, a contradiction. This proves Theorem 2.

The strict theorem is for interior roots. At boundary roots the earlier
inequality is `S_1>=8`, with both classified equality families retained.
The annulus radius comes from compactness and local uniformity, so it
must not be reported as an explicit numeric radius.

For a useful control, `p_a=(z-a)(z+1)^8` has critical points `-1` seven
times and `(8a-1)/9` once. Exactly,

\[
\mu(a)=\frac2{a+1},\qquad
\frac{\mu(a)-1}{1-a}=\frac1{a+1}\to\frac12,
\qquad v(a)=\frac7{(a+1)^2}\to\frac74.
\]

Thus any claim of a uniform boundary slope greater than `1/2` for the
mean is false. The `gamma<1/2` condition in the concentration mechanism
also cannot simply be removed: for every `gamma>1/2`, this thin family
satisfies (15) sufficiently near one and does not converge to `z^9-1`.
No sharpness is claimed for the local constant `1/3`.

The remaining degree-nine first-power conjecture on the middle annulus
is not resolved. A concrete next step is to quantify the annulus radius,
or sharpen the full root-containment coefficient constraints beyond the
two cube-root tests.
