# Degree-nine critical7+1: a polar mean gap and the remaining origin constraint

Author: **six-sendov-1**, role **researcher**, 2026-09-30.
This proves an abstract polar lemma, an exact obstruction to a relaxed
origin inequality, and a sufficient conditional reduction for the complex
critical7+1 first-power problem. The conditional origin inequality is
**open here**. Neither the full7+1 case nor the unrestricted degree-nine
first-power endpoint is claimed.

The classical communication identities and conjecture retain their
primary-source attribution in [LITERATURE.md](LITERATURE.md).
The weighted-mean coordinates and exact sparse arithmetic extend the
author's [critical6+2 proof](../sendov_degree9_critical_six_two_first_power/PROOF.md);
its origin minimum does not transfer to the present multiplicities.

## 1. The polar lemma

Let \(0<a<1\), \(D_a=1-a^2\), \(U,V\in\mathbb C\), and
\[
 r=|U|,\quad s=|V|,\quad r,s\ge(1+a)^{-1},\quad
 7r+s\le8,\quad \xi=(7\Re U+\Re V)/8.
\]
Define
\[
 C=\int_0^1(a+D_a\tau U)^7(a+D_a\tau V)\,d\tau.
\]
If \(\xi\le a\), then
\[
 |C|\le1-\frac89(1-a)^2<1.                         \tag{1}
\]
If \(|C|\ge1\), then
\[
 \xi-a\ge \frac{2}{9L(a)}
                  \frac{1-a}{a(1+a)},              \tag{2}
\]
where
\[
 Q(a)=\left(1+\frac87a(1-a)\right)^2,\qquad
 P(a)=\left(1+8a(1-a)\right)^2,\qquad
 L(a)=\frac{Q(a)^2(4Q(a)+3P(a))}{7}.
\]
In particular,
\[
 \xi-a\ge\gamma\,\frac{1-a}{a(1+a)},\qquad
 \gamma=\frac{1647086}{97253703}.                   \tag{3}
\]
These are rigorous conservative bounds; no optimality is asserted.
Coinciding \(U,V\) are allowed.

Put \(p=\Re U,q_0=\Re V\) and
\[
 X=a^2+2aD_a\tau p+D_a^2\tau^2r^2,\qquad
 Y=a^2+2aD_a\tau q_0+D_a^2\tau^2s^2.
\]
For admissible real projections \(X,Y\ge0\). Pairing one heavy and one
light factor gives the new polynomial envelope
\[
 X^{7/2}Y^{1/2}=X^3\sqrt{XY}
 \le H_\tau(X,Y):=\frac{X^4+X^3Y}{2},\qquad
 |C|\le H:=\int_0^1H_\tau(X,Y)\,d\tau.              \tag{4}
\]
The identity
\[
 H_\tau(X,Y)^2-X^7Y=\frac{X^6(X-Y)^2}{4}
\]
also checks the AM-GM step without a numerical square root.
The upper polynomial increases in each nonnegative input.

To prove (1), first increase radii, keeping their real projections
fixed, until \(7r+s=8\). This preserves both lower bounds and increases
\(X,Y\). Now increase the real projections coordinatewise, within
their radius intervals, until \(7p+q_0=8a\). The maximum weighted
projection is \(8\), while its starting value is at most \(8a\), so
such an increase exists. Throughout these paths the quadratics are
nonnegative and (4)'s upper polynomial increases.

Every saturated radius pair and projection pair can be written
\[
 r=\frac{1+(8/7)av}{1+a},\qquad
 s=\frac{1+8a(1-v)}{1+a},\quad 0\le v\le1,
\]
\[
 p=r-\frac87(1-a)\theta,\qquad
 q_0=s-8(1-a)(1-\theta),\quad 0\le\theta\le1.
\]
The second parameter follows from the nonnegative projection deficits
and \(7(r-p)+(s-q_0)=8(1-a)\).
Write \(\epsilon=1-a,R=1+(8/7)av,S=1+8a(1-v)\). The quadratics become
\[
 X=a^2+2a\epsilon R\tau
   -\frac{16}{7}a\epsilon^2(1+a)\theta\tau
   +\epsilon^2R^2\tau^2,
\]
\[
 Y=a^2+2a\epsilon S\tau
   -16a\epsilon^2(1+a)(1-\theta)\tau
   +\epsilon^2S^2\tau^2.                            \tag{5}
\]

[polar.py](polar.py) constructs
\[
 W=\frac{1-\int_0^1(X^4+X^3Y)/2\,d\tau}{(1-a)^2}
\]
as an exact polynomial in \(\mathbb Q[a,v,\theta]\). Polynomial division
has zero remainder; \(W\) has237 nonzero monomials and degrees
\((14,8,4)\). The two integral expansions agree coefficient by
coefficient. Its full tensor Bernstein representation on \([0,1]^3\)
contains all **675** coefficients, each at least **\(8/9\)**.
The checker verifies the complete inverse basis identity.
The Bernstein basis is nonnegative and sums to one on the cube, hence
\(W\ge8/9\), proving (1). Some abstract cube points are not physical
projection pairs; positivity on this larger cube is harmless.

At the boundary the regenerated quotient satisfies
\[
 W(1,v,\theta)=\frac83-\frac{16}{3}
                     \left(-\frac12+\frac47v\right)^2
 \ge\frac43.                                      \tag{6}
\]
The polynomial is defined at \(a=1\); this identity does not divide
by zero or extend the polar identity for a disk-root polynomial there.
The negative variance term records the loss from the single AM-GM
pair, while the whole quotient remains positive.

## 2. Separate heavy/light derivative bounds

The unsaturated radius budget gives
\[
 r\le\frac{1+(8/7)a}{1+a},\qquad
 s\le\frac{1+8a}{1+a}.
\]
Therefore, on every path of admissible real projections with these
radii fixed,
\[
 0\le X\le Q(a),\qquad 0\le Y\le P(a).
\]
Here \(P(a)\ge Q(a)\). For the real projections the partial derivatives
of the envelope in (4) satisfy
\[
 \partial_p H_\tau=aD_a\tau(4X^3+3X^2Y)
                  \le7L(a)aD_a\tau,
\]
\[
 \partial_{q_0}H_\tau=aD_a\tau X^3
                  \le L(a)aD_a\tau.
\]
If \(|C|\ge1\), (1) first gives \(\xi>a\). Decrease the projections
coordinatewise to a pair of weighted real mean \(a\), keeping radii
fixed. This is possible because the least weighted projection is
\(-(7r+s)/8<a\). If the decreases are \(\Delta p,\Delta q_0\), then
\(7\Delta p+\Delta q_0=8(\xi-a)\). Integrating the derivative bound
along that segment and in \(\tau\) yields
\[
 H(p,q_0)-H(p-\Delta p,q_0-\Delta q_0)
 \le4L(a)aD_a(\xi-a).
\]
Using (1) at the lower projections gives
\[
 1\le|C|\le H(p,q_0)
 \le1-\frac89(1-a)^2+4L(a)aD_a(\xi-a).
\]
Rearrangement proves (2). Finally,
\[
 Q(a)\le81/49,\quad P(a)\le9,\quad
 L(a)\le\frac{10805967}{823543},
\]
and \(2/(9L_{\max})=1647086/97253703\), proving (3).

## 3. Application to a hypothetical disk-root failure

Let \(p_9\) be a complex degree-nine polynomial with every zero in the
closed unit disk and critical multiset
\(\{\zeta_U^7,\zeta_V\}\). Rotate a simple marked zero to \(a\in(0,1)\)
and put \(U=(a-\zeta_U)^{-1},V=(a-\zeta_V)^{-1}\).
Gauss--Lucas gives \(r,s\ge(1+a)^{-1}\).
Under the hypothetical first-power failure \(7r+s\le8\), the classical
polar communication identity reads
\[
 C=\prod_{j=1}^8\frac{1-az_j}{a-z_j},\qquad |C|\ge1, \tag{7}
\]
where \(z_j\) are the other zeros. The modulus inequality follows from
\[
 |1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0.
\]
The polar lemma therefore gives (2) and (3) for the actual reciprocals.
This is a necessary condition for a hypothetical failure, not yet its
exclusion.

Put
\[
 m=(7r+s)/8\le1,\quad b=am,\quad
 \eta=(r-s)/(7r+s),\quad
 A=r/m=1+\eta,\quad B=s/m=1-7\eta,
\]
and \(U_0=U/m,V_0=V/m\). With labels fixed,
\[
 -\frac{b}{1+b}\le\eta\le\frac{b}{7(1+b)},\qquad
 \eta\in[-1/2,1/14].                               \tag{8}
\]
For example \((m+b)(1+\eta)=(1+a)r\ge1\) and \(m+b\le1+b\)
give the lower bound; the light radius gives the upper bound.
The normalized weighted real mean obeys
\[
 \mu=(7\Re U_0+\Re V_0)/8
 \ge \frac a m+\frac{2}{9mL(a)}
                      \frac{1-a}{a(1+a)}
 >b.                                              \tag{9}
\]

The critical points of the normalized polynomial \(p_9(z/m)\) are
\[
 b-\frac1{U_0}=m\zeta_U,\qquad
 b-\frac1{V_0}=m\zeta_V.
\]
Consequently both necessary disk constraints hold:
\[
 |b-1/U_0|\le1,\qquad |b-1/V_0|\le1.                \tag{10}
\]
These constraints retain the real parts, whereas (8) retains only
radius lower bounds.

The origin communication identity gives
\[
 N(b,U_0,V_0):=
 \frac{\left|9\int_0^1(1-b\tau U_0)^7
                           (1-b\tau V_0)\,d\tau\right|^2}
      {A^{14}B^2}
 =m^{16}\prod_{j=1}^8|z_j|^2\le m^{16}\le1.        \tag{11}
\]
Thus a sufficient remaining lemma is the following precise statement:

> For \(0<b\le1\), \(A=1+\eta,B=1-7\eta\), unit phases
> \(u,v\), \(U_0=Au,V_0=Bv\), impose (8), \(\mu\ge b\), and both (10).
> Then \(N\ge1\), with equality only at
> \(b=1,\eta=0,u=v=1\) or \(b=1,\eta=-1/2,u=v=1\).

This proposed conditional inequality is **not proved here**. If proved,
its equality would exclude (11) when \(0<a<1\), since \(b=am<1\).
At \(a=0\) the classical derivative product already yields
\(S_1\ge8\,9^{1/8}>8\). At a simple boundary root the classical
logarithmic-derivative inequality yields \(S_1\ge8\).
The two boundary equality families are already established in the
author's [boundary classification](../sendov_degree9_first_power_polar/PROOF.md)
and [real-polynomial proof](../sendov_degree9_real_root_first_power/PROOF.md):
\(C_0(z^9-a^9)\) and \(C_0(z-a)(z+a)^8\), \(|a|=1,C_0\ne0\).
Their presence is essential to a correct7+1 equality target.

## 4. Exact origin coordinates retaining both disk constraints

For the remaining lemma write
\[
 K=(3+7\eta)/4\in[-1/8,7/8],\quad
 A=(4/7)(1+K),\quad B=4(1-K),
\]
\[
 (7U_0+V_0)/8
   =\{(1+K)u+(1-K)v\}/2=\rho w,\quad
 w=x+iy,\quad x^2+y^2=1.
\]
When \(\mu\ge b>0\), \(\rho,x>0\). Put
\[
 q=\rho^2=K^2+(1-K^2)c,\quad
 0\le c\le1,\quad\delta^2=c(1-c),\quad
 t=b/(\rho x)\in(0,1].
\]
The same two-focus triangle argument as in the previous complex
classes, with these new weights, gives
\[
 U_0=\frac{4w}{7\rho}\{q+K+i(1-K^2)\delta\},\qquad
 V_0=\frac{4w}{\rho}\{q-K-i(1-K^2)\delta\}.         \tag{12}
\]
For completeness, the two sides
\((1+K)\bar w u,(1-K)\bar w v\) sum to \(2\rho\);
the first real part is \((q+K)/\rho\) and the squared imaginary part
is \((1-q)(q-K^2)/q=(1-K^2)^2c(1-c)/q\).
This proves (12), retaining the sign of \(\delta\).

Define
\[
 \alpha=(4/7)\{q+K+i(1-K^2)\delta\},\qquad
 \beta=4\{q-K-i(1-K^2)\delta\}.
\]
Then
\[
 I=9\int_0^1(1-tx\tau w\alpha)^7
                         (1-tx\tau w\beta)\,d\tau,
\quad
 R_0=(4/7)^{14}4^2(1+K)^{14}(1-K)^2>0.
\]
The exact norm reduces to
\[
 |I|^2=E+\lambda J,\quad \lambda=-\delta y,\quad
 \lambda^2=c(1-c)(1-x^2),\quad N=(E+\lambda J)/R_0.
\]
[algebra.py](algebra.py) regenerates the7+1 integral by independent
binomial powers and by a paired quadratic followed by six heavy
linear factors. It regenerates the full norm both by coefficient
cross-products and by squaring real and imaginary parts.
The even, skew and defect polynomials have5115,3642 and5129 nonzero
monomials. Their degrees are respectively \((16,8,16,32)\),
\((15,7,15,30)\), and \((16,8,16,32)\).
These are exact identities; **no origin sign certificate** is asserted.

Crucially, (10) becomes two inequalities linear in the same \(\lambda\):
\[
 G_U=(1-t^2qx^2)A^2-1+\frac87tx^2(q+K)
                        +\frac87tx(1-K^2)\lambda\ge0,
\]
\[
 G_V=(1-t^2qx^2)B^2-1+8tx^2(q-K)
                        -8tx(1-K^2)\lambda\ge0.    \tag{13}
\]
Indeed \(|b-1/U_0|\le1\) is equivalent to
\((1-b^2)A^2+2b\Re U_0-1\ge0\), and (12) gives (13);
the light case is identical. The exact checker verifies both identities
under both signs of each phase. They supply a concrete polynomial
domain for closing \(E+\lambda J-R_0\ge0\), with (8) retained.
The two target corners are \(t=c=x=1,K=3/4\) and
\(t=c=x=1,K=-1/8\).

## 5. Why dropping (13) is invalid

The following exact point satisfies the reciprocal budget, both radius
lower bounds, the strict signed bounds in (8), and a strict real mean
that even exceeds the adaptive polar gap from (2), taking \(a=b,m=1\):
\[
 b=63/100,\quad A=5/8,\quad B=29/8,\quad\eta=-3/8,
\]
\[
 U_0=\frac58\left(\frac{28}{53}+i\frac{45}{53}\right)
     =\frac{35}{106}+i\frac{225}{424},
\]
\[
 V_0=\frac{29}{8}\left(\frac{231}{281}+i\frac{160}{281}\right)
     =\frac{6699}{2248}+i\frac{580}{281}.
\]
Both parenthesized phases are unit phases, \(7A+B=8\), and
\[
 \mu=\frac{630427}{953152},\quad
 \mu-b=\frac{748531}{23828800}
 >\frac{28228759765625000000000}
         {4020558922818557644002957}
 =\frac{2}{9L(b)}\,\frac{1-b}{b(1+b)}.
\]
Nonetheless exact Gaussian-rational integration gives
\[
 N=
 \frac{5219893776544959999488590149762052691109849915477}
      {27760891127741967700000000000000000000000000000000}
 <\frac15<1.                                      \tag{14}
\]
The checker independently uses convolution and the elementary primitive
\[
 I=\frac{9}{bU_0}
 \left[
 \frac{1-V_0/U_0}{8}\{1-(1-bU_0)^8\}
 +\frac{V_0/U_0}{9}\{1-(1-bU_0)^9\}
 \right]
\]
and compares the exact results.
The heavy disk gap is
\[
 (1-b^2)A^2+2b\Re U_0-1=-\frac{472677}{1356800}<0,
\quad
 |b-1/U_0|^2=\frac{1002677}{530000}>1.
\]
Thus Gauss--Lucas excludes the point. It is an exact counterexample
to the enlarged origin lemma with (10) deleted, even if (2)'s necessary
mean gain is imposed. It is **not** a counterexample to the disk-root
inequality, or evidence of a failure of the proposed conditional lemma.
The full polar condition (7) is also not asserted at this artificial point.

## 6. Evidence and trust boundary

[verify.py](verify.py) checks all675 polar coefficients and their full
inverse identity, both polar expansions,27 polar rational controls,
(6), the derivative constants, the exact obstruction, and the two
credited boundary equality controls. It checks the two complete origin
integral and norm constructions coefficient by coefficient,288 signed
Gaussian identity controls,8 reference evaluations by Fraction,
a nondegenerate original-coordinate bridge, and (13).
An actual nonreal polynomial with
\(p_9'=9(z-i/20)^7(z-(1+i)/40)\) and marked zero \(3/4\)
is checked by its derivative, exact Rouché coefficient bound below one,
and both communication identities. Four rational AM-GM controls check
the modulus identity. The compact manifest is required and eight
corruptions are rejected with explicit exceptions in normal and
optimized Python.

The finite sign evidence proves only the polar upper bound. The
geometry, monotonicity, derivative comparison, obstruction
interpretation and conditional reduction are ordinary written
mathematical arguments. Neither author cross-checks nor source
publication are independent review or formalization.
The source has no solver, floating-point sign, private input, or large
external certificate. Read [README.md](README.md) for commands,
hashes and measured costs. The useful next frontier is a proof of the
conditional origin minimum with (13), not more refinement of an
origin minimum already falsified by (14).
