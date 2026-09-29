# First-power boundary stability around two equality families

Author: **six-sendov-2**, role **researcher**. Every root and critical point
is counted with its algebraic multiplicity. The proof is over the complex
numbers in characteristic zero. This is an ordinary written proof, not a
proof-assistant formalization or a literature-priority assertion.

## Statement

Let a degree-nine polynomial have all its roots in the closed unit disk,
and let `a` be one of its roots with `|a|=1`. Define the finite deficit

\[
 \tau=\frac18\sum_{j=1}^8|a-\zeta_j|^{-1}-1,
 \qquad 0\le\tau\le10^{-10}.                              \tag{1}
\]

The deficit is automatically nonnegative, as shown below. Exactly one of
the following algebraic branches applies. The labels in each branch are
bijections of multisets, and the distinguished root is anchored at `a`.

**Regular branch.** There is a labeling `z_0=a,z_1,...,z_8` such that

\[
 \max_{0\le k\le8}|z_k-ae^{2\pi i k/9}|
       \le2500\tau,
 \qquad Q:=\sum_j|\zeta_j|^2\le693000\tau.                \tag{2}
\]

More precisely, define the weighted radial defect of the other roots by
`D=sum_{k=1}^8 (1-|z_k|^2)/|a-z_k|^2`. The same anchored matching satisfies

\[
 \max_k|z_k-ae^{2\pi i k/9}|
       \le300D+2500(77000\tau)^{5/2}.                    \tag{3}
\]

If all nine original roots lie on the unit circle, `D=0`, giving the
restricted regular matching rate `2500(77000tau)^(5/2)`.

**Collapsed branch.** The other eight roots and a labeling of the critical
points satisfy

\[
 \max_{1\le k\le8}|z_k+a|\le800\sqrt\tau,\qquad
 \max\left\{\max_{1\le j\le7}|\zeta_j+a|,
                    |\zeta_8-7a/9|\right\}
       \le52\sqrt\tau.                                  \tag{4}
\]

The regular full-disk root exponent `1`, regular unit-circle root exponent
`5/2`, and collapsed root exponent `1/2` are sharp, even allowing either
equality family in the conclusion. The square-root critical-point rates
are also sharp. All constants are conservative; their optimality is not
asserted.

The two limiting polynomials are scalar multiples of `z^9-a^9` and
`(z-a)(z+a)^8`. Their first-power equality classification is already in
[the complementary lane's proof, sections 4 and 7](../sendov_degree9_first_power_polar/PROOF.md).
The contribution here quantifies proximity to that union and distinguishes
the rates; it does not claim the classification anew. The regular branch
uses the published [quadratic-deficit stability theorem](../sendov_degree9_boundary_stability/proof.md).
The coefficient mechanism behind the restricted improvement uses the independent
[unit-circle refinement](../sendov_degree9_boundary_stability_review2/REFINEMENT.md).

Rotate by `a` and divide by the leading coefficient, reducing to a monic
polynomial with distinguished root `1`. This preserves all asserted
distances and critical moduli. Finiteness of (1) means the distinguished
root is simple. Write

\[
 p(z)=(z-1)\prod_{k=1}^8(z-z_k),\qquad
 p'(z)=9\prod_{j=1}^8(z-\zeta_j),\qquad
 u_k=(1-z_k)^{-1},\quad q_j=(1-\zeta_j)^{-1},\quad r_j=|q_j|.
\]

## 1. Reciprocal identities and bounded coordinates

Let `e_k` denote elementary symmetric polynomials. Differentiating

\[
 p(1+w)=p'(1)w\prod_{k=1}^8(1+wu_k)
\]

and comparing with `p'(1+w)=p'(1)prod_j(1+wq_j)` gives

\[
 e_k(q)=(k+1)e_k(u),\qquad 1\le k\le8.                 \tag{5}
\]

In particular `sum q=2 sum u`. Disk containment implies

\[
 \operatorname{Re}u_k-\tfrac12
       =\frac{1-|z_k|^2}{2|1-z_k|^2}\ge0.               \tag{6}
\]

Thus `Re sum q>=8`, so `sum r>=8` and `tau>=0`. Put

\[
 \alpha_k=\operatorname{Re}u_k-\tfrac12,\quad
 A=\sum_k\alpha_k,\quad d_j=r_j-\operatorname{Re}q_j.
\]

All these quantities are nonnegative and

\[
 A\le4\tau,\qquad \sum_j d_j\le8\tau.                 \tag{7}
\]

Gauss–Lucas places every critical point in the closed unit disk, so
`r_j>=1/2`. With `mu=1+tau` and `sum r=8mu`,

\[
 \tfrac12\le r_j\le\tfrac92+8\tau<5.                  \tag{8}
\]

We also have `|u_k|<7mu<8`. For completeness, (5), the triangle
inequality, and the standard Maclaurin bound for nonnegative `r_j` give

\[
 |e_k(u)|\le\frac1{k+1}e_k(r)
       \le\frac{\binom8k}{k+1}\mu^k.
\]

If a root `u` of the monic reciprocal-root polynomial had `|u|>=7mu`,
its polynomial equation divided by `u^8` would imply

\[
 1\le\sum_{k=1}^8\frac{\binom8k}{(k+1)7^k}
       =\frac{41980912}{51883209}<1,
\]

a contradiction. The coordinate bounds (7)–(8), symmetric estimates
(9)–(14), variance comparisons in (15), and bound (16) hold on the larger
range `tau<=1/100`. The transfer to quadratic stability and the root
matching argument require the smaller range (1).

## 2. Approximate saturation of an exact Newton inequality

Project `u_k` to the vertical line by
`U_k=1/2+i Im u_k`. Then `|U_k|<=|u_k|<8` and
`sum |u_k-U_k|=A<=4tau`. Telescoping each product in `e_k` gives

\[
 |e_2(u)-e_2(U)|\le7\cdot8 A\le224\tau,
 \qquad
 |e_3(u)-e_3(U)|\le21\cdot8^2 A\le5376\tau.             \tag{9}
\]

If `t_k=Im u_k`, direct expansion gives
`Re e_2(U)=7-e_2(t)` and `Re e_3(U)=7-3e_2(t)`. Therefore
`Re e_3(U)=3 Re e_2(U)-14`. By (5) and (9),

\[
 |\operatorname{Re}e_3(q)-4\operatorname{Re}e_2(q)+56|
       \le4(5376+3\cdot224)\tau=24192\tau.              \tag{10}
\]

We need a phase bound that remains valid even when individual reciprocal
arguments are large. For `q_j=r_j exp(i theta_j)` and a `k`-element subset,
the triangle inequality followed by Cauchy–Schwarz implies

\[
 1-\cos\left(\sum\theta_j\right)
       \le k\sum(1-\cos\theta_j).
\]

Multiply by the corresponding product of moduli, use `r_j<=R`, and sum
over subsets. Each index belongs to `binom(7,k-1)` subsets, so

\[
 0\le e_k(r)-\operatorname{Re}e_k(q)
       \le k\binom7{k-1}R^{k-1}\sum_jd_j.              \tag{11}
\]

At `R=5`, the bounds for `k=2,3` are `560tau` and `12600tau`.
Set

\[
 x_j=r_j-\tfrac12\ge0,\qquad
 e=e_1(x)=4+8\tau,\qquad L=e_2(x),\qquad M=e_3(x).
\]

Expanding this shift gives the exact identity

\[
 M-L=e_3(r)-4e_2(r)+56+\frac{35}{4}(e_1(r)-8).
\]

Equations (10) and (11) yield

\[
 |M-L|\le(24192+12600+4\cdot560+70)\tau
       =39102\tau<40000\tau\quad(\tau>0).              \tag{12}
\]

The following eight-variable sum of squares is an exact polynomial
identity, checked coefficient by coefficient in `verify.py`:

\[
 12L^2-21eM
  =\sum_{i<j}(x_i-x_j)^2
     \left(\sum_{k\notin\{i,j\}}x_k^2
       +\sum_{\substack{k<l\\k,l\notin\{i,j\}}}x_kx_l\right)
  \ge0.                                               \tag{13}
\]

Here the nonnegative bracket uses `x_j>=0`. Consequently
`L^2>=(7/4)eM=(7+14tau)M`, and (12) implies

\[
 L(7-L)\le(7+14\tau)40000\tau-14\tau L
       \le300000\tau.                                 \tag{14}
\]

Define the regular branch by `L>=1` and the collapsed branch by `L<1`.
They are mutually exclusive and exhaustive. This boundary argument does
not exclude the collapsed branch: its reciprocal variance is `7/4` at
equality, despite its first-power deficit being zero.

## 3. Regular branch and transfer to quadratic stability

If `L>=1`, (14) gives `7-L<=300000tau`. Indeed, this follows by division
when `L<=7`, and is automatic when `L>7`. The variance of the moduli and
the quadratic deficit are exactly

\[
 v=\frac18\sum_j(r_j-\mu)^2
       =\frac{7-L}{4}+7\tau+7\tau^2\le76000\tau,
 \qquad
 \delta_2=\frac18\sum_jr_j^2-1
       =v+2\tau+\tau^2\le77000\tau.                   \tag{15}
\]

These comparisons hold for `tau<=1/100`. Under (1),
`delta_2<=77/10^7<2*10^-5`. The previously published quadratic-deficit
stability theorem gives `Q<=9delta_2`, and hence
`T=max |zeta_j|<=3sqrt(delta_2)<1/32`. This proves the energy part of (2).

We now quantify how radial root defects spoil the independent refinement's
self-inversive coefficient argument. By (6), the defect in (3) equals
`D=2A<=8tau`. Write `p(z)=z^9+sum_{k=0}^8 c_k z^k`. Replace each original
root by its radial projection to the unit circle, keeping `1` fixed; at a
zero root choose any unit argument. Let the resulting monic polynomial be
`p_tilde(z)=z^9+sum b_k z^k`. Its coefficients obey
`|b_0|=1` and `b_k=b_0 conjugate(b_{9-k})`.

For polynomial coefficient norm `||h||_1=sum |h_k|`, telescoping the nine
root factors and using submultiplicativity gives

\[
 \|p-\widetilde p\|_1
  \le2^8\sum_{k=1}^8(1-|z_k|)
  \le2^8\sum_{k=1}^8(1-|z_k|^2)\le1024D.              \tag{15a}
\]

The last inequality uses `|1-z_k|^2<=4` in the definition of `D`.
For each `1<=k<=4`, equal moduli of paired `b` coefficients imply

\[
 |c_{9-k}|\le|c_k|+|c_k-b_k|+|c_{9-k}-b_{9-k}|.
\]

Integration of the derivative gives
`c_k=(9/k)(-1)^(9-k)e_{9-k}(zeta)`. Pair averaging gives
`|e_h(zeta)|<=binom(8,h)(Q/8)T^(h-2)` for `h>=2`, as proved in the
quadratic input. Summing the four coefficient pairs, then using (15a),

\[
 C:=\sum_{k=1}^8|c_k|
  \le\frac Q4(126T^3+84T^4+36T^5+9T^6)+1024D
  \le\frac{31347}{4}\delta_2^{5/2}+1024D.              \tag{15b}
\]

Indeed `126+84/32+36/32^2+9/32^3<129` and
`(9/4)*129*27=31347/4`. This extends the published exact unit-circle
argument to a controlled radial error.

For `tau>0` set `rho=300D+2500delta_2^(5/2)`. This is positive because
`delta_2>=2tau+tau^2`. Also `rho<1/100`: use `D<=8*10^-10`,
`delta_2<=2*10^-5` and `sqrt(delta_2)<1/200` for a coarse bound.
On a circle of radius `rho` about a ninth root of unity `omega`, write
`z=omega(1+w)`, where `|w|=rho`. The binomial expansion gives
`|z^9-1|>=9rho-sum_{k=2}^9 binom(9,k)rho^k>=8rho`, since the increasing
tail divided by `rho` is less than one at `rho=1/100`. Since `p(1)=0`,

\[
 |p(z)-(z^9-1)|
   =\left|\sum_{k=1}^8c_k(z^k-1)\right|
   \le\bigl((101/100)^8+1\bigr)C
   <\frac{21}{10}C<8\rho.                             \tag{15c}
\]

The last comparison follows separately for both terms in (15b):
`(21/10)*1024<8*300` and `(21/10)*(31347/4)<8*2500`.
The nine disks are disjoint, since adjacent ninth roots have separation
at least `4/9`, whereas their diameters are less than `1/50`.
Rouché gives exactly one root per disk; the root in the disk about `1`
is the marked root itself. This proves the anchored matching (3), even
with `delta_2` in place of its bound `77000tau`.

Finally `sqrt(77000)<278` and `tau^(3/2)<=10^-15` show that
`2500(77000tau)^(5/2)<5tau` on (1). Therefore
`rho<=2400tau+5tau<2500tau`, proving the root part of (2).
When all original roots are on the circle, `D=0` recovers the restricted
regular rate with no radial term.

At `tau=0` on this branch, (15) gives `delta_2=0`. The exact boundary
reciprocal identity forces all critical points to be zero, and integration
with `p(1)=0` gives `p=z^9-1`. The zero bounds therefore also hold.

## 4. Collapsed original roots through reciprocal energy

If `L<1`, (14) and `7-L>6` give

\[
 L\le50000\tau.                                      \tag{16}
\]

Write `u_k=1/2+alpha_k+i t_k` and `B=sum t_k`. From
`e_1(u)=e_1(q)/2` and `e_2(u)=e_2(q)/3`, a direct expansion gives

\[
 \sum_k t_k^2
    =-14-7A-A^2+\sum_k\alpha_k^2+B^2
                  +\frac23\operatorname{Re}e_2(q).    \tag{17}
\]

The shift of the second symmetric polynomial is
`e_2(r)=L+21+28tau`. Thus `Re e_2(q)<=e_2(r)` gives

\[
 \sum_k|u_k-\tfrac12|^2
       \le2\sum_k\alpha_k^2+B^2+\frac23L+\frac{56}{3}\tau.
\]

Since `alpha_k>=0`, `sum alpha_k^2<=A^2<=16tau^2`.
Moreover

\[
 B^2=\frac14\left(\sum_j\operatorname{Im}q_j\right)^2
       \le2\sum_j(\operatorname{Im}q_j)^2
       \le4R\sum_jd_j\le160\tau.                     \tag{18}
\]

The second inequality follows from
`(Im q)^2=(r-Re q)(r+Re q)<=2R d`. Equations (16)–(18) imply, on (1),

\[
 \sum_k|u_k-\tfrac12|^2\le34000\tau.                 \tag{19}
\]

For every other original root, `|u_k|>=1/2` because `|1-z_k|<=2`.
Inverting its reciprocal coordinate therefore gives

\[
 |z_k+1|=\frac{2|u_k-1/2|}{|u_k|}
       \le4|u_k-1/2|\le800\sqrt\tau.                 \tag{20}
\]

This controls the repeated-root branch without using a root-continuity
estimate with a poor exponent. At `tau=0`, (19) directly forces every
other root to equal `-1`, and `p=(z-1)(z+1)^8`.

## 5. Collapsed critical-point matching

Choose a largest `x_j`, relabeling it as `x_8`. Since `sum x=4+8tau`,
`x_8>=1/2`. Its pair products occur in `L`, so

\[
 s:=\sum_{j=1}^7x_j\le2L\le100000\tau,
 \qquad |x_8-4|=|8\tau-s|\le100008\tau.
\]

Let the target reciprocals be `q_j^0=1/2` for `j<=7` and `q_8^0=9/2`.
The squared scalar matching error is at most

\[
 \sum_j|r_j-q_j^0|^2
       \le\bigl(100008^2+100000^2\bigr)\tau^2
       \le3\tau,                                     \tag{21}
\]

using `tau<=10^-10`. Also

\[
 \sum_j|q_j-r_j|^2=2\sum_jr_jd_j\le80\tau.
\]

The squared triangle bound gives
`sum |q_j-q_j^0|^2<=2*80tau+2*3tau=166tau`.
Every actual and target reciprocal has modulus at least `1/2`, so

\[
 \sum_j\left|\left(1-\frac1{q_j}\right)
                    -\left(1-\frac1{q_j^0}\right)\right|^2
       \le16\cdot166\tau=2656\tau.
\]

The targets are `-1` seven times and `7/9` once. Since `2656<52^2`, this
proves the critical part of (4), including zero deficit. Undo the rotation
to recover every assertion for a general boundary root `a`.

## 6. Sharpness, including a unit-circle collapsed family

### Regular full-disk branch

Use the admissible small-parameter family already proved in
[boundary stability, section 5](../sendov_degree9_boundary_stability/proof.md):

\[
 P_u(z)=z^9-\frac{27}{4}u z^8+\frac97(u+9u^2)z^7
        -1+\frac{27}{4}u-\frac97(u+9u^2),\qquad u>0.
\]

Its roots lie in the disk for all sufficiently small positive `u`, with
the root `1` fixed. Exactly,
`P'_u=9z^6((z-3u)^2+u)`, hence

\[
 F_u(1)=6+\frac2{\sqrt{1-5u+9u^2}},\qquad
 \tau_u=\frac58u+O(u^2),\qquad Q_u=2u+18u^2.
\]

Each nontrivial ninth root has a nonzero first root velocity, proved in
the cited source, so its displacement is comparable to `u`, and therefore
to `tau_u`. The critical modulus is comparable to `sqrt(u)`. This prevents
any improvement of the full-disk root exponent `1` or critical exponent
`1/2`. Only an unspecified sufficiently small parameter interval is needed;
no numerical endpoint for disk containment of this family is asserted.

### Regular all-unit-circle branch

Use the independent refinement's rigorously admissible family

\[
 G_t(z)=z^9-1+t(z^5-z^4),\qquad 0<t\le1/1000.
\]

The cited source proves all roots lie on the unit circle and
`Q_t=5b^2 t^(2/5)(1+o(1))`, where `b=(4/9)^(1/5)`, while a nontrivial
original root moves by a nonzero constant times `t`. To transfer its
sharpness to the first-power deficit, the second-order expansion is

\[
 |1-\zeta|^{-1}
   =1+\operatorname{Re}\zeta+\tfrac14|\zeta|^2
          +\tfrac34\operatorname{Re}\zeta^2+O(|\zeta|^3).
\]

The error is uniform in a fixed sufficiently small disk. Vieta gives
`sum zeta=sum zeta^2=0` for `G'_t=z^3(9z^5+5tz-4t)`. If
`T=max |zeta|`, summing the error gives `O(TQ)=o(Q)`; hence

\[
 \tau_t=Q_t/32+o(Q_t)
       =\frac5{32}b^2t^{2/5}(1+o(1)).
\]

The original-root displacement is therefore comparable to `tau_t^(5/2)`.
This proves sharpness of (3) and also of the regular critical exponent.
The quartic root-containment certificate and derivative factorization
are independently checked again by the checker in this directory.

### Collapsed branch, even with all roots on the unit circle

For `0<v<=1/100` define

\[
 H_v(z)=(z-1)\bigl(z^2+2(1-v)z+1\bigr)^4.
\]

The two non-distinguished roots are
`-(1-v) +/- i sqrt(2v-v^2)`, each with multiplicity four. They lie on the
unit circle and their distances from `-1` equal `sqrt(2v)`. Exactly,

\[
 H'_v(z)=\bigl(z^2+2(1-v)z+1\bigr)^3 f_v(z),\qquad
 f_v(z)=9z^2+(2-10v)z-7+8v.                            \tag{22}
\]

The quadratic discriminant is `256-328v+100v^2>0`. More directly,
`f_v(-1)=18v>0`, `f_v(0)=-7+8v<0`, and `f_v(1)=4-2v>0` show that its
two real roots lie in `(-1,0)` and `(0,1)`. Their inverse distances from
`1` sum to `f'_v(1)/f_v(1)=5`. The other six critical points have
distance `sqrt(4-2v)` from `1`. Consequently

\[
 F_v(1)=5+\frac3{\sqrt{1-v/2}},\qquad
 \tau_v=\frac38\left((1-v/2)^{-1/2}-1\right)
       =\frac3{32}v+O(v^2).                            \tag{23}
\]

Here `L->0`, so for sufficiently small `v` this is the collapsed branch.
Every other original root, and six of the critical points, move away
from the collapsed targets by `sqrt(2v)`, which is comparable to
`sqrt(tau_v)`. The two real criticals converge to the distinct targets
`-1,7/9`, with displacement `O(v)`. No root or critical matching bound
with exponent greater than `1/2` can hold for this branch.

For both regular families, `L->7` and the original roots tend to the
distinct ninth roots of unity. A matching with error tending to zero
must use those local root branches. For the collapsed family, the original
roots tend to `1,-1,...,-1`. These two target multisets are distinct and
have positive distance under any bijective maximal-distance matching:
there are only finitely many permutations, and none equates the multisets.
Switching to the other family cannot evade any sharpness conclusion.

## Verification and dependency boundary

`verify.py` uses only standard-library exact rational and sparse polynomial
arithmetic. It checks the Newton sum of squares, shifted and vertical-line
identities, reciprocal energy algebra, derivative identities, root-location
sign certificates, scalar constants and equality controls. It also rejects
deliberate mutations of three certificate identities. It does not certify
the universal analytic argument by sampling.

The proof uses ordinary complex factorization, Gauss–Lucas, Maclaurin's
inequality, elementary phase estimates, Rouché, and the two explicitly cited
quadratic stability inputs (whose proofs also use, for sharpness,
the implicit-function theorem). No expensive computation, solver,
unpublished external data, or omitted large certificate is required.
The full interior first-power Tang–Zhang endpoint is not established here.
