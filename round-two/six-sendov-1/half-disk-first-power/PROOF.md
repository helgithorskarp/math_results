# Degree-nine complex first-power inequality on the marked half disk

Actual author **six-sendov-1**, role **researcher**, 2026-10-03.
Complete ordinary analytic author proof with compact exact algebra checks;
**unformalized and independently unreviewed**. No global first-power
resolution or optimal radius is claimed.

## 1. Statements and the classical communication reduction

For a finite nonzero complex eight-tuple $q=(q_1,\ldots,q_8)$, put

\[
r_j=|q_j|,\quad F=\sum r_j,\quad
O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt,\quad
J_a(q)=\int_0^1\prod_{j=1}^8[a+(1-a^2)tq_j]\,dt.
\]

**Standalone channel theorem.** For every $a\in[2/5,1/2]$, if

\[
r_j\ge2/3\ (j=1,\ldots,8),\qquad F\le8,\qquad |J_a(q)|\ge1,
\tag{1}
\]

then, with $\mu=\frac18\sum q_j$,

\[
F>39/5,\qquad E:=\sum|q_j-1|^2<3,\qquad
|\mu|\le1,\qquad \Re\mu>63/80,
\qquad |O_a(q)|>129/128.                         \tag{2}
\]

The individual critical-disk inequalities are not assumptions in this
standalone theorem. Their radius floor is sufficient. No balance,
conjugacy, separation, equal radius, support-count, or second-moment
bound is imposed. Collisions among tuple entries are allowed.

**Actual-polynomial corollary.** Every complex degree-nine polynomial whose
nine zeros, counted with multiplicity, lie in the closed unit disk satisfies

\[
\sum_{j=1}^8\frac1{|a-\zeta_j|}>8
\qquad\text{at every zero } |a|\le1/2,                 \tag{3}
\]

where all eight critical points are counted with multiplicity and a zero
denominator contributes $+\infty$. In particular, the first-power
Tang--Zhang inequality holds on this entire closed marked half disk.

Here is the reduction for simple marked zeros (0<a<1), after rotation
and monic normalization. Write

\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\qquad
p'(z)=9\prod_{j=1}^8(z-\zeta_j),\qquad q_j=(a-\zeta_j)^{-1}.
\]

The classical origin and polar identities give

\[
O_a(q)=\prod_{j=1}^8z_jq_j,
\qquad J_a(q)=\prod_{j=1}^8\frac{1-az_j}{a-z_j}.
\tag{4}
\]

For completeness, integrate (p') from (a) to (0) and compare
with (p(0)=-a\prod z_j) to obtain the first identity. Integrate from
(a) to (1/a) and divide by (p'(a)(1/a-a)) to obtain the second.
Thus all eight factors are retained in both identities. Since

\[
|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0,
\]

the original-disk hypotheses imply

\[
|O_a(q)|\le\prod r_j,\qquad |J_a(q)|\ge1.          \tag{5}
\]

Gauss--Lucas gives $|\zeta_j|\le1$, hence

\[
r_j\ge\frac1{1+a}\ge\frac23\quad\text{if }a\le1/2.
\tag{6}
\]

Equivalently, the exact critical-disk condition is

\[
(1-a^2)r_j^2+2a\Re q_j\ge1.
\]

We use only (6), not that stronger condition. These are necessary
conditions, not an equivalence to all-original feasibility. Abstract tuples
in the algebra controls are never asserted to have disk-rooted originals.

The identities and the first-power polar AM--GM mechanism below are
credited to Tao's communication identities and Tang--Zhang's conjecture;
see [LITERATURE.md](LITERATURE.md). The new contribution is the explicit
first-moment concentration and full centered origin bridge on the stated
interior interval, together with (3).
The earlier published central polar argument already covers the disk ending
at its scalar threshold0.4398<rho<0.4399. The new conclusion extends that
central region to1/2; see the complete prior-art comparison in LITERATURE.md.

## 2. Small marked moduli and a mass floor

For $0\le a\le1/2$, the triangle and arithmetic--geometric mean
inequalities imply, for every finite tuple with $F\le8$,

\[
|J_a(q)|\le\int_0^1\left[a+(1-a^2)tF/8\right]^8dt. \tag{7}
\]

For fixed $m\in[0,1]$ and $t\in[0,1]$, the function
(a+(1-a^2)tm) is nondecreasing on $[0,1/2]$, since its derivative is
$1-2atm\ge0$. Therefore, for $a\le2/5$, (7) is at most

\[
\int_0^1(2/5+21t/25)^8dt<1.                      \tag{8}
\]

This rules out $F\le8$ under the polar lower bound throughout
$0<a\le2/5$. The complete binomial integral is checked in the source;
no sampled modulus grid is used.

Likewise, for every $a\le1/2$, the conjunction $F\le39/5$ and
$|J_a(q)|\ge1$ would imply

\[
1\le\int_0^1(1/2+117t/160)^8dt
=\frac{424265002554558889}{429496729600000000}<1.   \tag{9}
\]

Consequently (1) forces $F>39/5$.

## 3. A polar deficit involving the first moment and phase loss

Assume $a\in[2/5,1/2]$, $r_j\ge2/3$, and $F\le8$. Write

\[
e_j=r_j-1,\quad T=\sum e_j^2,\quad
\Pi=\sum(r_j-\Re q_j),\quad E=T+2\Pi.            \tag{10}
\]

The last identity follows by expanding each $|q_j-1|^2$.
In particular $\Pi\ge0$, and $\sum e_j=F-8\le0$.

Two elementary bounds hold:

\[
0\le T\le56/9,\qquad
e_j>0\implies e_j\le\sqrt{7T/8}.                \tag{11}
\]

For the first, write $r_j=2/3+x_j$, $x_j\ge0$,
$X=\sum x_j\le8/3$. Then

\[
T=8/9-(2/3)X+\sum x_j^2
\le8/9-(2/3)X+X^2\le56/9.
\]

The final quadratic is convex, so its maximum on the stated closed
interval is at an endpoint. For the second, if $e_j>0$, the other seven
entries sum to at most $-e_j$. Cauchy--Schwarz gives
$\sum_{k\ne j}e_k^2\ge e_j^2/7$, proving (11).

Set $b=1-a^2$, $B(t)=a+bt$, and suppose $e_j\le d$ for every (j),
where $d\ge0$. Put $C(t)=B(t)+btd$. We claim

\[
\prod_j|a+btq_j|
\le B(t)^8\exp\left[-\frac{b^2t^2T}{2B(t)C(t)}
                    -\frac{abt\Pi}{C(t)^2}\right].          \tag{12}
\]

This holds at $t=0$. If a complex factor vanishes, its left side is zero.
Otherwise the following logarithms are all well defined.

For $u>-1$ and $u\le v$, $v\ge0$,

\[
\log(1+u)\le u-\frac{u^2}{2(1+v)}.               \tag{13}
\]

For $u\ge0$, integrate $s/(1+s)\ge s/(1+u)$ from (0) to (u).
For $-1<u\le0$, the same integral, with its reversed orientation,
gives $u-\log(1+u)\ge u^2/2$. This proves (13) in both cases.
Apply it to $u=bte_j/B(t)$, $v=btd/B(t)$. The linear terms sum to a
nonpositive number. Hence

\[
\prod_j(a+btr_j)
\le B(t)^8\exp[-b^2t^2T/(2B(t)C(t))].           \tag{14}
\]

For each (j), put $\pi_j=r_j-\Re q_j\ge0$. The exact phase identity is

\[
|a+btq_j|^2=(a+btr_j)^2-2abt\pi_j.
\]

Using $\frac12\log(1-u)\le-u/2$ and $a+btr_j\le C(t)$, the extra
logarithmic loss is at least $abt\pi_j/C(t)^2$. Summing gives (12).
No cancellation, reality, or pairing assumption was used.

## 4. Fourteen closed cells force E<3

Suppose $E\ge3$. Cover the entire (a)-interval by
$[2/5,9/20]$, $[9/20,1/2]$, and cover all possible (T) in (11) by
the following seven closed cells:

| L | U | d | P=max(0,(3-U)/2) |
|---:|---:|---:|---:|
| 0 | 1/2 | 2/3 | 5/4 |
| 1/2 | 1 | 1 | 1 |
| 1 | 3/2 | 7/6 | 3/4 |
| 3/2 | 2 | 4/3 | 1/2 |
| 2 | 5/2 | 3/2 | 1/4 |
| 5/2 | 3 | 5/3 | 0 |
| 3 | 56/9 | 7/3 | 0 |

Every row satisfies $d^2\ge7U/8$. Thus (11) gives $e_j\le d$.
Moreover $T\ge L$ and $E=T+2\Pi\ge3$ give $\Pi\ge P$.

For one (a)-cell $[\ell,h]$, set

\[
b_h=1-h^2,\quad M=h+b_h,\quad
N=h+(1-\ell^2)(1+d),\quad
k_1=\frac{\ell(1-\ell^2)P}{N^2},\quad
k_2=\frac{b_h^2L}{2MN},\quad K(t)=k_1t+k_2t^2.   \tag{15}
\]

On the entire cell, $B(t)\le h+b_ht\le M$, $C(t)\le N$,
$b\ge b_h$, and $ab\ge\ell(1-\ell^2)$. The latter uses monotonicity
of $a(1-a^2)$ on $[2/5,1/2]$. Therefore the exponent's loss in (12)
is at least $K(t)\ge0$.

The elementary inequality $e^{-u}\le1-u+u^2/2$, valid for $u\ge0$,
now proves

\[
|J_a(q)|\le\int_0^1(h+b_ht)^8
                       [1-K(t)+K(t)^2/2]dt=:\mathcal U.       \tag{16}
\]

The integrand is a complete polynomial of degree at most twelve. In
particular its fourth-degree kernel term is retained. A compact exact way
to evaluate every row is

\[
M_j=\sum_{i=0}^8 {8\choose i}
              \frac{h^{8-i}b_h^i}{i+j+1},\qquad
\mathcal U=M_0-k_1M_1+(-k_2+k_1^2/2)M_2
                    +k_1k_2M_3+(k_2^2/2)M_4.                \tag{17}
\]

For all fourteen pairs of rows,

\[
\mathcal U<199/200<1.                              \tag{18}
\]

`EXPECTED.json` contains every complete thirteen-entry polynomial vector
and its exact rational integral. `verify.py` derives these vectors once
by coefficient convolution and independently by thirteen-node exact
interpolation, and compares the full vectors. It separately verifies
(17) by the complete binomial sum and proves all fourteen strict signs
by exact integer/rational comparison. The table in the appendix gives
the entire finite input and integral for (18), so no external certificate,
floating sign, or unlisted rectangle is needed.

Equation (18) contradicts $|J_a(q)|\ge1$. Hence $E<3$. Together with
(9), this gives

\[
|\mu|\le F/8\le1,\qquad
\Re\mu=F/8-\Pi/8>39/40-3/16=63/80,\qquad
S:=\sum|q_j-\mu|^2=E-8|\mu-1|^2<3.             \tag{19}
\]

## 5. The complete centered origin expansion

Put $w_j=q_j-\mu$, so $\sum w_j=0$. Write $e_l(w)$ for the
elementary symmetric polynomial of degree (l). Newton's identities and

\[
\left|\sum w_j^k\right|\le\sum|w_j|^k\le S^{k/2}\qquad(k\ge2)
\]

give, by induction,

\[
|e_l(w)|\le c_lS^{l/2},\qquad
c_0=1,\ c_1=0,\quad
c_l=\frac1l\sum_{k=2}^l c_{l-k}.                 \tag{20}
\]

The complete list for $l=2,\ldots,8$ is

\[
(1/2,1/3,3/8,11/30,53/144,103/280,2119/5760).    \tag{21}
\]

If $S=0$, all $w_j=0$ and the remainder below is zero directly.
The source also checks all eight generic Newton identities as entire
polynomials in eight independent variables, before imposing balance.
Their classical algebra is not claimed new.

The exact eight-factor expansion is

\[
\prod_j(1-atq_j)=
\sum_{l=0}^8 e_l(w)(-at)^l(1-at\mu)^{8-l}.       \tag{22}
\]

Its $l=1$ term vanishes, but all orders $l=2,\ldots,8$ must be retained.
Let $\gamma=63/80$ and $\beta(x)=1-2\gamma x+x^2$. From (19),

\[
|1-x\mu|^2\le\beta(x),\qquad 0\le x\le1/2.
\]

For even (l), majorize the remaining modulus power by
$\beta(x)^{(8-l)/2}$. For odd (l), use

\[
\sqrt{\beta(x)}\le(1+\beta(x))/2
\]

and multiply it by $\beta(x)^{(7-l)/2}$. These bounds include every
power and phase direction.

The required averages are largest at $a=1/2$. Indeed $\beta>0$ and
$\beta'<0$ on $[0,1/2]$. Every relevant monomial has the form
$x^l\beta(x)^m$, with $l\ge2$, $0\le m\le3$. For $x>0$, the
sign of its derivative is the sign of $l\beta+mx\beta'$, which is
bounded below by

\[
2\beta+3x\beta'=2-10\gamma x+8x^2
=8(x-63/128)^2+127/2048>0.                       \tag{23}
\]

This also treats the two summands of each odd-order majorant. The
average of a nondecreasing continuous function on $[0,a]$ is
nondecreasing in (a), which justifies the entire interval reduction.

Define $v(t)=\beta(t/2)=1-63t/80+t^2/4$. Set

\[
D_l=\begin{cases}3^{l/2}&l\text{ even},\\
(7/4)3^{(l-1)/2}&l\text{ odd},\end{cases}\quad
H_l(t)=\begin{cases}v(t)^{(8-l)/2}&l\text{ even},\\
v(t)^{(7-l)/2}(1+v(t))/2&l\text{ odd}.\end{cases}
\]

Here $\sqrt3<7/4$. Equations (19)--(23) give the uniform bound

\[
|O_a(q)-O_a(\mu,\ldots,\mu)|
\le R:=9\sum_{l=2}^8 2^{-l}c_lD_l\int_0^1t^lH_l(t)dt.
\tag{24}
\]

The seven complete rational integrals are

\[
\begin{array}{c|c}
l&9\,2^{-l}c_lD_l\int t^lH_l\\\hline
2&2440167/11468800\\
3&7357539/65536000\\
4&150363/1433600\\
5&13795551/131072000\\
6&462849/4587520\\
7&75087/655360\\
8&19071/163840
\end{array}
\]

Their sum is

\[
R=795509283/917504000<111/128.                    \tag{25}
\]

The source checks every power coefficient under multiplication and
multinomial expansion; it does not discard the eighth-order term.

## 6. Uniform diagonal margin and conclusion

By (19), $\mu\ne0$. Direct integration gives

\[
O_a(\mu,\ldots,\mu)=\frac{1-(1-a\mu)^9}{a\mu}.    \tag{26}
\]

On the entire interval $2/5\le a\le1/2$,

\[
|1-a\mu|^2\le1-2a\gamma+a^2\le53/100.
\]

The final upper bound is at $a=2/5$, because the quadratic is decreasing
on this interval. Therefore

\[
|1-a\mu|^9<(3/4)(53/100)^4<1/16,
\quad |O_a(\mu,\ldots,\mu)|>15/8.               \tag{27}
\]

Combining (24)--(27) proves

\[
|O_a(q)|>15/8-111/128=129/128,
\]

completing the standalone theorem. For an actual polynomial with
$2/5\le a\le1/2$, assuming $F\le8$ would give (1), while (5) and
AM--GM give $|O_a(q)|\le\prod r_j\le(F/8)^8\le1$, a contradiction.
The range $0<a\le2/5$ was already excluded by (8).

At $a=0$, a simple marked zero gives

\[
|p'(0)|=\prod_{j=1}^8|z_j|=9\prod_{j=1}^8|\zeta_j|,
\quad\prod r_j=9/\prod|z_j|\ge9,
\]

so $F\ge8\,9^{1/8}>8$. None of these factors is zero because the marked
zero is simple. If the marked zero is multiple, it is a critical point and
the asserted sum is infinite. This covers every multiplicity and both
closed endpoints. Rotation restores complex (a), proving (3).

## 7. Scope and trust boundary

The new theorem is an interior first-power result, not an implication of
the already published quadratic inequality. The exact abstract controls
have first moment eight and second moment strictly greater than eight;
they confirm algebra and scope only. They are not universal samples,
original-root constructions, or counterexamples.

The fourteen closed cells cover all possible $a,T$ in the proof and
their inequalities hold pointwise for every $t\in[0,1]$. They are
finite analytic estimates, not a search or an incomplete enumeration.
All nine coefficients of the integrated products and all seven centered
remainder orders are retained. Nothing is imported from a peer or reviewer
executable, fixture, seal, numerical oracle, or private ledger.

The written logarithmic bounds, continuous norm estimates, averaging,
communication identities, AM--GM and Gauss--Lucas are ordinary mathematics
outside any formal kernel. The exact checker validates finite algebra and
constants, not independent review or the analytic bridges themselves.

### Appendix: complete polar-cell integrals

The following table is generated from (15)--(17). Together with the seven
T-cell rows above it lists all fourteen cases. No row is suppressed.

| a interval | T cell | k1 | k2 | Exact integral U |
|---|---|---:|---:|---:|
| [2/5,9/20] | [0,1/2] | 168/1369 | 0 | 50820827431871785194694295261/55271256883200000000000000000 |
| [2/5,9/20] | [1/2,1] | 1120/15123 | 101761/1700592 | 683454968787349554242215279121174299051/745231998475399247953920000000000000000 |
| [2/5,9/20] | [1,3/2] | 2520/51529 | 101761/906184 | 5851972067228716859406378304665876637289/6489037471507474557173760000000000000000 |
| [2/5,9/20] | [3/2,2] | 1680/58081 | 305283/1924144 | 29248995379190947641025550062891618187129/32976534586542568337571840000000000000000 |
| [2/5,9/20] | [2,5/2] | 56/4335 | 101761/508980 | 668024984978140228186790817486924583/765427050859305369600000000000000000 |
| [2/5,9/20] | [5/2,3] | 0 | 508805/2147696 | 607826997154366587106884299683798121/707361477341573283840000000000000000 |
| [2/5,9/20] | [3,56/9] | 0 | 305283/1297400 | 222061512019235716242743620290884681/258133027612262400000000000000000000 |
| [9/20,1/2] | [0,1/2] | 25839/192721 | 0 | 12015771859823009/12170488657018880 |
| [9/20,1/2] | [1/2,1] | 14355/175561 | 45/838 | 573295882620876595/577699585078460416 |
| [9/20,1/2] | [1,3/2] | 1550340/28590409 | 540/5347 | 7521223037599946009507/7660492725327048409088 |
| [9/20,1/2] | [3/2,2] | 258390/8025889 | 405/2833 | 292987978496248820143/301836857388757909504 |
| [9/20,1/2] | [2,5/2] | 1276/88445 | 24/133 | 1054997402626197353/1099648281059328000 |
| [9/20,1/2] | [5/2,3] | 0 | 675/3152 | 176575693496431/186216595062784 |
| [9/20,1/2] | [3,56/9] | 0 | 81/379 | 12768399272183/13461528903680 |
