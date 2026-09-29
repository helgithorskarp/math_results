# Quantitative critical-energy stability and an explicit first-power annulus

Agent: **six-sendov-2**, role researcher, 2026-09-29.

## 1. Statements

All roots and critical points are counted with multiplicity. Let `p` have
degree nine and all its roots in the closed unit disk. Define

\[
F(a)=\sum_{j=1}^8|a-\zeta_j|^{-1},
\qquad Q=\sum_{j=1}^8|\zeta_j|^2.
\]

A zero denominator makes `F=+infinity`. Multiplication by a nonzero scalar
and rotation of the variable preserve these quantities, so normalize
`p` monic and its distinguished root to `a=|a|` in `[0,1]`.

**Quantitative reduction.** If `eta=1-a` satisfies `0<eta<=10^-6` and

\[
F(a)\le8+\frac\eta{20},                                 \tag{1}
\]

then

\[
Q\le1.6\times10^9\eta.                                 \tag{2}
\]

This is a necessary-condition statement, not an assertion that such
polynomials exist for any prescribed `eta`.

**Explicit annulus.** Every distinguished root with
`1-10^-18<=|a|<1` satisfies

\[
F(a)>8+\frac{1-|a|}{20}.                                \tag{3}
\]

The first theorem is proved in sections 2-6. Section 7 uses (2) and an
explicit local estimate to prove (3). No optimality is claimed for either
constant. At boundary roots the known inequality remains `F>=8`, with
both binomial and collapsed equality families; the strict result (3) is
only for interior roots.

## 2. Reciprocal other-root coordinates stay bounded

Assume (1). Finiteness makes `a` a simple root. Write the other roots as
`z_1,...,z_8`, and set

\[
q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|,\quad
\mu=\frac18\sum_j r_j,\quad
u_j=(a-z_j)^{-1},\quad \gamma=\frac1{160}.
\]

Thus `mu<=1+gamma eta`. All reciprocals are finite. Differentiating
`p(a+w)/p'(a)=w product_j(1+u_jw)` gives the exact identities

\[
e_k(q)=(k+1)e_k(u)\quad(0\le k\le8).                    \tag{4}
\]

Maclaurin's elementary-symmetric bound gives
`|e_k(q)|<=e_k(r)<=binom(8,k)mu^k`. Hence any root `u` of
`product_j(U-u_j)` with `|u|>=7mu` would satisfy

\[
1\le\sum_{k=1}^8\frac{|e_k(u_1,\ldots,u_8)|}{|u|^k}
\le\sum_{k=1}^8\frac{\binom8k}{(k+1)7^k}
=\frac{41980912}{51883209}<1,
\]

a contradiction. Therefore

\[
|u_j|<7\mu\le7(1+\eta/160)<8.                          \tag{5}
\]

Gauss–Lucas and the first-moment upper bound also imply

\[
\frac1{1+a}\le r_j\le8\mu-\frac7{1+a}<5.               \tag{6}
\]

The classical tools in this section are not claimed as new.

## 3. Root-containment controls real and angular defects

Put `b=1-a^2`. The disk condition on `z_j=a-1/u_j` is exactly

\[
b|u_j|^2+2a\operatorname{Re}u_j-1\ge0.                 \tag{7}
\]

Write `alpha_j=Re u_j-1/2`. Since `a>=99/100`, `b<=2eta`, and `|u_j|<8`,
equation (7) gives

\[
\alpha_j\ge-\frac{64\eta}{a}>-65\eta.
\]

Equation (4) for `k=1` gives
`sum alpha_j=(1/2)Re sum q_j-4<=eta/40`. Thus

\[
\sum_j|\alpha_j|<1100\eta,\qquad
|\alpha_j|<456\eta.                                    \tag{8}
\]

For example, the negative parts sum to at most `8*65eta=520eta`;
the positive parts sum to at most `520eta+eta/40`. An individual positive
part is at most `7*65eta+eta/40<456eta`.

Summing (7) and using (4) gives
`a Re sum q_j>=8-b sum |u_j|^2`. Consequently

\[
8-\operatorname{Re}\sum_jq_j
\le\frac{1016\eta}{a}<1030\eta.                         \tag{9}
\]

The formula for the upper bound is
`8-Re sum q <=(b sum|u|^2-8eta)/a`, with `sum|u|^2<512`.
Only the stated upper bound is used. Define the nonnegative angular defect

\[
D=\frac18\sum_j(r_j-\operatorname{Re}q_j).
\]

Equations (1) and (9) yield

\[
\sum_j(r_j-\operatorname{Re}q_j)<1100\eta,
\quad D\le140\eta,
\quad |\mu-1|\le130\eta.                               \tag{10}
\]

For the last bound, (9) implies `mu>=1-(1030/8)eta`, while
`mu<=1+eta/160` by assumption. This controls angular defects directly
from disk-root algebra, without invoking a compactness limit.

## 4. A finite polar variance bound

Let

\[
v=\frac18\sum_j(r_j-\mu)^2.
\]

We prove `v<5/4` on the present interval `0<eta<=10^-6`. The classical
polar identity, obtained by integrating `p'` from `a` to `1/a`, is

\[
\prod_j\frac{1-az_j}{a-z_j}
  =\int_0^1\prod_j(a+btq_j)\,dt.                        \tag{11}
\]

Each factor on the left has modulus at least one because
`|1-az|^2-|a-z|^2=b(1-|z|^2)>=0`. Triangle inequality and strong concavity
of `log(a+btr)` now give

\[
1\le\int_0^1(a+b\mu t)^8
 \exp\left[-\frac{4b^2t^2v}{(a+5bt)^2}\right]dt
\le J:=\int_0^1 A(t)e^{-E(t)}\,dt,                       \tag{12}
\]

where

\[
A(t)=(a+b(1+\gamma\eta)t)^8,\qquad
E(t)=\frac{4b^2t^2v}{(a+5bt)^2}.
\]

To justify the variance factor, on `0<=r<=5` the second derivative of
`log(a+btr)` is at most `-(bt)^2/(a+5bt)^2`. Taylor's inequality about
the mean `mu`, summed over the eight coordinates, cancels the linear
term and leaves `-4b^2t^2v/(a+5bt)^2`. The last inequality in (12) uses
`mu<=1+gamma eta`. This is the modulus-variance portion of the
complementary analytic lane's polar refinement; it is included here
self-contained.

The following bounds hold on the larger interval `0<eta<=1/100`:

\[
1-8\eta\le A(t)<2,\qquad
16(1-19\eta)\eta^2t^2v\le E(t)\le17\eta^2v\le425\eta^2. \tag{13}
\]

Indeed `a+b(1+gamma eta)t<=1+eta`, while `A>=a^8>=1-8eta`.
The upper bound uses `v<=25` by (6). For the lower bound, `a+5bt<=1+9eta`
and `b=(2-eta)eta`. The inequality

\[
\frac{(1-\eta/2)^2}{(1+9\eta)^2}\ge1-19\eta
\]

follows after clearing the denominator, leaving
`(1045/4)eta^2+1539eta^3>=0`.

We also have the finite expansion

\[
\int_0^1 A(t)\,dt
 \le1+\left(\frac{16}{3}+8\gamma\right)\eta^2+128\eta^3. \tag{14}
\]

For full uniformity, put
`w=(2t-1)eta+(2gamma-1)t eta^2-gamma t eta^3`, so `A=(1+w)^8`.
The terms of degrees at most two integrate to the displayed expression.
For `h=1/100`, the remaining absolute error divided by `eta^3` is at most

\[
8\gamma+28(1+h)(2+h+h^2)
 +\sum_{k=3}^8\binom8k h^{k-3}(1+h+h^2)^k<128.           \tag{15}
\]

Here use `|w|<=eta(1+h+h^2)` and
`|w-(2t-1)eta|<=eta^2(1+h)` for the quadratic binomial term.
All comparisons are rational and are verified in the checker.

Using `exp(-E)<=1-E+E^2/2`, equations (13)-(14) give

\[
\begin{split}
J\le 1+\left(\frac{16}{3}+8\gamma\right)\eta^2
 +128\eta^3
 -\frac{16}{3}(1-30\eta)\eta^2v+200000\eta^4.           \tag{16}
\end{split}
\]

For the loss term, `(1-8eta)(1-19eta)>=1-30eta` and
`int_0^1 t^2 dt=1/3`. For the last error, `A<2` and `E<=425eta^2`, so
`int A E^2/2 <=425^2 eta^4<200000eta^4`.
Since `1<=J` and `eta>0`, (16) implies

\[
v\le\frac{1+(3/2)\gamma+24\eta+37500\eta^2}{1-30\eta}
 <\frac54\qquad(0<\eta\le10^{-6}).                      \tag{17}
\]

The final rational expression increases with `eta` on this interval;
its endpoint value is less than `5/4`. No unquantified Taylor remainder
or limit is used in this variance exclusion.

## 5. An approximate symmetric relation

Replace `u_j` by `U_j=1/2+i Im u_j`. From (5), (8),
`|u_j|<8`, `|U_j|<9`, and `sum|u_j-U_j|<1100eta`.
Telescoping the factors in each elementary product gives

\[
|e_2(u)-e_2(U)|\le69300\eta,
\qquad |e_3(u)-e_3(U)|\le1871100\eta.                   \tag{18}
\]

The general constants are
`binom(7,k-1)9^(k-1) sum|u-U|`, for `k=2,3`.
For any eight numbers `U_j=1/2+i t_j` with real `t_j`, direct expansion
gives the real identity

\[
\operatorname{Re}e_3(U)=3\operatorname{Re}e_2(U)-14.      \tag{19}
\]

This does not require symmetry of the `t_j`. Indeed the real parts are
`Re e_2(U)=7-sum_(i<j)t_i t_j` and
`Re e_3(U)=7-3sum_(i<j)t_i t_j`.
Combining (4), (18), (19) yields

\[
|\operatorname{Re}e_3(q)-4\operatorname{Re}e_2(q)+56|
 \le8316000\eta.                                       \tag{20}
\]

To pass from complex `q_j` to nonnegative `r_j`, for any subset of `k`
coordinates write `q_j=r_j exp(i theta_j)`. The triangle inequality
and Cauchy–Schwarz for phase increments imply

\[
1-\cos\sum_j\theta_j\le k\sum_j(1-\cos\theta_j).
\]

Summing over subsets, using `r_j<5` and (10), gives

\[
0\le e_k(r)-\operatorname{Re}e_k(q)
 \le k\binom7{k-1}5^{k-1}(1100\eta).
\]

For `k=2,3` the respective bounds are `77000eta` and `1732500eta`.

Set `x_j=r_j-1/2>=0`, `e=e_1(x)=8mu-4`, `L=e_2(x)`, and `M=e_3(x)`.
The shifted symmetric identities are

\[
\begin{split}
L&=e_2(r)-\frac72e_1(r)+7,\\
M&=e_3(r)-3e_2(r)+\frac{21}{4}e_1(r)-7.
\end{split}
\]

Consequently

\[
\begin{split}
M-L&=e_3(r)-4e_2(r)+56+\frac{35}{4}(e_1(r)-8),\\
|M-L|&\le10366125\eta<11000000\eta,                     \tag{21}\\
4-1100\eta&\le e\le4+\eta/20.
\end{split}
\]

The coefficient in (21) is exactly
`8316000+1732500+4*77000+(35/4)*1100`.
At zero defect, the equality relation `M=L` is the degree-nine
boundary saturation relation from the complementary classification.
Here it is quantitative and is derived without assuming boundary roots
or real critical points.

## 6. Newton saturation gives linear energy control

For eight nonnegative `x_j`, Newton's inequality in the needed form is

\[
L^2\ge\frac74 eM.                                     \tag{22}
\]

An explicit polynomial certificate makes this step self-contained:

\[
12L^2-21eM
=\sum_{i<j}(x_i-x_j)^2
 \left(\sum_{k\ne i,j}x_k^2+
       \sum_{\substack{k<\ell\\k,\ell\ne i,j}}x_kx_\ell\right)\ge0. \tag{23}
\]

Direct expansion verifies (23). The coefficients on either side are
`12`, `3`, and `-12` for monomial types `x_i^2 x_j^2`,
`x_i^2 x_j x_k`, and `x_i x_j x_k x_l`; all other types vanish.
Each bracket on the right is nonnegative. The exact sparse checker
also verifies the full eight-variable identity and rejects a changed
coefficient. The classical Newton inequality is not claimed as new.

The variance is exactly

\[
v=\frac{7e^2-16L}{64}.                                 \tag{24}
\]

Equation (17) and `e>=4-1100eta` imply

\[
L>\frac7{16}(4-1100\eta)^2-5>1.
\]

Cauchy–Schwarz gives `L<=7e^2/16<8`. These inequalities hold throughout
`eta<=10^-6`. Combining (21)-(22), with `K=11000000`, gives

\[
\begin{split}
L^2&\ge\frac74 e(L-K\eta),\\
L(7-L)&\le\frac74(1100)\eta L+8K\eta
       <90000000\eta.
\end{split}
\]

Since `L>1`, we obtain `7-L<=90000000eta`; this conclusion also holds
if `L>7`. Using `e<=4+eta/20` in (24) then proves

\[
v\le22500000\eta+\eta<23000000\eta.                     \tag{25}
\]

The extra `eta` bounds
`(7/64)[(4+eta/20)^2-16]` on the entire interval.
The exact identity

\[
\sum_j|q_j-1|^2=8\left[v+(\mu-1)^2+2D\right]
\]

and (10), (25) imply

\[
\sum_j|q_j-1|^2<190000000\eta.                          \tag{26}
\]

Indeed its coefficient after division by `eta` is bounded by
`8(23000000+130^2*10^-6+280)<190000000`.
Finally
`zeta_j=-eta+(q_j-1)/q_j`, and `r_j>=1/(1+a)>1/2`. Therefore

\[
Q\le16\eta^2+8\sum_j|q_j-1|^2
 <1600000000\eta,                                      \tag{27}
\]

as claimed in (2). This is the explicit stability estimate toward the
binomial configuration. The polar variance exclusion is necessary:
at a boundary root the collapsed equality family has variance `7/4`,
whereas the finite bound (17) forces variance below `5/4` here.

## 7. Explicit local margin and the annulus

We use the fully quantified coefficient calculation in
[the preceding clustered-critical proof](https://github.com/helgithorskarp/math_results/blob/4387d05063a12f670bfa83e6924bf0e4ba59dbd7/sendov_degree9_clustered_critical_first_power/PROOF.md),
sections 2-5, with one changed hypothesis. Its uniform Taylor and Schur
estimates depend on `T<=1/100`, `a>=3/4`, and `eta<=3T`; the assumption
`F<=8` was used only to establish the last of these bounds. Below we
establish it from the weaker (1), making the reuse explicit.

Put `T=max|zeta_j|` and `s=|sum zeta_j|`. If `T<=1/10000`, `a>=3/4`,
and (1) holds, the preceding proof's coarse Taylor inequality gives

\[
(8-1/20)\eta\le2s+4Q,
\qquad \eta\le\frac s3+\frac{2Q}{3}\le3T.              \tag{28}
\]

For the last comparison use `s<=8T`, `Q<=8T^2`, and `T<=1/100`.
The earlier integration/Schur calculation then gives, with
`X=sum(Re zeta)^2`, `Y=sum(Im zeta)^2`, and `P_2=sum zeta^2`,

\[
\operatorname{Re}\sum\zeta_j
\ge s/16-8\eta-(4/7)\operatorname{Re}P_2-60Ts-58TQ,
\]

and its Taylor comparison gives

\[
F-8\ge(1/16-72T)s+(1/14-182T)Q
 >\frac{s+Q}{20}\ge\frac{3\eta}{40},                   \tag{29}
\]

where the strict step uses `eta>0` and (28). Both coefficients exceed
`1/20` at `T<=1/10000`, as verified rationally. This contradicts
`F-8<=eta/20`. Thus the following explicit local margin holds:

> Every interior root of a disk-root degree-nine polynomial with
> `T<=1/10000` has `F>8+(1-a)/20`.

For `a<3/4`, the same assertion follows directly from
`F>=8/(a+T)>8+1/20`, or infinity, so no case is omitted.

Now let `0<eta<=10^-18`. If (3) failed, (1) and (27) would give
`T^2<=Q<1.6*10^-9<10^-8`, hence `T<1/10000`. The explicit local
margin contradicts (1). This proves the announced numerical annulus.

## 8. Dependencies and verification boundary

The only substantive published input used without reproducing its full
coefficient derivation is the explicit local Taylor/Schur calculation
at source commit `4387d05063a12f670bfa83e6924bf0e4ba59dbd7`.
Section 7 states exactly why its hypotheses remain valid. The polar
variance method and saturation relation are cited complementary ideas;
sections 2-6 provide their own finite bounds and deductions and do not
invoke the qualitative concentration theorem.

The checker uses standard-library exact rational arithmetic and a sparse
integer polynomial expansion. It certifies every displayed rational
constant, the shifted identities, the Newton identity, and controls.
The universal analytic bridges are the written proof, not finite sampling.
Taylor remainder bounds here are finite binomial bounds. The local proof
dependency uses ordinary Taylor and Rouché/Schur arguments. No numerical
root solver, solver nonexistence output, imported formalization, or private
data establishes the result. Independent review of this new claim remains
outstanding. The full first-power inequality on the middle modulus range
is unresolved in this artifact.
