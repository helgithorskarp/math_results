# Arbitrary-dimensional rigidity of isolated two-level resonances

## 1. Setup and scope

For normalized active weights

\[
1^p a^r,\qquad p,r\geq1,\qquad q=p+r,\qquad0<a<1,
\]

write \(H_d(s;\omega)=(s-\omega)_+^d\) and
\(\lambda=(1-a)/a\).  The global weighted chamber formula cited in
SOURCES.md organizes the contribution at a candidate wall into structural
rows.  A unit-supplier row \(U_{k,\ell}\) and an \(a\)-supplier row
\(V_{i,j}\) have

\[
\begin{array}{c|c|c}
 &\text{wall}&\text{lowest hinge degree}\\ \hline
U_{k,\ell}&2(k+a\ell)&r+k,\\
V_{i,j}&\lambda B+2i/a+2j&p+j,
\end{array}                                               \tag{1}
\]

where \(0\leq k<p\), \(0\leq\ell\leq r\),
\(0\leq i\leq p\), and \(0\leq j<r\).  Here \(B>0\) is the normalized
boundary parameter.

We call a cross-family wall **isolated** if exactly one structural row from
each family occurs there.  This excludes the special parameters at which
two subset sums within one family agree.  The theorem below is uniform in
\(q\), but it is intentionally a classification of isolated walls; it does
not claim that a multirow collision cannot cancel.

If the two rows in (1) can cancel, their lowest degrees must agree.  Hence

\[
m:=p-k=r-j.                                               \tag{2}
\]

The wall equation then gives

\[
B=\frac{2(ak+a^2\ell-i-aj)}{1-a},\qquad
X:=k-i+a(\ell-j)>0,                                      \tag{3}
\]

and

\[
B+2k+2a\ell=\frac{2X}{1-a},\qquad
B+2i+2aj=\frac{2aX}{1-a}.                               \tag{4}
\]

The earlier arbitrary-\(q\) lowest-coefficient formula proves that leading
cancellation is possible only if \(r-\ell\) is odd.  We now show that if
\(m\geq2\), cancellation of that leading coefficient exposes a nonzero
next coefficient.

## 2. A two-jet calculation

For a set of \(n\) remaining weights, the rational transform used by the
global formula is

\[
T(t)=\frac{1}{(1-t)^n\prod_w w\prod_w(1-w+wt)}.           \tag{5}
\]

At a pole \(-\mu\) of multiplicity \(m\), let \(C_m\) and \(C_{m-1}\)
be the two highest principal-part coefficients.  A removed tail of weight
\(w\) contributes the moment factor

\[
\eta_h(w,\mu)=
\frac{w^h}{(1+w+\mu w)^{h+1}}
-\frac{1}{w(1+\mu)^{h+1}}.                              \tag{6}
\]

Put \(d=q-m\).  The coefficient of \(H_d\) uses \(C_m\) and moment zero
at every tail.  There are exactly two sources for \(H_{d+1}\): use
\(C_{m-1}\) with all moments zero, or use \(C_m\) with moment one at one
tail and moment zero at all others.

The beta factors telescope.  Relative to the all-zero path, replacing the
zero moment at any specified tail by moment one contributes

\[
\frac{m-1}{d+1}\frac{\eta_1(w,\mu)}{\eta_0(w,\mu)}.       \tag{7}
\]

Indeed, if the slack before that tail is \(s\) and \(L\) tails follow it,
the local beta-factor ratio is \((m-1)/(s+2)\); the later zero-moment
ratios telescope to \((s+2)/(s+L+2)\), and
\(s+L+2=d+1\).  Thus (7) is independent of the ordering of the tails.

### The unit-supplier row

After its \(k+\ell\) tails are removed, the regularized transform at
\(t=0\) is

\[
G_U(t)=\frac{1}{(1-t)^{m+r-\ell}a^{r-\ell}
                    (1-a+at)^{r-\ell}}.
\]

Consequently

\[
\frac{C_{m-1}}{C_m}
=m+r-\ell-\frac{a(r-\ell)}{1-a}.                         \tag{8}
\]

At \(\mu=0\), the tail ratios in (7) are

\[
\frac{\eta_1(1,0)}{\eta_0(1,0)}=\frac32,
\qquad
\frac{\eta_1(a,0)}{\eta_0(a,0)}=\frac{1+2a}{1+a}.        \tag{9}
\]

If \(c^U_d,c^U_{d+1}\) denote the first two hinge coefficients of this
row, (7)--(9) give

\[
R_U:=\frac{c^U_{d+1}}{c^U_d}
=\frac{m-1}{d+1}\frac{1}{B+2k+2a\ell}
\left(
m+r-\ell-\frac{a(r-\ell)}{1-a}
+\frac{3k}{2}+\frac{(1+2a)\ell}{1+a}
\right).                                                \tag{10}
\]

### The \(a\)-supplier row

Put \(P=p-i\).  At \(t=-\lambda\), its regularized transform is

\[
G_V(t)=\frac{1}{(1-t)^{P+m}a^{2m}t^P},
\]

so

\[
\frac{C_{m-1}}{C_m}=a(P+m)+\frac{aP}{1-a}.               \tag{11}
\]

At \(\mu=\lambda\),

\[
\frac{\eta_1(1,\lambda)}{\eta_0(1,\lambda)}
=\frac{a(a+2)}{a+1},
\qquad
\frac{\eta_1(a,\lambda)}{\eta_0(a,\lambda)}
=\frac{3a}{2}.                                          \tag{12}
\]

Therefore

\[
R_V:=\frac{c^V_{d+1}}{c^V_d}
=\frac{m-1}{d+1}\frac{1}{B+2i+2aj}
\left(
a(p-i+m)+\frac{a(p-i)}{1-a}
+\frac{a(a+2)i}{1+a}+\frac{3aj}{2}
\right).                                                \tag{13}
\]

## 3. Rigidity theorem

Substitute \(k=p-m\), \(j=r-m\), and (4) into (10)--(13).  Direct
collection gives the decisive identity

\[
\boxed{
R_U-R_V=
-\frac{(m-1)\{q(1+a)^2-4a(i+\ell)\}}
{4X(q-m+1)(1+a)}.}                                      \tag{14}
\]

The numerator in braces is strictly positive, because

\[
q(1+a)^2-4a(i+\ell)
=q(1-a)^2+4a(q-i-\ell)>0;                               \tag{15}
\]

here \(i+\ell\leq p+r=q\), \(0<a<1\), and \(q>0\).

**Theorem 1 (higher-multiplicity rigidity).**  At an isolated positive
cross-family resonance satisfying (2), if \(m\geq2\), the two structural
rows cannot cancel identically.

**Proof.**  Both leading row coefficients are nonzero because \(X>0\).
If they do not sum to zero, the wall remains.  If they do, write
\(c^V_d=-c^U_d\).  The aggregate next coefficient is then

\[
c^U_{d+1}+c^V_{d+1}=c^U_d(R_U-R_V),
\]

which is nonzero by (14)--(15).  \(\square\)

The sign in (14) is stronger than nonvanishing: after normalizing by the
leading coefficients, the unit-supplier two-jet always has the smaller
next coefficient.

## 4. Complete isolated-wall criterion

The earlier closed leading coefficient is

\[
\frac{2^{m-1}X^{m-1}}
{(m-1)!(q-m)!(1-a)^{m-1}}
\left[
\frac{(-1)^{p-m+\ell}\binom pm\binom r\ell}
{2^{p-m}a^r(1-a)^{r-\ell}(1+a)^\ell}
+
\frac{(-1)^{q-m}\binom pi\binom rm a^{2p-1}}
{2^{r-m}(1-a)^{p-i}(1+a)^i}
\right].                                                \tag{16}
\]

For \(m=1\), each row consists only of \(H_{q-1}\).  Combining (14)--(16)
therefore gives the promised arbitrary-dimensional classification.

**Corollary 2 (isolated two-level missing walls).**  An isolated positive
cross-family wall disappears if and only if all of the following hold:

1. \(k=p-1\) and \(j=r-1\);
2. \(r-\ell\) is odd;
3. the resonance boundary
   \[
   B=\frac{2\{a(p-1)+a^2\ell-i-a(r-1)\}}{1-a}
   \]
   is positive;
4. the exact magnitude equation
   \[
   \frac{p\binom r\ell}
   {2^{p-1}a^r(1-a)^{r-\ell}(1+a)^\ell}
   =
   \frac{r\binom pi a^{2p-1}}
   {2^{r-1}(1-a)^{p-i}(1+a)^i}                          \tag{17}
   \]
   holds.

The resulting missing wall is \(2(p-1+a\ell)\).  Condition (17) is an
exact algebraic equation after denominators are cleared.  Thus every
isolated cross-family missing wall in every active dimension is a
simple-pole resonance; higher repeated poles produce no exceptions.

## 5. Exact computational audit

`derive.py` independently constructs the rational transform (5), its exact
principal parts, every tail replacement, and the collected hinge rows.  In
all 36 positive-boundary higher-multiplicity candidate types for
\(q=4,5,6\), it checks both row-ratio formulas and (14) as identities in
\(\mathbb Q(a)\).  This includes all 12 types that survive the earlier
parity obstruction.

`verify.py` shares no symbolic code.  Using only `fractions.Fraction`, it
reconstructs (6), the two regularized logarithmic derivatives, and the beta
ratio for 53,595 exact rational instances: three positive-boundary samples
for every one of 17,865 higher-multiplicity candidate types in dimensions
\(4\) through \(20\).  It also checks (15) and the strict negative sign in
(14).  These computations audit the derivation; the arbitrary-\(q\) proof
is the algebra above, not finite sampling.
