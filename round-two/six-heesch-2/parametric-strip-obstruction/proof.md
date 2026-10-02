# An explicit domain inclusion would bound T_k by three

six-heesch-2, researcher. Author-checked ordinary argument and exact finite
certificates; unformalized and independently unreviewed. No priority claim.

## Shape and statement

Axial unit-hex cells have neighbor steps (1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1).
For k >= 6 define

\[
T_k=\{(0,0),(-2k,k-1),(-2k-1,k)\}\cup
\bigcup_{r=0}^{k-1}\{(-2r-1,r+1),(-2r-1,r+2),
                         (-2r-2,r+1),(-2r-2,r+2)\}.
\]

Use u=x+2y, v=y. The six columns are
u=-2:v=k-1; u=-1:v=k; u=0:0<=v<=k; u=1:1<=v<=k;
u=2 and3:2<=v<=k+1. Thus the area is4k+3. The columns0/1 connect along
neighbor steps (1,0) and(1,1); columns2/3 attach to these, as do the two
terminal cells. Hence T_k is connected. In every horizontal v-row its filled
u-values form an interval except for the missing cell(-1,k-1) between -2 and0.
Every other missing cell escapes horizontally to infinity. The exceptional
cell steps to(-2,k-2) and then escapes horizontally. Thus there is no finite
component of missing cells, and no hole in the regular-cell polyhex.

Write a pose as (M;a,b), meaning (u,v) maps to M(u,v)+(a,b). The literal
30-pose atlas A3(k) is the following table. Each row gives all its translations.

| M | translations (a,b) |
|---|---|
| [[1,0],[0,1]] | (-6,k-3), (6,3-k) |
| [[1,-3],[1,-2]] | (3k-1,3k+1), (3k+5,3k+2), (3k+5,3k+3) |
| [[-1,0],[0,-1]] | (-4,2k-1), (-3,2k-2), (-1,k-2), (-1,k-1), (5,2k+3), (8,2k+3) |
| [[-2,3],[-1,1]] | (-3k-5,-2), (-3k+1,2), (-3k+4,3) |
| [[2,-3],[1,-2]] | (3k,3k+1), (3k+3,3k+2) |
| [[1,0],[1,-1]] | (-4,k-3), (-4,k-2), (4,k+1), (4,k+2) |
| [[-1,3],[0,1]] | (-3k-4,-2), (-3k-4,-1), (-3k-1,1), (-3k+2,2) |
| [[-1,0],[-1,1]] | (1,-k), (1,k+1), (4,2-k), (4,k+2), (7,3), (7,4) |

Put M0=([[-1,0],[-1,1]];-5,-2). Its inverse is the same linear matrix
with translation(-5,-3). Define A2(k)=A3(k) union {M0,M0^-1}.
The input JSON is exactly this atlas, in a fixed order. It is a definition,
not an inferred classification of all possible contacts.

Let E0(T_k) be all disjoint registered contacts with the root. Define
E_(r+1) as the contacts g in E_r for which the fixed union T_k,g(T_k)
has a disjoint whole-copy halo cover whose every contacting pair has
relative pose in E_r. Holes are allowed in this local test. Hc requires
every corona prefix to be a disc; Hh allows holes only at the final prefix.

**Conditional proposition.** For each k >= 6, if E2(T_k) subset A2(k),
then Hc(T_k)<=Hh(T_k)<=3, and T_k does not tile the plane. The hypothesis
has not been proved here for all k.

## Exact affine geometry and the finite reduction

The [column lemma](STRIP_COLUMN_LEMMA.md) gives an ordinary all-k proof of
the six-column representation. Conjugating D6 into (u,v) coordinates gives
four matrices with beta=0 and eight with beta=+/-3. A nonparallel copy meets
at most10 root cells, or18 closed-halo cells. This also proves frame uniqueness
for k>=2: an automorphism with beta nonzero cannot preserve4k+3>10 cells.
For beta=0, a u-reversing matrix would send a singleton end column to the
k-cell column3, impossible for k>=2. The remaining reflection preserves u;
its two singleton columns would require the contradictory shifts b=2k and
b=2k+1. An identity-linear-part translation preserves the finite columns
only when its translation is zero. Thus there is no nontrivial stabilizer.

All translations and demanded points below are affine integer functions of k.
Membership in an image column is a conjunction of affine equality and interval
inequalities. For intersection of two copies, reduce to a relative pose
u'=alpha*u+beta*v+a, v'=gamma*u+delta*v+b. For source column c and target
column d, if beta=0, column equality and interval overlap are linear conditions.
If beta!=0, put B=abs(beta)=3 and n=sign(beta)*(d-alpha*c-a). The intersection
condition is exactly

\[
n\equiv0\pmod B,\quad B l_c\le n\le B h_c,\quad
B l_d\le B(\gamma c+b)+\delta n\le B h_d.
\]

Take the disjunction over the36 column pairs. Touching is obtained by testing
the six neighbor translates. Relative-pose atlas membership is a finite
disjunction of affine equalities. A conflict is overlap, or touching with a
relative pose outside the stipulated atlas. Both directions are tested.
These formulas are implemented in strip_parametric_geometry.py.

For an atom A*k+B>=0 with A>0, its truth changes at ceil(-B/A). For A<0,
it changes after floor(-B/A). An equality with A nonzero can hold only at its
integer root, so split at that root and the next integer. Congruences modulo3
are constant on residue classes modulo3. Therefore finitely many cuts and
residue representatives determine the truth of every formula for all k>=6.
In this atlas the congruences simplify to constants, so period is one.

The root calculation has135 distinct nonconstant atoms and cuts6,7,8:
the ranges are {6},{7},[8,infinity). The pair calculation has181 atoms and
cuts6,7,8,9,10: the last range is[10,infinity). The readers independently
derive these cuts and evaluate every representative, and materialized cell
sets audit each representative's incidence and conflict matrices.

## The two unconditional geometric obstructions

A complete A3-compatible root surround must cover these seven open-halo cells:

\[
(-4,k-2),(-3,k-1),(-1,k-1),(-2,k),(3,k+2),(4,k+2),(1,0).
\]

For each of the three ranges compute the supplier incidence and pair conflicts
among the30 poses. Union the suppliers and eligible poses across ranges,
and intersect the conflict sets. This produces a conservative relaxation:
every actual cover at every k>=6 is a cover in that single finite problem.
A seven-node exhaustive rejection DAG excludes even this relaxation.
Thus no mutually A3-compatible root surround exists for any k>=6.

For the fixed union T_k,M0(T_k), the only possible A2-compatible suppliers
come from A2(k) union M0*A2(k), giving58 distinct affine poses. Filter overlap
with either fixed copy and any forbidden contact with a fixed copy. The eight
demanded cells are

\[
(-8,k-3),(-5,k-1),(-4,k-2),(-2,k),(3,k+2),(4,k+2),(-7,-3),(-1,-1).
\]

The five parameter ranges again give a conservative supplier union and
conflict intersection. An eight-node DAG rejects the relaxation. Hence the
fixed pair has no mutually A2-compatible halo cover for any k>=6. Covariance
under the isometry M0 gives the identical conclusion for M0^-1.

Each DAG node has an available-pose mask, a nonempty remaining-demand mask,
and a remaining demand on which to split. The reader checks **every** supplier
of that demand. Selecting it removes its covered demands and incompatible
poses; the resulting state must have been certified. A state with no supplier
is a leaf. Every child has fewer remaining demands, and the root must be
certified. Thus the 7+8 nodes certify finite exhaustive rejection, rather
than merely reporting a failed heuristic search. Each reader rejects a
missing breakpoint, a changed relaxed matrix and a missing DAG leaf.

## Conditional implication for coronas

Assume E2(T_k) subset A2(k). The pair obstruction excludes M0 and its inverse
from E3. Since E3 subset E2, this gives E3(T_k) subset A3(k).

By the published [hex registration and pair-depth argument](../proof.md),
every contacting pair whose two levels are <=H-r in an H-corona patch belongs
to E_r. In a four-corona patch, the root and its first neighbors have levels
at most1, so their root contacts and mutual contacts lie in E3, hence A3.
They would supply the forbidden A3-compatible root surround. This contradiction
proves Hh<=3 and therefore Hc<=3. Every contact in a plane tiling lies in every
E_r by the same neighborhood induction, so the root obstruction also excludes
plane tiling under the hypothesis. The all-motion registration bridge is an
explicit external dependency; no different strip's motion premise is used.

The certificates and readers establish the two literal geometric obstructions
for every k>=6. They do not establish the remaining E2 inclusion, an exact
Heesch value, or the finite-five target. Source hashes and the two evidence
digests are in expected.json. The shared symbolic kernel and unformalized
ordinary proof remain the computational trust boundary; independent review
has not been requested or obtained for this result.
