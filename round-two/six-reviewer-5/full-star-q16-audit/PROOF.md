# Original-coordinate certification and a larger full repair box

Actual author **six-reviewer-5**, independent mathematical reviewer, 2026-10-04.
This is an ordinary, unformalized proof with a fresh integer checker. The
written target proof and its integer certificate were exposed; this is not
a blind audit. No current author checker, expected output, sector program,
optimizer or previous positive seed is used. The historical affine table is
read only as an explicitly credited definition for the separation comparison.

The target is LEMMA10242/0,
`bafkreif2iokscrqctqpmhyqzkjgcqap7qstyi5hbwm73qbxs3m6m6x2jda`,
six-downset-3/researcher. Its verified source commit is
`52ce9643a4eb700056e37c0df6e3ed3736f71808`:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-capped-q16/PROOF.md),
[original certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-capped-q16/CERTIFICATE.json).
The copy of that certificate here is byte-identical, SHA256
`132c164b1e453d93d8d8e2df4d75789b0211cb605e0b80247bc8ec31e7de4feb`.
Its entries and factors are proposed data, independently checked below.

## Scope and conclusion

Let (X) be any set of sixteen points, (Z\subset X) have eight points,
and (a,b,c) be three additional distinct points. On the nineteen-point
ground set put
\[
 D=\{A:|A|\le2\}\cup\{A:|A|=3,|A\cap\{a,b,c\}|\ge2\}
       \setminus\{\{b,c,x\}:x\in Z\}.
\]
The deletion applies to the union. This is a downset with (N=232),
unique maximum (a)-star of size (s=52), other core stars of size44,
and outside stars of sizes21 or22. Retain the actual empty vertex.

The explicitly decoded rational center satisfies original H, including
every intersection zero and every row sum, and the extra cap (M\preceq I).
Both endpoints (L=180M+52I) and (232I-L) have greatest possible rank231.
The unit and minimum eigenvalues of (M) are simple.

In the same complete 20,103 independent original repair coordinates as the
author, **every real coordinate assignment**
\[
 |t_j|\le 1/209664
\]
retains these conclusions and both proper-core margins (1/256).
This is more than49 times the author's radius (1/10292736), with the
same retained margin. All matrices in this enlarged box remain outside
the five-parameter sparse face. This is a sufficient box, not an optimal
radius or a boundary classification. No other (q,k), general H/I,
historical priority or formalization is proved.

## Literal center and actual empty completion

Label the core by bits0,1,2, the deleted pool by3 through10, and the other
pool by11 through18. Independently enumerate all permitted members by
the displayed set definition. For each proper member (A), its type is
\[
 o(A)=(A\cap\{a,b,c\}, |A\cap Z|, |A\cap(X\setminus Z)|).
\]
There are23 types. The certificate gives143 integer numerators over1024
for canonical unordered nonanchor disjoint type pairs. These exhaust
every such pair: two disjoint pairs with the same types are carried to
one another by pool permutations. No coefficient of an omitted pair is
assumed or obtained from a previous table.

Set (C_{AA}=51), (C_{AB}=-1) on distinct intersecting pairs; use the
given rational entries on all nonanchor disjoint pairs. For a nonstar
member (A), determine its anchor entry by
\[
 C_{A,\{a\}}=-\sum_{B\in S_a\setminus\{\{a\}\}} C_{AB}.
\]
This produces a symmetric matrix with (Ch=0), where (h=1_{S_a}).
All53,361 ordered entries and every star-row action are checked literally.
The two pool symmetric groups preserve (C); all747,054 original entries
under their fourteen adjacent-transposition generators are checked too.

With (n=231), use
\[
 E=\begin{bmatrix}-\mathbf1_n^T\\I_n\end{bmatrix},\quad
 U=232I_n-J_n-C,\quad L=J_{232}+ECE^T,\quad M=(L-52I)/180.
\]
Here (E^T\mathbf1=0), (E) is injective, and its range is
the original (mathbf1^\perp). Direct block multiplication gives
\[
 232I_{232}-J_{232}=E(232I_n-J_n)E^T,
 \qquad232I-L=EUE^T.
\]
All53,824 positions of the full lift, every row sum, every intersection
zero, and the complete centered-star action are verified. The actual
empty diagonal is (M_{\emptyset,\emptyset}=37927/92160); it is allowed
by the loop and has not been set to zero. Orthogonality of the ranges
of (J) and (E) proves (L\succeq0\iff C\succeq0); injectivity of
the congruence proves (M\preceq I\iff U\succeq0).

## Complete congruence on all original directions

Our method uses the **entire original basis Gram congruence**, rather than
running the author's sector decoder or comparing against its expected
record. Independently generate231 sparse original vectors:

* 23 indicators of the physical types (TT);
* 56 standard Z vectors: eight eligible types times seven contrasts;
* 63 standard W vectors: nine eligible types times seven contrasts;
* 20 incidence-zero outside-pair vectors in each pool (ZZ, WW);
* 49 mixed-pair rectangles (ZW).

In each standard type use contrasts (e_0-e_j) on its pool. Their complete
Gram is a positive multiplier times (I_7+J_7). In ZZ or WW, use the20
free edges among vertices1 through7 other than edge12: put2 on a free
edge, -2 on12, and the unique compensating values on edges0t making all
vertex incidences zero. Each vector has its own interior free pivot2.
Each mixed rectangle ((e_0-e_i)(e_0-e_j)^T) has its own interior pivot1.
These prove independence within their sectors. All Euclidean cross-sector
Gram entries are zero, so the dimensions sum to231 and exhaust the space.
This is a literal basis argument, not an assumed representation remainder.

Compute both full original matrix images of every vector:106,722 integer
positions. Then compare every entry of the three complete231-by231 Gram
matrices (Euclidean, lower, upper):160,083 entries. Every cross-sector
entry vanishes, and the full standard-copy Grams equal the seed block
times the contrast Gram. Scalar sectors are checked as literal eigenvector
actions on every original row of every vector, with no sampled copy.
Thus positivity on the checked blocks is equivalent to positivity on all
original directions. Hashes of the entire images, matrices, basis and
Grams are compact reproducibility witnesses; the checker recomputes the
full objects and all individual identities before hashing.

For TT lower, remove the plain (a) indicator coordinate, whose coefficient
in (h) is1. The remaining principal22-by22 form is positive definite;
the full form annihilates (h). For TT upper use all23 coordinates; for
the standard sectors use all eight or nine seed coordinates. Six integer
triangular factors (V), denominator (Q=2^{32}), certify the six blocks.
For every block entry independently recompute
\[
 F=G-(V/Q)(V/Q)^T.
\]
Every row satisfies (F_{ii}-\sum_{j\ne i}|F_{ij}|\ge\delta>0).
The elementary inequality (2|x_ix_j|\le x_i^2+x_j^2) gives
(F\succeq\delta I); the factor term is positive semidefinite.
No floating eigenvalue or approximate factor residual is accepted.

Divide each block bound by its largest actual seed squared norm. For
lower TT, if (x\perp h), subtract its anchor coefficient times (h)
to get a coefficient vector with zero anchor, without changing energy.
Projecting it back to (h^\perp) recovers (x) and cannot increase norm.
The maximum remaining type mass is64, so the same metric comparison is
valid. Standard-copy norms and energies use the same positive contrast
Gram; their seed metric is diagonal. For scalar sectors the exact action
directly gives the Rayleigh bound, irrespective of basis nonorthogonality.
All twelve rational comparisons are recomputed in RECORD.json. They give
\[
 C|_{h^\perp}\succeq (1/128)I,\quad Ch=0,
 \qquad U\succeq (1/128)I.
\]
There is no prior positive-seed or complementary-space premise.

## Complete repair coordinates and the sharp Frobenius budget

Let (R) be symmetric, zero on the proper diagonal and intersecting pairs,
with (Rh=0). The free original entries are every disjoint nonanchor
proper pair. A nonstar/nonstar free pair gives a symmetric unit edge;
a nonstar/star free pair gives that edge minus its nonstar-to-anchor
edge. Star/star disjoint pairs do not exist. Each nonstar anchor entry
is uniquely forced by its star-row equation, so these coordinates are
independent and span the entire allowed real repair space.

There are20,282 allowed unordered disjoint pairs,179 nonstar anchor
variables, and hence (d=20103) free coordinates. The checker validates
every basis support, its complete star action and its unique free pivot.
For the nonstar row (A), let (m_A) count its nonanchor disjoint star
neighbours. The complete original histogram is

| (m_A) |15|16|31|33|45|48|
|---|---:|---:|---:|---:|---:|---:|
| number of rows |8|1|32|2|120|16|

Therefore \(\sum_A m_A^2=314850\). If every free coefficient has absolute
value at most (epsilon), each nonanchor free entry has that bound and
each anchor entry has bound (m_A\epsilon). Consequently
\[
 \|R\|_{\rm op}\le\|R\|_F
 \le\sqrt{2(d+\sum_A m_A^2)}\,\epsilon
 =\sqrt{669906}\,\epsilon<819\epsilon.
\]
The exact integer enclosure is (818^2<669906<819^2). The **Frobenius
bound is sharp**: assigning every free coordinate (+epsilon) simultaneously
makes every anchor entry (-m_A\epsilon), so equality holds in its squared
bound. This does not claim sharpness of the operator bound or feasible radius.

Take (epsilon=1/(256\cdot819)=1/209664). The perturbation kills (h)
and has norm at most (1/256). Both endpoint cores retain margin at
least (1/256), with exactly the same kernels. The radius enlargement
factor is exactly (13402/273>49). This covers every independent REAL
assignment in the closed box; no finite test replaces that quantifier.

## Original ranks, both spectral gaps, and whole-box separation

Throughout the enlarged box, (\ker C=\operatorname{span}(h)) and (U)
is positive definite. Thus the original lower kernel is the centered
maximum star, and the original upper kernel is exactly (operatorname{span}(1)).
Both ranks are231. Every original H competitor has the centered maximum
star in its lower kernel: its size52 principal star block is (52I),
so its centered indicator has zero lower energy and PSD forces its
annihilation. Every capped competitor has the constant upper kernel.
These bounds prove greatest possible ranks without restricting competitors
to the repair box.

Since (E^TE=I+J\succeq I), congruence preserves a lower bound (1/256)
on **nonzero** eigenvalues of (ECE^T) and (EUE^T). For the singular
lower core this follows by restricting to (h^\perp): if (Q_h) is an
orthonormal basis there, the smallest singular value of (EQ_h) is at
least1. The nonzero singular congruence spectrum is therefore bounded
by the same margin. (J)'s independent eigenvalue is232. It follows that
both extreme eigenvalues of (M), (-13/45) and1, are simple, and its
remaining230 eigenvalues lie in
\[
 [-13/45+1/46080,\ 1-1/46080].
\]
This two-endpoint conclusion retains the actual original metric.

Use an outside singleton (x_0\in Z) and the disjoint pair
\(\{x_1,x_2\}\subset Z\). Its center entry is (-583/1024). The credited
[historical affine definition](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/literal.py)
has base (q(q-3)/((q-1)(q-2))) and zero Delta slope at this singleton/pair.
At (q=16), subtracting1 gives (-1/105). The three plain-core repairs
and the singleton-to-bc repair do not touch this pair. Thus every real
matrix in the five-parameter sparse face fixes this entry to (-1/105),
without any assumption about that face's feasibility.

Our entry has its own unit-edge coordinate, so every enlarged-box matrix
differs from that face at this entry by at least
\[
 60191/107520-1/209664=335347/599040>1/2.
\]
This proves separation for the **whole box**, independently of the prior
five-face impossibility theorem. In original off-diagonal (M) units
divide the displayed entry gap by180. The sparse obstruction and this
positive full-space result have different domains and are compatible.

Every choice of (Z\subset X) of size8 is carried to the canonical pools
by a permutation fixing the three core points. Permutation congruence
transports every matrix entry, basis coordinate, support equation,
endpoint bound, rank and separation statement. This ordinary bijection
proves the full relabeling quantifier; no incomplete deletion-set search
is used. All bridges here remain unformalized.
