# Sharp replica curvature and a degree-independent polynomial comparison

Status: complete author proofs; independent review and formalization are
pending. The full dimension-three Gaussian majorisation conjecture remains
open. Only the specified replica-loss constant is claimed optimal.

## 1. Statements

Let `mu` be a Borel probability measure supported in `B(a,R)` in `R^3`,
let `T:R^3 -> R^3` be 1-Lipschitz, and let `s>0`. Write

\[
C=(2\pi s)^{-3/2},\quad f=\mu*\gamma_s,\quad
g=(T_\#\mu)*\gamma_s,\quad \varepsilon=R^2/s,
\]

where the Gaussian covariance is `s I_3`. Define

\[
d_m=C^{1-m}\left(\int g^m-\int f^m\right),\qquad
a_j=\frac{d_{j+2}}{(j+1)(j+2)}.                         \tag{1}
\]

For iid samples `X_i~mu`, put `Y_i=T(X_i)` and

\[
\Delta_{ij}=|X_i-X_j|^2-|Y_i-Y_j|^2,\quad D=\mathbb E\Delta_{12},
\]
\[
Z_i(t)=(\sqrt{1-t}X_i,\sqrt t Y_i),\quad
Q_m(t)=\sum_{i=1}^m|Z_i(t)-\overline Z_m(t)|^2,
\]
\[
B_m=\mathbb E\left[\Delta_{12}\int_0^1e^{-Q_m(t)/(2s)}dt\right].
                                                               \tag{2}
\]

**Theorem 1 (averaged replica curvature).** For every integer `m>=2`,

\[
\boxed{B_mB_{m+2}\geq
 \exp\!\left[-\frac{R^2}{(m+1)(m+2)s}\right]B_{m+1}^2.} \tag{3}
\]

In particular

\[
\boxed{B_2B_4\geq e^{-R^2/(12s)}B_3^2.}                \tag{4}
\]

The constant `1/12` is the least possible constant `c` in a universal
bound `B_2 B_4 >= exp(-c R^2/s) B_3^2`. This sharpness already occurs
for two equally weighted atoms on a line and homotheties approaching
the identity. The best constants for `m>2` are not determined here.

**Theorem 2 (all degrees, at most three nonlinear terms).** If

\[
\boxed{s\geq\frac25R^2,}                               \tag{5}
\]

then every polynomial of the form

\[
U(\rho)=b\rho+\sum_{j\in J}c_j\rho^j,
\qquad J\subset\{2,3,\ldots\},\quad |J|\leq3,           \tag{6}
\]

that is convex on `[0,C]` satisfies `integral U(f)<=integral U(g)`.
There is **no bound on the exponents in J**. If `D>0` and `U` is
non-affine, the comparison is strict. Under (5), every `2 by 2` minor
of the infinite Hankel array `(a_(i+j))_(i,j>=0)` is nonnegative,
and strictly positive when its row and column indices are distinct
and `D>0`.

**Theorem 3 (improved quartic range).** Every polynomial of degree at
most four with `U(0)=0`, convex on `[0,C]`, has the same comparison if

\[
R^2/s\leq30\log(9/8),\qquad\text{in particular if}
\quad\boxed{s\geq\frac{17}{60}R^2.}                    \tag{7}
\]

At the rational threshold in (7), when `D>0`,

\[
a_0a_2>\left(1+\frac5{14739}\right)a_1^2,              \tag{8}
\]

and the energy comparison is strict for every non-affine quartic.
No optimality of (5) or (7) is asserted. Theorem 3 improves the earlier
radius-based sufficient variance by a factor of four; Theorem 2 is
the new consequence uniform in polynomial degree.

Every integral just stated is finite, since `0<f,g<=C` and a polynomial
vanishing at zero is bounded in absolute value by a multiple of its
argument on `[0,C]`.

## 2. Prior representation and degenerate cases

The team's [sharp relative-gap proof](../gaussian_contraction_moment_gaps/PROOF.md)
establishes, by the Gaussian replica identity and exchangeability,

\[
d_m=\frac{m-1}{4s m^{3/2}}B_m,\qquad
a_j=\frac{B_{j+2}}{4s(j+2)^{5/2}},\qquad B_{m+1}\leq B_m.
                                                               \tag{9}
\]

These are dependencies, not new identities. The last inequality follows
from `Q_(m+1)=Q_m+m|Z_(m+1)-mean_m Z|^2/(m+1)`. The replica identity
itself is prior to the team work; see Aishwarya--Li, equation (61).

Translate the input by `a` and the output by `T(a)`. Then `|Z_i(t)|<=R`
at every time. The translation leaves all quantities in (1)--(2)
unchanged. If `D=0`, all the nonnegative integrals `B_m` vanish and
all polynomial gaps vanish. If `D>0`, every `B_m`, and hence every
`a_j`, is positive. The case `R=0` implies `D=0`.

## 3. Average the two new replicas before estimating

Fix `t` and the first `m` replicas, whose mean is `b`. Write the next
two points as `b+u,b+v`, and let `Q_(m+1)^u,Q_(m+1)^v` denote their
separate one-point extensions. The exact identity used in the previous
[large-variance proof](../gaussian_contraction_high_noise_quartics/PROOF.md) is

\[
S:=Q_m+Q_{m+2}-Q_{m+1}^u-Q_{m+1}^v
=\frac{2}{m+1}\left|\frac{u-v}{2}\right|^2
 -\frac{2m}{(m+1)(m+2)}\left|\frac{u+v}{2}\right|^2.    \tag{10}
\]

The earlier argument bounded this pointwise. Instead let `nu` be the
probability law of an extra `Z=Z(t)` tilted by

\[
e^{-m|Z-b|^2/(2(m+1)s)},\qquad
r=\mathbb E e^{-m|Z-b|^2/(2(m+1)s)}>0.                 \tag{11}
\]

Let `z_nu=E_nu Z` and `V_nu=E_nu|Z-z_nu|^2`. Independent samples from
this tilted law satisfy

\[
\mathbb E_{\nu\otimes\nu}S
=\frac{2}{(m+1)(m+2)}
       \big[V_\nu-m|z_\nu-b|^2\big]
\leq\frac{2R^2}{(m+1)(m+2)}.                          \tag{12}
\]

Indeed `E|(u-v)/2|^2=V_nu/2` and
`E|(u+v)/2|^2=V_nu/2+|z_nu-b|^2`. Also `nu` is still supported in
`B(0,R)`, so `V_nu=E_nu|Z|^2-|E_nu Z|^2<=R^2`.

Using (10) exactly before any estimate gives

\[
\mathbb E_{Z_{m+1},Z_{m+2}}e^{-Q_{m+2}/(2s)}
=e^{-Q_m/(2s)}r^2\,\mathbb E_{\nu\otimes\nu}e^{-S/(2s)}.
\]

Jensen and (12) therefore imply

\[
\mathbb E e^{-Q_{m+2}/(2s)}
\geq e^{-R^2/((m+1)(m+2)s)}e^{-Q_m/(2s)}r^2.          \tag{13}
\]

The conditional expectation on the left concerns only the two extra
replicas. Integrate (13) against the remaining positive weight
`Delta_12 dt dmu^m`. Equivalently put

\[
dw=\Delta_{12}e^{-Q_m(t)/(2s)}dt\,d\mu^{\otimes m}.
\]

Then `B_m=integral dw`, `B_(m+1)=integral r dw`, and
`B_(m+2)>=exp[-R^2/((m+1)(m+2)s)] integral r^2 dw`.
Cauchy--Schwarz proves (3). Boundedness and nonnegativity justify all
integrations, including arbitrary non-atomic input laws. The same
estimate is valid at each fixed time with the time integral omitted,
but it does not assert unrestricted instantaneous Hankel positivity.

## 4. Log-convexity in all degrees and the sparse curvature lemma

Combining (3) with (9) gives

\[
a_{m-2}a_m\geq\kappa_m a_{m-1}^2,\qquad
\kappa_m=e^{-\varepsilon/((m+1)(m+2))}
 \left(\frac{(m+1)^2}{m(m+2)}\right)^{5/2}.             \tag{14}
\]

If `epsilon<=5/2`, then `-log(1-x)>x` for `0<x<1` shows

\[
\log\kappa_m>
\frac{5}{2(m+1)^2}-\frac{5}{2(m+1)(m+2)}
=\frac{5}{2(m+1)^2(m+2)}>0.                           \tag{15}
\]

For `D>0`, the sequence `a_j` is thus strictly log-convex. It is also
strictly decreasing by (9). Increasing successive ratios imply

\[
a_p a_{p+u+v}>a_{p+u}a_{p+v}
\quad(p\geq0,\ u,v\geq1).                            \tag{16}
\]

This proves the asserted positivity of every `2 by 2` Hankel minor.

We need a little more than squares of binomials to establish all of (6).
Here is an elementary three-moment fact. For integers `0<=p<q<r`, set

\[
M=a_q/a_p,\quad N=a_r/a_p,\quad \alpha=(r-p)/(q-p)>1.
\]

Log-convexity and monotonicity give

\[
0<M<1,\qquad M^\alpha<N<M.                            \tag{17}
\]

Define `z=(N/M)^(1/(alpha-1))` and `theta=M/z`. Then
`M<z<1` and `0<theta<1`. The probability measure

\[
\sigma=(1-\theta)\delta_0+
 \theta\delta_{\,z^{1/(q-p)}}
\]

has moments `integral t^(q-p) d sigma=M` and
`integral t^(r-p) d sigma=N`. It is a representing measure for these
three particular moments only; no global moment representation is claimed.

Let `P(t)=A t^p+B t^q+E t^r>=0` on `[0,1]`, with `p` its lowest
nonzero exponent. Then `h(t)=A+B t^(q-p)+E t^(r-p)>=0` there and
`A=h(0)>0`. Therefore

\[
A a_p+B a_q+E a_r
=a_p\int h\,d\sigma\geq a_p(1-\theta)A>0.            \tag{18}
\]

Fewer than three terms are handled by adding zero coefficients at higher
exponents. For a normalized energy `V(t)=U(Ct)/C`, cancellation of its
linear term and (1) give

\[
C\int[V(g/C)-V(f/C)]=\sum_j c_j a_j
\quad\text{if}\quad V''(t)=\sum_j c_jt^j.              \tag{19}
\]

The curvature of (6) has at most three nonzero terms and is nonnegative
on `[0,1]`. Apply (18)--(19), or the `D=0` case in Section 2. This proves
Theorem 2, including strictness.

For a concrete energy of degree nine, put

\[
V(t)=\frac{t^2}{64}-\frac{7t^5}{320}+\frac{t^9}{24}.
                                                               \tag{20}
\]

Its curvature is

\[
V''(t)=\frac{(2t-1)^2}{32}
 (24t^5+24t^4+18t^3+12t^2+4t+1)\geq0\quad(t\geq0).
\]

The energy `U(rho)=C V(rho/C)` is covered by (5). It fails `PC_2`
on the density interval: `t^2 V''(t)` decreases just below `t=1/2`.
It also fails the sufficient weighted-prefix condition in the earlier
relative-moment theorem, since its prefix ending at degree five is

\[
\frac{1}{128\sqrt2}-\frac7{400\sqrt5}<0.               \tag{21}
\]

Thus the uniform-degree conclusion adds energies to the previously
established sufficient cones. No claim is made that those cones are
necessary conditions.

## 5. The stronger quartic range

For `m=2`, (14) reads

\[
a_0a_2\geq e^{-\varepsilon/12}(9/8)^{5/2}a_1^2.
\tag{22}
\]

This gives a positive semidefinite first Hankel matrix under (7).
Also `a_1>a_2` when `D>0`, by (9). Every quadratic `P>=0` on `[0,1]`
can be written

\[
P(t)=[\sqrt{P(0)}(1-t)-\sqrt{P(1)}t]^2+c t(1-t),
\qquad c\geq0.
\]

The endpoint values determine `c`; evaluating at the zero of the square,
or using one-sided derivatives for a vanishing endpoint, proves `c>=0`.
The first Hankel matrix controls the square, and `a_1-a_2` controls the
second term. Equation (19) now proves the quartic comparison.

Finally
`log(9/8)=2 atanh(1/17)>2/17+2/(3*17^3)`. If `epsilon<=60/17`,
then `log[e^(-epsilon/12)(9/8)^(5/2)]>5/14739`.
Using `e^x>1+x` proves (8) and strictness exactly as claimed.

## 6. Optimal loss and failure of exact replica log-convexity

Take two atoms `X=+R e_1,-R e_1`, each with probability `1/2`, and the
global homothety `T(x)=lambda x`, `0<=lambda<1`. Write `u=R^2/s` and
`E_c=e^(-c lambda^2 u)-e^(-c u)`. Direct binomial replica enumeration gives

\[
B_2=2sE_1,\qquad B_3=\frac{3s}{2}E_{4/3},\qquad
B_4=\frac{2s}{3}E_{3/2}+\frac{s}{2}E_2.                \tag{23}
\]

For fixed `lambda<1`, with `D=2R^2(1-lambda^2)`, Taylor expansion yields

\[
\begin{aligned}
B_2/D&=1-\tfrac12(1+\lambda^2)u+O_\lambda(u^2),\\
B_3/D&=1-\tfrac23(1+\lambda^2)u+O_\lambda(u^2),\\
B_4/D&=1-\tfrac78(1+\lambda^2)u+O_\lambda(u^2).
\end{aligned}
\]

Consequently

\[
\log\frac{B_2B_4}{B_3^2}
=-\frac{1+\lambda^2}{24}u+O_\lambda(u^2).              \tag{24}
\]

The functions in (23), divided by `D`, extend analytically to `u=0`;
ordinary Taylor remainders justify (24). For any `c<1/12`, first choose
`lambda<1` with `(1+lambda^2)/24>c`, then take `u>0` sufficiently small.
Equation (24) violates the proposed bound with `c` in place of `1/12`.
Together with (4), this proves the optimality assertion.

Exact log-convexity of `B_m` cannot be recovered even by taking the noise
arbitrarily large. Here is an explicit whole range without asymptotics.
Set `lambda=0` in (23), and put `x=e^{-u/6}`. Then

\[
\frac{12}{s^2}(B_2B_4-B_3^2)=(x-1)^3(x+1)P(x),        \tag{25}
\]

where

\[
\begin{aligned}
P(x)={}&12x^{14}+24x^{13}+21x^{12}+34x^{11}+32x^{10}
 +46x^9+33x^8+36x^7+12x^6\\
&-12x^5-9x^4-6x^3-4x^2-2x-1.
\end{aligned}
\]

For `9/10<=x<=1`, the positive coefficients sum to `250`, and the
absolute negative coefficients sum to `34`; hence
`P(x)>=250(9/10)^14-34>0`. If `s>=5R^2/3` and `R>0`, then
`0<u<=3/5`, so `9/10<x<1` using `e^{-u/6}>=1-u/6`. Thus

\[
\boxed{B_2B_4<B_3^2\quad\text{for every }s\geq5R^2/3}
\tag{26}
\]

for this actual bounded contraction pair. These endpoints satisfy full
majorisation (they even undergo a homothetic continuous contraction).
The example is an obstruction to exact *replica* log-convexity, not a
counterexample to majorisation, to (5), or to (7).

## 7. Remaining obstruction and team context

Log-convexity does not imply positivity of every Hankel matrix. For example
`a_0,...,a_4=(1,1/2,1/3,1/4,19/100)` is positive, strictly decreasing,
and strictly log-convex, but its first `3 by 3` Hankel determinant is
`-1/2700`. Extending the sequence beyond index four with the constant
successive ratio `19/25` gives a decreasing log-convex infinite sequence.
This is an abstract illustration, not an admissible Gaussian example.

Accordingly (5) excludes every negative two-term square-curvature witness
in every degree, and more generally every convex energy (6), but it
does not settle the full Hankel hierarchy or all hinges. A polynomial
counterexample in this variance regime must have at least four nonzero
nonlinear energy terms. No new Kneser--Poulsen case follows here.

During the publication refresh the team independently supplied an
[actual instantaneous lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md),
an [all-variance symmetric-flap quartic theorem](../gaussian_symmetric_flap_quartics/PROOF.md),
and a [small-mass hinge window](../gaussian_majorisation_small_mass/PROOF.md).
They were inspected and are complementary. In particular the first rules
out unrestricted pointwise-in-time positivity; the present proof asserts
only the radius-controlled estimate (3), and uses the integrated sequence
for its endpoint comparisons. The large input radius in that obstruction
lies outside (5). Its failed pointwise route should not be pursued again.

The universal results above are analytic. The exact checker validates
the averaging identities, polynomial certificates, and selected finite
replica inequalities with rational enclosures. Those finite checks do
not replace the universal proof. See [SOURCES.md](SOURCES.md) for
attribution and [README.md](README.md) for reproduction and trust boundaries.
