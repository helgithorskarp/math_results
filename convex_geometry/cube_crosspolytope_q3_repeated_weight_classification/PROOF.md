# Complete repeated-weight classification for three active weights

## 1. Setup and multiple-pole hinges

For

\[
A_v(b,R)=\int_{\mathbb R^N}\delta(v\cdot x-b)
\mathbf 1_{\{\sum_i(|x_i|-1)_+\le R\}}\,dx,
\]

put

\[
M=\|v\|_\infty,\qquad B=(|b|-\|v\|_1)/M>0,\qquad s=R-B.
\]

Assume there are exactly three active normalized magnitudes. The
pairwise-distinct case was classified in the source cited in SOURCES.md.
This note treats every repeated-weight stratum. Up to coordinate permutation
and common scaling, these are

\[
(1,1,a),\qquad (1,a,a)\quad(0<a<1),\qquad (1,1,1).       \tag{1}
\]

Write \(H_r(s;\omega)=(s-\omega)_+^r\). For a nonempty weight multiset
\(W\), the global chamber formula starts from

\[
\mathcal R_W(t)=
\frac1{(1-t)^{|W|}\prod_{w\in W}w
\prod_{w\in W}(1-w+wt)}.                                \tag{2}
\]

If a weight \(u\) has multiplicity \(m\), the pole of (2) at
\(-\lambda_u=-(1-u)/u\) has orders \(1,\ldots,m\). Its order-\(\ell\)
principal part contributes

\[
A_{u,\ell}\frac{B^{\ell-1}}{(\ell-1)!}
\frac{H_{|W|-\ell}(s;\lambda_uB)}{(|W|-\ell)!}.          \tag{3}
\]

Applying the exact tail-replacement operator to (3), then collecting equal
walls and equal hinge degrees, gives the tables below. They are identities
in the rational function field \(\mathbb Q(a,B)\), not limits of the
simple-pole formula.

Put

\[
\lambda=\frac{1-a}{a}>0.                                \tag{4}
\]

For weights \((1,1,a)\), the complete nonpolynomial local part is:

| Wall \(\omega\) | coefficient of \(H_1(s;\omega)\) | coefficient of \(H_2(s;\omega)\) |
|---|---:|---:|
| \(0\) | \(-B/[a(a-1)]\) | \(-(4a-3)/[2a(a-1)^2]\) |
| \(2a\) | \(-(B+2a)/[a(a+1)]\) | \(-(4a+3)/[2a(a+1)^2]\) |
| \(2\) | \(0\) | \(1/[2a(a-1)]\) |
| \(2(1+a)\) | \(0\) | \(1/[2a(a+1)]\) |
| \(\lambda B\) | \(0\) | \(a^3/[2(a-1)^2]\) |
| \(\lambda B+2/a\) | \(0\) | \(-a^3/[(a-1)(a+1)]\) |
| \(\lambda B+4/a\) | \(0\) | \(a^3/[2(a+1)^2]\) |

For weights \((1,a,a)\), the corresponding table is:

| Wall \(\omega\) | coefficient of \(H_1(s;\omega)\) | coefficient of \(H_2(s;\omega)\) |
|---|---:|---:|
| \(0\) | \(0\) | \(1/[2a^2(a-1)^2]\) |
| \(2a\) | \(0\) | \(1/[a^2(a-1)(a+1)]\) |
| \(4a\) | \(0\) | \(1/[2a^2(a+1)^2]\) |
| \(\lambda B\) | \(B/(a-1)\) | \(a(3a-4)/[2(a-1)^2]\) |
| \(\lambda B+2\) | \(0\) | \(-a/[2(a-1)]\) |
| \(\lambda B+2/a\) | \(-(B+2)/(a+1)\) | \(-a(3a+4)/[2(a+1)^2]\) |
| \(\lambda B+2+2/a\) | \(0\) | \(a/[2(a+1)]\) |

When rows collide numerically, their coefficients of each hinge degree are
added. A positive candidate wall disappears exactly when every resulting
coefficient is zero.

## 2. Repeated-weight theorem

Let \(a_*\) be the unique root in \((0,1)\) of

\[
P(a)=a^4+a-1.                                           \tag{5}
\]

It is isolated by

\[
\frac{724491959}{10^9}<a_*<\frac{18112299}{25000000},
\qquad a_*=0.7244919590005156\ldots.                    \tag{6}
\]

**Theorem.** Up to coordinate permutation, the only disappearing positive
candidate wall with a repeated active weight is

\[
\boxed{
(w_0,w_1,w_2)=(1,1,a_*),\qquad
B=\frac{2a_*}{1-a_*},\qquad s=2.}                       \tag{7}
\]

Numerically, \(B=5.259316253509069\ldots\). There are no disappearing
positive candidate walls for \((1,a,a)\), \(0<a<1\), or for \((1,1,1)\).

### Proof for \((1,1,a)\)

The constant positive wall functions are \(2a,2,2(1+a)\); the moving ones are
\(\lambda B,\lambda B+2/a,\lambda B+4/a\). Since \(B>0\), a constant row
can meet a moving row only in the following four ways:

\[
\begin{array}{ll}
\lambda B=2a,&\lambda B=2,\\
\lambda B=2(1+a),&
\lambda B+2/a=2(1+a).
\end{array}                                             \tag{8}
\]

The last possibility requires \(a^2+a-1>0\). The first collision retains
the nonzero linear coefficient from the \(2a\) row. In the third and fourth
collisions, the two quadratic coefficients are both positive. Only
\(\lambda B=2\) can cancel. It forces

\[
B=\frac{2a}{1-a},                                       \tag{9}
\]

and the aggregate quadratic coefficient at \(s=2\) is

\[
\frac{a^3}{2(a-1)^2}+\frac1{2a(a-1)}
=\frac{a^4+a-1}{2a(a-1)^2}.                             \tag{10}
\]

There is no linear hinge in either row. Thus (10) vanishes exactly at (5),
and then the whole local truncated-power term disappears. Since
\(P'(a)=4a^3+1>0\), while \(P(0)<0<P(1)\), the root is unique. None of the
other five wall functions equals \(2\) at this root, so no additional term
survives there.

### Proof for \((1,a,a)\)

Here the only possible positive cross-collisions are

\[
\lambda B=2a,\quad \lambda B=4a,\quad
\lambda B+2=4a,\quad \lambda B+2/a=4a.                 \tag{11}
\]

The last two require \(a>1/2\) and \(a>1/\sqrt2\), respectively. The first
two retain the nonzero linear coefficient \(B/(a-1)\). The fourth retains
the nonzero linear coefficient \(-(B+2)/(a+1)\). In the third, both
quadratic coefficients

\[
-\frac{a}{2(a-1)},\qquad \frac1{2a^2(a+1)^2}            \tag{12}
\]

are positive. Hence no collision in this stratum disappears.

In each stratum the four displayed resonance values of \(B\) are pairwise
distinct in \(0<a<1\). Clearing denominators in their six pairwise
differences reduces every possible equality to \(a=0\), \(a=1\), or a
nonzero constant. Thus no omitted simultaneous resonance can alter either
argument.

### Fully equal weights

For \((1,1,1)\), the collected table is

\[
\begin{array}{c|ccc}
\omega& H_0&H_1&H_2\\ \hline
0&B^2/2&3B&3\\
2&0&-3(B+2)/2&-21/8\\
4&0&0&3/8.
\end{array}                                             \tag{13}
\]

Both positive walls are therefore genuine. This completes the proof.

## 3. Complete \(q=3\) consequence

The earlier pairwise-distinct theorem gives four rational two-label curves,
with its stated exclusions, and two isolated algebraic three-label orbits.
The theorem above exhausts the complementary repeated-weight strata.
Consequently all positive missing candidate walls for three active weights
consist, up to permutation, of those four curves and three isolated algebraic
orbits, one of which is (7).

Adjoining zero-normal coordinates applies \(2^z(1+I)^z\). If a local hinge
vector is nonzero, its lowest nonzero degree remains nonzero after this lift;
if the complete vector vanishes, it stays zero. Thus the classification is
unchanged in higher ambient dimension with exactly three active coordinates.

The symbolic derivation checks the tables as identities in
\(\mathbb Q(a,B)\). The independent checker rebuilds the repeated principal
parts with Python exact fractions, proves the isolating root count with an
integer Sturm sequence, checks 189 rational table instances and 31 instances
of (10), and compares 116 section values with exact polygons reconstructed
directly from the original 27 halfspaces. The polygon cases include both
rational endpoints in (6), where the resonant coefficient has opposite signs.
