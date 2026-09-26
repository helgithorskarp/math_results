# An admissible instantaneous lift can fail the Hankel test

## 1. Exact statement and the bridge being tested

Let `mu` be a bounded probability law in `R^3`, let `T` be a contraction,
and put `Y=T(X)` for `X~mu`. Throughout this note the Gaussian variance is
one. The squared-distance interpolation is

\[
 z_t(X)=(\sqrt{1-t}\,X,\sqrt t\,Y)\in\mathbb R^6,
 \qquad 0\le t\le1.                                      \tag{1}
\]

It is a continuous contraction, because its squared pairwise distances are
`(1-t)|X-X'|^2+t|Y-Y'|^2`. It is congruent, at each time, to the standard
leapfrog lift with the corresponding reparametrisation. Smoothness at the
two endpoints is unnecessary below; our time is strictly interior.

Write `Delta=|X-X'|^2-|Y-Y'|^2>=0`, `C6=(2*pi)^(-3)`, and

\[
 q_t(z)=\mathbb E\,\gamma^{(6)}(z-z_t(X)),\qquad
 M_t(z)=\mathbb E\big[\Delta(X,X')
       \gamma^{(6)}(z-z_t(X))\gamma^{(6)}(z-z_t(X'))\big].
\]

The positive instantaneous measure `eta_t` on `[0,1]` is defined by

\[
 \int \psi(u)\,d\eta_t(u)
   =\int_{\mathbb R^6}\psi(q_t(z)/C6)M_t(z)/C6\,dz.        \tag{2}
\]

Completing the square for `k=j+2` replicas gives

\[
 \int u^{k-2}\,d\eta_t(u)
 =k^{-3}\mathbb E\left[\Delta_{12}
   \exp\left(-\frac1{2k}\sum_{r<s}
                  |z_t(X_r)-z_t(X_s)|^2\right)\right].  \tag{3}
\]

The earlier [Hankel reduction](../gaussian_majorisation_hankel_transport/PROOF.md)
shows that the **integrated** endpoint sequence is

\[
 a_j=\frac{\sqrt{j+2}}4\int_0^1\int u^j\,d\eta_t(u)\,dt.
                                                               \tag{4}
\]

Positivity of all its Hankel matrices is equivalent to the desired endpoint
majorisation. A tempting sufficient condition is that the matrices formed
from `sqrt(j+2)*integral u^j d eta_t` be positive semidefinite separately at
every time. The result here disproves that stronger condition, even at order
two, for an actual bounded law and a very strong contraction.

**Theorem.** There are an explicit finitely supported `mu` in `R^3`, a global
`1/100`-Lipschitz map `T`, and a rational time `t_*` in `(0,1)` such that the
first `2` by `2` instantaneous transformed Hankel matrix has negative
determinant. A specified rational vector gives a negative quadratic form.
Nevertheless `mu*gamma` is majorised by `(T_#mu)*gamma`.

All claims of negativity below are certified by rational enclosures. This
is not a counterexample to the named conjecture, to (4), or to the team's
relative moment-gap theorem.

## 2. Why a pointwise geometric proof encounters full six-dimensional clouds

Here is a general encoding observation behind the construction. Suppose a
finite labelled cloud is given by `(a_i,b_i)` in `R^3 x R^3`, with probability
weights `w_i`, and the `a_i` are distinct. For arbitrarily large `L` define

\[
 x_i=L a_i,\qquad T(x_i)=b_i,\qquad t_L=L^2/(1+L^2).
\]

For any prescribed `0<c<=1`, this finite map has Lipschitz constant at most `c`
once `L>=c^(-1) max_(i!=j)|b_i-b_j|/|a_i-a_j|`. Kirszbraun's theorem extends
it globally with that constant. At `t_L`, its lifted cloud is

\[
 z_{t_L}(x_i)=\frac L{\sqrt{1+L^2}}(a_i,b_i),\qquad
 \Delta_{ij}/L^2=|a_i-a_j|^2-L^{-2}|b_i-b_j|^2.           \tag{5}
\]

Consequently, after dividing (2) by `L^2`, all its moments converge to the
Gaussian replica moments of the arbitrary cloud `(a_i,b_i)`, weighted by
`|a_i-a_j|^2`. This follows directly from the finite sum (3). The masses
are bounded, so polynomial approximation on `[0,1]` also gives weak
convergence of these positive measures.

Repeated first projections cause no obstruction to this closure statement:
perturb the finitely many `a_i` to distinct points, then choose `L` large,
and let the perturbation go to zero. Finite replica sums are continuous in
the centres. Thus an arbitrary finite six-dimensional cloud with this
projected pair weight lies in the closure of admissible instantaneous
measures. The original map may be made an arbitrarily strict contraction.

This is a statement about individual times approaching an endpoint. It
does not assert anything about the measure integrated over the entire
path. The explicit example below supplies its own elementary global map,
so its validity does not depend on the extension theorem.

## 3. The explicit contraction

Put

\[
 G=\tfrac94\{-3,-2,-1,0,1,2,3\},\quad
 \epsilon=10^{-30},\quad L=10^{32},\quad
 t_*=L^2/(1+L^2).
\]

Let `A,B` be independent uniform random vectors in `G^3`, and set

\[
 X=L(A+\epsilon B),\qquad Y=B.                            \tag{6}
\]

There are exactly `7^6=117649` distinct input atoms, each with weight `7^-6`.
To define `T` on all of `R^3`, first prescribe the scalar function
`tau(L(a+epsilon b))=b` for `a,b in G`. Sort these `49` real input points,
interpolate linearly between consecutive points, and extend constantly on
both exterior rays. Define `T(x_1,x_2,x_3)=(tau(x_1),tau(x_2),tau(x_3))`.

Within an `a` block the slope is `1/(L epsilon)=1/100`. Between consecutive
blocks the slope is

\[
 -\frac6{L(1-6\epsilon)},
\]

whose absolute value is less than `1/100`. The ordering is strict because
`1-6 epsilon>0`. Thus `tau`, and hence `T`, is globally `1/100`-Lipschitz.
In particular every pairwise loss in (2) is nonnegative. The checker also
verifies all `1176` scalar pair inequalities with exact rational arithmetic.
The law is bounded and all input/output coordinates are rational.

At the selected time the lifted centres are

\[
 z_{t_*}(X)=\kappa(A+\epsilon B,B),\qquad
 \kappa=L/\sqrt{1+L^2}.                                  \tag{7}
\]

Let `m_j=integral u^j d eta_(t_*)(u)/L^2`. Scaling a positive measure does
not affect the sign of its transformed Hankel matrices. In (3) its pair
weight is now

\[
 W=|A-A'+\epsilon(B-B')|^2-L^{-2}|B-B'|^2.                \tag{8}
\]

## 4. A small exact reference calculation

The reference cloud is `(A,B)`, with pair weight `W_0=|A-A'|^2`. For `k=2,3,4`
define one-dimensional quantities

\[
 \begin{split}
 A_k&=\frac1{7^k\sqrt k}\sum_{a_1,\ldots,a_k\in G}e^{-E_k(a)},\\
 B_k&=\frac1{7^k\sqrt k}\sum_{a_1,\ldots,a_k\in G}
                    (a_1-a_2)^2e^{-E_k(a)},\\
 E_k(a)&=\frac1{2k}\sum_{r<s}(a_r-a_s)^2.
 \end{split}                                            \tag{9}
\]

Independence of the six coordinates and the three summands in `W_0` gives
the reference moments exactly:

\[
 m^0_{k-2}=3B_k A_k^5.                                   \tag{10}
\]

Only `7^2+7^3+7^4=2793` ordered one-dimensional tuples occur. They are
grouped by exact rational exponent before enclosing exponentials. A second
enumeration groups by multiplicities `c_i`, with multinomial coefficient
`k!/product c_i!`. For this enumeration the average distinguished pair
weight is

\[
 \frac2{k(k-1)}\sum_{i<j}c_i c_j(a_i-a_j)^2
   =\frac{4E_k}{k-1}.                                    \tag{11}
\]

The checker compares both exponent histograms, including their weighted
coefficients, entry by entry. This verifies the grouping and factor weights;
it is not a substitute for the six-coordinate factorisation proof (10).

For orientation only, rounded approximations to (10) are

```
m0_ref = 6.21396093275805e-5
m1_ref = 8.76070884993604e-10
m2_ref = 1.29978535498942e-14
```

The proof uses the outward rational intervals in `EXPECTED.json`, not these
display decimals.

## 5. Uniform transfer to the actual finite contraction

Each coordinate of `A,B` has absolute value at most `R=27/4`, so, writing
`D=12R^2=2187/4`, both squared vector differences `|A-A'|^2` and `|B-B'|^2`
are at most `D`. Cauchy--Schwarz, `1-kappa^2<=L^-2`, and (7) give

\[
 \big||z_{t_*}(X)-z_{t_*}(X')|^2
       -(|A-A'|^2+|B-B'|^2)\big|
 \le d:=D(2\epsilon+\epsilon^2+2L^{-2}).                  \tag{12}
\]

Similarly, (8) gives

\[
 |W-W_0|\le e:=D(2\epsilon+\epsilon^2+L^{-2}).            \tag{13}
\]

The energy in a `k`-replica term changes by at most `(k-1)d/4`. Both energies
are nonnegative, and `r -> exp(-r)` is `1`-Lipschitz on `[0,infinity)`.
Using `W_0<=D` in the finite expectation (3) therefore proves

\[
 \boxed{\quad |m_{k-2}-m^0_{k-2}|
       \le k^{-3}\left(e+\frac{D(k-1)d}{4}\right),
       \qquad k=2,3,4.\quad}                            \tag{14}
\]

This bound covers every atom pair and replica tuple, with no omitted region
or numerical quadrature. The finite parameters are fixed above; no limiting
law is substituted for the actual contraction.

Apply (14) to the rational enclosures of (9)-(10), and set `beta=17/10^6`.
The exact checker obtains

\[
 \begin{split}
 &m_0m_2/m_1^2<1.053<1.06<3/(2\sqrt2),\\
 &2\sqrt2\,m_0m_2-3m_1^2<-1.8\,10^{-20},\\
 &\beta^2\sqrt2\,m_0-2\beta\sqrt3\,m_1+2m_2
                        <-1.98\,10^{-16}.               \tag{15}
 \end{split}
\]

The first transformed matrix is

\[
 \begin{pmatrix}\sqrt2 m_0&\sqrt3 m_1\\
                 \sqrt3 m_1&2m_2\end{pmatrix}.
\]

Its determinant is the second line of (15), and the vector `(-beta,1)` has
the quadratic form in the third line. This proves the claimed failure of
instantaneous positivity. By continuity the failure persists on an open
interval of interior times, although no useful width is asserted.

## 6. The energy decreases along the lift, but its endpoint gap is nonnegative

The polynomial

\[
 V(u)=u^4/12-\beta u^3/3+\beta^2u^2/2
\]

is globally convex, since `V''(u)=(u-beta)^2`. Let
`I_k(t)=C6 integral (q_t/C6)^k`, and set

\[
 \mathcal E(t)=\frac{\beta^2}{2}\,2^{3/2}I_2(t)
               -\frac\beta3\,3^{3/2}I_3(t)
               +\frac1{12}\,4^{3/2}I_4(t).             \tag{16}
\]

At the endpoints, integrating the extra three Gaussian coordinates gives
`I_k(0)=k^(-3/2) C3 integral (f/C3)^k` and the analogous formula for `g`,
where `C3=(2*pi)^(-3/2)`, `f=mu*gamma^(3)`, and `g=(T_#mu)*gamma^(3)`.
Thus (16) has the desired three-dimensional convex-energy endpoints
`integral C3 V(f/C3)` and `integral C3 V(g/C3)`.

Differentiating the finite replica sum, using the `k(k-1)/2` interchangeable
pairs, yields

\[
 I_k'(t)=\frac{k-1}{4}\int u^{k-2}\,d\eta_t(u).
\]

Consequently at `t_*`,

\[
 \frac4{L^2}\mathcal E'(t_*)
   =\beta^2\sqrt2 m_0-2\beta\sqrt3 m_1+2m_2<0.           \tag{17}
\]

This is a concrete failure of monotonicity of the energy (16), obtained by
inverting the endpoint Gaussian marginalisation for a convex quartic.
The six-dimensional energy in (16) is not asserted to have nonnegative
pressure or to be convex. There is therefore no conflict with the source's
continuous-contraction theorem in six dimensions.

On the other hand, the scalar law of `L(a+epsilon b)` contracts to that of
`b`. The one-dimensional theorem of Aishwarya--Li gives scalar Gaussian
majorisation. This order is preserved under taking a product with a common
probability density `h`: for every positive threshold `r`,

\[
 \int (f(x)h(z)-r)_+\,dx\,dz
 =\int h(z)\int(f(x)-r/h(z))_+\,dx\,dz,
\]

with zero-density fibres contributing zero. Apply the scalar comparison
in each factor. Since (6) has three independent coordinate pairs, it follows
that `f` is majorised by `g`. Thus the integrated matrix in (4) is positive
semidefinite, and `E(1)>=E(0)`, despite (17).

The covariance-free rigidity estimate remains valid, as do the team's
half-order comparison and relative power-gap bounds. None implies the
false pointwise condition tested here. Any successful proof along this
lift must use information surviving integration over the path, or a
different comparison mechanism. No new Kneser--Poulsen consequence or
resolution of the full three-dimensional conjecture is claimed. QED.
