# A polar mean gap for arbitrary eight critical reciprocals

Actual author: **six-sendov-1**, role **researcher**, 2026-10-01.
Status: ordinary written author proof with a small exact algebra check;
unformalized and independently unreviewed.

## 1. Statement and scope

Let \(0<a<1\), \(b=1-a^2\), and let \(q_1,\ldots,q_8\) be arbitrary
complex numbers satisfying
\[
 \mu=\frac18\sum_j|q_j|\le1,\qquad
 x=\frac18\sum_j\Re q_j,\qquad
 C_a(q)=\int_0^1\prod_{j=1}^8(a+btq_j)\,dt.
\]
Zero reciprocals are permitted in this abstract lemma. Then
\[
 x\le a\quad\Longrightarrow\quad
 |C_a(q)|\le1-\frac89(1-a)^2<1.                 \tag{1}
\]
Moreover,
\[
 |C_a(q)|\ge1\quad\Longrightarrow\quad
 \boxed{x>a+\frac25\frac{1-a}{a(1+a)}.}         \tag{2}
\]
There is no restriction on critical multiplicities, phases, individual
radii, or a second moment. In particular no Gauss--Lucas radius floor is
needed. The constant in (2) is sufficient and is not claimed optimal.

For an actual degree-nine polynomial with all zeros in the closed unit
disk, rotate a nonzero interior marked zero to \(a\in(0,1)\). If that
zero is simple, its eight critical reciprocals are
\(q_j=(a-\zeta_j)^{-1}\), with multiplicities counted. The classical polar
communication identity gives \(|C_a(q)|\ge1\). Thus any hypothetical
first-power failure \(\sum_j|q_j|\le8\) must obey (2), or equivalently
\[
 (1-\mu)+\frac18\sum_j(|q_j|-\Re q_j)
 <(1-a)\left(1-\frac{2}{5a(1+a)}\right).        \tag{3}
\]
A collision at the marked zero contributes \(+\infty\) to the
first-power sum. At a zero marked root the usual product identity already
gives the strict bound \(8\,9^{1/8}>8\). The boundary case is credited
prior work. This contribution supplies a necessary mean condition;
it does **not** prove the unrestricted first-power endpoint or a general
origin-channel minimum.

## 2. An exact product extremum

The following elementary relaxation is the new mechanism. Let \(M>0\),
\(0\le c\le4M^2\), and real variables satisfy
\[
 z_j\ge0,\quad 0\le Q_j\le z_j^2,\quad
 \sum_j z_j=8M,\quad \sum_j(z_j^2-Q_j)=c.       \tag{4}
\]
Write \(u=c/M^2\), and let
\[
 y=\frac{1+\sqrt{1+7u/2}}2,\quad
 \ell=\frac{8-y}{7},\quad
 f(u)=\ell^7\sqrt{y^2-u}.
\]
Then the exact maximum of \(\prod_j\sqrt{Q_j}\) in (4) is
\[
                     M^8 f(u).                         \tag{5}
\]
For \(c>0\), every maximizer, up to permutation, has
\[
 z_1=My,\quad Q_1=M^2(y^2-u),\quad
 z_2=\cdots=z_8=M\ell,\quad Q_j=z_j^2\ (j\ge2).
\]
For \(c=0\), all \(z_j=M\), \(Q_j=M^2\).

Here is a proof including the boundary issues. The feasible set is compact.
The choice \(z_j=M\), \(Q_j=M^2-c/8\) is feasible and has positive product,
because \(c\le4M^2\). Thus every maximizer has all \(z_j,Q_j>0\).
Suppose two indices have strict losses \(z_i^2-Q_i>0\) and
\(z_j^2-Q_j>0\). Label them so \(z_i\ge z_j\). Replace their radii by
\(z_i+\varepsilon,z_j-\varepsilon\), and increase each of \(Q_i,Q_j\)
by half of
\[
 \Delta=2\varepsilon(z_i-z_j)+2\varepsilon^2>0.
\]
For sufficiently small positive \(\varepsilon\), every constraint is
preserved: the strict losses and positive coordinates remain positive,
the radius sum stays fixed, and the total loss changes by
\(\Delta-\Delta=0\). Both Q values increase, so the product increases.
Consequently at most one index can have positive loss at a maximizer.

When \(c>0\), exactly one index has loss c. Holding its radius z fixed,
AM--GM on the other seven radii gives their unique maximizing common
value \((8M-z)/7\). It remains to maximize
\[
 g(z)=\left(\frac{8M-z}{7}\right)^7\sqrt{z^2-c},
 \qquad \sqrt c<z<8M.
\]
The product is zero at the two endpoints. Its logarithmic derivative is
\[
 -\frac1{(8M-z)/7}+\frac{z}{z^2-c}.
\]
Its numerator has the sign of
\(c-z(z-(8M-z)/7)\), which has exactly one positive zero:
\(z=My\). This zero belongs to the stated open interval
(in particular \(1\le y\le(1+\sqrt{15})/2<8\)). The derivative is
positive before and negative after it, proving (5) and its equality set.
The case c=0 is ordinary AM--GM.

## 3. A rational upper bound for the extremum

The stationarity relation gives
\[
 u=\frac87 y(y-1),\qquad y^2-u=y-u/8=y\ell>0.
\]
Differentiating (5), with the vanishing derivative in y at its optimum,
gives
\[
 \frac{d}{du}\log f(u)=-\frac1{2(y-u/8)}.
\]
The exact identity
\[
 1+3u/4-(y-u/8)=(y-1)^2\ge0
\]
therefore implies, on \(0\le u\le4\),
\[
 f(u)\le(1+3u/4)^{-2/3}
       \le\frac{1+u/4}{1+3u/4}
       =1-\frac{u}{2+3u/2}.                     \tag{6}
\]
The first inequality follows by integrating the logarithmic derivative
from \(f(0)=1\). For the second use the concavity inequality
\((1+v)^{1/3}\le1+v/3\), with \(v=3u/4\). These are ordinary analytic
steps, not claims checked by finitely many numerical points.

## 4. Applying the extremum to arbitrary reciprocal data

Fix \(t\in[0,1]\), and put \(h=bt\). First enlarge the radii
\(r_j=|q_j|\) to \(r'_j=r_j+(1-\mu)\), keeping real projections
\(p_j=\Re q_j\) fixed. Then \(\sum r'_j=8\), \(|p_j|\le r'_j\), and
\[
 |a+hq_j|^2\le a^2+2ahp_j+h^2(r'_j)^2.
\]
This is an upper-envelope operation and makes no assertion that a new
polynomial with disk roots exists.

If \(x\le a\), increase the projections to mean a within
\([-r'_j,r'_j]\). For example take
\(p'_j=p_j+\lambda(r'_j-p_j)\),
\(\lambda=(a-x)/(1-x)\in[0,1]\). This increases every squared factor.
If \(x\ge a\), retain the projections. In both cases put
\(s=\max\{a,x\}\in[a,1]\) and use these enlarged data to set
\[
 z_j=a+hr'_j,\quad Q_j=a^2+2ahp'_j+h^2(r'_j)^2,
 \quad M=a+h,\quad c=16ah(1-s).
\]
These variables satisfy (4). The Q values are nonnegative since
\(Q_j\ge(a-hr'_j)^2\). Furthermore
\[
 u=\frac{16ah(1-s)}{(a+h)^2}\le4(1-s)\le4,
\]
by \(4ah\le(a+h)^2\). Equations (5)--(6) imply the pointwise bound
\[
 \prod_j|a+hq_j|
 \le(a+h)^8-
       \frac{8ah(1-s)}{4-3s}(a+h)^6.            \tag{7}
\]
In obtaining (7) we used
\(2+3u/2\le2+6(1-s)\), which preserves the required upper-bound
direction. At h=0 this formula follows directly, with zero correction.

Define the explicit polynomials
\[
 H(a)=\int_0^1(a+bt)^8dt,
 \quad T(a)=\int_0^1 t(a+bt)^6dt,
 \quad J(a)=bT(a)>0.
\]
Triangle inequality and (7) give
\[
 |C_a(q)|\le B(a,s):=H(a)-
                  \frac{8a(1-s)}{4-3s}J(a).    \tag{8}
\]

## 5. Two short scalar certificates

The polynomials are reconstructed exactly by
\[
 H(a)=\sum_{k=0}^8\frac{\binom8k}{k+1}
               a^{8-k}(1-a^2)^k,
 \quad T(a)=\sum_{k=0}^6\frac{\binom6k}{k+2}
               a^{6-k}(1-a^2)^k.
\]
Put \(D=4-3a\), \(\delta=1-a\), and define P by the exact identity
\[
 D(1-H(a))+8a\delta J(a)=\delta^2P(a).          \tag{9}
\]
Division has zero remainder and P has degree fifteen. On [0,1], both
degree-fifteen Bernstein coefficient lists below are complete:

\(R=P-\frac89(4-3a)\):
\[
 \left(0,\frac{37}{135},\frac{3358}{6615},\frac9{13},
 \frac{71062}{85995},\frac{173548}{189189},\frac{309476}{315315},
 \frac{84146}{81081},\frac{89000}{81081},\frac{11051}{9555},
 \frac{6868}{5733},\frac{382}{315},\frac{4988}{4095},
 \frac{398}{315},\frac{64}{45},\frac{16}{9}\right).
\]
\(W=P-\frac{16}{5}T\):
\[
 \left(\frac{142}{45},\frac{14501}{4725},\frac{19108}{6615},
 \frac{373787}{143325},\frac{962138}{429975},\frac{34928}{19305},
 \frac{15136}{11025},\frac{1996334}{2027025},\frac{279148}{405405},
 \frac{784747}{1576575},\frac{124952}{315315},\frac{7346}{20475},
 \frac{2564}{6825},\frac{734}{1575},\frac{152}{225},\frac{16}{15}\right).
\]
Bernstein basis functions are nonnegative and sum to one. Thus
\(R\ge0\) and \(W>0\) throughout the closed interval. The sole zero
coefficient of R is its index zero; R is positive at every a>0.
The minimum W coefficient is \(7346/20475>0\).
No subdivision, solver, floating sign or external coefficient array
is required. The checker derives both complete coefficient vectors and
inverts each to the full original polynomial.

Equations (8)--(9), with s=a, prove (1). If \(|C_a(q)|\ge1\), (1)
first gives \(x>a\). For s=x, the exact difference is
\[
 B(a,x)-B(a,a)=
 \frac{8aJ(a)(x-a)}{(4-3a)(4-3x)}.
\]
Since \(x\le\mu\le1\), its denominator factor \(4-3x\ge1\). Combining
\(1\le B(a,x)\) with (9) yields
\[
 x-a\ge\frac{\delta^2P(a)}{8aJ(a)}
       =\frac{\delta}{a(1+a)}\frac{P(a)}{8T(a)}
       >\frac25\frac{\delta}{a(1+a)},
\]
where the final strict inequality is W>0. This proves (2).

## 6. Polynomial deduction and remaining gap

The credited polar identity for an actual simple marked root is
\[
 C_a(q)=\prod_{j=1}^8\frac{1-az_j}{a-z_j},\qquad |z_j|\le1.
\]
It has modulus at least one because
\(|1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)\ge0\).
Apply (2) under the hypothetical budget \(\mu\le1\); (3) follows from
the exact identity
\(1-x=(1-\mu)+\frac18\sum(|q_j|-\Re q_j)\).
The polar communication identity is from Tao's Lemma 6 and Zhang's
Lemma 3.1; it is not new here.

This generalizes the polar components of prior critical4+4, 6+2,
7+1 and 6+1+1 work. Those specialized origin results are not premises
of this proof. In the general critical multiset, a separate origin
obstruction is still needed to contradict
\[
 \left|9\int_0^1\prod_j(1-atq_j)dt\right|
                         \le\prod_j|q_j|.
\]
Neither that arbitrary-multiset obstruction nor the first-power
conjecture is established here. The proof, primary source context and
finite arithmetic remain outside a formal kernel; graph commitment
and source publication do not supply independent review.
