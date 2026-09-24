# Exact first chambers for arbitrary affine normals

## 1. Setup and normalization

Let

\[
g(x)=(|x|-1)_+,
\qquad
A_v(b,R)=\int_{\mathbb R^N}\delta(v\mathbin\cdot x-b)
 \mathbf1_{\{\sum_i g(x_i)\leq R\}}\,dx.                 \tag{1}
\]

Thus \(A_v\) is \(1/\|v\|_2\) times the Euclidean \((N-1)\)-volume of
the section of \([-1,1]^N+RB_1^N\) by \(v\cdot x=b\).

Put

\[
M=\|v\|_\infty,
\qquad h=\|v\|_1,
\qquad B=\frac{|b|-h}{M}.                                \tag{2}
\]

We consider the ray side \(|b|>h\), so \(B>0\).  The support function of
the body in direction \(v\) is \(h+MR\); hence the section is empty for
\(R<B\).  Reflection in coordinate hyperplanes and, if necessary, through
the origin reduces (1) to the positive normal \(|v|\) and positive offset.
Scaling the delta distribution contributes a factor \(M^{-1}\).

Let \(q\) be the number of nonzero coordinates of \(v\), put \(z=N-q\),
and normalize the active weights as

\[
w_i=\frac{|v_i|}{M}\in(0,1],\qquad 1\leq i\leq q.       \tag{3}
\]

Let \(k=|\{i:w_i=1\}|\).  If \(k<q\), define

\[
w_* = \max\{w_i:w_i<1\},
\qquad
\tau(B,w)=\min\left\{2\min_iw_i,
 B\left(\frac1{w_*}-1\right)\right\}.                   \tag{4}
\]

If \(k=q\geq2\), set \(\tau(B,w)=2\).  If \(q=k=1\), set
\(\tau(B,w)=+\infty\).  Write \(s=R-B\).

## 2. The weighted boundary polynomial

Define the rational generating function

\[
\boxed{
C_w(t)=\frac{1}{(1-t)^q\prod_{i=1}^q w_i
 \prod_{i:w_i<1}(1-w_i+w_it)}}                           \tag{5}
\]

and let

\[
c_j(w)=[t^j]C_w(t),\qquad 0\leq j\leq k-1.              \tag{6}
\]

These are explicit rational functions of rational weights.  In particular,

\[
c_0(w)=\frac{1}{\prod_iw_i\prod_{w_i<1}(1-w_i)}.         \tag{7}
\]

Set

\[
L_w(B,s)=\sum_{j=0}^{k-1}c_j(w)
 \frac{B^{k-1-j}s^{q-k+j}}
 {(k-1-j)!(q-k+j)!}.                                     \tag{8}
\]

For a function of \(s\), let

\[
(If)(s)=\int_0^s f(u)\,du,
\qquad I^0f=f.                                            \tag{9}
\]

**Theorem 1 (all weighted first chambers).**  For every nonzero
\(v\in\mathbb R^N\), \(|b|>\|v\|_1\), and
\(0\leq s\leq\tau(B,w)\),

\[
\boxed{
A_v(b,B+s)=\frac{2^z}{M}(1+I)^zL_w(B,s).}                \tag{10}
\]

Equivalently, the completely explicit formula is

\[
\boxed{
A_v(b,B+s)=\frac{2^z}{M}
\sum_{j=0}^{k-1}\sum_{r=0}^{z}{z\choose r}c_j(w)
\frac{B^{k-1-j}s^{q-k+j+r}}
{(k-1-j)!(q-k+j+r)!}.}                                   \tag{11}
\]

The endpoint is included.  Formula (11) is exact, finite-dimensional, and
contains no limiting or genericity assumption on the positive weights.

## 3. Vanishing-order and normal classification

Extend the section by zero for \(R<B\).  The first nonzero term in (11) is

\[
\frac{2^z}{M}\,c_0(w)
\frac{B^{k-1}s^{q-k}}{(k-1)!(q-k)!}.                     \tag{12}
\]

All its factors are positive.  Therefore:

**Theorem 2 (sharp onset regularity).**  The section vanishes to exactly
order \(q-k\) at \(R=B\).  If \(q>k\), it is \(C^{q-k-1}\) but not
\(C^{q-k}\) there, and its right-minus-left derivative jump is

\[
\boxed{
\partial_R^{q-k}A_v(b,B+)-\partial_R^{q-k}A_v(b,B-)
=\frac{2^z}{M}\frac{c_0(w)B^{k-1}}{(k-1)!}.}             \tag{13}
\]

If \(q=k\), the same expression is the nonzero jump in the section value.
Consequently the support-plane section has positive \((N-1)\)-volume if and
only if every nonzero coordinate of \(v\) has magnitude \(M\).

For a full-support normal, \(q=N\).  Hence a nonzero boundary section occurs
if and only if

\[
|v_1|=\cdots=|v_N|,                                      \tag{14}
\]

which classifies the signed diagonals as the unique full-support normals
retaining the nonvanishing boundary law.

## 4. Legendre law and its sparse lift

When all active weights equal one, \(k=q\) and
\(C_w(t)=(1-t)^{-q}\), so

\[
c_j(w)={q+j-1\choose j}.                                 \tag{15}
\]

Substitution in (8) gives

\[
L_w(B,s)=H_q(B,s)
=\frac{B^{q-1}}{(q-1)!}P_{q-1}\left(1+\frac{2s}{B}\right). \tag{16}
\]

Thus signed diagonal full-support normals recover exactly the previously
proved Legendre law.  More generally, if all nonzero coordinates of \(v\)
have equal magnitude but \(z>0\), then

\[
A_v(b,B+s)=\frac{2^z}{M}(1+I)^zH_q(B,s),                 \tag{17}
\]

an explicit sparse-normal lift of the Legendre polynomial.

## 5. Coordinate-state proof

It remains to prove (10).  First suppose that there are no zero weights and
that \(M=1\).  Relative to the support vertex \((1,\ldots,1)\), each
coordinate is in one of two states before an opposite tail appears:

\[
x_i=1+p_i\quad(p_i\geq0),
\qquad
x_i=1-y_i\quad(0\leq y_i\leq2).                          \tag{18}
\]

Call these states plus and inactive.  The affine and radial constraints are

\[
\sum_{i\in P}w_ip_i=B+\sum_{i\notin P}w_iy_i,
\qquad
\sum_{i\in P}p_i\leq B+s.                               \tag{19}
\]

For a submaximal plus coordinate introduce
\(u_i=(1-w_i)p_i\); for an inactive coordinate introduce
\(u_i=w_iy_i\).  Then the radial slack is simply

\[
\sum u_i\leq s.                                          \tag{20}
\]

Suppose a state pattern contains \(a\geq1\) maximal plus coordinates.
After the other variables are fixed, delta integration over those coordinates
gives

\[
\frac{1}{(a-1)!}
\left(B+\sum_{\rm inactive}u_i
-\sum_{\substack{\rm submaximal\\plus}}
 \frac{w_i}{1-w_i}u_i\right)^{a-1}.                     \tag{21}
\]

For a submaximal coordinate the inactive state has Jacobian \(1/w_i\)
and sign parameter \(+1\) in (21); the plus state has Jacobian
\(1/(1-w_i)\) and sign parameter \(-w_i/(1-w_i)\).  A maximal inactive
coordinate has unit Jacobian and parameter \(+1\).

The simplex moment identity

\[
\int_{\substack{u_i\geq0\\\sum u_i\leq s}}
 \prod_i u_i^{\alpha_i}\,du
=\frac{\prod_i\alpha_i!}{(d+|\alpha|)!}s^{d+|\alpha|}   \tag{22}
\]

turns (21) into a finite polynomial.  We now sum the state patterns by a
generating function.  For a variable with sign parameter \(\lambda\), its
complete homogeneous moments contribute \((1-\lambda t)^{-1}\).  A
submaximal coordinate contributes, after summing its two states,

\[
\frac{1}{w_i(1-t)}+
\frac{1}{(1-w_i)\left(1+\frac{w_i}{1-w_i}t\right)}
=\frac{1}{w_i(1-t)(1-w_i+w_it)}.                         \tag{23}
\]

For the \(k\) maximal coordinates, summing patterns with at least one plus
state gives

\[
\sum_{a=1}^k{k\choose a}
 \left(\frac{t}{1-t}\right)^{k-a}
=\frac{1-t^k}{(1-t)^k}.                                  \tag{24}
\]

Only coefficients through degree \(k-1\) enter the section polynomial, so
the numerator \(1-t^k\) in (24) may be replaced by one.  Multiplying (23)
and (24) gives exactly \(C_w(t)\).  If the selected Taylor degree is \(j\),
the powers forced by (21)--(22) are

\[
B^{k-1-j}s^{q-k+j},                                      \tag{25}
\]

with the factorials in (8).  This proves the active-coordinate formula.

The chamber bound has two independent parts.  When at least two active
coordinates are present, an inactive coordinate reaches the opposite tail
first at slack \(2w_i\).  A pattern with no maximal plus coordinate cannot
supply excess \(B\) before the most efficient submaximal
weight uses slack \(B(1/w_*-1)\).  Thus (18), (21), and the omission in
(24) are exact for \(0\leq s\leq\tau(B,w)\); newly entering strata have zero
section measure at the endpoint.

When \(q=1\), the single active coordinate is fixed on its plus ray for every
\(R\geq B\), so no opposite active tail can enter and the formula is global.

Finally, for a zero-normal coordinate, pushforward of Lebesgue measure by
\(g\) is

\[
2\delta_0+2\mathbf1_{(0,\infty)}(u)\,du.                 \tag{26}
\]

Convolving (26) for all \(z\) zero coordinates applies
\(2^z(1+I)^z\) to the active formula.  Restoring the delta-scaling factor
\(M^{-1}\) proves (10)--(11).  Equations (12)--(17) follow directly.

## 6. Verification boundary

The checker constructs (5)--(11) by truncated rational series.  A separate
engine enumerates every plus/inactive coordinate-state pattern and evaluates
its simplex moments via (22).  In dimension three, a third engine starts from
the original definition: it writes the body using all 27 halfspaces,
eliminates the affine equation, reconstructs the rational section polygon,
and computes its area exactly.  These computations corroborate the theorem;
the coordinate-state argument proves all dimensions and real weights in the
stated chamber.
