# A sharp simultaneous Frobenius budget for covered residual coordinates

Actual **six-reviewer-1 / independent mathematical reviewer**, 2026-10-04.
Ordinary proved refinement, unformalized. All seed-dependent feasibility
conclusions are conditional. The independent coordinate/cap audit and
definitions are in [REVIEW.md](REVIEW.md).

## General covered-residual proposition

Use the complete maximum-star coordinates L=J+ATA' for a finite downset
and the positive-saturated residual family V. Impose the additional
condition
\[
 r_B=|B\cap I_*|\ge1\quad\hbox{for every }B\in V.
\]
Let A_V retain those columns, and let H_V be the symmetric adjacency
matrix of ALL unordered disjoint pairs in V, with zero diagonal.
Put
\[
 P=A_VH_VA_V',\qquad B_*=\|P\|_F^2.
\]
For any real simultaneous parameters |\theta_e|<=r on every free pair,
let DeltaT have those symmetric entries and zero elsewhere.
Then
\[
 \|A\Delta T A'\|^2\le\|A\Delta T A'\|_F^2
     \le r^2 B_*.
\]
The second bound is SHARP as a simultaneous Frobenius box bound,
because all \theta_e=r gives DeltaL=rP and equality.
This does not assert equality of the operator and Frobenius norms.

**Proof.** Let D flip the original rows corresponding to eliminated
maximum-star singletons and leave all other original rows fixed.
Every entry of DA_V is nonnegative: its empty row is r_B-1>=0,
its flipped singleton rows are incidences, and its Q rows are identity.
For a free pair e={B,C}, its symmetric elementary lifted matrix becomes
\[
 (DA_B)(DA_C)' +(DA_C)(DA_B)'
\]
after the row flip on both sides, so it is entrywise nonnegative.
The sum of these elementary matrices is DPD.
Thus EVERY real simultaneous assignment obeys
|D DeltaL D|<=rDPD entrywise. Squaring and summing all original positions,
and using orthogonality of D, proves the Frobenius inequality.
The all-plus assignment proves sharpness. This is a full box argument,
not a sum of separate one-coordinate estimates.

If the face has no free pair, there is no perturbation and no positive
radius is required. Otherwise B_*>0: P's V-by-V block contains H_V.
Let c=ceil(sqrt B_*). With the exact seed K, simple constant eigenvalue N,
and common positive original floor epsilon of the audited theorem,
\[
 |\theta_e|\le \frac{\epsilon}{4c}
\]
gives ||DeltaL||<=epsilon/4. DeltaL kills the constant, every centered
maximum star and every selected original pair difference because its
selected T columns are zero. On K perpendicular the lower floor becomes
at least3epsilon/4. On1 perpendicular the cap floor also becomes
at least3epsilon/4. Therefore the full lower kernel is still exactly K,
both ranks are unchanged and the unit M eigenvalue is simple.
The complete real cube has the entire original face dimension and
contains an open relative neighbourhood of the seed.
No seed is produced by this argument.

If some r_B=0 the displayed nonnegative-column proof fails at its empty
entry. This hypothesis is sufficient, not claimed necessary for every
possible sharp budget. It is not part of the universal coordinate
description. No q16 refinement or margin transport is asserted here.

## Exact near-cube budget by all original entry types

For an n-point near cube, I*=[n]. Suppose V comprises exactly the layers
of sizes l..u, with2<=l<=u<=n-2. All its lifted empty entries are positive.
Use the convention C(t,j)=0 outside0<=j<=t. For a in[l,u] define
\[
 f_a=\sum_{b=l}^u {n-a-1\choose b-1},\qquad
 h_a=\sum_{b=l}^u(b-1){n-a\choose b}.
\]
They count, respectively, disjoint neighbours containing a specified
point outside B and their weighted empty entries.
Put
\[
 U=\sum_a {n-2\choose a-1}f_a,\quad
 V_0=\sum_a {n-1\choose a}(a-1)f_a,\quad
 W=\sum_a {n\choose a}(a-1)h_a,
\]
and
\[
 D_*=\tfrac12\sum_a\sum_b {n\choose a}{n-a\choose b}.
\]
The symbol V_0 is a scalar and is distinct from the residual family V.

The following list exhausts every ORIGINAL position of P=A_VH_VA_V':

* empty/empty: W;
* empty/singleton i and its transpose: -V_0;
* distinct singleton i,j: U; singleton diagonals:0;
* empty/B and its transpose, B in V of size a: h_a;
* singleton i/B and its transpose: -f_a if i is outside B, and0 otherwise;
* V/V:1 on disjoint distinct pairs,0 otherwise;
* any other Q row or column:0.

For example the singleton i,j entry chooses B containing i and not j,
then a disjoint C containing j. The count is
C(n-2,a-1)f_a, summed over a. The empty/singleton entry chooses B
avoiding i, weights its empty coefficient a-1, then chooses C containing
i; this gives V_0. The empty/empty entry sums the products
(a-1)(b-1) over all ORDERED disjoint pairs. V-by-V is H_V itself
because those original rows are identity. Rows outside the retained
columns, empty and original singleton rows are identically zero.
These derivations include both transposed positions and the actual empty
loop; they do not substitute a size quotient for the Euclidean norm.

Squaring all original entries consequently gives the exact integer
\[
\begin{split}
 B_*={}&W^2+2nV_0^2+n(n-1)U^2\\
 &+2\sum_a{n\choose a}h_a^2
   +2\sum_a{n\choose a}(n-a)f_a^2+2D_*.
\end{split}
\]
The complete entry-type formula is independently checked by literal
original endpoint outer products at n4..9. The proof covers all n and
all REAL coordinate assignments satisfying the stated hypotheses.

## Conditional n28 refinement

Take n=28, l=9, u=19, with all smaller-size2..8 complementary pairs
selected. The explicit seed hypothesis is precisely10208's
K of dimension28+4791294, simple constant eigenvalue, and common
epsilon=1/100000000 original lower/upper floor. The seed is neither
replayed nor independently reviewed in this capsule.

The independently computed scalars are
\[
 D_*=3629809216575,\quad
 U=1023748756500,\quad V_0=24958988471400,\quad
 W=631008912917550.
\]
As a second calculation, count ordered disjoint pairs with sizes a,b
by C(28,a)C(28-a,b). Their moments ab, (a-1)b, and (a-1)(b-1)
give28*27U,28V_0, and W. A separate unused-point count gives
\[
 2D_*=\sum_{c=0}^{10}{28\choose c}
             \sum_{a=9}^{28-c-9}{28-c\choose a}.
\]
It agrees with the ordered-size count. No n28 subset enumeration is used.

The six contributions to B_*, in the displayed order, are
\[
\begin{gathered}
398172248181388199253098002500,\quad
34885261908866774082605760000,\quad
792334506425083996941000000,\\
238063758594678568200,\quad
15659562138253983600,\quad7259618433150.
\end{gathered}
\]
Thus
\[
 B_*=433849844850403385325195747450,\qquad
 c=658672790428149.
\]
Integer arithmetic certifies (c-1)^2<B_*<=c^2; no floating square root
or rounded eigenvalue is used. The old payment was
gamma delta=51271151568*354522=18176751196190496.
The strict integer comparisons
\[
 27c<18176751196190496<28c
\]
prove the sufficient-radius improvement is greater than27 and less than28.
The new cube is
\[
 |\theta_e|\le
 \frac1{263469116171259600000000}
\]
on ALL3629809216575 individual free coordinates. Conditional on10208 it
keeps original lower rank263644105, cap rank268435426, exact K,
simple unit and both L floors3/400000000. In M units both nonzero
endpoint floors are3/53687090800000000.
Every unselected complementary pair remains strict. The36-dimensional
invariant subspace and representative-zero noninvariant slice of
dimension3629809216539 are as in the audited theorem; the same new
cube applies to that slice.

The Frobenius constant is an exact attained maximum over the full
parameter box. The spectral/payment radius is only sufficient and
can be conservative. No general seed existence, global H/I solution,
optimal feasible box or n28 seed verdict follows.
