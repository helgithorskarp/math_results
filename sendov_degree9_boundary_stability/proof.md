# Boundary stability, with sharp exponents

Agent: six-sendov-2 (researcher). Coefficient field: `C`, characteristic zero.
Every root and critical point is counted with its algebraic multiplicity.

## Statement

Let `p` have degree nine, all its roots in the closed unit disk, and
`p(a)=0`, where `|a|=1`. Suppose

\[
 \min_{p'(\zeta)=0}|a-\zeta|\ge 1-\varepsilon,
 \qquad 0\le\varepsilon\le 10^{-5}.
\]

Then the eight critical points obey

\[
 \sum_{j=1}^{8}|\zeta_j|^2\le20\varepsilon.                 \tag{1}
\]

There is a labeling of the nine roots, with `z_0=a`, such that

\[
 |z_k-a\exp(2\pi i k/9)|\le1000\varepsilon,
 \qquad 0\le k\le8.                                      \tag{2}
\]

For positive epsilon the inequalities in (2) can be made strict. The
exponents `1/2` in `max |zeta_j|=O(sqrt(epsilon))` and `1` in (2)
cannot be increased, even within this boundary-root class.

A stronger version uses an average rather than a pointwise distance
hypothesis. At a boundary root define the quadratic deficit

\[
 \delta=\frac18\sum_{j=1}^8\frac1{|a-\zeta_j|^2}-1.
\]

This quantity is nonnegative. If it is finite and `0<=delta<=2*10^-5`, then

\[
 \sum_j|\zeta_j|^2\le9\delta,
 \qquad |z_k-a\exp(2\pi i k/9)|\le500\delta              \tag{2a}
\]

for a bijective labeling with `z_0=a`. Both exponents are sharp for this
version as well. This is a quantitative refinement of the known boundary
case of the quadratic Tang–Zhang inequality; that inequality itself is
not claimed new.

Rotate by `a` and divide by the leading coefficient to reduce to a monic
polynomial with distinguished root `1`. Rotation preserves all the distances
in the statement and the moduli of critical points. The positive lower bound
on critical-point distance forces the distinguished root to be simple.

## 1. The exact boundary deficit

For any degree `n>=2`, put `m=n-1` and write

\[
 p(z)=(z-1)\prod_{k=1}^{m}(z-z_k),\qquad
 p'(z)=n\prod_{j=1}^{m}(z-\zeta_j),\qquad
 q_j=\frac1{1-\zeta_j}.
\]

The distinguished root is assumed simple here. Taking the logarithmic
derivative of `p'` at `1`, or differentiating `(z-1)g(z)` twice, gives the
classical Meir–Sharma identity

\[
 \sum_j q_j=\frac{p''(1)}{p'(1)}
       =2\sum_k\frac1{1-z_k}.                             \tag{3}
\]

Define the nonnegative weighted radial deficit

\[
 D=\sum_k\frac{1-|z_k|^2}{|1-z_k|^2}\ge0.
\]

Since `2 Re(1/(1-z))=1+(1-|z|^2)/|1-z|^2`, (3) yields

\[
 \operatorname{Re}\sum_jq_j=m+D,
 \qquad
 \sum_j|q_j-1|^2+2D=\sum_j|q_j|^2-m.                    \tag{4}
\]

If all `|1-zeta_j|>=r>0`, then

\[
 0\le D\le m(r^{-1}-1),\qquad
 \sum_j|q_j-1|^2\le B:=m(r^{-2}-1).                      \tag{5}
\]

In particular the hypotheses imply `r<=1`. If `B<1`, then
`|q_j|>=1-sqrt(B)` and `zeta_j=(q_j-1)/q_j`, so

\[
 Q:=\sum_j|\zeta_j|^2\le\frac{B}{(1-\sqrt B)^2}.         \tag{6}
\]

At `r=1`, (4) forces every `q_j=1`, hence every critical point is zero;
the normalized polynomial is exactly `z^n-1`. This recovers the known
boundary equality case, rather than claiming it as new.

For degree nine and `0<epsilon<=10^-4`, set `r=1-epsilon`. The function
`8(2-epsilon)/(1-epsilon)^2` is increasing on this interval and is less
than `17` at its right endpoint. Thus `B<=17 epsilon` and
`sqrt(B)<=1/24`. Equation (6) gives

\[
 Q\le\frac{9792}{529}\varepsilon<20\varepsilon,
 \qquad T:=\max_j|\zeta_j|\le\sqrt Q<\frac1{22}.          \tag{7}
\]

Also `D<=8 epsilon/(1-epsilon)<=9 epsilon`. These calculations prove
(1) and leave room for the coefficient estimates below.

## 2. A Schur coefficient inequality

If

\[
 h(z)=z^n+c_{n-1}z^{n-1}+\cdots+c_1z+c_0
\]

has all roots in the closed unit disk, then

\[
 |c_{n-1}-c_0\overline{c_1}|
       \le(n-1)(1-|c_0|^2).                              \tag{8}
\]

Here is a proof including the boundary case. First suppose all roots lie
strictly inside the disk. Define the reflected polynomial
`h*(z)=z^n conjugate(h(1/conjugate(z)))`. On the unit circle,
`|h*|=|h|`, and `|c_0|<1`. Rouché's theorem shows that
`h-c_0 h*` has its `n` roots in the open disk. Its constant coefficient
vanishes, its leading coefficient is `1-|c_0|^2`, and division by `z`
leaves a degree `n-1` polynomial whose roots all lie in the disk. Its
next-to-leading coefficient is `c_{n-1}-c_0 conjugate(c_1)`.
Vieta's sum-of-roots formula and the triangle inequality imply (8).
For closed-disk roots apply this argument to the polynomial with every
root multiplied by `s`, where `0<s<1`, and take `s` to `1`. All
coefficients and both sides of (8) converge. This also covers `|c_0|=1`.

## 3. All coefficients have linear deficit

Continue with degree nine and `0<epsilon<=10^-4`. Write

\[
 p(z)=z^9+c_8z^8+\cdots+c_1z+c_0,
 \qquad E=\sum_{k=1}^{7}|c_k|.
\]

Integrating the factored derivative coefficient by coefficient gives

\[
 c_{9-k}=\frac9{9-k}(-1)^k e_k(\zeta_1,\ldots,\zeta_8),
 \qquad 1\le k\le8.                                    \tag{9}
\]

An elementary pair-counting bound will suffice. For nonnegative numbers
`x_j<=T` with `sum x_j^2=Q`,

\[
 e_k(x_1,\ldots,x_m)
 \le {m\choose k}\frac Qm T^{k-2},\qquad 2\le k\le m.   \tag{10}
\]

Indeed, expand each `k`-fold product by choosing one of its `binom(k,2)`
pairs. Bound the other factors by `T`, and use
`sum_{i<j} x_i x_j <= (m-1)Q/2`, which follows from Cauchy–Schwarz.
The multiplicity factor is
`binom(m-2,k-2)/binom(k,2)`, giving exactly (10).

Apply (10) to `x_j=|zeta_j|`, then use (9). One obtains

\[
 E\le\frac Q8\left(36+84T+126T^2+126T^3
                   +84T^4+36T^5+9T^6\right)
   \le\frac{41Q}{8}\le103\varepsilon,                  \tag{11}
\]

because the polynomial in parentheses is less than `41` at `T=1/22`.
In addition

\[
 |c_1|\le\frac{9Q}{8}T^6\le\varepsilon.                 \tag{12}
\]

It remains to control `c_8`. From (4), `Re sum q_j>=8`. The exact
expansion `q_j=1+zeta_j+zeta_j^2/(1-zeta_j)` gives

\[
 \operatorname{Re}\sum_j\zeta_j\ge-\frac Q{1-T}.
\]

The critical-distance hypothesis also implies
`2 Re zeta_j <= 1-r^2+|zeta_j|^2`. Consequently

\[
 -\frac Q{1-T}\le\operatorname{Re}\sum_j\zeta_j
       \le\frac{8(1-r^2)+Q}{2}.
\]

Since `c_8=-(9/8) sum zeta_j`, `Q<=20 epsilon`, `T<=1/22`, and
`1-r^2<=2 epsilon`, it follows that

\[
 -\frac{81}{4}\varepsilon\le\operatorname{Re}c_8
      \le\frac{165}{7}\varepsilon,
 \qquad |\operatorname{Re}c_8|\le24\varepsilon.           \tag{13}
\]

Use `p(1)=0` to write `c_0=-1-c_8-R`, where
`R=sum_{k=1}^7 c_k` and `|R|<=E`. Thus

\[
 1-|c_0|^2=-2\operatorname{Re}(c_8+R)-|c_8+R|^2
        \le2(|\operatorname{Re}c_8|+E)\le254\varepsilon.
\]

The left side is nonnegative because `|c_0|` is the product of the root
moduli. Combining (8), (11), (12), and (13) gives

\[
 |c_8|\le8\times254\varepsilon+|c_0|\,|c_1|
       \le2033\varepsilon,
 \qquad\sum_{k=1}^8|c_k|\le2136\varepsilon<2200\varepsilon.\tag{14}
\]

In particular, `sup_{|z|<=1}|p(z)-(z^9-1)|<=4400 epsilon`.
The crucial point is that the Schur transform controls the possible
imaginary part of the leading perturbation, which the critical-point
energy alone bounds only at square-root scale.

### The quadratic-deficit version

Suppose instead that `0<delta<=10^-4`, with `delta` as in (2a). Finiteness
forces the distinguished root to be simple. Equation (4) now reads

\[
 \sum_j|q_j-1|^2+2D=8\delta.                            \tag{14a}
\]

Thus `D<=4 delta`. Apply the argument for (6) with the upper bound
`B=8 delta`, rather than a bound arising from the smallest critical-point
distance. Since `sqrt(8 delta)<=1/32`, this gives

\[
 Q\le\frac{8192}{961}\delta<9\delta,
 \qquad T<\frac1{32}.                                  \tag{14b}
\]

From `Re sum q_j=8+D` and `q_j=1+zeta_j+zeta_j^2/(1-zeta_j)`,

\[
 \left|\operatorname{Re}\sum_j\zeta_j\right|
       \le D+\frac Q{1-T}.
\]

Consequently `|Re c_8| <= (927/62)delta < 15 delta`. The same
pair-counting bound gives `E<=41Q/8<=47 delta` and `|c_1|<=delta`.
Repeating the Schur step yields

\[
 |c_8|\le16(15+47)\delta+\delta=993\delta,
 \qquad\sum_{k=1}^8|c_k|\le1040\delta<1100\delta.        \tag{14c}
\]

These estimates require no individual upper bound on `|q_j|`.

## 4. Bijective root matching

Now assume `0<epsilon<=10^-5` and put `rho=1000 epsilon<=1/100`.
Around each ninth root of unity `omega`, consider `|z-omega|=rho`.
Writing `z=omega(1+w)` gives `|w|=rho` and

\[
 |z^9-1|\ge9\rho-\sum_{k=2}^9{9\choose k}\rho^k
          \ge8\rho=8000\varepsilon.                    \tag{15}
\]

The last estimate follows by evaluating the increasing tail divided by
`rho` at `rho=1/100`; its value is less than one. Meanwhile (14) and
`p(1)=0` give

\[
 |p(z)-(z^9-1)|
   =\left|\sum_{k=1}^8c_k(z^k-1)\right|
   \le\left((101/100)^8+1\right)2200\varepsilon
   <4620\varepsilon<8000\varepsilon.                   \tag{16}
\]

Rouché's theorem gives exactly one root in each disk. The disks are
disjoint: the minimum separation of ninth roots of unity is
`2 sin(pi/9)>=4/9>2/100`. The root in the disk about `1` is `1`
itself. This proves the bijection and (2). The zero-deficit case follows
from the exact equality argument after (6).

For the quadratic version take `rho=500 delta`, with
`0<delta<=2*10^-5`, so again `rho<=1/100`. The lower bound on
`|z^9-1|` is now `4000 delta`; the perturbation bound from (14c) is
less than `(21/10)*1100 delta=2310 delta`. The same Rouché argument
proves (2a). At `delta=0`, (14a) forces the exact regular polynomial.

## 5. Both exponents are sharp

For real `u>0` define

\[
 P_u(z)=z^9-\frac{27}{4}u z^8+\frac97(u+9u^2)z^7
        -1+\frac{27}{4}u-\frac97(u+9u^2).                \tag{17}
\]

Then `P_u(1)=0` and, exactly,

\[
 P'_u(z)=9z^6\left((z-3u)^2+u\right).                  \tag{18}
\]

For sufficiently small positive `u`, all nine roots lie in the closed
unit disk. Here is a proof that does not rely on numerically finding
roots. At `u=0` the roots are the simple ninth roots of unity. The
implicit-function theorem supplies analytic root functions

\[
 w_\omega(u)=\omega+v_\omega u+O(u^2),
 \quad
 \frac{v_\omega}{\omega}
     =\frac34(\omega^{-1}-1)-\frac17(\omega^{-2}-1).     \tag{19}
\]

The root function at `omega=1` is identically `1`. For every other
`omega=exp(i theta)`, put `c=cos(theta)<1`. Equation (19) gives

\[
 \operatorname{Re}\frac{v_\omega}{\omega}
   =(1-c)\left(-\frac34+\frac27(1+c)\right)
   \le-\frac5{28}(1-c)<0.                              \tag{20}
\]

Therefore `|w_omega(u)|^2=1+2 Re(v_omega/omega)u+O(u^2)<1`
for sufficiently small positive `u`. There are only eight such root
functions, so one positive parameter interval works for all of them.
They remain distinct and exhaust the degree-nine roots. This proves
the root-location assertion in full for some neighborhood of zero;
no explicit numerical endpoint for that neighborhood is claimed.

By (18) the critical points are six copies of `0` and `3u +/- i sqrt(u)`.
For sufficiently small `u>0`, their closest distance to `1` is

\[
 r_u=\sqrt{1-5u+9u^2}<1,
 \qquad\varepsilon_u=1-r_u=\frac52u+O(u^2).              \tag{21}
\]

The largest critical modulus is `sqrt(u+9u^2)`, so its ratio to
`sqrt(epsilon_u)` tends to `sqrt(2/5)`. A bound by a fixed multiple of
`epsilon_u^alpha` with `alpha>1/2` is impossible.

For any nontrivial `omega`, (20) ensures `v_omega!=0`; consequently
`|w_omega(u)-omega|=|v_omega|u+O(u^2)` and its ratio to
`epsilon_u` tends to `2|v_omega|/5>0`. Since the limiting ninth
roots of unity are distinct, any matching whose maximal error tends
to zero must be the local matching in (19). A bound by a fixed
multiple of `epsilon_u^alpha` with `alpha>1` is likewise impossible.

For the same family the quadratic deficit is exactly

\[
 \delta_u=\frac18\left(6+\frac2{1-5u+9u^2}\right)-1
        =\frac{5u-9u^2}{4(1-5u+9u^2)}
        =\frac54u+O(u^2).                              \tag{22}
\]

Replacing `epsilon_u` by `delta_u` in the preceding nonzero-limit
arguments proves sharpness of both exponents in (2a).

## Verification boundary

The proof uses ordinary complex polynomial factorization, Vieta's
formulas, Cauchy–Schwarz, Rouché's theorem, and the implicit-function
theorem. It is not a proof-assistant formalization. `verify.py` checks
the rational constants, derivative factorization, the implicit root
velocity modulo `omega^9-1`, and the radial identity by exact coefficient
comparison. Those checks support, but do not replace, the written proof.
