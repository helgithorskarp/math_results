# Proof: a local first-power inequality and a uniform boundary annulus

Agent: **six-sendov-2**, researcher, 2026-09-29.

## 1. Statements and normalization

**Local theorem.** Let `p` be a degree-nine complex polynomial whose roots
are all in the closed unit disk. Write its eight critical points, with
multiplicity, as `zeta_1,...,zeta_8`. If

\[
 T:=\max_j|\zeta_j|\le\frac1{10000},
\]

then at every root `a` of `p`,

\[
 F(a):=\sum_{j=1}^8|a-\zeta_j|^{-1}\ge8.                 \tag{1}
\]

The sum is infinite if a denominator vanishes. Equality in (1) holds
exactly when `|a|=1` and `p(z)=C(z^9-a^9)` for a nonzero constant `C`.

**Annulus corollary.** There exists `eta_9>0`, independent of `p`, such that
every interior root with `1-eta_9<|a|<1` satisfies `F(a)>8`, even without
the hypothesis on `T`. This uses the published degree-nine concentration
result of six-sendov-1, specified in section 7. The proof here gives no
explicit numerical value for `eta_9`.

For the local theorem, multiply `p` by a nonzero scalar and rotate the
variable so that `p` is monic and `a` is real, `0<=a<=1`. Rotation preserves
`T` and every distance in (1). Multiple distinguished roots have `F=+infinity`
and are already covered. If `a<3/4`, every critical distance is at most
`a+T<1`, so each finite reciprocal is greater than one. It remains to
consider `3/4<=a<=1` and finite `F`.

Write

\[
 \begin{gathered}
 \eta=1-a,\qquad S=\sum_j\zeta_j,\qquad s=|S|,\qquad
 Q=\sum_j|\zeta_j|^2,\\
 X=\sum_j(\operatorname{Re}\zeta_j)^2,\qquad
 Y=\sum_j(\operatorname{Im}\zeta_j)^2,\qquad
 P_2=\sum_j\zeta_j^2.
 \end{gathered}
\]

Thus `Q=X+Y`, `Re P_2=X-Y`, `s<=8T`, and `Q<=8T^2`.
All auxiliary estimates below hold with the looser bound `T<=1/100`.
Assume throughout the contradiction argument that `F<=8`.

## 2. A uniform second-order expansion

For `zeta=x+iy`, put `u=2x/a-|zeta|^2/a^2`. When `a>=3/4` and `T<=1/100`,

\[
 |u|\le\frac83\frac1{100}+\frac{16}{9}\frac1{10000}
       <\frac1{10}.
\]

Taylor's theorem for `(1-u)^(-1/2)` gives

\[
 (1-u)^{-1/2}=1+\frac u2+\frac{3u^2}{8}+R(u),
 \qquad |R(u)|\le|u|^3.                                 \tag{2}
\]

Indeed the absolute third-order remainder coefficient is at most
`(5/16)(10/9)^(7/2)<(5/16)(10/9)^4<1`. Substitution into
`|a-zeta|^(-1)=a^(-1)(1-u)^(-1/2)` gives the constant, linear and quadratic
terms

\[
 \frac1a+\frac x{a^2}+\frac{3x^2-|\zeta|^2}{2a^3}.
\]

The remaining polynomial terms are
`-(3/2)x|zeta|^2/a^4+(3/8)|zeta|^4/a^5`. Since
`|u|<=3|zeta|/a`, the total absolute error for this critical point is at
most

\[
 \left[27(4/3)^4+\frac32(4/3)^4+
       \frac38(4/3)^5\frac1{100}\right]|\zeta|^3
 =\frac{182432}{2025}|\zeta|^3<100|\zeta|^3.
\]

Summing proves

\[
 F=\frac8a+\frac{\operatorname{Re}S}{a^2}
          +\frac{3X-Q}{2a^3}+E,
 \qquad |E|\le100TQ.                                   \tag{3}
\]

Because `1/(2a^3)+100T<=32/27+1<4`, equation (3) implies
`F>=8/a+Re S/a^2-4Q`. The assumption `F<=8` therefore gives

\[
 8\eta\le\frac8a-8\le2s+4Q,
 \qquad \eta\le\frac s4+\frac Q2
              \le2T+4T^2\le3T.                         \tag{4}
\]

## 3. Coefficient bounds from the derivative

Write

\[
 p(z)=z^9+c z^8+b z^7+\sum_{k=1}^6c_kz^k+c_0.
\]

From `p'(z)=9 product_j(z-zeta_j)`, integration of coefficients gives

\[
 c_{9-k}=\frac9{9-k}(-1)^k e_k(\zeta_1,\ldots,\zeta_8)
 \quad(1\le k\le8).
\]

In particular

\[
 c=-\frac98 S,\qquad b=\frac9{14}(S^2-P_2),
 \qquad |b|\le s^2+Q.                                  \tag{5}
\]

For nonnegative `x_j<=T` with `sum_j x_j^2=Q`, the elementary
pair-counting inequality is

\[
 e_k(x_1,\ldots,x_8)\le{8\choose k}\frac Q8 T^{k-2}
 \quad(2\le k\le8).                                    \tag{6}
\]

To see this, choose each pair in each `k`-element product and bound the
other `k-2` factors by `T`. Each pair occurs `binom(6,k-2)` times, while
each product has `binom(k,2)` pairs. Finally
`sum_(i<j) x_i x_j <=7Q/2` by Cauchy–Schwarz, which gives (6).
This is the same elementary estimate used in the earlier boundary
stability artifact; no novelty is claimed for (6).

Equations (5)-(6) show that, when `T<=1/100`,

\[
 \begin{split}
 \sum_{k=1}^6|c_k|
 &\le\frac Q8(84T+126T^2+126T^3+84T^4+36T^5+9T^6)
 \le13TQ,\\
 |c_1|&\le\frac98QT^6\le2TQ.                            \tag{7}
 \end{split}
\]

Put `R_a=sum_(k=1)^6 c_k a^k` and `Z=a^8c+a^7b+R_a`. Since `p(a)=0`,

\[
 c_0=-a^9-Z.                                           \tag{8}
\]

We now make the replacement of `Z` by `c+b` quantitative. For an integer
`k>=1`, `1-a^k<=k eta`. Using (4), (5), (7), and `s^2<=8Ts`,

\[
 \begin{split}
 |Z-(c+b)|
 &\le9\eta s+7\eta(s^2+Q)+13TQ\\
 &\le29Ts+34TQ,                                        \tag{9}\\
 |Z|&\le\frac98s+s^2+(1+13T)Q,\\
 9\eta|Z|&\le33Ts+31TQ.                               \tag{10}
 \end{split}
\]

For clarity, the coefficient of `Ts` in the first bound is at most
`27+168/100<29`, and in (10) at most `243/8+216/100<33`.
The coefficient of `TQ` in (10) is at most `27(1+13/100)<31`.
It follows that

\[
 |a^9Z-(c+b)|\le62Ts+65TQ.                             \tag{11}
\]

Because the roots of the monic polynomial lie in the disk, `|c_0|<=1`.
Equation (8), `1-a^18<=18 eta`, and (11) imply

\[
 \begin{split}
 1-|c_0|^2
 &=1-a^{18}-2a^9\operatorname{Re}Z-|Z|^2\\
 &\le18\eta-2\operatorname{Re}(c+b)+124Ts+130TQ\\
 &\le18\eta+\frac94\operatorname{Re}S
       +\frac97\operatorname{Re}P_2+135Ts+130TQ.        \tag{12}
 \end{split}
\]

In the last step `-(9/7)Re(S^2)<=(9/7)s^2<=(72/7)Ts` was used,
and `124+72/7<135`.

## 4. The Schur constraint on the critical first moment

For a monic disk-root polynomial
`h(z)=z^n+d_(n-1)z^(n-1)+...+d_1z+d_0`, the standard Schur transform gives

\[
 |d_{n-1}-d_0\overline{d_1}|
       \le(n-1)(1-|d_0|^2).                            \tag{13}
\]

Here is a proof to make the root-containment hypothesis explicit. If all
roots are strictly in the disk, let
`h*(z)=z^n conjugate(h(1/conjugate(z)))`. On `|z|=1`, `|h*|=|h|` and
`|d_0|<1`, so Rouché's theorem puts all `n` roots of `h-d_0 h*` in the
disk. Its constant term vanishes. Division by `z` leaves a degree `n-1`
disk-root polynomial with leading coefficient `1-|d_0|^2` and next
coefficient `d_(n-1)-d_0 conjugate(d_1)`. Vieta and the triangle inequality
give (13). For closed-disk roots, first scale every root by `r<1`, and
then let `r` increase to one. Both sides of (13) are continuous in the
coefficients. This also covers `|d_0|=1`.

Apply (13) with `n=9`. Its left side is at least
`(9/8)s-2TQ` by (5), (7), and `|c_0|<=1`. Combining with (12) gives

\[
 \frac98s-2TQ\le144\eta+18\operatorname{Re}S
       +\frac{72}{7}\operatorname{Re}P_2+1080Ts+1040TQ.
\]

Hence

\[
 \operatorname{Re}S
 \ge\frac{s}{16}-8\eta-\frac47\operatorname{Re}P_2
                         -60Ts-58TQ.                  \tag{14}
\]

The rounded last coefficient is safe because `(1040+2)/18=521/9<58`.
This is the disk-root information that controls potentially adverse
linear terms in the first-power expansion.

## 5. A strictly positive second-order estimate

For `3/4<=a<=1`,

\[
 a^{-2}-1\le4\eta,\qquad a^{-3}-1\le8\eta.
\]

Use these in (3). Since `|3X-Q|<=2Q` and `eta<=3T`,

\[
 F-8\ge8\eta+\operatorname{Re}S+\frac{3X-Q}{2}
                                      -12Ts-124TQ.     \tag{15}
\]

Substitute (14) and `Re P_2=X-Y`. The `eta` terms cancel, yielding

\[
 \begin{split}
 F-8
 &\ge\left(\frac1{16}-72T\right)s
       +\frac37X+\frac1{14}Y-182TQ\\
 &\ge\left(\frac1{16}-72T\right)s
       +\left(\frac1{14}-182T\right)Q.                 \tag{16}
 \end{split}
\]

At `T<=1/10000` the two coefficients in the last line are positive:

\[
 \frac1{16}-\frac{72}{10000}=\frac{553}{10000}>0,
 \qquad
 \frac1{14}-\frac{182}{10000}=\frac{1863}{35000}>0.
\]

The assumed `F<=8` therefore forces `Q=0`. All critical points are zero,
so `p(z)=z^9+c_0`. The equation `p(a)=0` makes this `p(z)=z^9-a^9`, and
`F=8/a` on the branch `a>=3/4`. Since `a<=1`, `F<=8` forces `a=1`.
Conversely, `p(z)=z^9-1` at any of its roots has eight critical points
at zero and `F=8`. Undoing normalization proves the local theorem and
its exact equality condition.

## 6. Logical scope of the computation

The proof is an ordinary universal argument. The attached standard-library
checker uses rational arithmetic to verify the constants in the estimate
chain and the polynomial Taylor algebra. It checks derivative-to-coefficient
identities and controls for scaled binomials, and rejects an intentionally
altered positivity margin. It does not certify root containment for a
sample family as a substitute for (13), nor does it establish a universal
statement by finite sampling. Taylor's theorem, Rouché's theorem,
Cauchy–Schwarz, and the written inequality deductions remain part of the
ordinary mathematical proof. No independent review or formal proof is
claimed.

## 7. The annulus corollary and its published dependency

The complementary analytic lane, **six-sendov-1**, proved the following
conditional concentration statement in sections 6-7 of
[its published proof](https://github.com/helgithorskarp/math_results/blob/728857924504f28020dea5de6590ae3458b7bc90/sendov_degree9_first_power_polar/PROOF.md):

> If monic degree-nine disk-root polynomials `p_k` have real roots
> `0<a_k<1` with `a_k->1` and `F_k(a_k)<=8`, then `p_k` converges
> coefficientwise to `z^9-1` and `max_j |zeta_(k,j)|->0`.

This statement includes equality in the failure hypothesis. Its proof
uses the polar identity with angular deficit and modulus variance, the
boundary equality classification into binomial and collapsed two-root
families, and the limiting variance bound `limsup v<=1`. The collapsed
family has variance `7/4` and is excluded. This artifact uses that
published ordinary proof as a mathematical dependency and does not
repackage the concentration or classification as a new result.

Suppose the annulus corollary were false. For every positive integer `k`
there would be a degree-nine disk-root polynomial and an interior root
`a_k` with `1-1/k<|a_k|<1` and `F_k(a_k)<=8`. Make the polynomials monic
and rotate their distinguished roots to be real. The cited concentration
statement gives `T_k->0`. For all sufficiently large `k`, `T_k<=1/10000`,
so the local theorem gives strict `F_k(a_k)>8`, since `a_k<1`. This is a
contradiction. Thus a uniform positive annulus width exists.

The width obtained by this compactness argument is not effective. The
first-power inequality in the intervening range of root moduli remains
open in this work. The result neither resolves the complete first-power
Tang–Zhang endpoint nor claims novelty for the already published Sendov
existence assertion.
