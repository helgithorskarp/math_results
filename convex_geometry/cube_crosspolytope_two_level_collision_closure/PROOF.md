# Collision closure for all two-level candidate walls

## 1. Structural rows

Fix normalized active weights

\[
1^p a^r,\qquad p,r\geq1,\qquad q=p+r,\qquad0<a<1.
\]

The global weighted chamber formula cited in SOURCES.md organizes every
candidate wall into unit-supplier rows \(U_{k,\ell}\) and
\(a\)-supplier rows \(V_{i,j}\):

\[
\begin{array}{c|c|c}
 &\text{wall}&\text{lowest hinge degree}\\ \hline
U_{k,\ell}&2(k+a\ell)&r+k,\\
V_{i,j}&\lambda B+2i/a+2j&p+j,
\end{array}                                               \tag{1}
\]

where \(\lambda=(1-a)/a\), \(B>0\),
\(0\leq k<p\), \(0\leq\ell\leq r\),
\(0\leq i\leq p\), and \(0\leq j<r\).  The lowest coefficient of every
individual row is nonzero.

The preceding arbitrary-\(q\) theorem classified a cross-family wall under
the hypothesis that exactly one row from each family occurs there.  This
proof removes that hypothesis.

## 2. The collision lattice

An internal same-family collision forces \(a\) to be rational.  Write

\[
a=\frac{s}{t},\qquad 1\leq s<t,\qquad\gcd(s,t)=1.         \tag{2}
\]

Two unit rows have the same wall exactly when

\[
tk+s\ell=tk'+s\ell'.                                    \tag{3}
\]

All integer solutions in one group are therefore

\[
(k',\ell')=(k+hs,\ell-ht).                              \tag{4}
\]

Their lowest degrees \(r+k'\) form an arithmetic progression with step
\(s\).  Similarly, two moving rows have the same wall exactly when

\[
ti+sj=ti'+sj',                                          \tag{5}
\]

and their indices differ by \((hs,-ht)\).  When ordered by increasing
lowest degree \(p+j\), their degrees form an arithmetic progression with
step \(t\).

Thus each family has a unique lowest-degree row in any collision group.
If a wall contains rows from only one family, its unique lowest coefficient
cannot cancel.  If it contains both families but their two minimum degrees
differ, the smaller one likewise survives.

It remains to consider a cross-family wall whose minimum degrees agree.
Write

\[
d=r+k=p+j=q-m,\qquad m=p-k=r-j.                          \tag{6}
\]

If the wall is multirow, then \(m\geq2\): an additional unit row of larger
degree requires \(k<p-1\), while an additional moving row of larger degree
requires \(j<r-1\).

The common-wall equation gives

\[
B=\frac{2(ak+a^2\ell-i-aj)}{1-a},\qquad
X=k-i+a(\ell-j)>0.                                      \tag{7}
\]

Let \(c^U_d,c^V_d\) be the two lowest coefficients and put

\[
R_U=\frac{c^U_{d+1}}{c^U_d},\qquad
R_V=\frac{c^V_{d+1}}{c^V_d}.
\]

The two-jet theorem proved in the source contribution gives

\[
R_U-R_V=
-\frac{(m-1)\{q(1+a)^2-4a(i+\ell)\}}
{4X(q-m+1)(1+a)}<0.                                    \tag{8}
\]

Indeed, its positive factor is

\[
q(1+a)^2-4a(i+\ell)
=q(1-a)^2+4a(q-i-\ell)>0.                               \tag{9}
\]

## 3. All cases except reciprocal collisions

Suppose first that \(s\geq2\).  By (4), no later unit row begins before
degree \(d+2\); by (5), no later moving row begins before degree
\(d+t\geq d+2\).  If \(c^U_d+c^V_d\neq0\), the wall remains.  If these
coefficients cancel, the aggregate coefficient in degree \(d+1\) is

\[
c^U_d(R_U-R_V)\neq0                                     \tag{10}
\]

by (8).

The same proof applies when \(s=1\) but the minimum unit row has no second
row in its group.  Extra moving rows still begin only in degree at least
\(d+t\), where \(t\geq2\).

The only case not yet covered is therefore

\[
a=1/t
\]

and a unit group containing at least two rows.  If its minimum row is
\(U_{k,\ell}\), the next row is

\[
U' = U_{k+1,\ell-t};                                    \tag{11}
\]

in particular \(m\geq2\), \(\ell\geq t\), and \(r\geq t\).

## 4. Even denominators: reinforcement

Put

\[
Y=B+2k+2a\ell>0.
\]

The closed lowest-coefficient formula for a unit row gives

\[
\frac{c^{U'}_{d+1}}{c^U_d}
=(-1)^{1-t}
\frac{m(m-1)}{2(k+1)(d+1)Y}
\frac{\binom\ell t}{\binom{r-\ell+t}t}
\left(\frac{1+a}{1-a}\right)^t.                        \tag{12}
\]

Every factor except the displayed sign is positive.  If \(t\) is even,
then (12) is negative.  Conditional on cancellation in degree \(d\), the
degree-\(d+1\) coefficient divided by \(c^U_d\) is

\[
(R_U-R_V)+\frac{c^{U'}_{d+1}}{c^U_d}.                   \tag{13}
\]

Both summands are strictly negative by (8) and (12), so (13) cannot vanish.

## 5. Odd denominators: a valuation obstruction

It remains to treat odd \(t\).  Cancellation of the two minimum
coefficients would require equality of their magnitudes.  From the closed
coefficient formula, their positive magnitude ratio is

\[
\rho=
\frac{\binom pm\binom r\ell}{\binom pi\binom rm}
2^{r-p}a^{-(2p+r-1)}
(1-a)^{p-i-r+\ell}(1+a)^{i-\ell}.                       \tag{14}
\]

At \(a=1/t\), this becomes

\[
\rho=
\frac{\binom pm\binom r\ell}{\binom pi\binom rm}
2^{r-p}t^{p+2r-1}
(t-1)^{p-i-r+\ell}(t+1)^{i-\ell}.                       \tag{15}
\]

Choose an odd prime \(\pi\mid t\).  Since \(\pi\nmid2(t-1)(t+1)\),

\[
\begin{split}
v_\pi(\rho)
={}&(p+2r-1)v_\pi(t)
+v_\pi\binom pm+v_\pi\binom r\ell\\
&-v_\pi\binom pi-v_\pi\binom rm.                     \tag{16}
\end{split}
\]

The two negative binomial valuations are at most
\(v_\pi(p!)+v_\pi(r!)\), which is strictly smaller than
\((p+r)/(\pi-1)\leq(p+r)/2\).  On the other hand,

\[
(p+2r-1)v_\pi(t)\geq p+2r-1.
\]

Here \(r\geq t\geq3\), so (16) is strictly positive.  Hence
\(\rho\neq1\), and the leading coefficients cannot cancel at all.

## 6. Closure theorem and full classification

The collision lattice has exhausted every way that additional rows can
enter the first two degrees.

**Theorem 1 (multirow noncancellation).**  For every \(p,r\geq1\),
\(0<a<1\), and \(B>0\), no candidate wall containing more than one
structural row from either two-level family disappears.

Combining this theorem with the preceding isolated-wall theorem yields a
complete arbitrary-dimensional criterion.

**Corollary 2 (all two-level missing walls).**  A positive candidate wall
disappears if and only if it contains exactly the two rows
\(U_{p-1,\ell}\) and \(V_{i,r-1}\), no additional structural row, and

\[
r-\ell\quad\text{is odd},                               \tag{17}
\]

\[
B=\frac{2\{a(p-1)+a^2\ell-i-a(r-1)\}}{1-a}>0,          \tag{18}
\]

and

\[
\frac{p\binom r\ell}
{2^{p-1}a^r(1-a)^{r-\ell}(1+a)^\ell}
=
\frac{r\binom pi a^{2p-1}}
{2^{r-1}(1-a)^{p-i}(1+a)^i}.                            \tag{19}
\]

The missing wall is \(2(p-1+a\ell)\).  When \(a\) is irrational, the
no-additional-row condition is automatic.  When \(a=s/t\) is reduced, it
is equivalent to

\[
p-1<s\ \text{ or }\ \ell+t>r,
\qquad
i+s>p\ \text{ or }\ t>r-1.                             \tag{20}
\]

Indeed, the only possible neighboring unit row is
\((p-1-s,\ell+t)\), and the only possible neighboring moving row is
\((i+s,r-1-t)\).  Thus (17)--(20) are an exact finite test for any fixed
\(p,r,a\).

## 7. Exact computational audit

`derive.py` uses SymPy 1.13.3 to reconstruct the rational transform,
principal parts, every tail replacement, and every collected degree vector.
It checks all 152 positive multirow cross-family walls at internal collision
parameters in dimensions four through seven, comprising 1,010 exact hinge
coefficients.  None vanishes.

`verify.py` shares no SymPy code.  Its first audit independently reconstructs
the same objects using only `fractions.Fraction` and checks all 1,021
multirow walls through dimension nine, comprising 8,561 exact hinge
coefficients.  Its second audit enumerates all 330,948 equal-minimum
multirow patterns through dimension thirty and verifies the exhaustive
three-way split used above: 300,098 untouched two-jet cases, 16,474 even
reciprocal sign-reinforcement cases, and 14,376 odd reciprocal valuation
cases.  Finite checks audit the implementation and case split; the proof of
Theorem 1 is the arbitrary-parameter argument in Sections 2--5.
