# First power for the full complex degree-nine critical 6+2 class

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.
Ordinary written author argument with exact finite evidence; unformalized.
Independent review is pending. Primary sources and preceding campaign
methods retain attribution in [LITERATURE.md](LITERATURE.md).

## 1. Statements

Let \(p\) be a complex polynomial of degree nine, all of whose zeros lie
in the closed unit disk, with critical multiset
\(\{\zeta_U^6,\zeta_V^2\}\), allowing coincidence. At every marked zero,

\[
 S_1(a)=6|a-\zeta_U|^{-1}+2|a-\zeta_V|^{-1}\ge8.       \tag{1}
\]

A collision contributes infinity. The inequality is strict for
\(|a|<1\). Equality in this class is precisely
\(p(z)=C(z^9-a^9)\), \(C\ne0,\ |a|=1\).
The unrestricted degree-nine first-power problem and other critical
multiplicity classes remain outside this result.

Two analytic lemmas give the proof. First, for
\[
 -\tfrac14\le\eta\le\tfrac1{12},\quad
 U=(1+2\eta)u,\quad V=(1-6\eta)v,\quad |u|=|v|=1,
\]
put \(\mu=(6\Re U+2\Re V)/8\). If \(0\le b\le\mu\), then
\[
 \frac{|9\int_0^1(1-b\tau U)^6(1-b\tau V)^2\,d\tau|^2}
 {(1+2\eta)^{12}(1-6\eta)^4}\ge1.                    \tag{2}
\]
Equality holds exactly at \(b=1,\eta=0,u=v=1\); in particular it is
strict for \(b<1\).

Second, take arbitrary nonzero complex \(U,V\), \(0<a<1\), and let
\[
 r=|U|,\ s=|V|,\quad r,s\ge(1+a)^{-1},\quad
 m=(3r+s)/4\le1,\quad \xi=(3\Re U+\Re V)/4.
\]
With \(D_a=1-a^2\) and
\[
 C=\int_0^1(a+D_a\tau U)^6(a+D_a\tau V)^2\,d\tau,
\]
the exact polar estimate is
\[
 \xi\le a\quad\Longrightarrow\quad
 |C|\le1-\tfrac89(1-a)^2<1.                         \tag{3}
\]
It retains the true even-multiplicity modulus, rather than replacing
the weighted squared radii by their maximum. Moreover,
\[
 |C|\ge1\quad\Longrightarrow\quad
 \boxed{\ \xi\ge a+\frac{1-a}{288a(1+a)}\ }.         \tag{4}
\]
This quantitative mean lemma concerns the stated polar-feasible
reciprocal budget; it is not a separate all-polynomial stability theorem.

## 2. Exact polar modulus and saturation

Write \(p_0=\Re U,q_0=\Re V\). The triangle inequality gives
\[
 |C|\le H=\int_0^1 X(\tau)^3Y(\tau)\,d\tau,\quad
 X=a^2+2aD_a\tau p_0+D_a^2\tau^2r^2,\quad
 Y=a^2+2aD_a\tau q_0+D_a^2\tau^2s^2.               \tag{5}
\]
Both quadratics are nonnegative because
\(|p_0|\le r,|q_0|\le s\). Thus the integrand is monotone in each
squared radius and each real part, while these inequalities hold.

For (3), first increase a radius while keeping both real parts fixed
until \(3r+s=4\). This preserves the lower-radius and projection bounds
and increases (5). Then increase the real parts within their respective
radius intervals until \(3p_0+q_0=4a\). This is possible: their weighted
maximum is now four, and the initial mean is at most \(a<1\).
Neither operation claims to preserve a polynomial's critical points;
these are monotone moves for a rigorous upper envelope.

Every saturated radius pair is parametrized by \(v\in[0,1]\):
\[
 r=\frac{1+\frac43av}{1+a},\qquad
 s=\frac{1+4a(1-v)}{1+a}.
\]
The losses satisfy \(3(r-p_0)+(s-q_0)=4(1-a)\). Hence for some
\(\theta\in[0,1]\),
\[
 p_0=r-\tfrac43(1-a)\theta,\qquad
 q_0=s-4(1-a)(1-\theta).
\]
Substitute \(\epsilon=1-a\),
\(R=1+\frac43av\), \(S=1+4a(1-v)\) into (5):
\[
 X=a^2+2a\epsilon R\tau
       -\tfrac83a\epsilon^2(1+a)\theta\tau
       +\epsilon^2R^2\tau^2,
\]
\[
 Y=a^2+2a\epsilon S\tau
       -8a\epsilon^2(1+a)(1-\theta)\tau
       +\epsilon^2S^2\tau^2.                       \tag{6}
\]
Some points of this larger cube need not correspond to admissible
projections. The next certificate covers the entire cube, so no
projection constraint or phase sign has been used to omit a point.

[polar.py](polar.py) reconstructs the polynomial
\[
 W(a,v,\theta)=\frac{1-\int_0^1X^3Y\,d\tau}{(1-a)^2}.
                                                               \tag{7}
\]
Exact polynomial division has zero remainder. The integral has 271
monomials and \(W\) has 225, of tensor degrees \((14,8,4)\).
Every one of its **675** Bernstein coefficients on the complete unit
cube is at least **\(8/9\)**. The full tensor is inverted to (7);
two independent expansion algorithms agree coefficient by coefficient.
Thus (7) proves (3). The quotient extends polynomially to \(a=1\),
where the separately checked identity is
\[
 W(1,v,\theta)=\tfrac83+
       \tfrac{16}3\,3\bigl(-\tfrac12+\tfrac23v\bigr)^2.            \tag{8}
\]
This shows explicitly the retained negative radial-variance contribution
to the polar envelope's near-boundary second-order term.

For comparison, the discarded-variance AM-GM envelope for ratio
\(6/2=3\) has near-boundary excess \(+\frac43(1-a)^2\).
It therefore cannot prove (3). This failure of an upper estimate is not
a counterexample to the polynomial inequality.

## 3. An explicit quantitative polar mean gap

For every pair in the radius budget,
\[
 r,s\le R_{\max}=\frac{1+4a}{1+a},\qquad
 a+D_a\tau R_{\max}\le1+4a-4a^2\le2.
\]
Consequently \(0\le X,Y\le4\) throughout every path of admissible real
projections with radii fixed. If \(\xi>a\), decrease those projections
coordinatewise to \(p_1,q_1\) with weighted mean \(a\). Such a point
exists because their weighted minimum is \(-m<a\).
The partial derivatives of the integrand in (5) obey
\[
 \partial_{p_0}(X^3Y)=6aD_a\tau X^2Y\le384aD_a\tau,\qquad
 \partial_{q_0}(X^3Y)=2aD_a\tau X^3\le128aD_a\tau.
\]
Integration along the segment yields
\[
 H(p_0,q_0)-H(p_1,q_1)
 \le256aD_a(\xi-a).
\]
Apply (3)'s envelope bound at the lower projections. If \(|C|\ge1\),
then (3) first forces \(\xi>a\), and
\[
 1\le |C|\le H(p_0,q_0)
 \le1-\tfrac89(1-a)^2+256aD_a(\xi-a).
\]
Rearrangement gives (4). The constant \(1/288\) is conservative and is
not asserted optimal.

## 4. The weighted complex mean and both signs of imbalance

For (2) set
\[
 K=\tfrac12+3\eta\in[-1/4,3/4],\quad
 A=1+2\eta=\tfrac23(1+K),\quad B=1-6\eta=2(1-K).
\]
Then \(6A+2B=8\). If \(b=0\), weighted AM-GM gives \(A^6B^2\le1\),
so the ratio in (2) is at least 81. Assume \(b>0\). Write
\[
 M=(6U+2V)/8=\{(1+K)u+(1-K)v\}/2=\rho w,
 \quad w=x+iy,\quad |w|=1.
\]
Now \(|K|\le\rho\le1\), and \(\rho x=\mu\ge b>0\), so \(\rho,x>0\).
Let \(q=\rho^2\) and
\[
 q=K^2+(1-K^2)c,\quad 0\le c\le1,\quad \delta^2=c(1-c).
\]
Keeping the sign of \(\delta\), two-focus triangle geometry gives
\[
 U=\frac{2w}{3\rho}\{q+K+i(1-K^2)\delta\},\qquad
 V=\frac{2w}{\rho}\{q-K-i(1-K^2)\delta\}.             \tag{9}
\]
Indeed, for \(S_0=(1+K)\bar w u,T_0=(1-K)\bar w v\) one has
\(S_0+T_0=2\rho\), \(|S_0|=1+K,|T_0|=1-K\), whence
\(\Re S_0=(q+K)/\rho\) and
\((\Im S_0)^2=(1-q)(q-K^2)/q\).
The latter numerator equals \((1-K^2)^2c(1-c)\), proving (9),
including parallel and opposite-direction limits.
This coordinate construction retains attribution to the preceding
5+3 proof; its new constants and domain are derived here.

Put \(t=b/(\rho x)\in(0,1]\) and
\[
 \alpha=\tfrac23\{q+K+i(1-K^2)\delta\},\qquad
 \beta=2\{q-K-i(1-K^2)\delta\}.
\]
The original integral becomes
\[
 I=9\int_0^1(1-tx\tau w\alpha)^6
                  (1-tx\tau w\beta)^2\,d\tau.       \tag{10}
\]
The divisor is
\[
 R_0=(2/3)^{12}\,2^4(1+K)^{12}(1-K)^4>0.
\]
The finite proof below covers every \(t,c,x\in[0,1]\) and
\(K\in[-1/4,3/4]\), including limiting zero-mean coordinates
where the inverse change of variables is undefined.

## 5. A third Newton bound and complete origin certificates

Reducing \(\delta^2=c(1-c)\), \(y^2=1-x^2\), the exact norm is
\[
 |I|^2=E+\lambda J,\quad \lambda=-\delta y,\quad
 \lambda^2=h=c(1-c)(1-x^2).
\]
[algebra.py](algebra.py) regenerates all 5,052 even and 3,577 skew
monomials by coefficient cross-products and, separately, by the full
real/imaginary squared norm. Put \(D=E-R_0\), with 5,068 monomials,
and \(s_0=1-cx^2\). The identity
\[
 s_0^2-4h=(1-2c+cx^2)^2\ge0
\]
gives \(\sqrt h\le f_0=s_0/2\).
For \(s_0>0\), all iterates
\(f_{j+1}=(f_j^2+h)/(2f_j)\) are positive upper bounds on \(\sqrt h\);
this follows from
\(f_{j+1}-\sqrt h=(f_j-\sqrt h)^2/(2f_j)\).
Use three iterations, with explicit positive denominators:
\[
 u=s_0^2+4h,\quad n_2=u^2+16s_0^2h,\quad d_2=8s_0u,
\]
\[
 n_3=n_2^2+d_2^2h,\quad d_3=2d_2n_2,\quad f_3=n_3/d_3.
\]
Both cleared polynomials
\[
 H_-=d_3D-n_3J,\qquad H_+=d_3D+n_3J                 \tag{11}
\]
are strictly positive wherever \(s_0>0\) on the stated complete cube.
Thus \(D>f_3|J|\ge|\lambda J|\), implying \(|I|^2>R_0\).
There is no fixed-sign assumption on \(J,\delta,y\).

The exact complete cell partition, sign counts, hashes and strictness
checks are recorded in [expected.json](expected.json) and reconstructed
by [verify.py](verify.py). Both polynomials have tensor degree
\((16,15,31,32)\) and 57,422 monomials each. Keep the full \(t\) interval.
For \(K\in[-1/4,1/2]\), the minus margin uses
\[
 (x,c)\in
 [0,1/2]\times[0,1],\
 [1/2,5/8]\times[0,1],\
 [5/8,3/4]\times[0,1],\
 [3/4,1]\times[0,1/2],\
 [3/4,1]\times[1/2,1].
\]
The plus margin replaces the middle two cells by
\([1/2,3/4]\times[0,1]\).
For \(K\in[1/2,3/4]\), each margin uses
\([0,1/2]\times[0,1]\) and \([1/2,1]\times[0,1]\).
These are **13** cells in total, seven minus and six plus.
Every origin cell contains
all 287,232 coefficients, and all are nonnegative. The cell interiors
are disjoint and their exact volumes cover the domain for each sign.
All coefficients in the zeroth \(c\) slice and the zeroth \(x\) slice
are positive. If \(c<1\), use the positive zeroth \(c\) Bernstein
function in a containing cell whose upper \(c\) endpoint exceeds \(c\).
If \(c=1,x<1\), use a containing cell with upper \(x\) endpoint exceeding
\(x\) and its positive zeroth \(x\) function. The other axes always have
at least one positive basis function. This proves strict positivity
off \(c=x=1\), including cell boundaries.

At \(s_0=0\) one has \(c=x=1,\delta=y=0\). Separate corner certificates,
of degrees \((16,0,0,16)\), split \(K\) at \(1/2\).
Each contains all 289 coefficients. The only zeros are
\((16,0,0,15),(16,0,0,16)\) on the left and
\((16,0,0,0),(16,0,0,1)\) on the right.
All other entries are positive. Hence
\[
 D(t,1,1,K)\ge0,\qquad D=0\ \Longleftrightarrow\
 t=1,\ K=1/2.
\]
This gives exactly \(b=1,\eta=0,u=v=1\), proving (2) and its equality.

Together with both corners and the polar tensor, **3,735,269** required
sign coefficients are regenerated.
The Bernstein transformation and its full inverse are verified on each
global margin, global corner and complete cell. Every cell coefficient
is compared between direct affine power substitution and de Casteljau
subdivision. The shared-integer affine substitution is additionally
compared with the retained Fraction implementation on a complete
nontrivial origin margin cell. No omitted coefficient, floating-point sign or solver
status enters the proof. Author algorithm cross-checks are not an
independent mathematical review.

## 6. Deduction for disk-root polynomials

Rotate the marked zero to real \(a=|a_{\rm old}|\).
At a simple marked zero put
\(U=(a-\zeta_U)^{-1},V=(a-\zeta_V)^{-1}\).
Gauss--Lucas gives \(r,s\ge(1+a)^{-1}\).
For \(0<a<1\), suppose \(S_1\le8\), and put
\[
 m=(6r+2s)/8\le1,\quad
 \eta=(r-s)/(6r+2s),\quad b=am<1.
\]
Then \(r=m(1+2\eta),s=m(1-6\eta)\).
The necessary signed bounds, with labels fixed, are
\[
 -\frac{b}{2(1+b)}\le\eta\le\frac{b}{6(1+b)}.        \tag{12}
\]
For \(\eta\ge0\), use \((m+b)(1-6\eta)=(1+a)s\ge1\)
and \(m\le1\); for \(\eta\le0\), use the analogous lower bound for \(r\).
Since \(b<1\), these imply the interval in (2).

With \(z_1,\ldots,z_8\) the other zeros, the classical communication
identities give
\[
 \frac{9\int_0^1(1-a\tau U)^6(1-a\tau V)^2\,d\tau}{U^6V^2}
       =\prod_{j=1}^8(-z_j),
\]
\[
 C=\int_0^1(a+D_a\tau U)^6(a+D_a\tau V)^2\,d\tau
       =\prod_{j=1}^8\frac{1-az_j}{a-z_j}.           \tag{13}
\]
They follow by integrating \(p'\) from \(a\) to zero and to \(1/a\).
The first identity gives actual squared origin ratio at most one.
The second gives \(|C|\ge1\), because
\(|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0\).
By (3), \(\xi>a\). The normalized reciprocals \(U/m,V/m\) have
weighted real mean \(\mu=\xi/m>a/m\ge am=b\).
Apply (2), strictly since \(b<1\): the actual origin ratio is
\[
 m^{-16}
 \frac{|9\int_0^1(1-b\tau U/m)^6(1-b\tau V/m)^2\,d\tau|^2}
 {(1+2\eta)^{12}(1-6\eta)^4}>m^{-16}\ge1,
\]
contradicting (13). This proves interior strictness.

At \(a=0\), the classical derivative product gives
\(\prod|q_j|=9/\prod|z_j|\ge9\), hence
\(S_1\ge8\,9^{1/8}>8\). At a simple boundary root \(a=1\),
\[
 6U+2V=2\sum_{j=1}^8(1-z_j)^{-1},\qquad
 \Re(1-z_j)^{-1}\ge1/2.
\]
Therefore \(S_1\ge\Re(6U+2V)\ge8\).
Equality forces \(U,V>0\) real and \(6r+2s=8\).
Now \(m=1,\mu=b=1\), and (12) lies within (2)'s range.
The origin identity and (2)'s equality force \(\eta=0,U=V=1\),
so all critical points are zero and \(p=C(z^9-1)\).
This polynomial attains equality; undoing the rotation gives (1)'s
stated classification. These classical endpoint identities retain
their primary-source and preceding-campaign attribution.

## 7. Evidence and proof boundary

The source uses CPython arbitrary-precision integers and Fraction only.
Two integral constructions and two origin norm constructions agree
coefficient by coefficient. The fresh polar kernel has two expansion
algorithms, a full inverse tensor identity, 27 rational controls and
the variance identity (8). Signed Gaussian controls include both phase
signs and degenerate faces, with direct Fraction evaluation controls.
An actual nonreal polynomial with the stated critical multiplicities
is checked by its derivative, marked root, exact Rouché coefficient
bound and both identities (13).

The checker requires its compact manifest and explicitly rejects altered
manifests under normal and optimized Python. Read [README.md](README.md)
for exact commands, measured resource use and output hashes.
The geometry, monotone polar saturation, rational bounds, Bernstein
interpretation and polynomial deductions remain ordinary written
mathematical obligations. This is not a proof-assistant formalization,
independent review or unrestricted first-power resolution.
