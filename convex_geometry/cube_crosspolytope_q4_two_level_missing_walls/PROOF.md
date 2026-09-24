# Complete two-level classification for four active weights

## 1. Setup

For the delta-normalized section

\[
A_v(b,R)=\int_{\mathbb R^N}\delta(v\cdot x-b)
\mathbf1_{\{\sum_i(|x_i|-1)_+\le R\}}\,dx,
\]

put

\[
M=\|v\|_\infty,\qquad
B=\frac{|b|-\|v\|_1}{M}>0,\qquad s=R-B.
\]

Let the four nonzero normalized magnitudes be \(w_i=|v_i|/M\). The global
weighted formula cited in SOURCES.md places every candidate wall among

\[
\omega_{u,J}=B(1/u-1)+\frac2u\sum_{w\in J}w,
\qquad u\notin J.                                      \tag{1}
\]

This note classifies (1) when the active weights take at most two values. Up
to permutation and scaling, the non-diagonal strata are

\[
1^p a^r,\qquad p+r=4,\qquad 0<a<1.                    \tag{2}
\]

Write \(H_d(s;\omega)=(s-\omega)_+^d\) and
\(\lambda=(1-a)/a\).

## 2. Residual-multiplicity obstruction in arbitrary dimension

The following lemma is not restricted to four active coordinates.

**Lemma.** For weights \(1^p a^r\), consider:

- a structural row supplied by a unit weight, with \(k\) other unit weights
  and \(\ell\) weights \(a\) in its tail set; and
- a structural row supplied by a weight \(a\), with \(i\) unit weights and
  \(j\) other weights \(a\) in its tail set.

Their walls and lowest nonzero hinge degrees are respectively

\[
\begin{array}{c|c|c}
&\text{wall}&\text{lowest degree}\\ \hline
1\text{-supplier}&2(k+a\ell)&r+k\\
a\text{-supplier}&\lambda B+2i/a+2j&p+j.
\end{array}                                            \tag{3}
\]

Consequently a cancellation between these two rows requires

\[
\boxed{r+k=p+j}.                                       \tag{4}
\]

**Proof.** After the indicated tails are removed, the pole belonging to the
supplier has residual order \(p-k\) in the first row and \(r-j\) in the
second. The highest-order principal part is unique and has a nonzero
coefficient. Its baseline hinge degree, plus the least degree increase from
each tail operator, is \(r+k\) and \(p+j\), respectively. If these degrees
differ, the lower one cannot be canceled. Equality is (4). The wall shifts
in (3) follow directly from \(2w(1+\lambda_u)\) for each tail weight. ∎

The resonance in (3) has \(B>0\) exactly when

\[
\ell a^2+(k-j)a-i>0.                                  \tag{5}
\]

Since the left side is convex, is nonpositive at \(a=0\), and is considered
on \(0<a<1\), it is positive somewhere precisely when
\(\ell+k-j-i>0\). Thus (4)--(5) leave only 12 candidates in dimension four.

## 3. Exact hinge tables

The tables below give every structural wall. An entry
\([c_1,c_2,c_3]\) denotes
\(\sum_{d=1}^3c_dH_d(s;\omega)\), with omitted leading zeroes written
explicitly where useful. Equal numerical walls are collected coefficient by
coefficient.

For \(1^3a\):

| \(\omega\) | \([c_1,c_2,c_3]\) |
|---|---|
| \(0\) | \(\left[-\frac{B^2}{2a(a-1)},-\frac{B(5a-4)}{2a(a-1)^2},-\frac{15a^2-24a+10}{6a(a-1)^3}\right]\) |
| \(2a\) | \(\left[-\frac{(B+2a)^2}{2a(a+1)},-\frac{(B+2a)(5a+4)}{2a(a+1)^2},-\frac{15a^2+24a+10}{6a(a+1)^3}\right]\) |
| \(2\) | \(\left[0,\frac{3(B+2)}{4a(a-1)},\frac{11a-9}{8a(a-1)^2}\right]\) |
| \(2(1+a)\) | \(\left[0,\frac{3(B+2a+2)}{4a(a+1)},\frac{11a+9}{8a(a+1)^2}\right]\) |
| \(4\) | \(\left[0,0,-\frac1{8a(a-1)}\right]\) |
| \(2(a+2)\) | \(\left[0,0,-\frac1{8a(a+1)}\right]\) |
| \(\lambda B\) | \(\left[0,0,\frac{a^5}{6(a-1)^3}\right]\) |
| \(\lambda B+2/a\) | \(\left[0,0,-\frac{a^5}{2(a-1)^2(a+1)}\right]\) |
| \(\lambda B+4/a\) | \(\left[0,0,\frac{a^5}{2(a-1)(a+1)^2}\right]\) |
| \(\lambda B+6/a\) | \(\left[0,0,-\frac{a^5}{6(a+1)^3}\right]\) |

For \(1^2a^2\):

| \(\omega\) | \([c_2,c_3]\) |
|---|---|
| \(0\) | \(\left[\frac{B}{2a^2(a-1)^2},\frac{3a-2}{3a^2(a-1)^3}\right]\) |
| \(2a\) | \(\left[\frac{B+2a}{a^2(a-1)(a+1)},\frac{2(3a^2-2)}{3a^2(a-1)^2(a+1)^2}\right]\) |
| \(4a\) | \(\left[\frac{B+4a}{2a^2(a+1)^2},\frac{3a+2}{3a^2(a+1)^3}\right]\) |
| \(2\) | \(\left[0,-\frac1{6a^2(a-1)^2}\right]\) |
| \(2(1+a)\) | \(\left[0,-\frac1{3a^2(a-1)(a+1)}\right]\) |
| \(2(1+2a)\) | \(\left[0,-\frac1{6a^2(a+1)^2}\right]\) |
| \(\lambda B\) | \(\left[\frac{Ba^2}{2(a-1)^2},\frac{a^3(2a-3)}{3(a-1)^3}\right]\) |
| \(\lambda B+2\) | \(\left[0,-\frac{a^3}{6(a-1)^2}\right]\) |
| \(\lambda B+2/a\) | \(\left[-\frac{a^2(B+2)}{(a-1)(a+1)},-\frac{2a^3(2a^2-3)}{3(a-1)^2(a+1)^2}\right]\) |
| \(\lambda B+2+2/a\) | \(\left[0,\frac{a^3}{3(a-1)(a+1)}\right]\) |
| \(\lambda B+4/a\) | \(\left[\frac{a^2(B+4)}{2(a+1)^2},\frac{a^3(2a+3)}{3(a+1)^3}\right]\) |
| \(\lambda B+2+4/a\) | \(\left[0,-\frac{a^3}{6(a+1)^2}\right]\) |

For \(1a^3\):

| \(\omega\) | nonzero coefficients |
|---|---|
| \(0,2a,4a,6a\) | \(c_3=-\frac1{6a^3(a-1)^3},-\frac1{2a^3(a-1)^2(a+1)},-\frac1{2a^3(a-1)(a+1)^2},-\frac1{6a^3(a+1)^3}\) |
| \(\lambda B\) | \(c_1=\frac{B^2}{2a(a-1)},\ c_2=\frac{B(4a-5)}{2(a-1)^2},\ c_3=\frac{a(10a^2-24a+15)}{6(a-1)^3}\) |
| \(\lambda B+2\) | \(c_2=-\frac{3(B+2a)}{4(a-1)},\ c_3=-\frac{a(9a-11)}{8(a-1)^2}\) |
| \(\lambda B+4\) | \(c_3=\frac a{8(a-1)}\) |
| \(\lambda B+2/a\) | \(c_1=-\frac{(B+2)^2}{2a(a+1)},\ c_2=-\frac{(B+2)(4a+5)}{2(a+1)^2},\ c_3=-\frac{a(10a^2+24a+15)}{6(a+1)^3}\) |
| \(\lambda B+2+2/a\) | \(c_2=\frac{3(B+2a+2)}{4(a+1)},\ c_3=\frac{a(9a+11)}{8(a+1)^2}\) |
| \(\lambda B+4+2/a\) | \(c_3=-\frac a{8(a+1)}\) |

These are identities in \(\mathbb Q(a,B)\), obtained directly from repeated
principal parts rather than by taking limits of distinct-weight formulas.

## 4. The classification theorem

Let \(a_1,a_2\) be the unique roots in \((0,1)\) of

\[
P_1(a)=4a^6-3a^2+6a-3,\qquad
P_2(a)=a^6+a^5+2a-2.                                  \tag{6}
\]

They have the rational isolations

\[
\frac{663190523}{10^9}<a_1<
\frac{165797631}{250000000},\qquad
\frac{766427599}{10^9}<a_2<
\frac{1916069}{2500000}.                              \tag{7}
\]

Numerically,

\[
a_1=0.663190523044811862\ldots,\qquad
a_2=0.766427599571476336\ldots.                        \tag{8}
\]

**Theorem.** Up to permutation and common scaling, the complete list of
missing positive candidate walls with four active weights taking at most two
distinct values is

\[
\boxed{
\begin{array}{c|c|c}
\text{weights}&B&\text{missing wall}\\ \hline
(1,1,1,a_1)&4a_1/(1-a_1)&4\\
(1,1,1,1/\sqrt2)&2\sqrt2&4\\
(1,1,a_2,a_2)&2a_2^2/(1-a_2)&2(1+a_2).
\end{array}}                                          \tag{9}
\]

There are no missing positive walls for \(1a^3\) or \(1^4\).

**Proof.** Equations (4)--(5) give the following 12 possible cross-family
cancellations. In each row, the listed expression is the numerator factor of
the aggregate coefficient in its lowest common hinge degree; denominators
are nonzero on the admissible interval.

| stratum | \((k,\ell;i,j)\) | admissibility | lowest aggregate factor |
|---|---:|---:|---|
| \(1^3a\) | \((2,0;0,0)\) | all \(a\) | \(P_1\) |
| \(1^3a\) | \((2,0;1,0)\) | \(a>1/2\) | \((2a^2-1)(2a^4+a^2+1)\) |
| \(1^3a\) | \((2,1;0,0)\) | all \(a\) | \(4a^7+4a^6-3a^3+9a^2-9a+3\) |
| \(1^3a\) | \((2,1;1,0)\) | \(a>\sqrt2-1\) | \(4a^6+a^2-2a+1\) |
| \(1^3a\) | \((2,1;2,0)\) | \(a>\sqrt3-1\) | \(4a^6-a^2+1\) |
| \(1^2a^2\) | \((0,1;0,0)\) | all \(a\) | \(P_2\) |
| \(1^2a^2\) | \((0,2;0,0)\) | all \(a\) | \(a^7+2a^6+a^5+a^2-2a+1\) |
| \(1^2a^2\) | \((0,2;1,0)\) | \(a>1/\sqrt2\) | \((2a-1)(2a^6+2a^5-a+1)\) |
| \(1^2a^2\) | \((1,1;0,1)\) | all \(a\) | \(P_2\) |
| \(1^2a^2\) | \((1,2;0,1)\) | all \(a\) | \(a^7+2a^6+a^5+a^2-2a+1\) |
| \(1^2a^2\) | \((1,2;1,1)\) | \(a>1/\sqrt2\) | \(2a^6+2a^5-a+1\) |
| \(1a^3\) | \((0,3;0,2)\) | \(a>2/3\) | \(3a^7+9a^6+9a^5+3a^4-4a+4\) |

Exact Sturm sequences show that every auxiliary polynomial in the last
column has no root in \((0,1)\). The positive factor
\(2a^4+a^2+1\) introduces none, and the admissibility restrictions discard
the root \(a=1/2\) where it occurs.

The first two \(1^3a\) rows yield the first two cases of (9). The corresponding
resonances are

\[
B=\frac{4a}{1-a},\quad\omega=4,
\qquad\text{and}\qquad
B=\frac{4a-2}{1-a},\quad\omega=4.                     \tag{10}
\]

The second equation with \(2a^2-1=0\) simplifies to \(B=2\sqrt2\).

For \(1^2a^2\), the two rows carrying \(P_2\) occur simultaneously at

\[
B=\frac{2a^2}{1-a}.                                   \tag{11}
\]

At \(\omega=2(1+a)\), the only common degree is three, so the row disappears
at \(a=a_2\). At the other collision \(\omega=2a\), the degree-two
coefficient also vanishes, but the degree-three numerator is

\[
Q(a)=2a^8+a^7-4a^6-3a^5+6a^3-6a^2-4a+4.             \tag{12}
\]

Euclidean division gives

\[
Q(a)\equiv2(a^3-1)\pmod {P_2(a)},
\qquad \operatorname{Res}(P_2,Q)=896,                 \tag{13}
\]

so this neighboring wall remains genuine.

It remains to audit internal subset-sum collisions, which the generic
structural-row argument does not separate. There are exactly two in
\(0<a<1\):

- in \(1^2a^2\), at \(a=1/2\), the constant rows \((k,\ell)=(0,2)\) and
  \((1,0)\) meet at wall \(2\); even at the only relevant cross-resonance
  \(B=2\), the collected \(H_2\) coefficient is \(41/9\);
- in \(1a^3\), at \(a=1/2\), moving rows \((i,j)=(0,2)\) and \((1,0)\)
  meet; their collected row retains a nonzero \(H_1\) coefficient
  (for example \(-32/3\) at \(B=2\)).

Finally, at the diagonal \(1^4\), the positive-wall rows are

\[
\begin{array}{c|ccc}
\omega&H_1&H_2&H_3\\ \hline
2&-(B+2)^2&-9(B+2)/2&-49/12\\
4&0&3(B+4)/4&5/4\\
6&0&0&-1/12,
\end{array}                                            \tag{14}
\]

and none can disappear. This exhausts every two-level stratum and proves the
theorem. ∎

## 5. Verification

derive.py constructs and checks the four exact hinge tables in
\(\mathbb Q(a,B)\), enumerates the 12 candidates, isolates the three roots,
checks all auxiliary Sturm counts, and computes (13).

The standard-library verify.py independently reconstructs repeated
principal parts with fractions.Fraction. It checks 282 rational table
instances and 248 exact candidate-aggregate instances, uses rational Sturm
sequences for all root claims, computes the resultant by fraction-free
Bareiss elimination, audits both internal collisions, and compares seven
values against exact three-dimensional polytopes reconstructed from all 81
halfspaces of the original four-dimensional body.
