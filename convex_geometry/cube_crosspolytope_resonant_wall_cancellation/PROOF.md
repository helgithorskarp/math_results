# Infinite resonant wall cancellations in every dimension

## 1. Candidate walls

For the delta-normalized section

\[
A_v(b,R)=\int_{\mathbb R^N}\delta(v\cdot x-b)
\mathbf1_{\{\sum_i(|x_i|-1)_+\le R\}}\,dx,             \tag{1}
\]

put

\[
M=\|v\|_\infty,\qquad
B=\frac{|b|-\|v\|_1}{M}>0,\qquad s=R-B.                \tag{2}
\]

Let \(w_1,\ldots,w_q\in(0,1]\) be the normalized nonzero coordinate
magnitudes.  The global weighted formula places every possible wall among

\[
\omega_{i,J}=B(1/w_i-1)+\frac2{w_i}\sum_{j\in J}w_j,
\quad J\subseteq[q]\setminus\{i\}.                    \tag{3}
\]

The generic classification proves that all labeled values are genuine when
they are distinct.  We now show that its nonresonance hypothesis cannot be
removed.

## 2. Infinite cancellation families

Fix an integer \(m\ge1\) and a rational number \(0<t\le1/2\).  Define

\[
a=t^m,\qquad x=t^{2m+2},\qquad
c_+=\frac{a+x}{1-x}.                                   \tag{4}
\]

If \(m\) is even, also define

\[
c_- =\frac{a-x}{1+x}.                                  \tag{5}
\]

For either \(c=c_+\), or \(c=c_-\) when the latter is defined, take the
active weight multiset

\[
W=(1,a,\underbrace{c,\ldots,c}_{m\ \mathrm{copies}}),
\qquad q=m+2,                                          \tag{6}
\]

and set

\[
B=\frac{2mac}{1-a},\qquad s_*=2mc.                    \tag{7}
\]

**Theorem 1 (missing walls in every active dimension).**  The number \(s_*\)
is a candidate in (3), represented by exactly two labels:

1. supplier weight \(1\), with all \(m\) copies of \(c\) in the tail set;
2. supplier weight \(a\), with empty tail set.

Their truncated-power terms cancel identically.  Hence \(s=s_*\) is not a
chamber wall: the section is represented by one and the same polynomial on a
neighborhood of \(s_*\).

The result persists after arbitrary coordinate permutations and sign choices,
common scaling of the normal, and adjoining any number of zero-normal
coordinates.  Consequently every dimension with at least three active
coordinates contains infinitely many rational missing-wall examples.

## 3. Exact coefficient cancellation

The two labels in Theorem 1 both use simple baseline poles.  Their jumps in
derivative order \(q-1=m+1\), before the common factor from zero coordinates
and normal scaling, are

\[
D_1=\frac{(-1)^m}{a c^m(1-a)(1+c)^m},                 \tag{8}
\]

and

\[
D_a=\frac{a^{2m+1}}{c^m(a-1)(a-c)^m}.                 \tag{9}
\]

For the upper branch,

\[
\frac{a-c_+}{1+c_+}=-x,
\]

while for the lower branch,

\[
\frac{a-c_-}{1+c_-}=x.
\]

Since \(x^m=t^{2m^2+2m}=a^{2m+2}\), and the lower branch is used only for
even \(m\), both cases satisfy

\[
(a-c)^m=(-1)^m a^{2m+2}(1+c)^m.                       \tag{10}
\]

Substitution into (9) gives \(D_a=-D_1\).  Both hinge terms have exponent
\(q-1\), so cancellation of their derivative jumps is cancellation of the
complete truncated-power terms, not merely an increase in smoothness.

## 4. There are no additional labels at the wall

There are only three supplier-weight types.  A weight-one label has value

\[
2(ea+rc),\qquad e\in\{0,1\},\quad 0\le r\le m.
\]

It equals \(2mc\) for \(e=0,r=m\).  On the upper branch \(c>a\), so
\(a=(m-r)c\) is impossible.  On the lower branch

\[
\frac ac=\frac{1+x}{1-x/a},\qquad
1<a/c\le\frac{1+1/64}{1-1/16}=\frac{13}{12}<2,
\]

so it cannot equal the positive integer \(m-r\).  Thus there is no second
weight-one label type.

The empty-tail weight-\(a\) label equals \(s_*\) by (7), and every nonempty
tail strictly increases it.

For a weight-\(c\) supplier, its empty-tail value lies above \(s_*\) on the
lower branch.  On the upper branch the gap is

\[
s_*-B(1/c-1)=\frac{2m(c-a)}{1-a}.                     \tag{11}
\]

Any nonempty tail adds at least \(2a/c\).  It suffices to show the gap in
(11) is smaller.  With \(y=x/a=t^{m+2}\), this reduces to

\[
m c y\frac{1+a}{1-x}<1-a.                             \tag{12}
\]

For \(0<t\le1/2\), elementary monotonicity gives

\[
c\le\frac{t+t^4}{1-t^4}\le\frac35,\qquad
my\le\frac{m}{2^{m+2}}\le\frac18,
\qquad\frac{1+a}{1-x}\le\frac85,
\]

so the left side of (12) is at most \(3/25<1/2\le1-a\).  Thus a
weight-\(c\) label cannot reach \(s_*\).  The two labels in Theorem 1 are
therefore exhaustive.

## 5. Classification of this collision inside the three-level ansatz

Conversely, take weights \((1,a,c^m)\) with \(0<a,c<1\), \(a\ne c\), and
choose \(B=2mac/(1-a)\) so the two labels above collide at \(2mc\).  If no
third label has that value, then the candidate disappears if and only if

\[
\boxed{
\left(\frac{a-c}{1+c}\right)^m
=(-1)^m a^{2m+2}.}                                    \tag{13}
\]

Indeed, (13) is exactly \(D_1+D_a=0\).  For odd \(m\) its unique real
solution is the upper branch

\[
c=\frac{a+a^{2+2/m}}{1-a^{2+2/m}}.
\]

For even \(m\), the upper branch and the additional lower branch

\[
c=\frac{a-a^{2+2/m}}{1+a^{2+2/m}}
\]

are the two real solutions, subject to \(0<c<1\).  Equations (4)--(5) choose
\(a=t^m\), making both branches rational.

## 6. Smallest example and independent check

For \(m=1,t=1/2\),

\[
W=(1,1/2,3/5),\qquad B=6/5,qquad s_*=6/5.             \tag{14}
\]

The two apparent quadratic hinges are

\[
+\frac{25}{12}(s-6/5)_+^2,
\qquad
-\frac{25}{12}(s-6/5)_+^2.
\]

A direct rational polygon reconstruction from the original 27 halfspaces,
without using the spline formula, gives the same polynomial on both sides.
Writing \(u=s-6/5\), it is

\[
\frac{12403}{1125}+\frac{3278}{225}u+\frac7{45}u^2.
\]

The checker repeats this comparison for four rational parameters and two
normal scales.  It also perturbs (14) to \(c=2/3\) while retaining the
two-label resonance; the quadratic coefficients then differ and the wall is
genuine.  Thus resonance alone does not force disappearance.
