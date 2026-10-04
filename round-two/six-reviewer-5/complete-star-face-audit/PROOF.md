# Complete original coordinates, weighted stability, and the equal-half boundary

Actual author six-reviewer-5, independent mathematical reviewer, 2026-10-04.
This is an ordinary, unformalized proof audit and two proved refinements of
LEMMA10248. The n28 positive seed is an explicit separate premise throughout.

## 1. Original affine converse and actual cap

Let \(\mathcal D\) be a finite downset with at least one nonempty member,
on exactly its active points. Write \(N=|\mathcal D|\), \(s\) for its
largest point-star size, \(h=N-s\), and \(I_*\) for the \(p\) points
with that size. Removing a point injects its star into the complementary
part of the downset, so \(0<s\le N/2\). Every active singleton and the
actual empty vertex belong to \(\mathcal D\). If \(s=1\), the downset
has no higher member. The PSD centered-star equality proved below applies
also to every singleton, forcing \(L=J\) and uniquely
\(M=(J-I)/(N-1)\). This has the required cap. Support and row equations
without PSD or the forced-star equations would not establish uniqueness.

For \(s\ge2\), let \(Q\) remove only the empty vertex and the maximum-star
singletons. Smaller-star singletons remain. Put \(m=N-p-1\),
\(R_{B,i}=1_{i\in B}\), \(r_B=|B\cap I_*|\), and let the original
\(N\)-by-\(m\) matrix \(A\) have rows
\[
A_{\emptyset,B}=r_B-1,\qquad
A_{\{i\},B}=-1_{i\in B}\ (i\in I_*),\qquad
A_{C,B}=1_{C=B}\ (C\in Q).
\]
The identity block proves injectivity; direct column sums give
\(A^T\mathbf1=0\) and \(A^Tw_i=0\) for each maximum-star indicator.
For every real symmetric \(T\) with diagonal \(s-1\) and entry \(-1\)
at distinct intersecting residual sets, define
\[
L=J+ATA^T,\qquad M=(L-sI)/h.
\]
Every individual unordered disjoint pair in \(Q\), including complements,
is free. The row and maximum-star equations follow immediately. A remaining
maximum star has exactly \(s-1\) residual members, all pairwise intersecting.
Their diagonal/off-diagonal sum is \(s-1\). If a residual set contains
the point, its corresponding sum is \((s-1)-(s-2)=1\). These two sums
give the eliminated singleton diagonal and every required singleton support
zero. The identity rows give all other proper support entries. Empty entries
are determined by the displayed original rows, with an allowed empty loop.

Conversely, start with any symmetric supported row-one matrix satisfying
the maximum-star equations, and put \(H=L-J\). The zero row sums express
\(H=ECE^T\), with \(E=[-\mathbf1^T;I]\) and \(C\) its proper block.
Order maximum singletons first. The star equations say
\(C[I_p;R]=0\). Solving the two block equations, with \(T\) the bottom
principal block, gives
\[
C=[-R^T;I]T[-R^T;I]^T.
\]
Thus the preceding parametrization is the entire affine space, and the
residual block \(L[Q,Q]-J\) recovers \(T\) uniquely. For every ordinary
H certificate the star equations are forced: the centered star
\(u_i=w_i-(s/N)\mathbf1\) satisfies
\(u_i^TLu_i=s^2-s^2=0\), and positivity implies \(Lu_i=0\).
This reproves, and credits, the earlier core/star mechanism7578.

The \(u_i\) are independent: their empty coordinate first sets the sum
of coefficients to zero, and the maximum-singleton coordinates then set
each coefficient to zero. For \(U=\operatorname{span}(u_i)\),
\(\operatorname{range}A=(\operatorname{span}(\mathbf1,U))^\perp\).
With \(b_B=1-r_B\), the actual original metric is
\[
G=A^TA=I+RR^T+bb^T.
\]
Consequently \(P_U=I-J/N-AG^{-1}A^T\), and entrywise multiplication gives
\[
NI-L=NP_U+A(NG^{-1}-T)A^T.
\]
The summands act on orthogonal original spaces. Surjectivity of \(A^T\)
on its residual coordinates proves
\[
L\succeq0\iff T\succeq0,\qquad
L\preceq NI\iff T\preceq NG^{-1}.
\]
The ranks are \(1+\operatorname{rank}T\) and
\(p+\operatorname{rank}(NG^{-1}-T)\). The lower kernel is
\(U\oplus AG^{-1}\ker T\); the unit eigenvalue of \(M\) is simple
exactly when the upper residual is positive definite. Replacing the metric
by the identity is false, even when both naive matrices are positive definite.

Our explicit near-cube n4 control takes residual pairs with diagonal3,
intersecting entry-1 and complementary entry15/8. Its \(T\) and
\(11I-T\) are positive definite. Nevertheless, for \(v=A\mathbf1\),
\(v^T(11I-L)v=-117/4\). This independently constructed original-energy
control differs from the author's stated -156 witness.

## 2. Positive saturation and its exact coordinate face

Select any collection \(S\) of distinct whole-ground complementary pairs
with both endpoints in \(Q\). Let \(q=|S|\), remove those endpoints
to form \(V\), and write \(D_S\) for the number of unordered disjoint
pairs in \(V\). For positive-semidefinite \(T\), saturation
\(L_{B,B^c}=s\) gives \(T_{B,B^c}=s-1\). Its equal-diagonal two-by-two
minor puts \(e_B-e_{B^c}\) in \(\ker T\). Every other nonempty
residual member meets an endpoint, so the equal selected columns have
entry-1 everywhere else. Their two endpoint entries are \(s-1\).
Different selected pairs have distinct endpoints and these prescriptions
agree. Conversely the prescribed columns force both saturation and the
difference kernel. The remaining affine variables are exactly the
\(D_S\) individual disjoint pairs in \(V\), without additional row,
star, empty or complementary equations.

This reduction uses PSD; merely imposing saturated entry values in a
general affine matrix is insufficient. The feasible subset is a face:
PSD and diagonal \(s\) bound every selected original entry by \(s\),
and equality of their sum with \(qs\) forces all equalities.
Neither this description nor the coordinate count alone asserts existence.

The selected ORIGINAL columns equal \(s\) on their two endpoints,
zero at every other nonempty vertex, and \(N-2s\) at the empty vertex.
Support, column equality and the original row sum prove each entry.
The forced lower space
\[
K_L=\operatorname{span}(u_i:i\in I_*,\ e_B-e_{B^c}:\{B,B^c\}\in S)
\]
has dimension \(p+q\): empty and maximum-singleton coordinates separate
the star generators, and selected differences have disjoint endpoint
supports. Every unselected complementary difference with both endpoints
in \(Q\) lies outside \(K_L\).

## 3. Proved refinement: arbitrary positive weights

Assume the original seed hypotheses of10248 Section3: exact lower kernel
\(K_L\), simple unit, and both positive endpoint gaps at least
\(0<\epsilon\le N\) in \(L\) units. For any positive real weights
\(w_B\), \(B\in V\), define
\[
\delta_w=\max_{B\in V}\sum_{C\in V:\ C\ne B,\ B\cap C=\emptyset}
                 \frac{w_C}{w_B},\qquad
\gamma=\operatorname{tr}G=\sum_{B\in Q}(r_B^2-r_B+2).
\]
When \(D_S>0\), every real free-coordinate assignment with
\[
|\theta_e|\le\frac{\epsilon}{4\gamma\delta_w}
\]
is capped feasible, has the same exact lower kernel, simple unit and ranks,
and retains both gaps at least \(3\epsilon/4\). The full affine-hull and
relative-interior conclusions hold. For \(D_S=0\) the affine set is a
single point, so a positive radius denominator is unnecessary.

For the proof, on every free edge use
\[
2|x_Bx_C|\le(w_C/w_B)x_B^2+(w_B/w_C)x_C^2.
\]
Summing proves \(\|\Delta T\|\le r\delta_w\) in the ordinary
Euclidean norm. Since \(\|A\|^2=\|G\|\le\gamma\),
\(\|\Delta L\|\le\epsilon/4\). Free perturbations have zero
selected columns and annihilate \(\mathbf1\), every centered maximum
star and every selected original difference. The exact seed kernels
therefore persist and the remaining orthogonal endpoint spaces retain
their positive floors. This covers the entire closed REAL cube, not just
its corners or rational points. Injectivity gives an open neighborhood in
the whole affine coordinate space. An unselected complementary entry
stays strictly below \(s\), since equality would add its difference
to the exact lower kernel. Unit weights recover the author's bound.
Weighted quadratic domination is a standard estimate; the refinement is
its application to this complete original coordinate face.

## 4. Conditional n28 radius more than twice as large

ONLY assume the separate10208 original n28 seed theorem, including its
exact lower kernel, simple unit and \(\epsilon=10^{-8}\). This review
reads that written premise but does not replay or verify its certificate,
its existence, its minimum-class theorem or its harmonic bridge.

For the near cube \(|B|\le26\), select every complementary pair with
smaller size2..8. Then \(V\) consists of all sets of sizes9..19.
Independently counting ordered disjoint pairs by their two sizes, or by
the unused points, gives
\[
D_S=\frac12\sum_{a=9}^{19}\sum_{b=9}^{\min(19,28-a)}
 {28\choose a}{28-a\choose b}=3629809216575.
\]
The other count is
\(\frac12\sum_{c=0}^{10}{28\choose c}
\sum_{a=9}^{28-c-9}{28-c\choose a}\).
Swapping two nonempty disjoint sets has no fixed point. Also
\(q=4791294\), \(\gamma=51271151568\), and the unweighted maximum
degree is354522. These reproduce the target constants without enumerating
the original matrix or its trillions of basis directions.

Choose \(w_B=2^{14-|B|}\). At a set of size \(a\), its exact weighted
row sum is
\[
d_w(a)=\sum_{b=9}^{\min(19,28-a)}{28-a\choose b}2^{a-b}.
\]
For \(a=9,10,\ldots,19\), all eleven values, in that order, are
\[
169870299/1024,\ 41687369/256,\ 9746883/64,\ 2150721/16,
442347/4,\ 83385,\ 56268,\ 32784,\ 15552,\ 5376,\ 1024.
\]
Their maximum is the first. Section3 therefore gives the closed radius
\[
r_w=\frac1{3402127283957218293750000},\qquad
\frac{r_w}{r_{10248}}=\frac{121010176}{56623433}>2.
\]
It retains the same original lower/cap ranks263644105 and268435426,
the same exact kernel, every required strict complement, and the same
\(L\)-gap \(3/400000000\) and \(M\)-gap
\(3/53687090800000000\). It retains all36 invariant orbit directions.
Fixing one representative per unordered size orbit gives the claimed
3629809216539-dimensional slice, every nonzero member of which is
noninvariant. For a size14 complementary edge, the actual empty-loop
slope is \(2(14-1)^2=338\). All these conclusions remain conditional
on the unreplayed n28 seed. Neither weighted degrees nor an affine count
can establish that premise. These weights and radius are not claimed optimal.

## 5. Proved refinement at N=2s, with an explicit nonvacuous seed

When \(N=2s\), selected original columns have zero empty entry. Therefore
each selected pair sum is an \(N\)-eigenvector of \(L\), or a unit
eigenvector of \(M\). Put
\[
K_U=\operatorname{span}(\mathbf1,\ e_B+e_{B^c}:\{B,B^c\}\in S).
\]
It has dimension \(q+1\), since the constant is nonzero at the empty
vertex and the pair supports are disjoint. It is orthogonal to \(K_L\):
a centered star has pair-sum inner product \(1-2s/N=0\), and each
difference is orthogonal to every pair sum and to the constant.

Replace the author's impossible simple-unit premise for \(q>0\) by
an original seed with EXACT lower kernel \(K_L\), EXACT cap kernel
\(K_U\), and both remaining endpoint floors at least \(\epsilon>0\).
Then the entire weighted closed cube of Section3 preserves those exact
kernels, both gaps \(3\epsilon/4\), lower rank \(N-p-q\), cap rank
\(N-q-1\), and unit multiplicity \(q+1\). It has affine dimension
\(D_S\) and the same strict unselected complements. Free perturbations
annihilate every selected sum as well as difference: the original
transpose \(A^T\) sends those sums to their residual sum, whose two
columns in \(\Delta T\) are zero. The same full norm estimate and
orthogonal-kernel argument prove every assertion. This is a conditional
stability theorem, not an all-order existence theorem.

It is nonvacuous with a genuine free coordinate. Take the three-point path
\(\mathcal D=(\emptyset,\{0\},\{1\},\{0,1\},\{2\},\{1,2\})\),
so \(N=6,s=3,p=1\). Select only \(\{0\},\{1,2\}\); the residual
unselected complementary pair is \(\{2\},\{0,1\}\), and \(D_S=1\).
The original seed is
\[
L_0=\begin{pmatrix}
3&0&1&2&0&0\\
0&3&0&0&0&3\\
1&0&3&0&2&0\\
2&0&0&3&1&0\\
0&0&2&1&3&0\\
0&3&0&0&0&3
\end{pmatrix}.
\]
Direct rational Schur checks on the ENTIRE original matrices show
\(\operatorname{rank}L_0=\operatorname{rank}(6I-L_0)=4\) and
\[
L_0\succeq\tfrac12(I-P_{K_L}),\qquad
6I-L_0\succeq\tfrac12(I-P_{K_U}).
\]
The projectors are computed from the original displayed generators using
their actual Gram inverses, not a quotient metric. Here \(\gamma=8\)
and \(\delta=1\), so the full closed one-coordinate real interval
\(|\theta|\le1/64\) preserves both ranks4, both gaps at least3/8 and
unit multiplicity2. Change the unselected \(T\) entry by \(\theta\);
all original support/row/star equations persist. This control demonstrates
the extension; it is not a claim that this elementary path first acquires
an H certificate here.

## 6. Independent finite evidence and boundaries

[check.py](check.py) uses new stdlib integer/Fraction code. It enumerates
every active downset on one through three points (12 literal families),
and adds five specified four-point families. It independently builds all
original symmetric-entry variables, support, row and maximum-star equations.
Exact sparse elimination proves consistency and full affine dimensions;
every individual free decoder direction is checked against those original
equations. The actual Gram matrix, original projector and full cap identity
are checked entrywise. Twenty-seven selected-column faces include multiple
simultaneous pairs and every remaining individual face direction.
The wrong-metric witness and the equal-half seed/floors are exact rational
whole-matrix checks. The n28 arithmetic uses complete closed sums and eleven
weighted rows; the positive seed is never loaded.

Finite coverage validates the independent implementation and illustrates
the proof, without converting these controls into an exhaustive proof of
the universal theorem. Every converse, PSD/kernel argument, norm bound,
equivariance and conditional implication above is an ordinary unformalized
argument. No H/I resolution, all-order cap existence, seed-verdict transfer,
radius optimum, complete boundary classification or historical priority
is asserted.
