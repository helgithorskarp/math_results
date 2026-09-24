# Classification of isolated double-pole missing walls for `(1,1,a,a,b)`

## 1. Statement and terminology

Use the normalization and the global weighted ray-chamber formula cited in
[`SOURCES.md`](SOURCES.md).  Fix

\[
        (w_1,\ldots,w_5)=(1,1,a,a,b),\qquad 0<b<a<1,
        \qquad B>0.                                      \tag{1}
\]

A *double-pole row* is a structural row whose supplier still has residual
multiplicity two after its tails are removed.  A candidate wall is called
*isolated double-pole* when exactly two structural rows reach it and both are
double-pole rows.  A wall is *missing* when the sum of its entire hinge vector
is zero.

For later reference define

\[
\begin{aligned}
D_1&=a^6-a^5+a^4-a^3+a^2-a+1,\\
N_1&=-a(a-1)(a^2-a+1)(a^2+a+1),\\
D_2&=a^8+a^7+2a-2,\\
N_2&=a(a^7+a^6+2a-2),\\
D_3&=a^9+2a^8+a^7+a^2-2a+1,\\
N_3&=a(a^2+1)(a^2+a-1)(a^4+a^3-a+1),\\
D_4&=2a^8+2a^7-a+1,\\
N_4&=a(2a^7+2a^6+a-1).
                                                               \tag{2}
\end{aligned}
\]

The following theorem is the exact endpoint.

**Theorem.**  Among all parameters satisfying (1), there are exactly three
isolated double-pole missing-wall families.  They are Families I--III in
Table 1 below.  Each displayed polynomial has exactly one root in its
displayed interval, so each row specifies one exact pair \((a,b)\).

| family | unit-supplier tails | \(a\)-supplier tails | \(b\) | defining polynomial and root interval | wall | \(B\) |
|---|---|---|---|---|---|---|
| I | \(b\) | none | \(N_1/D_1\) | \(P_1(a)=0\), \((127/200,637/1000)\) | \(2b\) | \(2ab/(1-a)\) |
| II | one \(a\) | none | \(N_2/D_2\) | \(P_2(a)=0\), \((27/40,677/1000)\) | \(2a\) | \(2a^2/(1-a)\) |
| III | two \(a\)'s and \(b\) | none | \(-N_3/D_3\) | \(P_3(a)=0\), \((64/125,513/1000)\) | \(2(2a+b)\) | \(2a(2a+b)/(1-a)\) |

Here

\[
\begin{aligned}
P_1={}&a^{10}-3a^9+4a^8-4a^7+5a^6-7a^5
       +5a^4-4a^3+4a^2-3a+1,\\
P_2={}&a^{15}+2a^{14}+a^{13}+6a^9+2a^8-2a^7-6a^6
       +4a^2-8a+4,\\
P_3={}&a^{15}+4a^{14}+5a^{13}-4a^{11}+a^9-a^8+a^7-a^6
       +4a^4-5a^2+4a-1.                              \tag{3}
\end{aligned}
\]

Numerically, only for orientation,

\[
\begin{array}{c|ccc}
 &a&b&B\\ \hline
\mathrm I&0.635988208014771&0.569915848324062&1.991472623005279\\
\mathrm {II}&0.675942551239167&0.611108335127635&2.819860085443809\\
\mathrm {III}&0.512290716800301&0.388651250803741&2.968924356531757.
\end{array}                                             \tag{4}
\]

Family I is the previously published minimal example.  Families II and III
are new solutions, and the theorem proves that the list is complete within
the stated isolated class.

## 2. Reduction to 36 pairs, then eight

A unit-supplier double-pole row cannot remove either unit coordinate.  Write
its tail counts as

\[
       (\ell,h),\qquad 0\leq\ell\leq2,\quad 0\leq h\leq1,
\]

where \(\ell\) is the number of \(a\)-tails and \(h\) is the number of
\(b\)-tails.  Its wall is

\[
       \omega_U=2(a\ell+bh).                            \tag{5}
\]

Similarly an \(a\)-supplier double-pole row has \(i\) unit tails and \(g\)
\(b\)-tails, with

\[
       0\leq i\leq2,\quad 0\leq g\leq1,
       \qquad
       \omega_A=\frac{1-a}{a}B+\frac2a(i+bg).          \tag{6}
\]

Rows of the same supplier have distinct walls under (1).  A missing wall
must have at least two double-pole rows because its leading \(H_3\)
coefficient cannot otherwise vanish.  Hence every isolated double-pole
missing wall is one of the \(6\cdot6=36\) resonant pairs (5)--(6), with

\[
 B=\frac{2\{a(a\ell+bh)-(i+bg)\}}{1-a}.                \tag{7}
\]

For a supplier \(u\), every tail contributes the negative moment factor

\[
 \eta_0(u,w)=\frac{u}{u+w}-\frac{u}{w}
             =-\frac{u^2}{w(u+w)}.                     \tag{8}
\]

All other sign-bearing factors in a unit-supplier leading coefficient are
positive.  Thus its sign is \((-1)^{\ell+h}\).  For an \(a\)-supplier row,
the \(2-i\) retained unit weights and the \(i+g\) tails give total sign
\((-1)^g\).  Cancellation therefore requires

\[
                    \ell+h+g\quad\hbox{odd}.           \tag{9}
\]

Combining (9) with positivity of the numerator in (7) leaves exactly

\[
\begin{split}
&(0,1,0,0),(1,0,0,0),(1,1,0,1),(2,0,0,1),\\
&(2,0,1,1),(2,1,0,0),(2,1,1,0),(2,1,2,0),             \tag{10}
\end{split}
\]

where a tuple means \((\ell,h,i,g)\).  For completeness, this last reduction
is elementary.  If \(\ell=0\), (7) is positive only for the first tuple in
(10).  If \(\ell=1\), the odd-parity cases with \(i\geq1\) are negative using
\(a^2<1\), leaving the next two tuples.  If \(\ell=2\), odd parity forces
\(h\ne g\); the five possibilities not immediately bounded above by zero are
exactly the last five tuples in (10).

## 3. Exact leading-coefficient classification

For a repeated supplier, both rows contain precisely \(H_3\) and \(H_4\).
The global formula gives the following factorization of the sum of their
\(H_3\) coefficients.  Nonzero rational factors have been suppressed.

| \((\ell,h,i,g)\) | leading equation |
|---|---|
| \((0,1,0,0)\) | \(D_1b-N_1=0\) |
| \((1,0,0,0)\) | \(D_2b-N_2=0\) |
| \((1,1,0,1)\) | \(D_2b+N_2=0\) |
| \((2,0,0,1)\) | \((2a-b)(D_3b-N_3)=0\) |
| \((2,0,1,1)\) | \((2a-b-1)(D_4b-N_4)=0\) |
| \((2,1,0,0)\) | \((2a+b)(D_3b+N_3)=0\) |
| \((2,1,1,0)\) | \((2a+b-1)(D_4b+N_4)=0\) |
| \((2,1,2,0)\) | \((2a+b-2)(D_1b-N_1)=0\) |

The labeled-tail multiplicities \(\binom2\ell\) and \(\binom2i\) are
included here.  This is essential in the two patterns with exactly one tail
from a doubled level.

There is no lost solution at a zero of a \(D_j\): in every case
\(\gcd(D_j,N_j)=1\).  The five extra linear-factor branches are inadmissible:

\[
\begin{array}{c|c|c}
\text{pattern}&\text{extra branch}&\text{obstruction}\\ \hline
(2,0,0,1)&b=2a&b>a\\
(2,0,1,1)&b=2a-1&B=-4a\\
(2,1,0,0)&b=-2a&b<0\\
(2,1,1,0)&b=1-2a&B=-2\\
(2,1,2,0)&b=2-2a&B=-4.
\end{array}                                             \tag{11}
\]

It remains to impose cancellation of \(H_4\).  If \(c_3,c_4\) are the two
coefficients of one row, logarithmic differentiation of its regularized
double pole gives

\[
\frac{c_4}{c_3}
=\frac1{4(B+\omega)}
\left[
 |W|-\sum_{\substack{x\in W\\x\ne u}}\frac{x}{u-x}
 +\sum_{w\in T}\frac{u+2w}{u+w}
\right],                                                \tag{12}
\]

where \(W\) is the labeled multiset left after the tails \(T\) are removed.
Once the \(H_3\) coefficients are opposite, \(H_4\) cancels exactly when the
two values in (12) agree.

Substitution of the nondegenerate branches in the table above gives the
following complete eliminant table.  In each entry, the omitted numerator
factor has no zero in \((0,1)\), and the denominator is coprime to the stated
polynomial.

| pattern | \(b\)-branch | eliminant |
|---|---|---|
| \((0,1,0,0)\) | \(N_1/D_1\) | \(P_1\) |
| \((1,0,0,0)\) | \(N_2/D_2\) | \(P_2\) |
| \((1,1,0,1)\) | \(-N_2/D_2\) | \(P_2\) |
| \((2,0,0,1)\) | \(N_3/D_3\) | \(P_3\) |
| \((2,0,1,1)\) | \(N_4/D_4\) | \(P_4\) |
| \((2,1,0,0)\) | \(-N_3/D_3\) | \(P_3\) |
| \((2,1,1,0)\) | \(-N_4/D_4\) | \(P_4\) |
| \((2,1,2,0)\) | \(N_1/D_1\) | \(P_5\) |

The two remaining polynomials are

\[
\begin{aligned}
P_4={}&4a^{15}+8a^{14}+4a^{13}+6a^9-2a^8-2a^7+6a^6
        -a^2+2a-1,\\
P_5={}&a^{12}+a^{11}+a^{10}+a^9+a^8+a^7-2a^6
        +a^5+a^4+a^3+a^2+a+1.                         \tag{13}
\end{aligned}
\]

## 4. Root census and admissibility

Exact Sturm sequences give

\[
\begin{array}{c|ccccc}
 &P_1&P_2&P_3&P_4&P_5\\ \hline
\#\{a\in(0,1):P_j(a)=0\}&1&2&1&1&0.
\end{array}                                             \tag{14}
\]

The two roots of \(P_2\) lie respectively in
\((27/40,677/1000)\) and \((9/10,901/1000)\).  The root of \(P_4\) lies in
\((71/125,569/1000)\).  Exact sign isolation at these rational intervals
gives:

- the \(P_1\) root on the \(N_1/D_1\) branch is admissible;
- the first \(P_2\) root on the \(N_2/D_2\) branch is admissible, while the
  second has \(b>a\), and both roots on the reflected branch have \(b<0\);
- the \(P_3\) root is admissible only on \(-N_3/D_3\); the reflected branch
  has \(b<0\);
- the \(P_4\) root has \(b<0\) on \(N_4/D_4\), while the reflected branch
  has \(b>0\) but \(B<0\);
- \(P_5\) contributes no root.  Indeed,
  \(P_5=(1-a^6)^2+a+a^2+a^3+a^4+a^5+a^7+a^8+a^9+a^{10}+a^{11}>0\)
  on \((0,1)\).

This proves that only Families I--III survive.

## 5. Isolation and conclusion

For arbitrary parameters (1), the complete structural-wall list is

\[
\begin{array}{c|c|c}
\text{supplier}&\text{wall}&\text{index ranges}\\ \hline
1&2(k+a\ell+bh)&0\leq k\leq1,\ 0\leq\ell\leq2,\ 0\leq h\leq1,\\
a&\displaystyle\frac{1-a}{a}B+
 \frac2a(i+aj+bg)&0\leq i\leq2,\ 0\leq j\leq1,\ 0\leq g\leq1,\\
b&\displaystyle\frac{1-b}{b}B+
 \frac2b(i+a\ell)&0\leq i,\ell\leq2.
\end{array}                                             \tag{15}
\]

There are \(12+12+9=33\) rows.  For each of Families I--III, exact
substitution into all 33 walls leaves precisely the intended two identities.
For every other row, the numerator of its difference from the target wall is
coprime to the corresponding \(P_j\).  Thus no third row reaches the wall.

The two intended rows have support exactly \(\{H_3,H_4\}\).  Section 3
cancels \(H_3\), and the defining polynomial cancels \(H_4\).  Consequently
the whole hinge vector vanishes.  Sections 2--4 prove that every isolated
double-pole missing wall must be one of these three.  This completes the
proof. \(\square\)

## 6. Computational audit

`derive.py` uses SymPy 1.13.3 to rebuild the global transform, all principal
parts and tail actions, and the complete 33-row table.  It checks all 36 pair
patterns, the eight leading factorizations, the five eliminants, exact root
and sign isolation, both coefficient cancellations, and all 31 non-target
rows in each physical family.

`verify.py` imports no SymPy code.  Its standard-library implementation uses
`fractions.Fraction`, polynomial Euclidean division, Sturm sequences, and
rational functions.  It independently reconstructs each row's two jets from
the regularized principal part and tail moments, checks all eliminants and
admissibility signs, and enumerates the 33 walls for each survivor.  No
floating-point value decides a mathematical claim.
