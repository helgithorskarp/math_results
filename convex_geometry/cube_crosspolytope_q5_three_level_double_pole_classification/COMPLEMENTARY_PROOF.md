# Complete ordering classification for three-level double-pole walls

## 1. Strengthened theorem

Fix active weights

\[
                     (1,1,a,a,b),\qquad 0<a,b<1,\quad a\ne b,\quad B>0. \tag{1}
\]

A *double-pole missing wall* is a missing structural wall reached by at least
one row whose supplier retains multiplicity two.  Other rows are allowed to
reach the same wall.

**Complementary-order theorem.**  If

\[
                              0<a<b<1,                 \tag{2}
\]

there is no double-pole missing wall.

Together with [`NONISOLATED_PROOF.md`](NONISOLATED_PROOF.md), this gives a
complete ordering classification under (1): the three exact families in
[`PROOF.md`](PROOF.md) are all the double-pole missing walls when the
singleton lower weight satisfies \(b<a\), and none exists when \(a<b\).
Thus no ordering hypothesis is needed beyond specifying which lower level
has multiplicity two.  The excluded boundary \(a=b\) is a two-level weight
system with multiplicity three, not a three-level instance.

## 2. Leading signs and the six candidate patterns

A unit-supplier double-pole row has tail counts

\[
             (\ell,h),\qquad 0\leq\ell\leq2,\quad 0\leq h\leq1,
\]

and wall \(2(\ell a+hb)\).  An \(a\)-supplier double-pole row has tail
counts

\[
             (i,g),\qquad 0\leq i\leq2,\quad 0\leq g\leq1,
\]

and wall

\[
             \frac{1-a}{a}B+\frac2a(i+gb).
\]

Equating the walls fixes

\[
 B=\frac{2\{a(\ell a+hb)-(i+gb)\}}{1-a}.              \tag{3}
\]

Every tail contributes the negative leading moment

\[
                   \eta_0(u,w)=-\frac{u^2}{w(u+w)}.   \tag{4}
\]

Under (2), the unit-supplier leading sign is
\((-1)^{\ell+h}\).  For an \(a\)-supplier row, the retained larger weights
are the \(2-i\) unit weights and, when \(g=0\), the singleton \(b\).  The
regularized pole and the \(i+g\) tails therefore give total sign

\[
             (-1)^{(2-i)+(1-g)+(i+g)}=-1.             \tag{5}
\]

Cancellation requires \(\ell+h\) even.  The case \((\ell,h)=(0,0)\) has
\(B\leq0\).  For \((1,1)\) or \((2,0)\), equation (3) can be positive only
for

\[
                (i,g)\in\{(0,0),(0,1),(1,0)\}.       \tag{6}
\]

Indeed, \(i\geq2\) is immediate.  If \((i,g)=(1,1)\), then
\(a(a+b)<a+b<1+b\), and similarly \(2a^2<2a<1+b\).
Consequently exactly six of the 36 unit/\(a\)-supplier pairs can enter the
physical domain.

## 3. Complete leading branches

Put

\[
\begin{aligned}
D_2&=a^8+a^7+2a-2,\\
D_3&=a^9+2a^8+a^7+a^2-2a+1,\\
D_4&=2a^8+2a^7-a+1,\\
S_6&=1+a+a^2+a^3+a^4+a^5+a^6.
\end{aligned}                                         \tag{7}
\]

Exact factorization of the aggregate \(H_3\) coefficient gives the six
nondegenerate branches below.

| name | \((\ell,h,i,g)\) | \(b=\beta(a)\) | other leading branch |
|---|---|---|---|
| C1100 | \((1,1,0,0)\) | \(-a(a^7+a^6-2a+2)/D_2\) | \(b=-a\) |
| C1101 | \((1,1,0,1)\) | \(-a(a^7+a^6+2a-2)/D_2\) | none |
| C1110 | \((1,1,1,0)\) | \(-a(a^2+1)(a^4-a^2+1)/((a-1)S_6)\) | \(b=1-a\) |
| C2000 | \((2,0,0,0)\) | \(a(a^8+2a^7+a^6+a^2-2a+1)/D_3\) | none |
| C2001 | \((2,0,0,1)\) | \(a(a^2+1)(a^2+a-1)(a^4+a^3-a+1)/D_3\) | \(b=2a\) |
| C2010 | \((2,0,1,0)\) | \(a(2a^7+2a^6-a+1)/D_4\) | \(a=1/2\) |

These branches are exhaustive, not selected solutions of a larger equation:
the first, third, and fifth leading numerators have respectively the two
displayed linear-in-\(b\) factors, the second and fourth have one, and the
sixth has the displayed vertical factor times one linear-in-\(b\) factor.
The extra branches are inadmissible.  The first has \(b<0\); the C1110 and
C2010 extras give \(B=-2\); and the C2001 extra gives \(B=-4a\).

There is one same-supplier commensurability not represented by a generic
pair.  At \(b=2a\), the rows \(U(0,2,0)\) and \(U(0,0,1)\) meet.  Since
\(a<1/2\), positivity of (3) leaves only \(A(0,0,0)\) at their common wall.
The numerator of the complete three-row \(H_3\) sum, after removing the
positive endpoint factor \(a\), is

\[
             4-a^3-2a^4+3a^5+8a^6+4a^7.             \tag{8}
\]

It is positive on \((0,1)\), since \(a^3+2a^4<3\).  Hence the exceptional
three-row stratum cannot be missing.

## 4. Generic next-coefficient exclusion

On each nondegenerate branch the two generic rows already cancel in degree
three.  Up to branch-denominator factors, their aggregate \(H_4\) numerator
is the corresponding polynomial below:

\[
\begin{aligned}
E_{1100}={}&a^{15}+2a^{14}+a^{13}-6a^9-6a^8-6a^7-6a^6-4a^2+8a-4,\\
E_{1101}={}&a^{15}+2a^{14}+a^{13}+6a^9+2a^8-2a^7-6a^6+4a^2-8a+4,\\
E_{1110}={}&a^{10}-2a^8-a^7+2a^6+2a^5+2a^4-a^3-2a^2+1,\\
E_{2000}={}&a^{17}+4a^{16}+6a^{15}+4a^{14}+a^{13}+3a^{11}-a^{10}
              -2a^9-2a^8-a^7+3a^6+a^4-4a^3+6a^2-4a+1,\\
E_{2001}={}&a^{15}+4a^{14}+5a^{13}-4a^{11}+a^9-a^8+a^7-a^6
              +4a^4-5a^2+4a-1,\\
E_{2010}={}&4a^{15}+8a^{14}+4a^{13}-6a^9+6a^8-6a^7+6a^6+a^2-2a+1.
                                                               \tag{9}
\end{aligned}
\]

Exact Sturm counts in \((0,1)\) are

\[
                    (0,2,0,0,1,0).                  \tag{10}
\]

The two roots of \(E_{1101}\) lie in
\((27/40,677/1000)\) and \((9/10,901/1000)\); on both, its branch has
\(b<0\).  The root of \(E_{2001}\) lies in
\((64/125,513/1000)\), where that branch also has \(b<0\).  Thus no generic
point on a physical leading branch cancels \(H_4\).

## 5. Every extra-row collision

A simple-pole row contributes only \(H_4\), so it can matter only by joining
one of the leading branches.  On each branch, substitute \(b=\beta(a)\) and
the boundary (3) into all 33 structural walls.  For each of the other 31
rows, factor the numerator of its difference from the target wall over
\(\mathbb Q\).  Exact open-interval root counts give:

| branch | collision factors | roots in \((0,1)\) |
|---|---:|---:|
| C1100 | 13 | 13 |
| C1101 | 14 | 14 |
| C1110 | 8 | 9 |
| C2000 | 3 | 3 |
| C2001 | 6 | 7 |
| C2010 | 2 | 2 |
| **total** | **46** | **48** |

The maximum factor degree is 19.  After the recorded factors are divided
from every wall difference, the residual polynomial has no root in
\((0,1)\).

For a recorded factor \(F\), let \(S_F\) contain every structural row whose
wall difference is divisible by \(F\), including the two generic rows.
All labeled-tail multiplicities are included.  If

\[
                      C_{4,F}=\sum_{r\in S_F}c_{4,r},
\]

then exact polynomial reduction gives

\[
                \gcd\!\left(F,\operatorname{num}C_{4,F}\right)=1
                                                               \tag{11}
\]

for all 46 factors.  Therefore no extra-row collision cancels the complete
\(H_4\) coefficient.  The certificate also records the aggregate \(H_3\)
gcd at every factor, but (11) alone excludes every collision point.

Sections 2--5 cover every generic and nongeneric way a double-pole row can
reach a missing wall under (2).  This proves the complementary-order theorem
and, with the earlier \(b<a\) theorem, the complete classification. \(\square\)

## 6. Reproducibility and trust boundary

[`COMPLEMENTARY_CERTIFICATE.json`](COMPLEMENTARY_CERTIFICATE.json) records
the six exact branches, their eliminants, all 46 collision factors, exact
open-unit root counts, colliding-row sets, and both aggregate-jet gcds.  Its
canonical JSON SHA-256 is

```text
de1a906731d27aea2c5b8cd202cdf390f5192f4464ce03ced8397b62c48c888c
```

`derive_complementary.py` reconstructs the global transform in SymPy 1.13.3.
`verify_complementary.py` imports no SymPy code.  It independently rebuilds
all 33 rows from regularized principal parts and tail moments using only
standard-library integer and rational arithmetic, verifies the eliminants
with Sturm sequences, recomputes all colliding-row sets and aggregate gcds,
and checks collision-factor coverage.

The result imports the global weighted ray-chamber formula and the earlier
classification for the \(b<a\) half of (1).  The complementary exclusion is
proved by the reduction above and the exact finite certificate.  No decimal
or floating-point comparison decides a claim.
