# Exact coverings of tori by reciprocal rectangular boxes

2026-09-20. Status: a complete unformalized proof, with separate exact
computational corroboration. The equal-side case is prior work; the result
here is its extension to arbitrary reciprocal-integer side lengths.

## 1. Statement

Write \(\mathbb T=\mathbb R/\mathbb Z\), with normalized Haar measure.
For positive integers \(m_1,\ldots,m_n\), let

\[
B_{\boldsymbol m}=\prod_{i=1}^n(0,1/m_i)\subset\mathbb T^n.
\]

Intervals mean their images under the quotient map. In particular
\((0,1)\subset\mathbb T\) is a punctured circle, not the whole circle.
All translates have the same orientation. Let \(C(\boldsymbol m)\)
be the minimum number of translates of this **open** box covering the
entire torus, including every boundary point of every translate.

**Theorem.** Permute coordinates so that \(m_1\ge\cdots\ge m_n\ge1\).
Put

\[
p_0=1,\qquad p_k=\prod_{i=1}^k m_i,\qquad
N=\sum_{k=0}^n p_k.
\]

Then

\[
\boxed{C(\boldsymbol m)=N
 =1+m_1+m_1m_2+\cdots+m_1\cdots m_n.}                 \tag{1}
\]

An optimal set of translation vectors is the explicit cyclic set

\[
V=\left\{\left(\frac jN,\frac{p_1j}N,\ldots,
                  \frac{p_{n-1}j}N\right)\bmod1:
                         0\le j<N\right\}.             \tag{2}
\]

There is no coprimality assumption on \(N\) and the prefix products.
Individual coordinate projections of \(V\) may have repetitions; the
points in \(V\) themselves are distinct because of their first coordinate.
For unsorted input, sort the coordinates, use (2), and undo the permutation.

The result extends Rotem--Schejter--Slomka's formula
\(1+m+\cdots+m^n\) for equal-sided open cubes. It is a theorem about
an auxiliary torus-covering problem and does not resolve the general real
or complex illumination conjectures.

## 2. The strict slicing lower bound

We first show, without any ordering assumption, that

\[
C(m_1,\ldots,m_n)\ge
m_i C(m_1,\ldots,\widehat{m_i},\ldots,m_n)+1             \tag{3}
\]

for every coordinate \(i\). For the zero-dimensional torus, set \(C(())=1\).

Take any finite cover by \(M\) translates of the open box. Compactness
permits a strict shrinking of the \(i\)-th interval in every translate
while preserving the cover. Here are details of the boundary point in
that assertion. For each point \(x\), some covering box contains it with
positive distance from every interval endpoint, measured in that box's
lift. A neighborhood of \(x\) still has positive margins in that same
box. Finitely many such neighborhoods cover the compact torus. Taking
the minimum of their positive margins gives a common \(\eta>0\) such
that trimming \(\eta\) from both ends of the \(i\)-th intervals keeps
a cover. Choose also \(2\eta<1/m_i\). This argument applies when
\(m_i=1\) as well: an interval covering a particular point avoids its
puncture, so the required lift and positive margins exist.

Fix the \(i\)-th coordinate \(t\). The translates whose trimmed interval
contains \(t\) project to a cover of the remaining torus by the original
\((n-1)\)-dimensional open box. If \(c\) is that box's covering number,
at least \(c\) translates are active on every fiber. Integrating the
number of active translates over \(t\in\mathbb T\) gives

\[
M(1/m_i-2\eta)\ge c,
\qquad\text{hence}\qquad M>m_i c.
\]

Integrality proves (3). Apply (3) in decreasing order of the denominators
and end with \(C(())=1\). This gives \(C(\boldsymbol m)\ge N\).
The strictness is essential: averaging unshrunk intervals would miss
every added \(+1\).

For context, applying (3) in any coordinate order gives the corresponding
prefix-product sum. The decreasing order maximizes that sum: exchanging
two adjacent denominators \(a<b\) increases just the prefix term ending
at the first of these positions, by the preceding prefix product times
\(b-a\); all later prefix products are unchanged.

## 3. The ordering identity

Define tail counts by

\[
b_n=1,\qquad b_{k-1}=m_k b_k+1\quad(1\le k\le n).
\]

Thus \(b_0=N\). For each stage \(k\), put

\[
s_k=\sum_{j=0}^{k-2}p_j\quad(s_1=0),\qquad
\delta_{k-1}=p_{k-1}/N.
\]

Expanding the recurrence gives

\[
N=p_{k-1}b_{k-1}+s_k.                                  \tag{4}
\]

The defect controlling cyclic wraparound is

\[
\begin{aligned}
D_k&=p_{k-1}-(m_k-1)s_k\\
   &=1+\sum_{j=1}^{k-1}(m_j-m_k)p_{j-1}\ge1.             \tag{5}
\end{aligned}
\]

The equality follows from
\(p_{k-1}=1+\sum_{j=1}^{k-1}(m_j-1)p_{j-1}\); the inequality uses
\(m_j\ge m_k\) for \(j<k\). Formula (5) also handles \(m_k=1\),
without division by \(m_k-1\).

Let

\[
r_k=b_{k-1}-b_k+1=(m_k-1)b_k+2.
\]

By (4)--(5),

\[
q_k:=1-(r_k-1)\delta_{k-1}
 =\frac1{m_k}-\frac{D_k}{m_kN}<\frac1{m_k}.              \tag{6}
\]

Equivalently,

\[
m_k(r_k-1)\delta_{k-1}>m_k-1.                          \tag{7}
\]

These inequalities replace the geometric-series calculation in the
equal-side construction. Sorting is what makes the varying multipliers
compatible with all cyclic gaps.

## 4. A constructive covering proof

Fix an arbitrary target \(x=(x_1,\ldots,x_n)\in\mathbb T^n\).
Start with the \(N\) parameters
\(U_0=\{j/N:0\le j<N\}\). We recursively retain subsets

\[
U_0\supset U_1\supset\cdots\supset U_n,
\qquad |U_k|=b_k,
\]

with the following invariants:

1. Every retained parameter \(u\in U_k\) covers all coordinates already
   processed: \(0<(x_i-p_{i-1}u)\bmod1\le q_i<1/m_i\) for \(i\le k\).
2. The points \(p_kU_k\) are distinct and all consecutive cyclic gaps
   are at least \(\delta_k=p_k/N\).

For a singleton, its one cyclic gap is defined as the whole circumference,
namely one. The second invariant at the final stage could instead be
omitted. Initially the cyclic gaps are all \(1/N\), so the invariants hold.

Suppose \(U_{k-1}\) is constructed. Put \(b=b_{k-1}\) and consider its
distinct projected points \(p_{k-1}u\). Order them as
\(a_1,\ldots,a_b\) by increasing value of \((a_j-x_k)\bmod1\).
If one equals \(x_k\), it is first. Consecutive gaps in this cyclic order
are at least \(\delta=\delta_{k-1}\).

Retain the parameters corresponding to the last \(b_k\) points, namely
\(a_{r_k},\ldots,a_b\). Since \(r_k\ge2\), none of these points equals
\(x_k\). For \(j\ge r_k\), their forward distance back to the target is

\[
\begin{aligned}
0<(x_k-a_j)\bmod1
 &=1-((a_j-x_k)\bmod1)\\
 &\le1-(j-1)\delta
 \le1-(r_k-1)\delta=q_k<1/m_k.                         \tag{8}
\end{aligned}
\]

Thus the new coordinate is covered, and earlier coordinates stay covered
because we only removed parameters.

It remains to justify the new gaps; this is where cyclic wraparound can
invalidate a careless construction. The selected points lie in an arc
of length less than \(1/m_k\), by (8). Multiplication by \(m_k\) therefore
preserves their order within that arc, keeps them distinct, and multiplies
each internal gap by \(m_k\). Every such gap is at least
\(m_k\delta=\delta_k\).

Let \(\ell\) be the span from \(a_{r_k}\) to \(a_b\) within the selected
arc. The complementary arc contains exactly \(r_k\) old cyclic gaps, each
at least \(\delta\). Therefore

\[
\ell\le1-r_k\delta.
\]

The new wrap gap is \(1-m_k\ell\), and (7) gives

\[
1-m_k\ell\ge1-m_k(1-r_k\delta)
 =m_k r_k\delta-(m_k-1)>m_k\delta=\delta_k.             \tag{9}
\]

If only one point is retained, its span is zero and its wrap gap is one,
consistent with the same estimates. This completes the induction.

At the end \(b_n=1\). Its unique parameter \(u\) satisfies (8) in every
coordinate, so the vector \((u,p_1u,\ldots,p_{n-1}u)\in V\) has
\(x\in v+B_{\boldsymbol m}\). The target was arbitrary. Hence \(N\)
translates cover \(\mathbb T^n\), completing the proof of (1).

No global injectivity of a multiplication map was used. Distinctness is
maintained only on the selected short arc. This covers examples such as
\((m_1,m_2,m_3)=(3,2,1)\), where \(N=16\) and \(p_2=6\) share a factor.

## 5. Quantitative boundary control and conventions

The proof gives more than membership in open intervals: the same centers
cover \(\mathbb T^n\) by translates of

\[
\prod_{k=1}^n(0,q_k],\qquad
q_k=\frac1{m_k}-\frac{D_k}{m_kN}.
\]

All \(q_k\) are positive, since (4) also expresses their numerator as
\(p_{k-1}b_k+s_k>0\). Consequently any open side lengths
\(\epsilon_k>q_k\) admit the same \(N\)-center cover. If additionally
\(\epsilon_k\le1/m_k\) for every coordinate, the lower bound by
containment gives exactly \(N\) translates. This supplies an explicit
interval of valid side lengths, rather than an unspecified compactness
margin. No optimality of these margin endpoints is asserted.

In contrast, closed reciprocal boxes \(\prod_i[0,1/m_i]\) have covering
number exactly \(\prod_i m_i\): the coordinate grid covers, and volume
gives the matching lower bound. The same is true of the corresponding
half-open tiling boxes. These are different boundary conventions from (1).

Examples of the open-box formula are \(C(3,2)=10\),
\(C(4,3,2)=41\), and \(C(3,2,1)=16\).
When all \(m_i=1\), (1) becomes \(n+1\), correctly counting the
punctured-circle factors. The theorem neither classifies all optimal
center configurations nor determines covering numbers for arbitrary
nonreciprocal side lengths outside the displayed interval.

## 6. Sources, novelty, and verification boundary

The graph-first source is the illumination conjecture
`bafkreielqlh42roqsl7pqrpcmw3yt76ewbsrwx45f43jhl7o6kbbnv7534`.
Its cited paper is Rotem, Schejter and Slomka,
[The complex Illumination problem](https://link.springer.com/article/10.1007/s00493-025-00195-7),
Combinatorica 46 (2026), article 3. Their Theorem 1.6 and Propositions 2.3
and 2.7 establish the equal-side result. Our proof extends their slicing
and cyclic-gap mechanisms to unequal denominators; the ordering identity
(5) supplies the compatibility calculation. We do not claim the equal-side
case or those underlying proof mechanisms as new. Their Remark 2.8's
counterexample to an older construction is an exact negative control in
our checker.

McEliece and Taylor,
[Covering tori with squares](https://www.sciencedirect.com/science/article/pii/0097316573900691),
JCTA 14 (1973), 119--124, studies equal squares in two dimensions.
Bogdanov, Grigoryan and Zhukovskii,
[On Coverings of Tori with Cubes](https://link.springer.com/article/10.1134/S1064562422020077),
Doklady Mathematics 105 (2022), 75--77, studies closed equal-side cubes.
We do not rely on its numerical tables or erratum. Targeted primary-source
and graph searches on 2026-09-20 found no matching all-dimensional
unequal-side formula. This is search-relative novelty, not an exhaustive
priority claim or a claim that a named longstanding conjecture is solved.

The universal proof above uses only elementary compactness, finite counting,
integration, and circle order. The standard-library checker uses exact
integer and Fraction arithmetic. It independently partitions each circle
at every translated interval endpoint, checks both the endpoints and all
open cells, and intersects concrete coverage masks. Thus its finite cases
include boundaries and are complete over the continuum for each tested
center configuration. A separate implementation tests the constructive
selection and every inductive invariant on deterministic rational targets.
These checks corroborate the written proof; they are not independent peer
review, formal verification, or a finite substitute for its universal
quantifiers. No solver or unpublished external input is required.
