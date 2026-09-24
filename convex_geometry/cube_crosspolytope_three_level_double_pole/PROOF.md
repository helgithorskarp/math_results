# Sharp failure of higher-pole rigidity at three weight levels

## 1. Structural rows and a general two-jet formula

Use the normalization and global weighted chamber formula cited in
[SOURCES.md](SOURCES.md).  For a supplier weight \(u\), let \(T\) be the
labeled multiset of removed tails and let \(W\) be the multiset of remaining
weights.  Suppose \(u\) has multiplicity \(m\) in \(W\).  Write

\[
N=|W|,\qquad q=N+|T|,\qquad d=q-m,
\]

and let \(\omega\) be the row wall.  At the supplier pole
\(\lambda_u=(1-u)/u\),

\[
\omega=\lambda_uB+\frac2u\sum_{w\in T}w,
\qquad B+2\sum_{w\in T}w=u(B+\omega).                 \tag{1}
\]

Let \(c_d,c_{d+1}\) be the first two hinge coefficients of this row.
The following identity is useful beyond the example below:

\[
\boxed{
\frac{c_{d+1}}{c_d}
=\frac{m-1}{(d+1)(B+\omega)}
\left[
N-\sum_{\substack{x\in W\\x\ne u}}\frac{x}{u-x}
+\sum_{w\in T}\frac{u+2w}{u+w}
\right].}                                             \tag{2}
\]

Both sums are over labeled weights.  To prove (2), regularize the rational
transform at \(-\lambda_u\).  If \(C_m,C_{m-1}\) are its two highest
principal-part coefficients, logarithmic differentiation gives

\[
\frac{C_{m-1}}{C_m}
=u\left[N-\sum_{\substack{x\in W\\x\ne u}}\frac{x}{u-x}\right]. \tag{3}
\]

For a tail of weight \(w\), the moment factors in the global formula obey

\[
\frac{\eta_1(w,\lambda_u)}{\eta_0(w,\lambda_u)}
=\frac{u(u+2w)}{u+w}.                                  \tag{4}
\]

The beta-integral factors telescope exactly as in the two-level two-jet
argument: every source for the next coefficient has common multiplier
\((m-1)/(d+1)\), followed by division by the shifted boundary in (1).
Substituting (3)--(4) and the last equality in (1) proves (2).  In the
two-level setting the difference of two expressions (2) has a fixed sign.
A third weight makes exact equality possible.

## 2. The three-level construction

Take five active weights

\[
(1,1,a,a,b),\qquad 0<b<a<1.                            \tag{5}
\]

Consider two rows:

- \(U\): supplier \(1\), with the single \(b\)-coordinate removed as a
  tail;
- \(A\): supplier \(a\), with no tails.

Their walls are respectively \(2b\) and \((1-a)B/a\).  They resonate when

\[
B=\frac{2ab}{1-a}.                                     \tag{6}
\]

Each supplier has residual multiplicity two, so both rows contain precisely
the hinges \(H_3(s;2b)\) and \(H_4(s;2b)\).  Exact principal-part and tail
calculation gives

\[
\begin{array}{c|cc}
 &c_3&c_4\\ \hline
U&\displaystyle\frac1{3a^2(a-1)^3(b+1)}
&\displaystyle-\frac{8ab+7a-6b-5}
 {24a^2b(a-1)^3(b+1)^2}\\[3mm]
A&\displaystyle-\frac{a^5}{3(a-1)^3(a-b)}
&\displaystyle\frac{a^5(5a^2-6ab-7a+8b)}
 {24b(a-1)^3(a-b)^2}.
\end{array}                                            \tag{7}
\]

The degree-three coefficients cancel exactly when

\[
a-b=a^7(1+b),
\qquad	ext{that is,}\qquad
b=\frac{a(1-a^6)}{1+a^7}.                              \tag{8}
\]

The difference of the normalized next coefficients simplifies to

\[
\frac{c^U_4}{c^U_3}-\frac{c^A_4}{c^A_3}
=-\frac{(a+1)(3ab+2a-2b^2-3b)}
 {8b(a-b)(b+1)}.                                       \tag{9}
\]

Put

\[
P(a)=a^{10}-3a^9+4a^8-4a^7+5a^6-7a^5
     +5a^4-4a^3+4a^2-3a+1                             \tag{10}
\]

and \(S(a)=a^6-a^5+a^4-a^3+a^2-a+1\).  Substitution of
(8) into the numerator in (9) gives the identity

\[
3ab+2a-2b^2-3b
=-\frac{a(a^2+1)P(a)}{S(a)^2}.                         \tag{11}
\]

Thus any root of \(P\) in \((0,1)\) makes the ratios in (9) equal.
Together with (8), this cancels the degree-four coefficients as well.

## 3. Exact root and admissibility

An exact Sturm calculation for \(P\) on

\[
I=\left(\frac{127}{200},\frac{637}{1000}\right)
\]

has sign sequences

\[
(+,-,-,+,+,-,+,+,-,-,+),
\qquad
(-,-,-,+,+,-,+,+,-,-,+)
\]

at the left and right endpoints.  Their variation counts are six and five,
so \(I\) contains exactly one root \(\alpha\).  Define

\[
\beta=\frac{\alpha(1-\alpha^6)}{1+\alpha^7},
\qquad
B=\frac{2\alpha\beta}{1-\alpha}.                       \tag{12}
\]

Because \(0<\alpha<1\), one has

\[
0<\frac{1-\alpha^6}{1+\alpha^7}<1,
\]

and hence \(0<\beta<\alpha<1\) and \(B>0\).  Rational bisection gives

\[
(\alpha,\beta,B)
=(0.635988208014771\ldots,
  0.569915848324062\ldots,
  1.991472623005279\ldots).                            \tag{13}
\]

## 4. No other row reaches the wall

For the weights in (5), the 33 structural walls split into the following
three supplier families:

\[
\begin{array}{c|c|c}
\text{supplier}&\text{wall}&\text{index ranges}\\ \hline
1&2(k+a\ell+bh)&0\le k\le1,\ 0\le\ell\le2,\ 0\le h\le1,\\
a&\displaystyle\frac{1-a}{a}B+
 \frac2a(i+aj+bg)&0\le i\le2,\ 0\le j\le1,\ 0\le g\le1,\\
b&\displaystyle\frac{1-b}{b}B+
 \frac2b(i+a\ell)&0\le i,\ell\le2.
\end{array}                                            \tag{14}
\]

In the first family, the only value equal to \(2b\) is
\((k,\ell,h)=(0,0,1)\): when \(h=0\), a positive wall is at least
\(2a>2b\), and when \(h=1\), every other index adds a positive quantity.
By (6), the second family is \(2b+2(i+aj+bg)/a\), so only
\((i,j,g)=(0,0,0)\) reaches the target.  Finally the least wall in the
third family satisfies

\[
\frac{1-b}{b}B=\frac{2a(1-b)}{1-a}>2b,                 \tag{15}
\]

where the last inequality is equivalent to \(a>b\).  Hence exactly the two
rows in Section 2 occur at the wall.

## 5. The theorem and minimality

**Theorem (minimal three-level double-pole missing wall).**  For the exact
parameters (10)--(12), the global weighted ray-chamber expansion with active
weights \((1,1,\alpha,\alpha,\beta)\) has no hinge contribution at
\(s=2\beta\), even though both structural rows at that candidate wall arise
from residual poles of multiplicity two.

**Proof.**  Section 4 shows that exactly the rows \(U,A\) occur at the wall.
They have only degrees three and four.  Equations (8) and (11) cancel those
two coefficients, respectively.  Therefore their complete hinge vectors
sum to zero. \(\square\)

Two different suppliers of multiplicity at least two require four active
coordinates.  Requiring a third distinct weight requires one more.  Thus
\(q=5=2+2+1\) is the smallest active dimension in which a genuinely
three-level double-pole cancellation of this type can occur.  The theorem is
therefore a sharp failure, at the first possible dimension, of the
two-level higher-pole rigidity result.

## 6. Computational audit

`derive.py` reconstructs the rational transform, all principal parts, every
tail replacement, and the complete 33-row hinge table in SymPy 1.13.3.  It
checks (7)--(11), the two row supports, the Sturm root count, and exact
coprimality of every other row-difference numerator with \(P\).

`verify.py` shares no SymPy code.  Using only `fractions.Fraction`, it
implements polynomial Euclidean division, Sturm sequences, rational
functions, exact bisection, the coefficient identities, and an independent
enumeration of all 33 walls.  It obtains exactly the two intended target
rows and 31 coprime exclusions.  Neither checker uses floating-point values
to decide any mathematical claim.
