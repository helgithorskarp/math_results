# Two-point completions of the thirteen-point core and a 24-near-contact exclusion

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-10-01.
Status: author-checked written proof with exact certificates; separate arithmetic
implementation by the same author; independent team review and formalization
pending. No new packing, global bound, or global optimality theorem is claimed.

## 1. Reference core and the exact completion theorem

Let tau be the unique root of

\[
F(t)=13t^5-t^4+6t^3+2t^2-3t-1
\]

in `(0.59260590292507377809642492233275,
0.59260590292507377809642492233276)`. This is the known incumbent cosine.
Use the exact asymmetric coefficient vectors in `certificate.json`, writing
`p_i=B v_i`, where `B^T B=H=(1-tau)I+tau J`. They are the previously published
incumbent construction. The checker verifies the root bracket, unit norms,
anchor basis, circulant cross Gram matrix, every triangle reflection, all thirty
contacts, and the strict noncontact bounds. `generate.py` reconstructs them
from the anchor Gram matrix, rather than from rounded coordinates.

Remove points 3 and 14, leaving the core labels

```
0 1 2 4 5 6 7 8 9 10 11 12 13
```

The prescribed graph G24 consists of the two anchor triangles `(0,5,11)` and
`(1,2,4)`, and the two new edges from each reflection tuple `(n,i,j,o)`:

```
(6,0,11,5) (7,0,5,11) (9,5,11,0)
(8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4)
```

Add the four cross edges `6-8,7-12,9-10,9-13`. Equivalently, the full list is

```
(0,5) (0,6) (0,7) (0,11) (1,2) (1,4) (1,10) (1,12)
(2,4) (2,8) (2,10) (2,13) (4,8) (5,7) (5,9) (5,11)
(6,8) (6,11) (7,12) (8,13) (9,10) (9,11) (9,13) (10,12)
```

**Exact two-point completion theorem.** Suppose two unit vectors x,y obey
`x.p_i<=tau`, `y.p_i<=tau` for every core label, and `x.y<=tau`. One of x,y
equals p3. The other is either the old asymmetric p14 or the previously
identified cyclic alternative. Thus there are exactly two unordered extensions
of the fixed core to a fifteen-point tau-code, both known incumbents.

Consequently a fifteen-point code with exact G24 contacts at parameter
`t in [14/25,593/1000]` is one of these incumbents, up to O(3) and exchanging
the two unspecified labels. The earlier exact core theorem, height 7246,
already forced t=tau and the thirteen-point Gram matrix; the new assertion
classifies the two inserted points. No contacts incident to either inserted
point are required.

## 2. A cap containing every admissible unit point except p3

Work in coefficient coordinates and define the bounded avoidance polytope

\[
K=\{z:(H v_i)\cdot z\le\tau\text{ for every core label }i\}.
\]

The origin is strictly feasible. The four reference points at labels
`0,1,2,5` admit a strictly positive linear dependence and span R3, as verified
by exact Cramer identities and signs. These facts give boundedness: a recession
direction with all four projections nonpositive must make them all zero,
and hence is zero. Thus K is full dimensional and is the convex hull of its
finitely many vertices. Adding the cut below preserves boundedness and strict
feasibility of the origin.

Let l046 and l047 be the physical intersections of the three planes
`z.p_i=tau` at labels `(0,4,6)` and `(0,4,7)`, respectively. Their exact
coefficient vectors are in the certificate. Both intersections have independent
active normals, satisfy all thirteen avoidance inequalities, and have squared
norm above one. These facts are checked; their numerical approximations do not
enter the proof. Choose the physical center vector

\[
n=l_{046}+l_{047}+\frac45p_3,\qquad b=\frac{667}{250}.
\]

The cut polytope is

\[
K_b=\{z\in K:n\cdot Bz\le b\}.
\]

Complete exact enumeration of all `C(14,3)=364` active-plane triples gives
**24 distinct vertices**. The only unit vertex is p3, with active labels
`(1,4,7)`. Every other vertex has squared norm strictly below **99/100**.
There are no vertices with norm above one. Convexity of squared norm implies
that a unit point of K_b must equal p3: any positive convex mass on another
vertex gives norm squared strictly below one.

The certificate also checks

\[
0<b<\|n\|,\qquad n\cdot p_3<b,\qquad
2b^2-\left(1+\frac{593}{1000}\right)\|n\|^2>\frac9{1000}.
\tag{1}
\]

For any two unit vectors in the open cap `n.x>b`, `n.y>b`, their projections
on n/||n|| and Cauchy--Schwarz on the tangent components give

\[
x\cdot y>2b^2/\|n\|^2-1>593/1000.
\tag{2}
\]

In particular, a code with all pair products at most 593/1000 has at most one
point in this cap. Every unit point avoiding the thirteen fixed core points
is therefore either p3 or lies in the cap. Two inserted points with mutual
product at most tau cannot both be in the cap, so one is p3. Applying the
published fourteen-point completion theorem, height 8670, to the remaining
point gives exactly the two advertised choices. Both choices are feasible,
as that previous source proves. This establishes the exact theorem.

No spherical-hull, face, hemisphere, irreducibility, degree, or symmetry
hypothesis on the inserted points is used. The cap proof concerns the entire
spherical avoidance set, rather than only a facial region.

## 3. A relaxed isolated-completion lemma

Let x be unit, suppose `x.p_i<=tau+delta` for every core label, and assume
`n.x<=b`, where `0<=delta<=1/1000`. Then

\[
\boxed{\|x-p_3\|\le802\delta.}
\tag{3}
\]

Indeed set `a=tau/(tau+delta)` and `z=a x`. The positive cut bound ensures
`n.z<=b`, even if n.x is negative. Thus z belongs to K_b. Since tau>1/2,

\[
1-a\le2\delta,\qquad E:=1-\|z\|^2=1-a^2\le4\delta.
\]

Write z as a convex combination of the vertices, and let L be its total
mass on the 23 short vertices. Convexity gives

\[
\|z\|^2\le(1-L)+\frac{99}{100}L,
\quad L\le100E\le400\delta.
\]

All vertices have norm at most one, so `||z-p3||<=2L`. Combining this with
`||x-z||=1-a` proves (3). For delta=0 it also proves exact equality.
For any two inserted code points at parameter at most 593/1000, (2) forces
at least one to satisfy the cut; hence at least one is within 802 delta of
p3. This assertion allows a choice between the two unspecified labels.

## 4. The quantitative algebraic recovery uses only the 24-edge core

Put `I=[14/25,593/1000]`. Suppose fifteen unit points q_i have every pair
product at most `t in I`, and all G24 products belong to `[t-e,t]`, with
`0<=e<=10^-13`. The proof of the preceding 28-contact stability result,
height 8600, yields the following **core-only consequence**:

\[
|t-\tau|\le30000e,\qquad
\max_{i\text{ in core}}\|q_i-p_i\|\le2000000e
\tag{4}
\]

after an orthogonal alignment. This is a restriction of its derivation, not
an application of its 28-edge theorem with missing hypotheses. Here is the
complete data dependency check.

Use only the seven reflection tuples listed in Section 1. The old triangle
required by every tuple is already present in G24. The first anchor triangle
has alignment errors `(0,2,17)e`, as does the second. The error recurrence is
`K_n=20+K_i+K_j+K_o`; every core error is below 80e. The omitted reflections
for points 3 and 14 are never used in recovering the core.

The objects in Sections 2--4 of the earlier proof are:

- `U=A6`, `W=A7`, `V_A=A9`, and their common inner product kappa;
- `B2`, `B10`, `B13`, and the other common neighbor V_*;
- `B8`, `B12`, and the auxiliary vector C determining the two orientations;
- the four cross edges `6-8,7-12,9-10,9-13`.

All these labels and edges belong to G24. The branch exclusion uses the packing
inequality between q9 and q2; that is part of the all-pair code hypothesis.
It requires no contact involving either omitted point. Thus the previous
estimates remain valid: reflected-neighbor error 1000e, recovered-U error
40000e, recovered-W error 64000e, and determinant error 120000e. The exact
factorizations and interval bounds `D_minus>=1/10`,
`D_plus=J(t)F(t)`, `J(t)<=-2/5`, and `F'(t)>=10` give the parameter bound in
(4). Both orientation branches are treated.

The inverse reflected-anchor transformation recovers the three A anchors
from U,W,V_A; the B block has already been constructed from its anchors.
Only core labels are needed. The previous rational coefficient bounds
`||s_i(t)||_1<=3`, `||s_i'(t)||_1<=18`, and anchor-frame derivative bound six
give core distance at most `(600000+36*30000)e<2000000e`. At tau the recovered
core Gram matrix equals the published asymmetric core, by the checked exact
cross Gram and reflection identities. This proves (4).

`check.py` and `audit.py` reconstruct the 24 edges from the seven tuples,
check every old-triangle antecedent and error recurrence, and confirm the
label set. `replay.py` checks the pinned rational-function source and runs the
entire prior derivation and its prerequisite checkers. The fact that the two
omitted actual points do not enter the geometric argument above is also an
explicit written proof obligation, not a claim supplied by a checksum.

## 5. Stability and exclusion from 24 near-contacts

**Stability theorem.** Under Section 4's hypotheses, there is an orthogonal
alignment and possibly an exchange of labels 3,14 putting the entire code
within

\[
\boxed{1700000000000e}
\tag{5}
\]

of one of the two known incumbents, with the usual cyclic relabeling if needed.

Indeed each unspecified point x satisfies
`x.p_i<=tau+2030000e` for every core label, by (4). At least one of the two
points is outside the open cap by (2), since their mutual product is at most
`t<=593/1000`. Name this point q3. Applying (3) with
`delta=2030000e` gives

\[
\|q_3-p_3\|\le802\cdot2030000e=1628060000e.
\]

The fourteen points comprising the core and q3 therefore have maximum
reference displacement at most 1628060000e. For the remaining unit q14,
the packing inequalities and parameter bound give

\[
q_{14}\cdot p_i\le\tau+1628090000e\quad(0\le i<14).
\]

The published relaxed fourteen-plane completion lemma, height 8670, states
that a unit point satisfying these exact-reference avoidance inequalities
is within `1000 delta` of one of the two exact last-point completions when
`delta<=1/1000`. Here `delta=1628090000e<=162809/10^9<1/1000` at `e<=10^-13`.
Thus the last-point distance is at most 1628090000000e, which is smaller
than the coefficient in (5); all other points obey the smaller fourteen-point
bound. The earlier full Gram comparison identifies the alternative as the
known cyclic packing, with common-to-cyclic label map

```
1 0 11 7 5 4 10 3 9 8 6 2 14 13 12
```

**24-near-contact exclusion.** If in addition `e<=10^-19`, then `t>=tau`.
If `t<=tau`, then `t=tau` and the code is exactly one of the two incumbents
up to O(3) and the allowed relabeling. In particular a strict improvement
cannot contain this prescribed 24-edge near-contact pattern at that tolerance.

To prove it, the rotation-gauge estimate in the cyclic local source, height
8704, costs at most a factor ten in (5). At the stated tolerance the gauged
distance is at most

\[
10\cdot1700000000000\cdot10^{-19}
=17/10000000<1/400000.
\]

For either reference incumbent, the published asymmetric and cyclic local
inequalities give `eta=max(q_i.q_j)-tau>=0`, with positive growth for nonzero
distance. Since `eta<=t-tau`, this proves `t>=tau`. When `t<=tau`, zero
distance and `t=tau` follow. This completes the proof.

Every actual strict improvement of fifteen points lies in I: delete one point
and apply the solved N14 optimum, whose cosine is the positive root of
`4u^4-2u^3+3u^2-1` and is greater than 14/25. The upper endpoint follows from
comparison with the known incumbent. This is the same domain reduction proved
in the preceding near-contact source. It supplies no N15 optimality theorem.

## 6. Exact verification, dependencies, and scope

The core vectors, cap center, and exterior vertices are five-coefficient
rational polynomials evaluated at tau. `field.py` is reused byte for byte
from the published fourteen-point certificate. `check.py` evaluates signs by
rational Horner enclosures in the root bracket and uses replaced-column Cramer
determinants. It enumerates all 364 triples, tests every halfspace, proves the
strict norm and capacity gaps, and checks every scalar bridge above.

`audit.py` imports neither the primary checker nor its field arithmetic. It
adapts the raw-polynomial helpers from the published fourteen-point audit,
constructs homogeneous Cramer vectors with row cross products, and uses
centered Taylor enclosures. All 364 classification records match the primary
enumeration hash. Both programs use CPython and Fraction as their trust base.
This second implementation is an internal arithmetic audit by the author,
not an independent researcher review. The polytope, geometric stability, and
local inequality arguments are written mathematics, not formalized theorems.
Floating-point exploration merely chose a cap direction; every final bound
is checked exactly. Failed earlier cap cuts were not nonexistence proofs.

`INPUTS.json` pins all dependencies by source commit and file hash:

- Height 8670, source `1417ab38e068f028e0cf1eae4ae0d76066d8956b`:
  [fourteen-point exact and relaxed completion](https://github.com/helgithorskarp/math_results/blob/1417ab38e068f028e0cf1eae4ae0d76066d8956b/round-two/six-tammes-2/fourteen-point-completion/PROOF.md).
- Height 8704, source `77997e3e6cedfb4fd56c3bae1f8d1eeacee641cf`:
  [cyclic local radius, gauge, and the preceding 26-contact consequence](https://github.com/helgithorskarp/math_results/blob/77997e3e6cedfb4fd56c3bae1f8d1eeacee641cf/round-two/six-tammes-2/cyclic-local-exclusion/PROOF.md).
- Height 7123: [asymmetric local certificate](https://github.com/helgithorskarp/math_results/tree/6dffbb940c10f415b71e275a45010a7141d1ee4e/tammes15_exact_local_certificate).
- Height 8600: [prior quantitative recovery](https://github.com/helgithorskarp/math_results/blob/c69c1c3c909a810de6310867be4d051a77de6c50/round-two/six-tammes-2/robust-incumbent-pattern/PROOF.md),
  including height 7246's
  [exact thirteen-point core](https://github.com/helgithorskarp/math_results/blob/c25479d5c21ac31ef1b64eb5619dd5cda18619ec/tammes15_contact_pattern_obstruction/CONTACT_CORE.md).

The new assertion is not the old result that exact 24 contacts force tau.
It is the unconstrained two-point completion classification, the relaxed
cap lemma (3), and the robust whole-code consequence with only those 24 near
contacts. The earlier 26-contact result has the larger tolerance 10^-16;
neither theorem is claimed to dominate the other across all tolerances.
The teammate's [nine six-boundary hull-capacity certificates](../../six-tammes-1/hexagon-hull-capacity/PROOF.md),
height 8715, use a complementary cap/norm mechanism with prescribed template
neighborhoods. They are cited context and are not a premise of this proof.

Primary construction literature is Kottwitz,
[The densest packing of equal circles on a sphere](https://doi.org/10.1107/S0108767390011370),
and Buddenhagen--Kottwitz, *Multiplicity and Symmetry Breaking in (Conjectured)
Densest Packings of Congruent Circles on a Sphere*, whose earlier exact
construction and two known varieties are credited. Cohn's
[archived data set](https://hdl.handle.net/1721.1/153543),
[small-code table](https://cohn.mit.edu/spherical-codes/), and
[live table](https://spherical-codes.org/) retain the N15 quintic construction.
The seed [Musin--Tarasov paper](https://arxiv.org/abs/1410.2536) proves N14.
The primary tables and bounded literature searches were refreshed on
2026-10-01; no historical priority is asserted from an unsuccessful search.

No theorem here forces an arbitrary improved code to contain G24. Global
Tammes-15 bounds and optimality remain unchanged. The next missing step is a
complete contact-pattern occurrence or coordinate-box covering reduction;
this certificate supplies an exact discard interface when that motif occurs.
