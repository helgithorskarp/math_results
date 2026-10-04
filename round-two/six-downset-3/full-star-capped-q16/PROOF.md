# A full capped Hoffman face at q16/k8

**Author: six-downset-3, researcher.** Ordinary proof plus exact finite
certificates; the mathematical bridges below are unformalized, and the
new contribution is independently **UNREVIEWED**. A numerical search was
used only to propose coefficients and factor entries. The standalone
integer checker is independent of that search and the prior affine table.

Let `a,b,c` be distinct core elements, let `X` have16 outside elements,
and let `Z` be any eight-element subset of `X`. Define

\[
\mathcal D=\{A:|A|\le2\}\cup
 \{A:|A|=3,\ |A\cap\{a,b,c\}|\ge2\}
 \setminus\{\{b,c,x\}:x\in Z\}.
\]

In this formula the ground set is `{a,b,c} union X`, and the deletion
applies to the whole union. This is a downset. It has `N=232` members.
The unique maximum star is `S_a`, of size `s=52`; the `b,c` stars have
size 44, outside stars have size 21 on `Z` and 22 on its complement.
The canonical certificate labels `a,b,c` by bits0,1,2 and the two outside
pools by bits3..10 and11..18. Relabeling covers every choice of `X,Z`.

**Theorem.** The rational matrix defined by `CERTIFICATE.json` satisfies
Conjecture H on this original downset, including the actual empty vertex,
and also satisfies the additional spectral cap `M <= I`. Both
`L=180M+52I` and `232I-L` have ordinary rank 231; the unit eigenvalue of
`M` is simple. There is a 20,103-dimensional real box of independent
support-preserving repairs, with each coordinate in
`[-1/10292736,1/10292736]`, for which all these properties persist.
The center is outside the earlier five-parameter sparse repair face.
No other `q,k` or general-downset existence/nonexistence is asserted.

## Original core and the actual empty completion

Write `n=231`, index the proper members first in the core, and put

\[
 E=\begin{bmatrix}-\mathbf1_n^T\\I_n\end{bmatrix},\qquad
 K=232I_n-J_n,\qquad U=K-C.
\]

The actual empty member occupies the first row of the full matrix. Set

\[
 L=J_{232}+ECE^T,\qquad M=(L-52I_{232})/180.
\]

`E` has full column rank, `E^T 1=0`, and its column space is
`1^perp`. Therefore `L1=2321`, and `M1=1`. The proper block of `L` is
`J_n+C`. The certificate gives every proper diagonal entry of `C` as51
and every distinct intersecting entry as-1. Thus every intersecting
entry of `M`, including every proper diagonal, vanishes.

The identity

\[
232I_{232}-J_{232}=E(232I_n-J_n)E^T
\]

holds on **all** positions, including the actual empty row. Consequently
`232I-L=EUE^T`. The orthogonal decomposition
`span(1) direct-sum 1^perp` proves

\[
 L\succeq0\iff C\succeq0,
 \qquad M\preceq I\iff U\succeq0.
\]

This preserves the empty loop; it does not impose a zero empty diagonal.
For the center the checker obtains `M[empty,empty]=37927/92160`.

Let `h` be the characteristic vector of the actual proper `a`-star.
Every H matrix necessarily has `Ch=0`: its full proper star block in `L`
is `52I_52`. For
`u=1_(S_a)-(52/232)1_232`, direct use of `L1=2321` gives `u^T L u=0`.
Positive semidefiniteness forces `Lu=0`. As `E^T u=h`, this gives `ECh=0`,
and the full column rank of `E` gives `Ch=0`. Equivalently, the fixed
proper star block is `52I_52-J_52` and has zero `h` energy. The checker
verifies the complete original centered-star action of `L`, not merely
a fixed quotient.

## Complete original maximum-star repair coordinates

For any finite downset containing `{a}`, let `R` be symmetric, zero on
the proper diagonal and on intersecting pairs, with `Rh=0`. Every such
`R` has the following canonical basis.

For each disjoint pair of non-`a` members take its symmetric unit edge.
For each non-`a` member `A` and disjoint `a`-star member `B != {a}`, take
the symmetric `+1` edge `(A,B)` and `-1` edge `(A,{a})`.
There are no disjoint star/star pairs. Every nonstar member is disjoint
from the anchor `{a}`. Its star-row equation uniquely determines its
anchor entry as the negative sum of its other star entries. Hence the
displayed coordinates span all allowed `R`, and they are independent:
each nonanchor free entry recovers its own unique coefficient.

On the present original carrier there are 20,282 allowed unordered proper
disjoint pairs and 179 nonstar rows. Each row has its own anchor variable,
so the complete repair dimension is `20282-179=20103`. This is an exact
original dimension, not a dimension inferred from a rank quotient.
Each basis matrix has operator norm at most 2: a unit edge has norm 1;
an anchored trade on three distinct vertices has eigenvalues
`0,+sqrt(2),-sqrt(2)`.

The group `S_Z times S_(X\Z)` preserves the domain and the anchor. Its
disjoint-pair orbits are indexed by the two core masks and the two pools'
cardinalities at each endpoint. There are 143 free edge orbits. Averaging
any feasible `C` preserves all affine entries, `Ch=0`, and both PSD
endpoint constraints. Thus the invariant143-parameter search is a
complete symmetry reduction for feasibility on **this** carrier.
The final 20,103-coordinate box is not restricted to invariant repairs.
No numerical failure would prove absence even in the invariant space.

## Literal decoding of the center

For each proper member `A`, put
`o(A)=(A core mask, |A intersect Z|, |A intersect(X\Z)|)`.
There are23 physical member orbits, with masses at most64.
`CERTIFICATE.json` lists every canonical unordered nonanchor disjoint-
pair orbit and its integer numerator over1024. For such a pair `(A,B)`,
use that exact entry. Use51 on the proper diagonal, -1 on intersecting
pairs, and, for each nonstar `A`, use

\[
C[A,\{a\}]= -\sum_{B\in S_a\setminus\{\{a\}\}}C[A,B].
\]

These instructions determine **all 53,361 ordered original core entries**,
including every anchor, without using the old author table or a Schur
decoder. They give a symmetric `C` with `Ch=0`. The upper core is the
literal `U=232I-J-C`. The checker reconstructs all 53,824 full lift
positions and confirms the support, every row sum, both endpoint
identities, all 19 star sizes, and the actual empty centered-star kernel.

## A complete original231-coordinate positivity certificate

The following six orthogonal subspaces exhaust the original proper space.

* `TT`: constant on each physical member orbit, dimension 23.
* `Z`: on each of its eight eligible member orbits use
  `sum_(x in A intersect Z) v_x`, with `sum v_x=0`; dimension `8*7=56`.
* `W`: the analogous nine orbits in the other pool, dimension `9*7=63`.
* `ZZ`, `WW`: functions on the 28 outside pairs within a pool with every
  vertex's incidence sum zero; each has dimension `28-8=20`.
* `ZW`: functions on the8-by-8 mixed outside pairs with row and column
  sums zero, dimension 49.

The `TT` indicators have positive diagonal Gram entries (the orbit
masses). On a standard orbit the seven differences `v=e_0-e_j` have
Gram equal to a positive orbit multiplier times `I_7+J_7`. Thus each
standard block has the stated dimension. Cross-sector orthogonality
follows from these zero sums and the pair-incidence constraints; the
checker also verifies every cross-sector Gram entry directly.

For `ZZ` and `WW` the checker takes the 20 pairs `(i,j)` in `{1,..,7}`
other than `(1,2)` as free edges. For one such pair put weight2 on it,
weight-2 on `(1,2)`, and weight
`-2*1_(t in {i,j})+2*1_(t in {1,2})` on each `(0,t)`.
Each vector has zero incidence, and its own unique free coordinate 2,
proving independence of all 20 vectors. For `ZW` take all 49 rectangles
`(e_0-e_i)(e_0-e_j)^T`. Each has its own unique interior entry 1.
All231 basis vectors are generated and checked literally. There is no
unexamined remainder or assumption about nonfixed positivity.

For both `C` and `U`, the verifier checks **every original row** of the
image of **every basis vector**: `2*231*231=106722` image positions.
The `TT` action is represented by its full23-coordinate Gram matrix.
Each of the seven standard copies uses its full eight- or nine-coordinate
Gram matrix. The20,20,49 pair directions are each verified as scalar
actions. The block Gram matrices are computed by direct sums of original
entries. These literal action identities, the Gram identities and the
complete basis prove that the twelve checked blocks suffice for BOTH
full endpoint matrices. Positive `TT` forms alone would not suffice.

The lower `TT` Gram annihilates its star indicator. Deleting the plain
`{a}` coordinate, whose coefficient in that indicator is1, gives a
22-by-22 positive block. Adding or subtracting a multiple of the star
does not change the lower energy, so this principal block controls all
`TT` directions modulo the known star kernel.

For each of the six matrix blocks the certificate gives a lower-
triangular integer factor `V`, with dyadic denominator `Q=2^32`.
All Gram entries are integers over `D=1024`. The checker computes

\[
F=G-(V/Q)(V/Q)^T
\]

on every position, using the common denominator `Q^2`, and verifies
`F[i,i]-sum_(j!=i)|F[i,j]| >= delta > 0` on every row. Then `F >= delta I`
by `2|x_i x_j| <= x_i^2+x_j^2`, and hence `G >= delta I`.
The six scalar sectors are checked directly. No floating Cholesky
factor or numerical eigenvalue is accepted as a certificate.

To transfer these bounds to the original Euclidean norm, divide each
`delta` by its maximum seed norm. For `TT` that norm is at most64.
For its lower star complement, if `x` is perpendicular to `h`, subtract
the `{a}` coefficient times `h` to obtain a coefficient vector with the
anchor zero. Orthogonal projection back onto `h^perp` does not increase
norm, so the same maximum-orbit-mass bound applies. For standard blocks,
choose an orthonormal zero-sum pool basis; its Gram and energy matrices
are the checked seed matrices scaled by the same factor 1/2. Each pair
seed has norm squared4. The exact residual/scalar comparisons give

\[
C|_{h^\perp}\succeq(1/128)I,\qquad Ch=0,
\qquad U\succeq(1/128)I.
\]

These comparisons and all twelve exact rational bounds are in
`EXPECTED.json`; they are recomputed by the checker.

## Full real repair box, ranks, and the sparse-face separation

Let `R_j`, `1 <= j <= d=20103`, be the complete original basis above.
For arbitrary **independent real** coefficients with

\[
 |t_j|\le\epsilon=1/(512d)=1/10292736,
 \qquad C(t)=C+\sum_jt_jR_j,
\]

the displacement annihilates `h` and has operator norm at most
`2d epsilon=1/256`. Therefore `C(t)` retains exact kernel `span(h)`
and is at least `1/256` on its perpendicular; `U(t)` is at least
`1/256` everywhere. All fixed entries and all original empty-lift
identities persist. This proves the full real box, not just finitely many
sampled parameter choices. Rational coordinates give rational matrices.

At the center and throughout this box, `rank C(t)=230` and `rank U(t)=231`.
Because `E` is injective and `J` has range orthogonal to `E`, this gives
`rank L(t)=231` and `rank(232I-L(t))=231`. The former rank is greatest
possible because the centered maximum star is a nonzero lower kernel;
the latter is greatest possible because the all-ones vector is an upper
kernel. Positivity of `U(t)` makes that upper kernel exactly `span(1)`,
so the unit eigenvalue of `M(t)` is simple. Since `E^TE=I+J >= I`, the
nonzero upper-endpoint eigenvalues are at least `1/256`; hence the
nonunit eigenvalues of `M(t)` are at most `1-1/46080`.

Take the outside singleton `x_0` and the disjoint pair `{x_1,x_2}` in `Z`.
Their center entry is exactly **`-583/1024`**. In the credited original
table at `q=16` this entry is
`q(q-3)/((q-1)(q-2))-1 = -1/105`; the original `Delta` coefficient here
is zero, and the four other sparse repairs do not meet this pair.
Every matrix in the five-parameter sparse face therefore fixes that
entry to `-1/105`. The exact inequality of the two rational entries
proves separation. The earlier no-cap result for that face at `k=8`
and this capped completion in the full space are compatible.

## Sources and trust boundary

The named problem is [Ellis--Filmus--Friedgut, Section4,
Conjecture H](https://arxiv.org/html/2609.28404v1#S4), live checked as
version 1 on 2026-10-04. The original carrier/table is credited to
[the original core-edge-six source](../core-edge-six-cutoff/PROOF.md).
[LEMMA10232's five-repair obstruction](../fifth-repair-obstruction/PROOF.md)
is prior scope context; its proof is not an input to the new endpoint
certificate. The earlier independent low-count review covers its stated
earlier leaf only. No review or positive margin is transferred here.
The separate [noninvariant tensor-face result](../../six-downset-2/noninvariant_tensor_face/PROOF.md)
is a methodological comparison on a different carrier; neither its seed
nor its cube is a premise of this result.

The complete source manifest,143-entry rational matrix, six integer
factors and scalar entries are compact public evidence. The verifier
uses only the standard library and explicit integer arithmetic. Its
soundness still depends on the ordinary linear-algebra arguments above,
the interpreter, and the checker implementation; none is formalized in
a proof assistant. This author certificate has no independent review
verdict and does not settle Conjecture H in general.
