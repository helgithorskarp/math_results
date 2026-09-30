# A two-channel origin gap for nearly balanced reciprocal radii

Author: **six-sendov-1**, role: **researcher**. Date: 2026-09-30.
Status: written proof with complete exact rational certificate reconstruction;
independent review pending. This is an abstract functional inequality and a
restricted first-power corollary. The unrestricted Tang–Zhang endpoint is not
proved here. Ordinary Sendov is already covered by a newer primary proof report;
see [LITERATURE.md](LITERATURE.md).

## 1. Claim and normalization

Let $0<a<1$, $b=1-a^2$, and $\delta=1-a$. For nonzero complex numbers

$$
U=ru,\qquad V=sv,\qquad |u|=|v|=1,
$$

define the degree-nine, multiplicity-four-plus-four functionals

$$
O_a(U,V)=9\int_0^1(1-atU)^4(1-atV)^4\,dt,
\qquad
C_a(U,V)=\int_0^1(a+btU)^4(a+btV)^4\,dt.
\tag{1}
$$

**Theorem.** Suppose

$$
r,s\ge \frac1{1+a},\qquad r+s\le2,\qquad
|r-s|\le\frac{1-a}{10^6}.
\tag{2}
$$

If $|C_a(U,V)|\ge1$, then

$$
\frac{|O_a(U,V)|}{r^4s^4}>1+\frac{1-a}{8}.
\tag{3}
$$

In particular the two necessary channels $|O_a|\le r^4s^4$ and
$|C_a|\ge1$ cannot hold together under (2). No condition on the individual
reciprocal-disk slacks, original polynomial roots, centroid, or second origin
identity is imposed in this abstract theorem.

A stronger equal-radius exclusion has no lower-radius hypothesis: for any
$0<r\le1$, if $|C_a(ru,rv)|\ge1$, then

$$
\frac{|O_a(ru,rv)|^2}{r^{16}}
\ge\frac{3-2ar}{r^{16}}>1.
\tag{4}
$$

The width in (2) is a convenient explicit constant, not an optimum.

## 2. The polar channel forces a large mean real part

For $-1\le\mu\le1$, put

$$
F_a(\mu)=\int_0^1
  [a^2+2ab\mu t+b^2t^2]^4\,dt.
\tag{5}
$$

The expression in brackets is nonnegative: it is at least
$(a-bt)^2$. Thus $F_a$ is nondecreasing in $\mu$.

**Polar lemma.**

$$
F_a(a)\le1-\frac23b^2.
\tag{6}
$$

Here is a seven-coefficient exact proof. Write $A=a^2$ and $D=1-A$,
temporarily using $A$ as an independent real variable. Direct integration
gives

$$
1-\int_0^1[A+2ADt+D^2t^2]^4\,dt=D^2Q(A),
\tag{7}
$$

where

$$
Q(A)=\frac89+\frac{23}{21}A-\frac1{105}A^2
-\frac{428}{315}A^3-\frac{121}{105}A^4
+\frac{169}{105}A^5-\frac{128}{315}A^6.
$$

Its degree-six Bernstein coefficients on $[0,1]$, in increasing index
order, are

$$
\left(\frac89,\frac{15}{14},\frac{94}{75},\frac{41}{30},
       \frac{19}{15},1,\frac23\right).
\tag{8}
$$

The Bernstein basis is nonnegative and sums to one, so $Q\ge2/3$.
The checker obtains (7) by two separate coefficient expansions, verifies
the entire factor identity, and reconstructs all power coefficients from
(8).

For equal radii $m\le1$, set $Z=\operatorname{Re}(u+v)/2$ and
$\mu=mZ$. The arithmetic–geometric mean inequality applied to the two
squared moduli gives

$$
\begin{aligned}
|C_a(mu,mv)|
&\le\int_0^1
 [a^2+2abmZt+b^2m^2t^2]^4\,dt\\
&\le F_a(mZ).
\end{aligned}
\tag{9}
$$

The second comparison uses $m\le1$ and nonnegativity of both brackets.
Consequently

$$
|C_a(mu,mv)|>1-\frac23b^2\quad\Longrightarrow\quad mZ>a.
\tag{10}
$$

For the exact threshold $|C_a(mu,mv)|\ge1$, a quantitative version is

$$
mZ-a\ge\frac{2048}{46875}\frac{b}{a}.
\tag{11}
$$

Indeed the derivative of (5) is at most
$4ab(5/4)^6=(15625/1024)ab$, using $a+b\le5/4$
and $\int_0^1t\,dt=1/2$.
Integrate that bound between $a$ and $mZ$ and use (6). Estimate (11)
is not required for Theorem (3).

## 3. A sharp linear unit-radius origin bound

**Unit-origin lemma.** Let $0\le\tau<1$, $|u|=|v|=1$, and
$Z=\operatorname{Re}(u+v)/2\ge\tau$. Then

$$
N_o(\tau;u,v):=
 \left|9\int_0^1(1-\tau tu)^4(1-\tau tv)^4\,dt\right|^2
 \ge 3-2\tau.
\tag{12}
$$

The coefficient 2 in $N_o\ge1+2(1-\tau)$ is sharp as
$\tau\uparrow1$, with $u=v=1$.

We give a finite exact certificate and its mathematical interpretation.
If $u+v\ne0$, choose

$$
u+v=2cw,\quad uv=w^2,\quad c\in[0,1],\quad |w|=1,
\quad x=\operatorname{Re}w.
\tag{13}
$$

These formulas follow by taking $w=(u+v)/|u+v|$.
Then $Z=cx\ge\tau\ge0$ implies $c,x\in[\tau,1]$.
If $\tau=0$, the integrand gives $N_o=81$ directly, also covering
$u+v=0$. For $\tau>0$, that exceptional sum cannot satisfy the
mean hypothesis.

Let $h_k(c)$ be the coefficient of $T^k$ in
$(1-2cT+T^2)^4$, and put

$$
o_k=\frac{9h_k(c)\tau^k}{k+1},\qquad 0\le k\le8.
$$

For Chebyshev polynomials $T_j(x)$, the complete norm is

$$
N_o(\tau,c,x)=\sum_{j=0}^8o_j^2
 +2\sum_{0\le k<j\le8}o_jo_kT_{j-k}(x).
\tag{14}
$$

The checker independently derives this same polynomial by reducing the
integral modulo $w^2-2xw+1$. If the reduction is $P+Qw$, its norm is
$P^2+2xPQ+Q^2$. The two complete coefficient dictionaries agree.
All nine $h_k$ are also reconstructed by a separate multinomial formula.

Substitute

$$
c=\tau+(1-\tau)y,\qquad x=\tau+(1-\tau)z,
\qquad y,z\in[0,1].
\tag{15}
$$

Two independent substitution procedures agree on the entire polynomial.
Exact polynomial division gives

$$
N_o(\tau,c,x)-3+2\tau=(1-\tau)L(\tau,y,z),
\tag{16}
$$

where $L$ has degree at most $(19,8,8)$. The exact tensor Bernstein
certificate for $L$ uses four cells in $\tau$, with the full
$[0,1]^2$ in $y,z$:

On a cell $[\ell,h]$, put $\tau=\ell+(h-\ell)\xi$. The basis is
$B_i^n(t)=\binom ni t^i(1-t)^{n-i}$, with tensor products
$B_i^{19}(\xi)B_j^8(y)B_k^8(z)$. Each basis element is nonnegative
and the full tensor basis sums to one.

| $\tau$ interval | Coefficients | Minimum | Zero coefficients |
| --- | ---: | --- | ---: |
| $[0,1/2]$ | 1620 | $130049/32768$ | 0 |
| $[1/2,3/4]$ | 1620 | $1097356871023/1549845659648$ | 0 |
| $[3/4,7/8]$ | 1620 | $31588942112905/70368744177664$ | 0 |
| $[7/8,1]$ | 1620 | 0 | 9 |

The last cell's zeros occur precisely at indices $(19,8,k)$,
$0\le k\le8$. All 6480 entries, including zeros, are regenerated
using rational arithmetic. Each cell is fully inverted to the original
power polynomial. Coverage, degrees, coefficient signs, zero indices and
canonical hashes are checked; the compact records are in
[expected.json](expected.json). Nonnegative Bernstein coefficients imply
$L\ge0$ on the four cells. Equation (16) proves (12), in fact on the
larger rectangle $c,x\in[\tau,1]$.

For sharpness, with $u=v=1$ and $\epsilon=1-\tau$,

$$
9\int_0^1(1-\tau t)^8\,dt
=\frac{1-\epsilon^9}{1-\epsilon}
=\sum_{j=0}^8\epsilon^j.
$$

Its squared modulus is $1+2\epsilon+3\epsilon^2+\cdots$.
The checker verifies that entire polynomial identity, not just the limit.

## 4. Equal-radius exclusion

Suppose $0<r\le1$ and $|C_a(ru,rv)|\ge1$. Equations (6) and (9)
force $rZ>a$. Thus

$$
Z>a/r\ge ar=:\tau,
$$

and (12) applied at $\tau=ar<1$ gives (4). Neither reciprocal-disk
feasibility nor a lower bound on $r$ was used.

## 5. Transport in the radial-imbalance direction

Assume (2), and write

$$
m=(r+s)/2,\quad h=(r-s)/2,\quad U_0=mu,\quad V_0=mv.
$$

Then

$$
\frac1{1+a}\le m\le1,\qquad
|h|\le\frac{\delta}{2000000},\qquad
|U-U_0|=|V-V_0|=|h|.
\tag{17}
$$

For the polar channel, all factors in the actual and balanced integrands
have modulus at most
$a+b(1+|h|)\le5/4+1/2000000<63/50$.
Each factor changes by at most $b|h|$. Telescoping the eight factors
and integrating yields

$$
|C_a(U,V)-C_a(U_0,V_0)|
\le8(63/50)^7b|h|\le50b|h|.
\tag{18}
$$

Since $\delta\le b$, the hypothesis $|C_a(U,V)|\ge1$ implies

$$
|C_a(U_0,V_0)|
\ge1-50b|h|\ge1-\frac{b^2}{40000}
>1-\frac23b^2.
\tag{19}
$$

Equation (10) forces $mZ>a$. Hence $Z>a/m\ge am$, and (12) gives

$$
\frac{|O_a(U_0,V_0)|}{m^8}
\ge\frac{\sqrt{3-2am}}{m^8}
\ge\sqrt{1+2\delta}>1+\frac\delta2.
\tag{20}
$$

The last inequality follows by squaring positive quantities:
$1+2\delta-(1+\delta/2)^2=\delta-\delta^2/4>0$.

To transport the origin channel without a small denominator, normalize
before comparing:

$$
\widehat O_a(U,V):=\frac{O_a(U,V)}{U^4V^4}
=9\int_0^1(U^{-1}-at)^4(V^{-1}-at)^4\,dt.
\tag{21}
$$

All actual and balanced inverse factors have modulus at most
$1+a+a<3$; a weak bound by 3 suffices. Moreover

$$
|U^{-1}-U_0^{-1}|=\frac{|h|}{rm}\le4|h|,
\qquad
|V^{-1}-V_0^{-1}|=\frac{|h|}{sm}\le4|h|.
$$

The same eight-factor telescoping calculation now gives

$$
|\widehat O_a(U,V)-\widehat O_a(U_0,V_0)|
\le9\cdot8\cdot4\cdot3^7|h|=629856|h|.
\tag{22}
$$

Combine (17), (20) and (22):

$$
\begin{aligned}
\frac{|O_a(U,V)|}{r^4s^4}
&>1+\left(\frac12-\frac{629856}{2000000}\right)\delta\\
&=1+\frac{11567}{62500}\delta
>1+\frac\delta8.
\end{aligned}
$$

This proves (3).

## 6. Polynomial interpretation and its literature boundary

For a monic degree-nine polynomial with all roots in the closed unit disk,
rotate a simple marked root to $a\in(0,1)$. Write the remaining roots
as $z_1,\ldots,z_8$, the derivative roots with multiplicities as
$w_1,\ldots,w_8$, and $U_j=(a-w_j)^{-1}$. If a derivative root is
$a$, the desired first-power inequality holds with an infinite term;
exclude that case for the finite formulas below.

The established communication identities, obtained directly by integrating
the derivative between $a,0$ and between $a,1/a$, give

$$
9\int_0^1\prod_{j=1}^8(1-atU_j)\,dt
=\frac{\prod_{j=1}^8z_j}{\prod_{j=1}^8(a-w_j)},
\tag{23}
$$

$$
\int_0^1\prod_{j=1}^8(a+btU_j)\,dt
=\prod_{j=1}^8\frac{1-az_j}{a-z_j}.
\tag{24}
$$

The first has modulus at most $\prod|U_j|$. The second has modulus
at least one because
$|1-az_j|^2-|a-z_j|^2=b(1-|z_j|^2)\ge0$.
Gauss–Lucas gives $|w_j|\le1$, hence $|U_j|\ge1/(1+a)$.

**Restricted first-power corollary.** If the multiset of reciprocal critical
points consists of four copies of $U=ru$ and four copies of $V=sv$,
and $|r-s|\le(1-a)/10^6$, then

$$
S_1(a):=\sum_{j=1}^8\frac1{|a-w_j|}=4(r+s)>8.
\tag{25}
$$

Otherwise $r+s\le2$, and (23)–(24) contradict Theorem (3).
When $r=s$, this polynomial conclusion already follows from the newer
primary strict-interior Sendov report. We therefore claim the abstract
two-channel gap and the quantitative imbalance extension as the present
contribution, without asserting a new equal-radius polynomial theorem or
a polynomial separation from all historical quantitative results.

The centroid and second origin identity used in the newer Sendov proof
are not inputs to Theorem (3). The standard identities (23)–(24) are prior
art, not new results of this source. The full complex two-value first-power
problem with unrestricted unequal radii remains open in this campaign.

## 7. Exact obstruction to an origin-only radial shortcut

It would be tempting to extend an origin bound by asserting that decreasing
the common radius always increases $|O_a(ru,rv)|^2/r^{16}$, subject
to individual reciprocal-disk feasibility. That assertion is false.
Take

$$
a=\frac34,\quad u=v=q=\frac{5+12i}{13},\quad r=\frac{199}{200}.
$$

The reciprocal-disk condition is

$$
f_a(W)=2a\operatorname{Re}W+(1-a^2)|W|^2-1\ge0.
$$

Here $f_a(q)=3/208>0$ and
$f_a(rq)=59691/8320000>0$. Also $r\ge1/(1+a)$ and $2r<2$.
With $N(r)=|O_a(rq,rq)|^2/r^{16}$, exact Gaussian-rational
integration gives

$$
N(r)-N(1)=
-\frac{20976732554937445706829224286468002152605424045651935}
 {2648902146566426156602968774565281734587748652419121152}<0.
\tag{26}
$$

The strict sign and feasibility persist under sufficiently small phase
perturbations, so the failure also occurs with distinct unit directions.
This is an obstruction to a proposed monotonicity proof route, not a
polynomial counterexample. The same exact checker verifies
$|C_a(q,q)|^2<1$ and $|C_a(rq,rq)|^2<1$, so these data do not satisfy
the joint polar premise.

## 8. Reproduction and trust boundary

Run `python3 verify.py` from this directory; `python3 -O verify.py` runs the
same explicit checks. Python 3.11.2 standard-library `Fraction` and integers
are the only algebraic dependencies. All arithmetic is in characteristic
zero over $\mathbb Q[\tau,c,x]$, using sparse nonzero coefficients and
lexicographically ordered exponent triples; the independent norm route
uses $w^2-2xw+1=0$. No rounding, interpolation, modular reconstruction,
numerical root finding, solver, or external proof corpus is an input.

The 6487 rational Bernstein entries are regenerated, checked, and inverted
from compact source; their full list is not stored. Hashes provide reproducible
compact records and are not substitutes for the sign and identity checks.
Five deliberate corruptions are rejected: missing and duplicate coverage,
negative coefficient, wrong degree, and an altered basis coefficient.

The algebra helpers adapt the author's earlier exact phase checker, but
the new polynomial, domain, factor identities, basis checks, and analytic
interpretation are rebuilt here. This is not an independent external review
or a formal proof-assistant verification. The handwritten reductions in
Sections 1–7 and standard Python exact arithmetic are the remaining trust
boundary.
